from queue import Queue, LifoQueue, PriorityQueue

class State:
    def __str__(self):
        raise NotImplementedError()
    
    def __eq__(self, other):
        raise NotImplementedError()

class StateWrapper:
    def __init__(self, state, depth, parent):
        self.state = state
        self.depth = depth
        self.parent = parent
        self.cost = 0
        self.priority = 0
    
    def __lt__(self, other):
        return self.priority < other.priority

class SearchProblemSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
    
    def set_initial_state(self, initial_state):
        self.initial_state = initial_state
    
    # Methods to be overwritten
    def cost(self, state):
        raise NotImplementedError()
    
    def heuristic(self, state):
        raise NotImplementedError()
    
    def operators(self, state):
        raise NotImplementedError()
    
    def is_final_state(self, state):
        raise NotImplementedError()
    
    #################################
    
    def breath_first_search(self, max_depth):
        return self.search_algorithm(max_depth, Queue(), False, False)
    
    def depth_first_search(self, max_depth):
        return self.search_algorithm(max_depth, LifoQueue(), False, False)
    
    def iterative_deepening_search(self, max_iterations):
        total_visited_nodes = 0
        for i in range(1, max_iterations + 1):
            (path, visited_nodes) = self.depth_first_search(i)
            total_visited_nodes += visited_nodes
            if len(path) > 0:
                break
        return (path, total_visited_nodes)

    def uniform_cost_search(self, max_depth):
        return self.search_algorithm(max_depth, PriorityQueue(), True, False)

    def greedy_search(self, max_depth):
        return self.search_algorithm(max_depth, PriorityQueue(), False, True)

    def A_star_search(self, max_depth):
        return self.search_algorithm(max_depth, PriorityQueue(), True, True)

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
            #print(f"{' ' * state_wrapper.depth}{state_wrapper.state.instructions} - {state_wrapper.depth}")

            # Check for final state
            if self.is_final_state(state_wrapper.state):
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
                next_state_wrapper.priority += self.heuristic(next_state) if has_heuristic else 0

                queue.put(next_state_wrapper)
        return ([], visited_nodes)

    def get_path(state_wrapper):
        result = []
        while state_wrapper.parent != None:
            result.append(state_wrapper.state)
            state_wrapper = state_wrapper.parent
        result.append(state_wrapper.state)
        return result[::-1]
    
    def path_to_string(path):
        return "[{}]".format(", ".join(str(state) for state in path))
