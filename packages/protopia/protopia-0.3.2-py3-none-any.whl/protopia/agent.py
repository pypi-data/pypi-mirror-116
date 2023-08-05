import os
from typing import Dict, List
import json
import grpc
import numpy as np
import torch
from torch import Tensor

from .noise_layer.cloak import Cloak

from .api.noise.v1beta1.distribution_pb2 import GetNoiseDistributionRequest
from .api.noise.v1beta1.distribution_pb2_grpc import NoiseStub
from .grpc_auth.jwt import JwtAuthMetadataPlugin

MAX_MESSAGE_LENGTH = 20 * 1024 * 1024
PROTOPIA_CLOUD_STAGE_URL = 'api.stage-01.stage.protopia.ai:443'
STAGE_TOKEN_URL = 'https://protopia-cloud-stage-01.auth.us-east-1.amazoncognito.com/oauth2/token'
SCOPES = ['https://api.stage-01.protopia.ai/noise:read']

class Agent:
    """
    Note, the following variables must be set prior to calling this method:
    - OIDC_CLIENT_ID: the OAuth2 client_id.
    - OIDC_CLIENT_SECRET: the OAuth2 client_secret.
    """
    def __init__(self, client_id: str = None, client_secret: str = None) -> None:
        self.MAX_MESSAGE_LENGTH = MAX_MESSAGE_LENGTH
        self.PROTOPIA_CLOUD_URL = PROTOPIA_CLOUD_STAGE_URL
        self.TOKEN_URL = STAGE_TOKEN_URL
        self.SCOPES = SCOPES

        self.OIDC_CLIENT_ID = client_id
        self.OIDC_CLIENT_SECRET = client_secret

        self.channel = None

        self.nnid = None
        self.distributions = dict()

    def set_url(self, url: str) -> None:
        self.PROTOPIA_CLOUD_URL = url
        print("PROTOPIA_CLOUD_URL is set to " + url)

    def set_token_url(self, token_url: str) -> None:
        self.TOKEN_URL = token_url
        print("TOKEN_URL is set to " + token_url)

    def set_scopes(self, scopes: List[str]) -> None:
        self.SCOPES = scopes
        print("SCOPES is set to " + scopes)

    def set_client(self, id: str, secret: str) -> None:
        self.OIDC_CLIENT_ID = id
        self.OIDC_CLIENT_SECRET = secret
        print("OIDC_CLIENT_ID is set to " + id)
        print("OIDC_CLIENT_SECRET is set to " + secret)

    def set_option(self, option_dict: Dict[str, str]) -> None:
        for k, v in option_dict.items():
            self[k] = v
            print(k + " is set to " + v)

    def get_option(self) -> None:
        print("PROTOPIA_CLOUD_URL is set to " + self.PROTOPIA_CLOUD_URL)
        print("TOKEN_URL is set to " + self.TOKEN_URL)
        print("SCOPES is set to " + str(self.SCOPES))
        print("OIDC_CLIENT_ID is set to " + str(self.OIDC_CLIENT_ID))
        print("OIDC_CLIENT_SECRET is set to " + str(self.OIDC_CLIENT_SECRET))

    def connect(self) -> bool:
        if self.OIDC_CLIENT_ID is None or self.OIDC_CLIENT_SECRET is None:
            raise ValueError('OIDC_CLIENT_ID and OIDC_CLIENT_SECRET environment variables must be specified')

        self.distributions[self.OIDC_CLIENT_ID] = dict()

        ssl = grpc.ssl_channel_credentials()
        jwt_auth_plugin = JwtAuthMetadataPlugin(self.OIDC_CLIENT_ID, self.OIDC_CLIENT_SECRET, self.TOKEN_URL, self.SCOPES)
        jwt_auth = grpc.metadata_call_credentials(jwt_auth_plugin)
        credentials = grpc.composite_channel_credentials(ssl, jwt_auth)

        try:
            self.channel = grpc.secure_channel(PROTOPIA_CLOUD_STAGE_URL, credentials, options=[
                ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
            ])
            print('successfully connected to cloud API')
            return True
        except Exception as e:
            print('Can not connect to cloud API, caused by:', e)
            return False

    def get_noise_distribution(self, nnid: str):
        """Connects to Protopia Cloud API over SSL protocol authorized by JWT tokens and downloads a noise distribution.
        """

        if self.channel is None or self.OIDC_CLIENT_ID not in self.distribution:
            self.connect()

        client = NoiseStub(self.channel)

        if nnid is None:
            raise ValueError("nnid must be specified")

        request = GetNoiseDistributionRequest(nnid=nnid)
        try:
            response = client.GetNoiseDistribution(request)
            decrypt_response = response
        except grpc.RpcError as e:
            print('failed to retrieve noise distribution, caused by:', e)
            return False

        try:
            retrieved_nnid = decrypt_response.nnid
            if nnid != retrieved_nnid:
                raise ValueError("provided nnid: {} doesn't match with retrieved nnid : {}".format(nnid, retrieved_nnid))

            distribution = decrypt_response.payload.decode('utf8')

            distribution = json.loads(distribution)

            print('successfully retrieved encrypted noise distribution')
            self.distributions[self.OIDC_CLIENT_ID][nnid] = distribution
            return distribution

        except Exception as e:
            print('failed to retrieve noise distribution, caused by:', e)
            return False

    @staticmethod
    def allocate_noise_distribution(noise_distribution):
        rtn = {}
        try:
            for key, info in noise_distribution.items():
                if key != 'version':
                    for layer, layer_info in info.items():
                        for noise, noise_info in layer_info.items():
                            rtn[noise] = noise_info
            return rtn
        except Exception as e:
            print('failed to apply noise distribution, caused by:', str(e))
            return False

    @staticmethod
    def get_cloak_noise_generator(rtn):
        locs = torch.FloatTensor(rtn['Weight']['locs'])
        rhos = torch.FloatTensor(rtn['Weight']['rhos'])

        NoiseGenerator = Cloak()
        NoiseGenerator.locs = torch.nn.Parameter(locs)
        NoiseGenerator.rhos = torch.nn.Parameter(rhos)
        return NoiseGenerator

    def noise(self, rtn, x):
        max_scale = rtn['layer_config']['max_scale']
        min_scale = rtn['layer_config']['min_scale']
        given_shape = rtn['layer_config']['given_shape']
        threshold_value = rtn['layer_config']['threshold_value']
        locs = np.asarray(rtn['Weight']['locs'])
        rhos = np.asarray(rtn['Weight']['rhos'])
        std = (1.0 + np.tanh(rhos)) / 2 * (max_scale-min_scale) + min_scale
        mask = (std < threshold_value).float()
        data = x + std * np.random.normal(locs, std, given_shape)

        x = np.clip(
                data * mask + np.min(x) * (1 - mask) + locs,
                np.min(x),
                np.max(x)
            )
        return x

    def apply_noise_distribution(self, nnid: str, x: Tensor) -> Tensor:
        noise_distribution = None
        if nnid not in self.distributions.get(self.OIDC_CLIENT_ID, []):
            noise_distribution = self.get_noise_distribution(nnid)
        else:
            noise_distribution = self.distributions[self.OIDC_CLIENT_ID][nnid]

        rtn = self.allocate_noise_distribution(noise_distribution)
        NoiseGenerator = self.get_cloak_noise_generator(rtn)

        x = NoiseGenerator(x)
        return x

    def get_noise_generator(self, nnid: str) -> Tensor:
        noise_distribution = None
        if nnid not in self.distributions.get(self.OIDC_CLIENT_ID, []):
            noise_distribution = self.get_noise_distribution(nnid)
        else:
            noise_distribution = self.distributions[self.OIDC_CLIENT_ID][nnid]

        rtn = self.allocate_noise_distribution(noise_distribution)
        NoiseGenerator = self.get_cloak_noise_generator(rtn)

        return NoiseGenerator

    def parse_local_json(self, path: str) -> Tensor:
        # with open(path) as f:
        #     d = json.load(f)
        noise_distribution = None
        with open(path) as fd:
            noise_distribution = json.load(fd)
        rtn = self.allocate_noise_distribution(noise_distribution)
        return self.get_cloak_noise_generator(rtn)

    @staticmethod
    def convert_model(model, input_size=(1, 3, 224, 224)):
        rand_input = torch.rand(input_size)
        model.eval()
        model_traced = torch.jit.trace(model, rand_input)
        torch.jit.save(model_traced, "tmp/noiselayerJit.pth")
