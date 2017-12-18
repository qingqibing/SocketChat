//
// Created by 王润基 on 2017/11/13.
//

#include "SocketServer.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <zconf.h>

using std::cerr;
using std::endl;


chat::NetMsg SocketServer::onReceive(chat::NetMsg const &msg) const {
	auto ret = NetMsg();
#define TEST(REQ_TYPE, SERVER_METHOD) \
	if(msg.data().Is<REQ_TYPE>()) {\
		auto req = REQ_TYPE();\
		msg.data().UnpackTo(&req);\
		auto rsp = server.SERVER_METHOD(req);\
		ret.mutable_data()->PackFrom(rsp);\
		return ret;\
	}
	TEST(chat::LoginRequest, login);
	TEST(chat::LogoutRequest, logout);
	TEST(chat::SignupRequest, signup);
	TEST(chat::GetUserInfosRequest, getUserInfos);
	TEST(chat::GetMessagesRequest, getMessages);
	TEST(chat::MakeFriendRequest, makeFriend);
	TEST(chat::ChatMessage, newMessage);
#undef TEST
	auto rsp = Response();
	rsp.set_success(false);
	rsp.set_info("Invalid command");
	ret.mutable_data()->PackFrom(rsp);
	return ret;
}

SocketServer::SocketServer(Server &server) : server(server) {

}

SocketServer::~SocketServer() {

}

void SocketServer::run(int port) {
	this->port = port;

	socketId = socket(AF_INET, SOCK_STREAM, IPPROTO_IP);
	if(socketId == -1)
		throw std::runtime_error("Failed to open socket");

	auto serverAddr = sockaddr_in{0};
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serverAddr.sin_port = htons(port);

	int rc = bind(socketId, (sockaddr*)&serverAddr, sizeof(sockaddr));
	if(rc == -1)
		throw std::runtime_error("Failed to bind socket");

	rc = listen(socketId, QUEUE_SIZE);
	if(rc == -1)
		throw std::runtime_error("Failed to listen socket");

	listenLoop();
//	thread = std::thread(&SocketServer::listenLoop, this);
}

void SocketServer::end() {
	close(socketId);
}

void SocketServer::listenLoop() const {
	sockaddr_in addr;
	socklen_t addrSize;
	while (true) {
		int connectId = accept(socketId, (sockaddr*)(&addr), &addrSize);
		if (connectId == -1) {
			cerr << "Failed to accept a request" << endl;
			continue;
		}
		cerr << "Accept: " << inet_ntoa(addr.sin_addr) << endl;

		static char buffer[BUFFER_SIZE];
		auto len = (int)recv(connectId, buffer, sizeof(buffer), 0);
		auto msg = NetMsg();
		msg.ParseFromArray(buffer, len);
		cerr << msg.data().DebugString() << endl;
		auto rsp = onReceive(msg);
		len = rsp.ByteSize();
		rsp.SerializeToArray(buffer, len);
		send(connectId, buffer, len, 0);
	}
}
