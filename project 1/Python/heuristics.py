from solver import State, SearchProblemSolver

class LTPState(State):
    def __init__(self, x, y, current_direction='', turns=[]):
        self.x = x
        self.y = y
        self.current_direction = current_direction
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
    def __init__(self, initial_state, maze):
        super().__init__(initial_state)
        self.maze = maze

    def cost(self, state):
        return state.get_number_of_turns()
    
    def heuristic(self, state):
        raise NotImplementedError()

    def operators(self, state):
        new_states = []
        for pos in self.maze.adjacencies[(state.x, state.y)]:
            delta_x = pos[0] - state.x
            delta_y = pos[1] - state.y
            direction = ''
            if(delta_x == 0):
                direction = 'U' if delta_y < 0 else 'D'
            elif(delta_y == 0):
                direction = 'R' if delta_x > 0 else 'L'
            else:
                raise "TODO: this shouldn't happen"

            turns = state.turns.copy()
            if direction != state.current_direction:
                turns += [direction]
            new_states.append(LTPState(pos[0], pos[1], direction, turns))
        return new_states

    def is_final_state(self, state):
        return state.x == 3 and state.y == 0

if __name__ == "__main__":
    from maze import Maze
    initial_state = LTPState(0, 3)
    maze = Maze('example_maze.txt')
    solver = LTPSolver(initial_state, maze)
    solution = solver.breath_first_search(50)
    print('\n'.join(str(i) for i in solution[0]))
