//
// Created by 王润基 on 2017/11/13.
//

#ifndef SERVER_USER_H
#define SERVER_USER_H

#include <string>
#include <set>
#include <protobuf/chat.pb.h>

struct User {
	int id;
	std::string username;
	std::string password;
	std::set<int> friendIDs;

	bool isFriend(int othersID) const;
	void addFriend(int othersID);
	void toUserInfo(chat::UserInfo& info) const;
};

#endif //SERVER_USER_H
