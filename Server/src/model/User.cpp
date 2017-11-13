//
// Created by 王润基 on 2017/11/13.
//

#include "User.h"

bool User::isFriend(int othersID) const {
	return friendIDs.find(othersID) != friendIDs.end();
}

void User::addFriend(int othersID) {
	friendIDs.insert(othersID);
}

void User::toUserInfo(chat::UserInfo &info) const {
	info.set_id(id);
	info.set_username(username);
}
