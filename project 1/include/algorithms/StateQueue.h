#ifndef ROBOT_MAZES_STATEQUEUE_H
#define ROBOT_MAZES_STATEQUEUE_H

#include <queue>
#include <stack>
#include "State.h"

class StateQueue {
public:
    StateQueue();
    virtual void push(StateWrapper *state) = 0;
    virtual StateWrapper * pop() = 0;
    virtual size_t size() = 0;
};

class PriorityStateQueue : public StateQueue {
private:
    std::priority_queue<StateWrapper *> queue;
public:
    PriorityStateQueue();
    void push(StateWrapper *state) override;
    StateWrapper* pop() override;
    size_t size() override;
};

class LIFOStateQueue : public StateQueue {
private:
    std::stack<StateWrapper *> stack;
public:
    LIFOStateQueue();
    void push(StateWrapper *state) override;
    StateWrapper* pop() override;
    size_t size() override;
};

class FIFOStateQueue : public StateQueue {
private:
    std::queue<StateWrapper *> queue;
public:
    FIFOStateQueue();
    void push(StateWrapper *state) override;
    StateWrapper* pop() override;
    size_t size() override;
};

#endif //ROBOT_MAZES_STATEQUEUE_H
