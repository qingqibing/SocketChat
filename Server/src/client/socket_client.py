import socket
from chat_pb2 import NetMsg
from google.protobuf.message import Message
from google.protobuf.any_pb2 import Any


class SocketClient:
    _host = ('localhost', 8000)
    token = ''
    _MAX_LENGTH = 1 << 30
    _socket = None

    def __init__(self, host) -> None:
        self._host = host
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(self._host)

    def __del__(self):
        self._socket.close()

    def send(self, request: Message, response_type: type):
        data = Any()
        data.Pack(request)
        msg = NetMsg()
        msg.token = self.token
        msg.data.CopyFrom(data)
        self._socket.send(msg.SerializeToString())
        recv_data = self._socket.recv(self._MAX_LENGTH)
        rsp = NetMsg()
        rsp.ParseFromString(recv_data)
        ret = response_type()
        rsp.data.Unpack(ret)
        return ret

