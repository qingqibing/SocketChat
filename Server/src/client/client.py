from socket_client import SocketClient
from chat_pb2 import *


class Client:
    sc = SocketClient()
    id = None
    token = None

    def check_login(self):
        if self.id is None:
            raise Exception("Must login first")

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
        self.check_login()
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
        self.check_login()
        req = GetUserInfosRequest()
        req.senderID = self.id
        rsp = self.sc.send(req, GetUserInfosResponse)
        return rsp.users

    def get_messages(self) -> [ChatMessage]:
        self.check_login()
        req = GetMessagesRequest()
        req.senderID = self.id
        req.afterTimeUnix = 0
        rsp = self.sc.send(req, GetMessagesResponse)
        return rsp.messages

    def get_userid(self, username) -> int:
        self.check_login()
        users = self.get_users()
        users = [u for u in users if u.username == username]
        if len(users) == 0:
            raise Exception('No such user \'%s\'' % username)
        return users[0].id

    def make_friend_with(self, username):
        self.check_login()
        req = MakeFriendRequest()
        req.senderID = self.id
        req.targetID = self.get_userid(username)
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise Exception('Failed to make friend: %s' % rsp.info)

    def send_message(self, targetId, text):
        self.check_login()
        req = ChatMessage()
        req.senderID = self.id
        req.targetID = targetId
        # req.timeUnix = 0
        req.text = text
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise Exception('Failed to send message: %s' % rsp.info)

    def send_file(self, targetId, filepath):
        self.check_login()
        req = ChatMessage()
        req.senderID = self.id
        req.targetID = targetId
        # req.timeUnix = 0
        file = open(filepath, 'rb')
        data = file.read()
        file.close()
        req.file = data
        rsp = self.sc.send(req, Response)
        if not rsp.success:
            raise Exception('Failed to send file: %s' % rsp.info)

    def recv_message(self) -> [ChatMessage]:
        self.check_login()
        req = GetMessagesRequest()
        req.senderID = self.id
        rsp = self.sc.send(req, GetMessagesResponse)
        return rsp.messages
