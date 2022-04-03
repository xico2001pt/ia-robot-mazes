cmake_minimum_required(VERSION 3.13)  # CMake version check
project(robot_mazes)               # Create project "simple_example"
set(CMAKE_CXX_STANDARD 14)            # Enable c++14 standard
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/build)
set(CMAKE_MODULE_PATH lib)
set(INCLUDE_DIR include)
set(LIB_DIR lib)
set(SRC_DIR src)
set(TEST_DIR tests)

# Add main.cpp file of project root directory as source file
set(SOURCE_FILES
        ${INCLUDE_DIR}/algorithms/State.h
        ${SRC_DIR}/algorithms/State.cpp
        ${INCLUDE_DIR}/algorithms/StateQueue.h
        ${SRC_DIR}/algorithms/StateQueue.cpp
        #${SRC_DIR}/algorithms/RobotMazeSolver.cpp
        ${INCLUDE_DIR}/algorithms/SearchProblemSolver.h
        ${SRC_DIR}/algorithms/SearchProblemSolver.cpp
        ${SRC_DIR}/main.cpp)

# SDL2 Config
if(MSVC OR MSYS OR MINGW) # Windows
    link_directories(lib)
    add_executable(robot_mazes ${SOURCE_FILES})
    target_link_libraries(robot_mazes mingw32 SDL2main SDL2)
else() # Linux (sudo apt install libsdl2-dev) or MacOS
    find_package(SDL2 REQUIRED)
    add_executable(robot_mazes ${SOURCE_FILES})
endif()


# Add executable target with source files listed in SOURCE_FILES variable
target_include_directories(robot_mazes PUBLIC ${INCLUDE_DIR})
target_link_libraries(robot_mazes ${SDL2_LIBRARIES})