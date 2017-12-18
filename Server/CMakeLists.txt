cmake_minimum_required(VERSION 3.8)
project(Server)

set(CMAKE_CXX_STANDARD 11)

find_package(Protobuf REQUIRED)
include_directories(${Protobuf_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})
EXECUTE_PROCESS(
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        --cpp_out=. --python_out=../client protobuf/chat.proto
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src)

include_directories(src)

file(GLOB BASE_SRC src/model/* src/protobuf/*)
add_library(Base SHARED ${BASE_SRC})
target_link_libraries(Base ${Protobuf_LIBRARIES})

file(GLOB SERVER_SRC src/server/*)
list(REMOVE_ITEM SERVER_SRC src/server/main.cpp)
add_library(ServerLib SHARED ${SERVER_SRC})
target_link_libraries(ServerLib Base)
add_executable(Server src/server/main.cpp)
target_link_libraries(Server ServerLib)

#file(GLOB CLIENT_SRC src/client/*)
#list(REMOVE_ITEM CLIENT_SRC src/client/main.cpp)
#add_library(ClientLib SHARED ${CLIENT_SRC})
#target_link_libraries(ClientLib Base)
#add_executable(Client src/client/main.cpp)
#target_link_libraries(Client ClientLib)

# Download and unpack googletest at configure time
configure_file(CMakeLists.txt.in googletest-download/CMakeLists.txt)
execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
        RESULT_VARIABLE result
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/googletest-download )
if(result)
    message(FATAL_ERROR "CMake step for googletest failed: ${result}")
endif()
execute_process(COMMAND ${CMAKE_COMMAND} --build .
        RESULT_VARIABLE result
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/googletest-download )
if(result)
    message(FATAL_ERROR "Build step for googletest failed: ${result}")
endif()

# Prevent overriding the parent project's compiler/linker
# settings on Windows
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Add googletest directly to our build. This defines
# the gtest and gtest_main targets.
add_subdirectory(${CMAKE_BINARY_DIR}/googletest-src
        ${CMAKE_BINARY_DIR}/googletest-build)

# The gtest/gtest_main targets carry header search path
# dependencies automatically when using CMake 2.8.11 or
# later. Otherwise we have to add them here ourselves.
if (CMAKE_VERSION VERSION_LESS 2.8.11)
    include_directories("${gtest_SOURCE_DIR}/include")
endif()

file(GLOB TEST_SOURCES test/*.cpp test/*.h test/**/*.cpp)

# Now simply link against gtest or gtest_main as needed. Eg
add_executable(Test ${TEST_SOURCES})
target_link_libraries(Test ServerLib)
#target_link_libraries(Test ClientLib)
target_link_libraries(Test gtest gtest_main)
#target_link_libraries(Test gmock gmock_main)
#add_test(NAME example_test COMMAND example)