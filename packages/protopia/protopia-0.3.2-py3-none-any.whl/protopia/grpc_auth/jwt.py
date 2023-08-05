import grpc

from threading import Timer
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class JwtAuthMetadataPlugin(grpc.AuthMetadataPlugin):
    TOKEN_RENEWAL_GRACE_SECONDS = 60

    def __init__(self, client_id, client_secret, token_url, scope=None):
        """Constructs a new instance of JWT gRPC authentication plugin that injects credentials as call metadata.
            :param client_id: Client id obtained during registration
            :param client_secret: The `client_secret` paired to the `client_id`.
                              This is generally required unless provided in the
                              `auth` tuple. If the value is `None`, it will be
                              omitted from the request, however if the value is
                              an empty string, an empty string will be sent.
            :param token_url: Token endpoint URL, must use HTTPS.
            :param scope: List of scopes you wish to request access to
        """
        if scope is None:
            scope = []
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.access_token = None
        self.token_type = None
        self.sess = OAuth2Session(client=BackendApplicationClient(client_id), scope=scope)
        self.fetch()

    def fetch(self):
        """Generates a new JWT token by performing OAuth2 Client Credentials Flow.
           In addition, it will start a timer that will re-generate the token 60 seconds before it expires.
        """
        resp = self.sess.fetch_token(token_url=self.token_url,
                                     client_id=self.client_id,
                                     client_secret=self.client_secret)
        self.access_token = resp['access_token']
        self.token_type = resp['token_type']
        exp = resp['expires_in']
        Timer(exp - JwtAuthMetadataPlugin.TOKEN_RENEWAL_GRACE_SECONDS, self.fetch)

    def __call__(self, context, callback):
        auth = bytes('%s %s' % (self.token_type, self.access_token), 'utf-8')
        metadata = ((b'authorization', auth),)
        callback(metadata, None)
