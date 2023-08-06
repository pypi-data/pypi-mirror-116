import binascii
import platform
import os
import grpc

# from impgrpc.compiled.messaging_pb2 import (
#     messaging_pb2 as msgrpc,
#     messaging_pb2_grpc as msgstub,
#     websocket_pb as websocketrpc,
#     websocket_pb2_grpc as websocketstub
# )

import impgrpc.compiled.messaging_pb2 as msgrpc
import impgrpc.compiled.messaging_pb2_grpc as msgstub

import impgrpc.compiled.websocket_pb2 as websocketrpc
import impgrpc.compiled.websocket_pb2_grpc as websocketstub

import impgrpc.compiled.signing_pb2 as signingrpc
import impgrpc.compiled.signing_pb2_grpc as signingstub

import impgrpc.compiled.lightning_pb2 as lightningrpc
import impgrpc.compiled.lightning_pb2_grpc as lightningstub

import impgrpc.compiled.federate_pb2 as federaterpc
import impgrpc.compiled.federate_pb2_grpc as federatestub

import impgrpc.compiled.socket_pb2 as socketrpc
import impgrpc.compiled.socket_pb2_grpc as socketstub

import impgrpc.compiled.vpn_pb2 as vpnrpc
import impgrpc.compiled.vpn_pb2_grpc as vpnstub

system = platform.system().lower()

if system == 'linux':
    TLS_FILEPATH = os.path.expanduser('~/.lnd/tls.cert')
    ADMIN_MACAROON_BASE_FILEPATH = '~/.lnd/data/chain/bitcoin/{}/admin.macaroon'
    READ_ONLY_MACAROON_BASE_FILEPATH = '~/.lnd/data/chain/bitcoin/{}/readonly.macaroon'
elif system == 'darwin':
    TLS_FILEPATH = os.path.expanduser('~/Library/Application Support/Lnd/tls.cert')
    ADMIN_MACAROON_BASE_FILEPATH = '~/Library/Application Support/Lnd/data/chain/bitcoin/{}/admin.macaroon'
    READ_ONLY_MACAROON_BASE_FILEPATH = '~/Library/Application Support/Lnd/data/chain/bitcoin/{}/readonly.macaroon'
elif system == 'windows':
    TLS_FILEPATH = os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Lnd', 'tls.cert')
    ADMIN_MACAROON_BASE_FILEPATH = os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Lnd', 'data', 'chain', 'bitcoin', 'mainnet', 'admin.macaroon')
    READ_ONLY_MACAROON_BASE_FILEPATH = os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Lnd', 'data', 'chain', 'bitcoin', 'mainnet', 'readonly.macaroon')
else:
    raise SystemError('Unrecognized system')


# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'


def get_cert(filepath=None):
    """Read in tls.cert from file

    Note: tls files need to be read in byte mode as of grpc 1.8.2
          https://github.com/grpc/grpc/issues/13866
    """
    filepath = filepath or TLS_FILEPATH
    with open(filepath, 'rb') as f:
        cert = f.read()
    return cert


def get_macaroon(network='mainnet', filepath=None):
    """Read and decode macaroon from file

    The macaroon is decoded into a hex string and returned.
    """
    if filepath is None:
        if admin:
            filepath = os.path.expanduser(ADMIN_MACAROON_BASE_FILEPATH.format(network))
        else:
            filepath = os.path.expanduser(READ_ONLY_MACAROON_BASE_FILEPATH.format(network))

    with open(filepath, 'rb') as f:
        macaroon_bytes = f.read()
    return binascii.hexlify(macaroon_bytes).decode()


def generate_credentials(cert, macaroon):
    """Create composite channel credentials using cert and macaroon metatdata"""
    # create cert credentials from the tls.cert file
    cert_creds = grpc.ssl_channel_credentials(cert)
    # cert_creds = grpc.ssl_channel_credentials()

    # build meta data credentials
    metadata_plugin = MacaroonMetadataPlugin(macaroon)
    auth_creds = grpc.metadata_call_credentials(metadata_plugin)

    # combine the cert credentials and the macaroon auth credentials
    # such that every call is properly encrypted and authenticated
    return grpc.composite_channel_credentials(cert_creds, auth_creds)


class MacaroonMetadataPlugin(grpc.AuthMetadataPlugin):
    """Metadata plugin to include macaroon in metadata of each RPC request"""

    def __init__(self, macaroon):
        self.macaroon = macaroon

    def __call__(self, context, callback):
        callback([('macaroon', self.macaroon)], None)


class BaseClient(object):
    grpc_module = grpc

    def __init__(self, ip_address='127.0.0.1:8881', cert=None,
                 cert_filepath=None, macaroon=None, macaroon_filepath=None):

        # if macaroon is None:
        #     macaroon = get_macaroon(network=network, filepath=macaroon_filepath)

        # if cert is None:
        #     cert = get_cert(cert_filepath)

        # self.network = network
        # self._credentials = generate_credentials(cert, macaroon)
        self.ip_address = ip_address

    @property
    def _msg_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        # grpc.insecure_channel('X.X.X.X:8881')
        channel = self.grpc_module.insecure_channel(
            self.ip_address, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return msgstub.MessagingStub(channel)

    @property
    def _msg_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.insecure_channel(
            self.ip_address, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return msgstub.MessagingStub(channel)

    @property
    def _websocket_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.insecure_channel(
            self.ip_address, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return websocketstub.WebsocketStub(channel)

    @property
    def _signing_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.insecure_channel(
            self.ip_address, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return signingstub.SigningStub(channel)

    @property
    def _lightning_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.insecure_channel(
            self.ip_address, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return lightningstub.LightningStub(channel)

    @property
    def _federate_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.insecure_channel(
            self.ip_address, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return federatestub.FederateStub(channel)

    @property
    def _socket_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.insecure_channel(
            self.ip_address, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return socketstub.SocketStub(channel)

    @property
    def _vpn_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.insecure_channel(
            self.ip_address, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return vpnstub.VPNStub(channel)