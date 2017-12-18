//
// Created by 王润基 on 2017/11/13.
//

#include "Server.h"

Response Server::signup(SignupRequest const &request) {
	if(getUserByName(request.username()) != nullptr)
		return Error("Username exist.");
	newUser(request.username(), request.password());
	return OK();
}

LoginResponse Server::login(LoginRequest const &request) {
	auto user = getUserByName(request.username());
	LoginResponse rsp;
	if(user == nullptr) {
		rsp.set_success(false);
		rsp.set_info("User not exist.");
		return rsp;
	}
	if(user->password != request.password()) {
		rsp.set_success(false);
		rsp.set_info("Wrong password.");
		return rsp;
	}
	onlineUsers.insert(user->id);
	auto token = tokens[user->id] = makeToken();
	rsp.set_success(true);
	rsp.set_id(user->id);
	rsp.set_token(token);
	return rsp;
}

Response Server::logout(LogoutRequest const &request) {
	onlineUsers.erase(request.senderid());
	return OK();
}

Response Server::OK() {
	Response r;
	r.set_success(true);
	return r;
}

Response Server::Error(std::string const &info) {
	Response r;
	r.set_success(false);
	r.set_info(info);
	return r;
}

User *Server::getUserByName(std::string const &username) const {
	for(auto const& pair: users)
		if(pair.second->username == username)
			return pair.second;
	return nullptr;
}

User *Server::getUser(int id) const {
	return users.at(id);
}

User *Server::newUser(std::string const &username, std::string const &password) {
	auto user = new User();
	user->id = static_cast<int>(users.size() + 1);
	user->username = username;
	user->password = password;
	users[user->id] = user;
	return user;
}

GetUserInfosResponse Server::getUserInfos(GetUserInfosRequest const &request) const {
	auto sender = getUser( request.senderid() );
	GetUserInfosResponse rsp;
	if(sender == nullptr)
		return rsp;
//		throw std::runtime_error("User not exist");
	for(auto pair: users) {
		auto user = pair.second;
		auto info = rsp.add_users();
		user->toUserInfo(*info);
		info->set_isfriend(sender->isFriend(user->id));
		info->set_isonline(isOnline(user->id));
	}
	return rsp;
}

bool Server::isOnline(int userID) const {
	return onlineUsers.find(userID) != onlineUsers.end();
}

GetMessagesResponse Server::getMessages(GetMessagesRequest const &request) const {
	auto rsp = GetMessagesResponse();
	for(auto const& m: messages)
		if(m.targetid() == request.senderid() && m.timeunix() >= request.aftertimeunix())
			rsp.add_messages()->CopyFrom(m);
	return rsp;
}

Response Server::makeFriend(MakeFriendRequest const &request) {
	auto user1 = getUser(request.senderid());
	auto user2 = getUser(request.targetid());
	if(user1 == nullptr || user2 == nullptr)
		return Error("User not exist");
	user1->addFriend(user2->id);
	user2->addFriend(user1->id);
	return OK();
}

Response Server::newMessage(ChatMessage const &message) {
	if(getUser(message.senderid()) == nullptr
	   || getUser(message.targetid()) == nullptr)
		return Error("User not exist");
	auto m = message;
	m.set_timeunix(time(0));
	messages.push_back(std::move(m));
	return OK();
}

std::string Server::makeToken() {
	const int TOKEN_LENGTH = 16;
	auto s = std::string();
	for(int i=0; i<TOKEN_LENGTH; ++i)
		s.push_back(static_cast<char>(rand() % 64 + 32));
	return s;
}

std::string Server::getToken(int id) const {
	return tokens.at(id);
}
