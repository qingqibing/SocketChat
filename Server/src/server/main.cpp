#include <iostream>
#include <server/Server.h>
#include <server/SocketServer.h>
#include "protobuf/chat.pb.h"

int main(int argc, char* argv[]) {
	int port = argc >= 2? atoi(argv[1]): 8000;
	auto server = Server();
	SocketServer socket(server);
	socket.run(port);
	return 0;
}