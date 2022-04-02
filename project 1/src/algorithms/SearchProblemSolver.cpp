#include <queue>
#include <list>
#include "StateQueue.cpp"

class State {
    public:
        virtual bool operator==(const State& rhs) = 0;
};
// TODO: MOVE TO .H
// TODO: CHANGE FILENAME TO SearchProblemSolver.cpp

class StateWrapper {
    private:
        State *state, *parent;
        int depth, priority;
        float totalCost;
    
    public:
        StateWrapper(State &state, State &parent, int depth);
        State * getState();
        State * getParent();
        int getDepth();
        int getPriority();
        float getTotalCost();
        void setPriority(int priority);
        void setTotalCost(float totalCost);
        bool operator<(const StateWrapper &rhs);
};

StateWrapper::StateWrapper(State &state, State &parent, int depth) : state(&state), parent(&parent), depth(depth) {
    totalCost = 0;
    priority = 0;
}

State * StateWrapper::getState() { return this->state; }

State * StateWapper::getParent() { return this->parent; }

int StateWrapper::getDepth() { return this->depth; }

int StateWrapper::getPriority() { return this->priority; }

float StateWrapper::getTotalCost() { return this->totalCost; }

void StateWrapper::setPriority(int priority) { this->priority = priority; }

void StateWrapper::setTotalCost(int totalCost) {this->totalCost = totalCost; }

bool StateWrapper::operator<(const StateWrapper &rhs) { return priority < rhs.priority; }

class SearchProblemSolver {
    private:
        State *initialState;

        std::list<State *> searchAlgorithm(int maxDepth, StateQueue *queue, bool hasCost, bool hasHeuristic);

    public:
        SearchProblemSolver(State &initialState);
        
        virtual int cost(State *state) = 0;

        virtual int heuristic(State *state) = 0;
        
        virtual std::list<State *> operators(State *state) = 0;
        
        virtual bool isFinalState(State *state) = 0;

        std::list<State *> breadthFirstSearch(int maxDepth);

        std::list<State *> depthFirstSearch(int maxDepth);

        std::list<State *> iterativeDeepeningSearch(int maxDepth);

        std::list<State *> uniformCostSearch(int maxDepth);
        
        std::list<State *> greedySearch(int maxDepth);

        std::list<State *> AStarSearch(int maxDepth);

        std::list<State *> getPath(StateWrapper *stateWrapper);
};

SearchProblemSolver::SearchProblemSolver(State &initialState) : initialState(&initialState) {}

std::list<State *> SearchProblemSolver::breadthFirstSearch(int maxDepth) {
    FIFOStateQueue queue;
    return this->searchAlgorithm(maxDepth, &queue, false, false);
}

std::list<State *> SearchProblemSolver::depthFirstSearch(int maxDepth) {
    LIFOStateQueue stack;
    return this->searchAlgorithm(maxDepth, &stack, false, false);
}

std::list<State *> SearchProblemSolver::iterativeDeepeningSearch(int maxDepth) {
    std::list<State *> path;
    for (int i = 1; i <= maxDepth; ++i) {
        path = this->depthFirstSearch(i);
        if (path.size() > 0) break;
    }
    return path;
}

std::list<State *> SearchProblemSolver::uniformCostSearch(int maxDepth) {
    PriorityStateQueue priorityQueue;
    return this->searchAlgorithm(maxDepth, &priorityQueue, true, false);
}

std::list<State *> SearchProblemSolver::greedySearch(int maxDepth) {
    PriorityStateQueue priorityQueue;
    return this->searchAlgorithm(maxDepth, &priorityQueue, false, true);
}

std::list<State *> SearchProblemSolver::AStarSearch(int maxDepth) {
    PriorityStateQueue priorityQueue;
    return this->searchAlgorithm(maxDepth, &priorityQueue, true, true);
}

std::list<State *> getPath(StateWrapper *stateWrapper) {
    std::list<State *> path;
    for (; stateWrapper != null; stateWrapper = stateWrapper.getParent()) {
        path.push_back(stateWrapper.getState());
    }
    path.reverse();
    return path;
}