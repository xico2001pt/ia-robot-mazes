from solver import State, SearchProblemSolver, StateWrapper

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
    def __init__(self, initial_state, maze, heuristic):
        super().__init__(initial_state)
        self.maze = maze

        self.heuristic = heuristic
    
    def cost(self, state):
        return len(state)
    
    def operators(self, state):
        new_states = []
        instructions = state.get_instructions()
        
        for instruction in ['U','D','L','R']:
            new_instructions = instructions.copy() + [instruction]
            new_states.append(RobotMazeState(new_instructions))

        return new_states
    
    def get_final_position(self, state):
        #if state.has_cycle(): TODO:
        #    return False
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
                    return position

                # Check if nextPosition is obtainable
                if self.maze.connected(position, nextPosition):
                    position = nextPosition
        return position
    
    def search_algorithm(self, max_depth, queue, has_cost, has_heuristic):
        """Cycles through the states according to the given data structure and operators up to a maximum depth.

        Parameters
        ----------
        max_depth : int
            Maximum depth that the algorithm will reach
        
        queue : buffer
            Data Structure used to cycle through the states. Eg: FIFO, LIFO, ...
        
        Return Value
        ----------
        ([State], int) : Tuple with the path if a solution is found, or empty list if not, and the cost of the solution.
        """
        queue.put(StateWrapper(self.initial_state, 0, None))

        visited_nodes = 1
        while queue.qsize() > 0:
            state_wrapper = queue.get()

            # Check for final state
            if self.is_final_state(state_wrapper.state):
                #print('cost', next_state_wrapper.cost, 'visited_nodes', visited_nodes)
                return (SearchProblemSolver.get_path(state_wrapper), visited_nodes)

            visited_nodes += 1
            depth = state_wrapper.depth
            depth += 1
            if depth > max_depth:
                continue

            next_states = self.operators(state_wrapper.state)
            filter(lambda state: state != state_wrapper.parent, next_states) # Exludes the previous state

            for next_state in next_states:
                next_state_wrapper = StateWrapper(next_state, depth, state_wrapper)

                # Update cost
                cost = self.cost(next_state)
                next_state_wrapper.cost = cost if has_cost or has_heuristic else depth

                # Update priority
                next_state_wrapper.priority = cost if has_cost else 1
                final_position = self.get_final_position(next_state)
                final_position = final_position if final_position != False else (0,0)
                next_state_wrapper.priority += self.heuristic(next_state, final_position, self.maze.end_position) if has_heuristic else 0

                queue.put(next_state_wrapper)
        return ([], visited_nodes)

    def is_final_state(self, state):
        return self.get_final_position(state) == self.maze.end_position

# Testing
if __name__ == "__main__":
    from maze import Maze
    from heuristics import *

    for test in range(20):
        print(f"Testing maze {test + 1}")
        maze = Maze(f"../assets/mazes/maze{str(test+1).zfill(2)}.txt")
        solver = RobotMazeSolver(RobotMazeState([]), maze, LTPHeuristic(maze))
        solution = solver.A_star_search(15)
        if len(solution[0][-1]) > maze.minimum_instructions:
            print(f"Maze: {test + 1} Solution: {solution[0][-1]} visited {solution[1]} states")