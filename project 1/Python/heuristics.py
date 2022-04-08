from solver import State, SearchProblemSolver

class LTPState(State):
    def __init__(self, x, y, turns=[]):
        self.x = x
        self.y = y
        self.turns = turns

    def get_number_of_turns(self):
        return len(self.turns)
    
    def __str__(self):
        return f"({self.x},{self.y}) - {self.turns}"

    def __eq__(self, other):
        if isinstance(other, LTPState):
            return self.x == other.x and self.y == other.y and self.turns == other.turns
        return False

class LTPSolver(SearchProblemSolver):
    def cost(self, state):
        return state.get_number_of_turns()
    
    def operators(self, state):
        raise NotImplementedError()

    def is_final_state(self, state):
        raise NotImplementedError()
    
