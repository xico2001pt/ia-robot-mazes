from solver import State, SearchProblemSolver

class RobotMazeState(State):
    def __init__(self, instructions):
        self.instructions = instructions
        # ['U','D','L','R']

    def get_instructions(self):
        return self.instructions
    
    def __str__(self):
        return '[' + ', '.join(i for i in self.get_instructions()) + ']'
    
    def __eq__(self, other):
        if isinstance(other, RobotMazeState):
            return self.get_instructions() == other.get_instructions()
        return False

class RobotMazeSolver(SearchProblemSolver):
    def __init__(self, initial_state):
        super.__init__(initial_state)
        # TODO: Add adjacencies matrix
    
    def cost(self, state):
        instructions = state.get_instructions()
        return len(instructions) - (1 if instructions[-1] == 'E' else 0) # TODO: Empty instructions
    
    def heuristic(self, state):
        raise NotImplementedError()
    
    def operators(self, state):
        new_states = []
        instructions = state.get_instructions()
        if (instructions[-1] != 'E'): # TODO: Empty instructions
            for instruction in ['U','D','L','R']:
                new_states.append(instructions.copy() + [instruction])
        
            # TODO: Verify if there's a cycle before adding (= verify if the first half is equal to the second half)
            new_states.append(instructions.copy() + ['E'])
        else: # Already ended
            return []
        return new_states
    
    def is_final_state(self, state):
        # TODO: Simulate and check if reaches end
        raise NotImplementedError()