cmake_minimum_required(VERSION 3.13)  # CMake version check
project(robot_mazes)               # Create project "simple_example"
set(CMAKE_CXX_STANDARD 14)            # Enable c++14 standard
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/build)
set(LIB_DIR lib)
set(SRC_DIR src)
set(TEST_DIR tests)

# SDL2 Config
find_package(SDL2 REQUIRED)

# TODO: For linux use sudo apt install cmake libsdl2-dev g++

if(MSVC OR MSYS OR MINGW) # Windows
    include_directories(${LIB_DIR})

    # https://trenki2.github.io/blog/2017/06/02/using-sdl2-with-cmake/
    set(SDL2_INCLUDE_DIRS "${CMAKE_CURRENT_LIST_DIR}/lib")
    # Support both 32 and 64 bit builds
    if (${CMAKE_SIZEOF_VOID_P} MATCHES 8)
        set(SDL2_LIBRARIES "${CMAKE_CURRENT_LIST_DIR}/lib/x64/SDL2.lib;${CMAKE_CURRENT_LIST_DIR}/lib/x64/SDL2main.lib")
    else ()
        set(SDL2_LIBRARIES "${CMAKE_CURRENT_LIST_DIR}/lib/x86/SDL2.lib;${CMAKE_CURRENT_LIST_DIR}/lib/x86/SDL2main.lib")
    endif ()

    string(STRIP "${SDL2_LIBRARIES}" SDL2_LIBRARIES)
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