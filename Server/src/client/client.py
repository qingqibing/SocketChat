from socket_client import SocketClient
from chat_pb2 import *


class Client:
    sc = SocketClient()
    id = None
    token = None

    def login(self, username, password):
        req = LoginRequest()
        req.username = username
        req.password = password
        rsp = self.sc.send(req, LoginResponse)
        if not rsp.success:
            raise 'Failed to login: %s' % rsp.info
        self.token = rsp.token
        self.sc.token = rsp.token
        self.id = rsp.id

    def logout(self):
        req = LogoutRequest()
        req.senderID = self.id
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise 'Failed to logout: %s' % rsp.info

    def signup(self, username, password):
        req = SignupRequest()
        req.username = username
        req.password = password
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise 'Failed to signup: %s' % rsp.info

    def get_users(self) -> [UserInfo]:
        req = GetUserInfosRequest()
        req.senderID = self.id
        rsp = self.sc.send(req, GetUserInfosResponse)
        return rsp.users

    def get_messages(self) -> [ChatMessage]:
        req = GetMessagesRequest()
        req.senderID = self.id
        req.afterTimeUnix = 0
        rsp = self.sc.send(req, GetMessagesResponse)
        return rsp.messages

    def make_friend_with(self, othersID):
        req = MakeFriendRequest()
        req.senderID = self.id
        req.targetID = othersID
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise 'Failed to make friend: %s' % rsp.info


if __name__ == '__main__':
    client = Client()
    # client.signup('user1', 'password')
    client.login('user1', 'password')
