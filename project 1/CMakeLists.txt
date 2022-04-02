cmake_minimum_required(VERSION 3.13)  # CMake version check
project(robot_mazes)               # Create project "simple_example"
set(CMAKE_CXX_STANDARD 14)            # Enable c++14 standard
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/build)
set(INCLUDE_DIR include)
set(LIB_DIR lib)
set(SRC_DIR src)
set(TEST_DIR tests)

# SDL2 Config
find_package(SDL2 REQUIRED)

# TODO: For linux use sudo apt install cmake libsdl2-dev g++

if(MSVC OR MSYS OR MINGW) # Windows
    target_link_libraries(SDL2 PRIVATE "${LIB_DIR}")
    target_include_directories("${INCLUDE_DIR}/SDL2")
endif()


# Add main.cpp file of project root directory as source file
set(SOURCE_FILES
    #${SRC_DIR}/algorithms/RobotMazeSolver.cpp
    #${SRC_DIR}/algorithms/SearchProblemSolver.cpp
    #${SRC_DIR}/algorithms/StateQueue.cpp
    ${SRC_DIR}/main.cpp)

# Add executable target with source files listed in SOURCE_FILES variable
add_executable(robot_mazes ${SOURCE_FILES})
target_link_libraries(robot_mazes ${SDL2_LIBRARIES})