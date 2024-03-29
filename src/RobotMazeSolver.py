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
    with open("../docs/results.md", "w") as f:
        f.write("| Maze | DFS | IDS | BFS | Uniform | Greedy (Directions Heuristic) | Greedy (LTP Heuristic) | A* (Directions Heuristic) | A* (LTP Heuristic) |\n")
        f.write("| --- " * 9 + "|\n")
        for test in range(1, n_mazes + 1):
            maze_name = f"maze{str(test).zfill(2)}"
            f.write(f"| {maze_name} |")
            maze = Maze(f"../assets/mazes/{maze_name}.txt")
            solver = RobotMazeSolver(RobotMazeState([]), maze)
            algorithms = [
                solver.depth_first_search,
                solver.iterative_deepening_search,
                solver.breath_first_search,
                solver.uniform_cost_search,
                solver.greedy_search,
                solver.A_star_search
            ]
            heuristics = [
                DirectionsHeuristic(maze),
                LTPHeuristic(maze)
            ]
            print(f"> Testing {maze_name}")
            for algorithm in algorithms:
                if not (algorithm.__name__ == "greedy_search" or algorithm.__name__ == "A_star_search"):
                    print(f" - Running {algorithm.__name__}")
                    f.write(f" {algorithm(15)[1]} |")
                else:
                    for n, heuristic in enumerate(heuristics):
                        solver.heuristic = heuristic
                        print(f" - Running {algorithm.__name__} with Heuristic {n + 1}")
                        f.write(f" {algorithm(15)[1]} |")
            f.write("\n")