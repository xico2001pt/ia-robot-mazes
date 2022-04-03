#ifndef ROBOT_MAZES_STATE_H
#define ROBOT_MAZES_STATE_H

class State {
public:
    virtual bool operator==(const State& rhs) = 0;
};

class StateWrapper {
private:
    State *state;
    StateWrapper *parent;
    int depth, priority;
    int totalCost;

public:
    StateWrapper(State &state, StateWrapper &parent, int depth);
    State * getState();
    StateWrapper * getParent();
    int getDepth() const;
    int getPriority() const;
    float getTotalCost() const;
    void setPriority(int priority);
    void setTotalCost(int totalCost);
    bool operator<(const StateWrapper &rhs) const;
};
#endif //ROBOT_MAZES_STATE_H
