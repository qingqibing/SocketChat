//
// Created by 王润基 on 2017/11/13.
//

#ifndef SERVER_USER_H
#define SERVER_USER_H

#include <string>
#include <set>

struct User {
	int id;
	std::string username;
	std::string password;
	std::set<int> friendIDs;
};

#endif //SERVER_USER_H
