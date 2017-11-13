//
// Created by 王润基 on 2017/11/13.
//

#ifndef SERVER_SOCKETSERVER_H
#define SERVER_SOCKETSERVER_H

#include "protobuf/chat.pb.h"
#include "Server.h"

class SocketServer {
	// resolve type, auth, dispatch
	chat::NetMsg onReceive(chat::NetMsg const& msg);

public:
	SocketServer(Server& server);
};


#endif //SERVER_SOCKETSERVER_H
