from solver import State, SearchProblemSolver

class RobotMazeState(State):
    def __init__(self, instructions):
        self.instructions = instructions
        # ['U','D','L','R']

    def get_instructions(self):
        return self.instructions
    
    def is_simulation_state(self):
        return len(self.instructions) > 0 and self.instructions[-1] == 'E'
    
    def has_cycle(instructions):
        n = len(instructions) // 2
        return len(instructions) % 2 == 0 and all(instructions[i] == instructions[i+n] for i in range(n))
    
    def __str__(self):
        return '[' + ', '.join(i for i in self.get_instructions()) + ']'
    
    def __eq__(self, other):
        if isinstance(other, RobotMazeState):
            return self.get_instructions() == other.get_instructions()
        return False
    
    def __len__(self):
        return len(self.instructions)

class RobotMazeSolver(SearchProblemSolver):
    def __init__(self, initial_state, maze):
        super().__init__(initial_state)
        self.maze = maze
    
    def cost(self, state):
        return len(state) - (1 if state.is_simulation_state() else 0)
    
    def heuristic(self, state):
        raise NotImplementedError()
    
    def operators(self, state):
        new_states = []
        instructions = state.get_instructions()
        if (not state.is_simulation_state()):
            for instruction in ['U','D','L','R']:
                new_instructions = instructions.copy() + [instruction]
                new_states.append(RobotMazeState(new_instructions))

            if not RobotMazeState.has_cycle(instructions):
                new_states.append(RobotMazeState(instructions.copy() + ['E']))
        else: # Already ended
            return []
        return new_states
    
    def is_final_state(self, state):
        visited = set()
        position = self.maze.start_position
        endPosition = self.maze.end_position
        while (position not in visited) and (position != endPosition):
            # Add current position to the visited set
            visited.add(position)
            for instruction in state.get_instructions():
                # Obtain next position
                if instruction == 'U':               
                    nextPosition = (position[0], position[1] - 1)
                elif instruction == 'D':
                    nextPosition = (position[0], position[1] + 1)
                elif instruction == 'L':
                    nextPosition = (position[0] - 1, position[1])
                elif instruction == 'R':
                    nextPosition = (position[0] + 1, position[1])
                
                if position == endPosition:
                    return True

                # Check if nextPosition is obtainable
                if self.maze.connected(position, nextPosition):
                    position = nextPosition
        return position == endPosition