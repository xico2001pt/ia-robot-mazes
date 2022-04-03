#include "algorithms/StateQueue.h"


StateQueue::StateQueue() {}

PriorityStateQueue::PriorityStateQueue() {}

void PriorityStateQueue::push(StateWrapper *state) {
    this->queue.push(state);
}

StateWrapper* PriorityStateQueue::pop(){
    StateWrapper *top = this->queue.top();
    this->queue.pop();
    return top;
}

size_t PriorityStateQueue::size(){
    return this->queue.size();
}

LIFOStateQueue::LIFOStateQueue() {}

void LIFOStateQueue::push(StateWrapper *state) {
    this->stack.push(state);
}

StateWrapper* LIFOStateQueue::pop() {
    StateWrapper *top = this->stack.top();
    this->stack.pop();
    return top;
}

size_t LIFOStateQueue::size() {
    return this->stack.size();
}

FIFOStateQueue::FIFOStateQueue() {}

void FIFOStateQueue::push(StateWrapper *state) {
    this->queue.push(state);
}

StateWrapper* FIFOStateQueue::pop() {
    StateWrapper *top = this->queue.front();
    this->queue.pop();
    return top;
}

size_t FIFOStateQueue::size() {
    return this->queue.size();
}
