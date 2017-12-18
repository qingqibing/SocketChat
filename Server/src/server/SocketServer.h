//
// Created by 王润基 on 2017/11/13.
//

#ifndef SERVER_SOCKETSERVER_H
#define SERVER_SOCKETSERVER_H

#include "protobuf/chat.pb.h"
#include "Server.h"
#include <thread>

class SocketServer {
	Server& server;
	int port;
	int socketId;
	std::thread thread;
	static const int QUEUE_SIZE = 5;
	static const int BUFFER_SIZE = 1 << 20;
	// resolve type, auth, dispatch
	chat::NetMsg onReceive(chat::NetMsg const& msg) const;
	void listenLoop() const;
public:
	SocketServer(Server &server);
	void run(int port);
	void end();
	~SocketServer();
};


#endif //SERVER_SOCKETSERVER_H
