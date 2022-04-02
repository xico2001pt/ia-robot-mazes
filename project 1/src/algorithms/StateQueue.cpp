#include <queue>
#include <stack>
#include "Solver.cpp"

class StateQueue {
    public:
        StateQueue();
        virtual void push(State *state) = 0;
        virtual State * pop() = 0;
        virtual size_t size() = 0;
};

class PriorityStateQueue : public StateQueue {
    private:
        std::priority_queue<State *> queue;
    public:
        PriorityStateQueue();
        void push(State *state) override;
        State* pop() override;
        size_t size() override;
};

class LIFOStateQueue : public StateQueue {
    private:
        std::stack<State *> stack;
    public:
        LIFOStateQueue();
        void push(State *state) override;
        State* pop() override;
        size_t size() override;
};

class FIFOStateQueue : public StateQueue {
    private:
        std::queue<State *> queue;
    public:
        FIFOStateQueue();
        void push(State *state) override;
        State* pop() override;
        size_t size() override;
};

void PriorityStateQueue::push(State *state) {
    this->queue.push(state);
}

State* PriorityStateQueue::pop(){
    State *top = this->queue.top();
    this->queue.pop();
    return top;
}

size_t PriorityStateQueue::size(){
    return this->queue.size();
}

void LIFOStateQueue::push(State *state) {
    this->stack.push(state);
}

State* LIFOStateQueue::pop() {
    State *top = this->stack.top();
    this->stack.pop();
    return top;
}

size_t LIFOStateQueue::size() {
    return this->stack.size();
}

void FIFOStateQueue::push(State *state) {
    this->queue.push(state);
}

State* FIFOStateQueue::pop() {
    State *top = this->queue.front();
    this->queue.pop();
    return top;
}

size_t FIFOStateQueue::size() {
    return this->queue.size();
}