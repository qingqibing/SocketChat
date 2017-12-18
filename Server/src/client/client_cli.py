from client import Client


HELP = """
    help
    login   <username> <password>
    signup  <username> <password>
    logout
    add     <username>
    search
    ls
""".strip('\n')

class ClientCLI:
    client = Client()

    def handle_help(self, args):
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

    def run(self):
        while True:
            print('>> ', end='')
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
