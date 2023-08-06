from .common import ( 
    BaseClient, msgrpc, websocketrpc, signingrpc,
    lightningrpc, federaterpc, socketrpc, vpnrpc
)
from .errors import handle_rpc_errors


class IMPClient(BaseClient):
    @handle_rpc_errors
    def send_message(self, msg, pubkey, **kwargs):
        request = msgrpc.SendMessageRequest(
            msg=msg,
            pubkey=pubkey,
            **kwargs
        )
        try:
            response = self._msg_stub.SendMessage(request)
            return response
        except Exception as e:
            print(e)

    @handle_rpc_errors
    def subscribe(self):
        request = websocketrpc.SubscribeRequest()
        try:
            response = self._websocket_stub.Subscribe(request)
            return response
        except Exception as e:
            print(e)

# federate
# RequestFederate
    @handle_rpc_errors
    def request_federate(self, pubkey):
        request = federaterpc.RequestFederateRequest(pubkey=pubkey)
        try:
            response = self._federate_stub.RequestFederate(request)
            return response
        except Exception as e:
            print(e)

# LeaveFederation
    @handle_rpc_errors
    def leave_federation(self, pubkey):
        request = federaterpc.LeaveFederationRequest(pubkey=pubkey)
        try:
            response = self._federate_stub.LeaveFederation(request)
            return response
        except Exception as e:
            print(e)

# signing
# SignMessage
    @handle_rpc_errors
    def send_socket(self, pubkey):
        request = signingrpc.SignMessageRequest(pubkey=pubkey)
        try:
            response = self._signing_stub.SignMessage(request)
            return response
        except Exception as e:
            print(e)

# VerifySignature
    @handle_rpc_errors
    def send_socket(self, pubkey):
        request = signingerpc.VerifySignatureRequest(pubkey=pubkey)
        try:
            response = self._signing_stub.VerifySignature(request)
            return response
        except Exception as e:
            print(e)

# lightning
# GenerateInvoice
    @handle_rpc_errors
    def send_socket(self, pubkey):
        request = lightningrpc.GenerateInvoiceRequest(pubkey=pubkey)
        try:
            response = self._lightning_stub.GenerateInvoice(request)
            return response
        except Exception as e:
            print(e)

# PayInvoice
    @handle_rpc_errors
    def send_socket(self, pubkey):
        request = lightningrpc.PayInvoiceRequest(pubkey=pubkey)
        try:
            response = self._lightning_stub.PayInvoice(request)
            return response
        except Exception as e:
            print(e)

# CheckInvoice
    @handle_rpc_errors
    def send_socket(self, pubkey):
        request = lightningrpc.CheckInvoiceRequest(pubkey=pubkey)
        try:
            response = self._lightning_stub.CheckInvoice(request)
            return response
        except Exception as e:
            print(e)

# socket
# SendSocket
    @handle_rpc_errors
    def send_socket(self, pubkey):
        request = socketrpc.SendSocketRequest(pubkey=pubkey)
        try:
            response = self._socket_stub.SendSocket(request)
            return response
        except Exception as e:
            print(e)

# StartSocket
    @handle_rpc_errors
    def start_socket(self, pubkey):
        request = socketrpc.StartSocketRequest(pubkey=pubkey)
        try:
            response = self._socket_stub.StartSocket(request)
            return response
        except Exception as e:
            print(e)

# StopSocket
    @handle_rpc_errors
    def stop_socket(self, pubkey):
        request = socketrpc.StopSocketRequest(pubkey=pubkey)
        try:
            response = self._socket_stub.StopSocket(request)
            return response
        except Exception as e:
            print(e)

# VPNRpc
# RequestQuote
    @handle_rpc_errors
    def request_quote(self, pubkey):
        request = vpnrpc.RequestQuoteRequest(pubkey=pubkey)
        try:
            response = self._vpn_stub.RequestQuote(request)
            return response
        except Exception as e:
            print(e)

# AcceptContract
    @handle_rpc_errors
    def accept_contract(self, pubkey, nonce, price):
        request = vpnrpc.AcceptContractRequest(
            pubkey=pubkey,
            nonce=nonce,
            price=price
        )
        try:
            response = self._vpn_stub.AcceptContract(request)
            return response
        except Exception as e:
            print(e)

# RefreshContract
    @handle_rpc_errors
    def refresh_contract(self, pubkey, nonce, price):
        request = vpnrpc.RefreshContractRequest(
            pubkey=pubkey,
            nonce=nonce,
            price=price
        )
        try:
            response = self._socket_stub.RefreshContract(request)
            return response
        except Exception as e:
            print(e)