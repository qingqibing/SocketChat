//
// Created by 王润基 on 2017/11/13.
//

#ifndef SERVER_SERVER_H
#define SERVER_SERVER_H

#include "protobuf/chat.pb.h"
using namespace chat;

class Server {
public:
	LoginResponse login(LoginRequest const& request);
	Response logout(LogoutRequest const& request);
	GetUserInfosResponse getUserInfos(GetUserInfosRequest const& request);
	GetMessagesResponse getMessages(GetMessagesRequest const& request);
	Response makeFriend(MakeFriendRequest const& request);
	Response sendMessage(ChatMessage const& message);
};


#endif //SERVER_SERVER_H
