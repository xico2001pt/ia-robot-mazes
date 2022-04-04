#include "algorithms/SearchProblemSolver.h"

SearchProblemSolver::SearchProblemSolver(State &initialState) : initialState(&initialState) {}

std::list<State *> SearchProblemSolver::breadthFirstSearch(int maxDepth) {
    FIFOStateQueue queue{};
    return this->searchAlgorithm(maxDepth, &queue, false, false);
}

std::list<State *> SearchProblemSolver::depthFirstSearch(int maxDepth) {
    LIFOStateQueue stack{};
    return this->searchAlgorithm(maxDepth, &stack, false, false);
}

std::list<State *> SearchProblemSolver::iterativeDeepeningSearch(int maxDepth) {
    std::list<State *> path;
    for (int i = 1; i <= maxDepth; ++i) {
        path = this->depthFirstSearch(i);
        if (!path.empty()) break;
    }
    return path;
}

std::list<State *> SearchProblemSolver::uniformCostSearch(int maxDepth) {
    PriorityStateQueue priorityQueue{};
    return this->searchAlgorithm(maxDepth, &priorityQueue, true, false);
}

std::list<State *> SearchProblemSolver::greedySearch(int maxDepth) {
    PriorityStateQueue priorityQueue{};
    return this->searchAlgorithm(maxDepth, &priorityQueue, false, true);
}

std::list<State *> SearchProblemSolver::AStarSearch(int maxDepth) {
    PriorityStateQueue priorityQueue;
    return this->searchAlgorithm(maxDepth, &priorityQueue, true, true);
}

std::list<State *> SearchProblemSolver::getPath(StateWrapper *stateWrapper) {
    std::list<State *> path;
    for (; stateWrapper != nullptr; stateWrapper = stateWrapper->getParent()) {
        path.push_back(stateWrapper->getState());
    }
    path.reverse();
    return path;
}

std::list<State *>
SearchProblemSolver::searchAlgorithm(int maxDepth, StateQueue *queue, bool hasCost, bool hasHeuristic) {
    return std::list<State *>();
}
