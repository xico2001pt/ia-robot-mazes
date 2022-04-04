#include "algorithms/State.h"

StateWrapper::StateWrapper(State &state, StateWrapper &parent, int depth) : state(&state), parent(&parent), depth(depth) {
    totalCost = 0;
    priority = 0;
}

State * StateWrapper::getState() { return this->state; }

StateWrapper * StateWrapper::getParent() { return this->parent; }

int StateWrapper::getDepth() const { return this->depth; }

int StateWrapper::getPriority() const { return this->priority; }

float StateWrapper::getTotalCost() const { return this->totalCost; }

void StateWrapper::setPriority(int priority) { this->priority = priority; }

void StateWrapper::setTotalCost(int totalCost) {this->totalCost = totalCost; }

bool StateWrapper::operator<(const StateWrapper &rhs) const { return priority < rhs.priority; }