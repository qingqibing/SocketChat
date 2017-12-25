import datetime
import time
import os
import signal
import sys
from client import Client


def message_tostr(m):
    time_str = datetime.datetime.fromtimestamp(m.timeUnix).strftime('%H:%M:%S')
    return '[%s] %d: %s' % (time_str, m.senderID, m.text)


def input_intime(timeout=0):
    def interrupted(signum, frame):
        raise TimeoutError
    signal.signal(signal.SIGALRM, interrupted)
    signal.alarm(timeout)
    try:
        return input()
    finally:
        signal.alarm(0)


class ChatCLI:
    client = None
    targetId = None
    last_recv_time = time.time()

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

    def recv_messages(self):
        msgs = self.client.get_messages(afterTime=self.last_recv_time)
        self.last_recv_time = time.time()
        msgs = [m for m in msgs if m.senderID == self.targetId]
        for m in msgs:
            print(message_tostr(m))

    def run(self):
        TIMEOUT = 2
        while True:
            print('chat %d > ' % self.targetId, end='')
            while True:
                try:
                    cmd = input_intime(TIMEOUT)
                    break
                except TimeoutError:
                    try:
                        self.recv_messages()
                    except Exception as e:
                        print('Error: ' + str(e))

            tokens = cmd.split(' ')
            if tokens[0] == 'exit':
                return
            if cmd == '':
                continue
            if not hasattr(self, 'handle_' + tokens[0]):
                print('Invalid command')
                continue
            try:
                getattr(self, 'handle_' + tokens[0])(tokens[1:])
            except Exception as e:
                print('Error: ' + str(e))


class ClientCLI:
    client = None
    DOWNLOAD_PATH = '/Users/wangrunji/Downloads/'

    def __init__(self, client) -> None:
        self.client = client

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

    def handle_profile(self, args):
        info = self.client.get_self()
        print(info)

    def handle_recvmsg(self, args):
        msgs = self.client.recv_message()
        for m in msgs:
            if m.text:
                print(message_tostr(m))

    def handle_recvfile(self, args):
        msgs = self.client.recv_message()
        for m in msgs:
            if m.file:
                time_str = datetime.datetime.fromtimestamp(m.timeUnix).strftime('%Y%m%d_%H%M%S')
                path = os.path.join(self.DOWNLOAD_PATH, 'file_'+time_str)
                if os.path.exists(path):
                    continue
                file = open(path, 'wb')
                file.write(m.file)
                file.close()
                print('File saved to: ' + path)

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
    host = sys.argv[1] if len(sys.argv) >= 2 else 'localhost:8000'
    print('Linking to ' + host)
    client = Client(host)
    cli = ClientCLI(client)
    cli.run()
