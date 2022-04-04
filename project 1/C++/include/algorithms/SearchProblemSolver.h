#ifndef ROBOT_MAZES_SEARCHPROBLEMSOLVER_H
#define ROBOT_MAZES_SEARCHPROBLEMSOLVER_H

#include <list>
#include "algorithms/StateQueue.h"

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

#endif //ROBOT_MAZES_SEARCHPROBLEMSOLVER_H
