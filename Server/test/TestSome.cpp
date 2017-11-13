#include <gtest/gtest.h>
#include <protobuf/chat.pb.h>

namespace {

class TestSome : public testing::Test
{
};

TEST_F(TestSome, ProtobufAny)
{
	chat::ChatMessage message, message1;
	message.set_senderid(1);
	message.set_targetid(2);
	message.set_text("123");

	::google::protobuf::Any any, any1;
	any.PackFrom(message);
	auto data = any.SerializeAsString();

	any1.ParseFromString(data);
	ASSERT_TRUE( any1.Is<chat::ChatMessage>() );

	any1.UnpackTo(&message1);
	ASSERT_EQ(1, message1.senderid());
	ASSERT_EQ(2, message1.targetid());
	ASSERT_EQ("123", message1.text());
}

}