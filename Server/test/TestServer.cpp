#include <gtest/gtest.h>
#include "server/Server.h"

namespace {

class TestServer : public testing::Test
{
protected:
	void SetUp() override
	{
		server.reset(new Server());
	}

	std::unique_ptr<Server> server;

	bool signup(std::string username, std::string password)
	{
		SignupRequest req;
		req.set_username(username);
		req.set_password(password);
		auto rsp = server->signup(req);
		return rsp.success();
	}
};

TEST_F(TestServer, Signup)
{
	ASSERT_TRUE( signup("user1", "password") );
}

TEST_F(TestServer, Signup_UserExist)
{
	ASSERT_TRUE( signup("user1", "password") );
	ASSERT_FALSE( signup("user1", "password") );
}

TEST_F(TestServer, Login)
{
	signup("user1", "password");
	LoginRequest req;
	req.set_username("user1");
	req.set_password("password");
	auto rsp = server->login(req);
	ASSERT_TRUE(rsp.success());
	ASSERT_EQ(1, rsp.id());
}

TEST_F(TestServer, Login_WrongPassword)
{
	signup("user1", "password");
	LoginRequest req;
	req.set_username("user1");
	req.set_password("password0");
	auto rsp = server->login(req);
	ASSERT_FALSE(rsp.success());
	ASSERT_EQ(0, rsp.id());
	ASSERT_EQ("", rsp.token());
}

}