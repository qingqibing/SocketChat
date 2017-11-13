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
	rsp.set_success(true);
	rsp.set_id(user->id);
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
	if(sender == nullptr)
		throw std::runtime_error("User not exist");
	GetUserInfosResponse rsp;
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
