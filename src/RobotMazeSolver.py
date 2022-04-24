from solver import State, SearchProblemSolver

class RobotMazeState(State):
    def __init__(self, instructions):
        self.instructions = instructions
        # ['U','D','L','R']

    def get_instructions(self):
        return self.instructions
    
    def has_cycle(self):
        n = len(self.instructions)
        for length in range(1, n // 2 + 1):
            if n % length == 0:
                timesRepeated = n // length
                if self.instructions[0 : length] * timesRepeated == self.instructions:
                    return True
        return False            
    
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
        return len(state)
    
    def operators(self, state):
        new_states = []
        instructions = state.get_instructions()
        
        for instruction in ['U','D','L','R']:
            new_instructions = instructions.copy() + [instruction]
            new_states.append(RobotMazeState(new_instructions))

        return new_states
    
    def is_final_state(self, state):
        if state.has_cycle():
            return False
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

# Testing
if __name__ == "__main__":
    from maze import Maze
    from heuristics import *
    n_mazes = 20
    sum_nodes = [0] * 2
    for test in range(1, n_mazes + 1):
        maze = Maze(f"../assets/mazes/maze{str(test).zfill(2)}.txt")
        solver = RobotMazeSolver(RobotMazeState([]), maze, DirectionsHeuristic(maze))
        sum_nodes[0] += solver.A_star_search(15)[1]
        sum_nodes[1] += solver.breath_first_search(15)[1]
    print(f"AStar = {sum_nodes[0]}\nBFS = {sum_nodes[1]}\nAStar/BFS = {sum_nodes[0] / sum_nodes[1]}")