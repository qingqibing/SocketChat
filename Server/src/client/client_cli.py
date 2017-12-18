import datetime
import os
from client import Client


class ChatCLI:
    client = Client()
    targetId = None

    def __init__(self, client, targetId):
        self.client = client
        self.targetId = targetId

    def handle_help(self, args):
        HELP = """
    help
    exit
    sendmsg     <text>
    sendfile    <filepath>
""".strip('\n')
        print(HELP)

    def handle_sendmsg(self, args):
        self.client.send_message(self.targetId, text=args[0])

    def handle_sendfile(self, args):
        self.client.send_file(self.targetId, filepath=args[0])

    def run(self):
        while True:
            print('chat %d > ' % self.targetId, end='')
            cmd = input()
            tokens = cmd.split(' ')
            if tokens[0] == 'exit':
                return
            if not hasattr(self, 'handle_' + tokens[0]):
                print('Invalid command')
                continue
            try:
                getattr(self, 'handle_' + tokens[0])(tokens[1:])
            except Exception as e:
                print('Error: ' + str(e))


class ClientCLI:
    client = Client()
    DOWNLOAD_PATH = '~/Downloads'

    def handle_help(self, args):
        HELP = """
    help
    chat    <username>
    login   <username> <password>
    signup  <username> <password>
    logout
    add     <username>
    search
    ls
    recvmsg
""".strip('\n')
        print(HELP)

    def handle_login(self, args):
        self.client.login(username=args[0], password=args[1])

    def handle_logout(self, args):
        self.client.logout()

    def handle_signup(self, args):
        self.client.signup(username=args[0], password=args[1])

    def handle_add(self, args):
        self.client.make_friend_with(username=args[0])

    def handle_search(self, args):
        users = self.client.get_users()
        for u in users:
            print(u.username)

    def handle_ls(self, args):
        users = self.client.get_users()
        for u in users:
            if u.isFriend:
                print(u.username)

    def handle_recvmsg(self, args):
        msgs = self.client.recv_message()
        for m in msgs:
            if m.text:
                time_str = datetime.datetime.fromtimestamp(m.timeUnix).strftime('%H:%M:%S')
                print('[%s] %d: %s' % (time_str, m.senderID, m.text))

    def handle_recvfile(self, args):
        msgs = self.client.recv_message()
        for m in msgs:
            if m.file:
                path = os.path.join(self.DOWNLOAD_PATH, 'file')
                file = open(path, 'wb')
                file.write(m.file)
                file.close()
                print('Saved file to download path')


    def handle_chat(self, args):
        userid = self.client.get_userid(username=args[0])
        sub = ChatCLI(self.client, userid)
        sub.run()

    def run(self):
        while True:
            print('> ', end='')
            cmd = input()
            tokens = cmd.split(' ')
            if not hasattr(self, 'handle_' + tokens[0]):
                print('Invalid command')
                continue
            try:
                getattr(self, 'handle_' + tokens[0])(tokens[1:])
            except Exception as e:
                print('Error: ' + str(e))


if __name__ == '__main__':
    cli = ClientCLI()
    cli.run()
