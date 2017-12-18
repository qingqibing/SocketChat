//
// Created by 王润基 on 2017/11/13.
//

#ifndef SERVER_SERVER_H
#define SERVER_SERVER_H

#include "protobuf/chat.pb.h"
#include "model/User.h"
using namespace chat;

class Server {
	std::map<int, User*> users;
	std::map<int, std::string> tokens;
	std::set<int> onlineUsers;
	std::vector<ChatMessage> messages;

	static std::string makeToken();
	bool isOnline(int userID) const;
	User* getUserByName(std::string const& username) const;
	User* getUser(int id) const;
	User* newUser(std::string const& username, std::string const& password);

	static Response OK();
	static Response Error(std::string const& info);
public:
	std::string getToken(int id) const;
	LoginResponse login(LoginRequest const& request);
	Response logout(LogoutRequest const& request);
	Response signup(SignupRequest const& request);
	GetUserInfosResponse getUserInfos(GetUserInfosRequest const& request) const;
	GetMessagesResponse getMessages(GetMessagesRequest const& request) const;
	Response makeFriend(MakeFriendRequest const& request);
	Response newMessage(ChatMessage const& message);
};


#endif //SERVER_SERVER_H
