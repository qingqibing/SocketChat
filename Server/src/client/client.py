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
            raise Exception('Failed to login: %s' % rsp.info)
        self.token = rsp.token
        self.sc.token = rsp.token
        self.id = rsp.id

    def logout(self):
        req = LogoutRequest()
        req.senderID = self.id
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise Exception('Failed to logout: %s' % rsp.info)

    def signup(self, username, password):
        req = SignupRequest()
        req.username = username
        req.password = password
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise Exception('Failed to signup: %s' % rsp.info)

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

    def make_friend_with(self, username):
        users = self.get_users()
        users = [u for u in users if u.username == username]
        if len(users) == 0:
            raise Exception('No such user \'%s\'' % username)
        req = MakeFriendRequest()
        req.senderID = self.id
        req.targetID = users[0].id
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise Exception('Failed to make friend: %s' % rsp.info)
