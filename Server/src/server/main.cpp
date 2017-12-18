#include <iostream>
#include <server/Server.h>
#include <server/SocketServer.h>
#include "protobuf/chat.pb.h"

int main() {
	auto server = Server();
	SocketServer socket(server);
	socket.run(8002);
	return 0;
}