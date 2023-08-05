# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protopia.api.noise.v1beta1 import distribution_pb2 as protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2


class NoiseStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetNoiseDistribution = channel.unary_unary(
                '/protopia.cloud.noise.v1beta1.Noise/GetNoiseDistribution',
                request_serializer=protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.GetNoiseDistributionRequest.SerializeToString,
                response_deserializer=protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.EncryptedNoiseDistribution.FromString,
                )
        self.NotifyUsage = channel.unary_unary(
                '/protopia.cloud.noise.v1beta1.Noise/NotifyUsage',
                request_serializer=protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.Usage.SerializeToString,
                response_deserializer=protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.NotifyUsageResponse.FromString,
                )


class NoiseServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetNoiseDistribution(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NotifyUsage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NoiseServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetNoiseDistribution': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNoiseDistribution,
                    request_deserializer=protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.GetNoiseDistributionRequest.FromString,
                    response_serializer=protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.EncryptedNoiseDistribution.SerializeToString,
            ),
            'NotifyUsage': grpc.unary_unary_rpc_method_handler(
                    servicer.NotifyUsage,
                    request_deserializer=protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.Usage.FromString,
                    response_serializer=protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.NotifyUsageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'protopia.cloud.noise.v1beta1.Noise', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Noise(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetNoiseDistribution(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protopia.cloud.noise.v1beta1.Noise/GetNoiseDistribution',
            protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.GetNoiseDistributionRequest.SerializeToString,
            protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.EncryptedNoiseDistribution.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NotifyUsage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protopia.cloud.noise.v1beta1.Noise/NotifyUsage',
            protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.Usage.SerializeToString,
            protopia_dot_api_dot_noise_dot_v1beta1_dot_distribution__pb2.NotifyUsageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
