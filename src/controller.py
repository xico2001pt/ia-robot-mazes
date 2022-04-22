from graphics import Action
from model import GameOverInformation, Position, Game
from maze import Maze
from RobotMazeSolver import RobotMazeSolver, RobotMazeState
from heuristics import LTPHeuristic, DirectionsHeuristic
import state

class Controller:
    def __init__(self, model):
        self.model = model
    
    def update(self, game_loop, actions, elapsed_time):
        for action in actions:
            if action == Action.QUIT:
                game_loop.stop()
                return
            self.handle_action(game_loop, action, elapsed_time)
        self.step(game_loop, elapsed_time)

    def handle_action(self, game_loop, action, elapsed_time):
        raise NotImplementedError()
    
    def step(self, game_loop, elapsed_time):
        raise NotImplementedError()

class MainMenuController(Controller):
    def handle_action(self, game_loop, action, elapsed_time):
        if action == Action.ENTER:
            game_loop.set_state(self.get_state_selected())
        elif action == Action.DOWN:
            self.model.get_selections().next_option()
        elif action == Action.UP:
            self.model.get_selections().previous_option()
        elif action == Action.RIGHT:
            self.model.get_selections().get_selected_option().next_option()
        elif action == Action.LEFT:
            self.model.get_selections().get_selected_option().previous_option()
    
    def step(self, game_loop, elapsed_time):
        pass

    def get_state_selected(self):
        game_type, maze_path, algorithm = (selection.get_selected_option().get_value() for selection in self.model.get_selections().get_options())
        maze = Maze(maze_path)
        model = Game(maze)
        if game_type == "human":
            from state import HumanGameState
            return HumanGameState(model)
        elif game_type == "AI":
            from state import AIGameState
            return AIGameState(model, algorithm)

class GameController(Controller):
    directions = {
        'U': (0,-1),
        'D': (0, 1),
        'R': (1,0),
        'L': (-1,0)
    }

    def __init__(self, model):
        super().__init__(model)
        self.speed = 0.05
        self.running = False
        self.solver = RobotMazeSolver(RobotMazeState([]), self.model.get_maze(), LTPHeuristic(self.model.get_maze()))

    def handle_action(self, game_loop, action, elapsed_time):
        raise NotImplementedError("GameController is an abstract class")
    
    def set_gameover_state(self, game_loop):
        game_loop.set_state(state.GameOverState(GameOverInformation()))
    
    def step(self, game_loop, elapsed_time):
        if(abs(self.model.current_pos.x - self.model.target_pos.x) < 0.01 and
            abs(self.model.current_pos.y - self.model.target_pos.y) < 0.01):
            if(self.model.current_target < len(self.model.path)):
                if(self.model.path[self.model.current_target] in ['U','D','L','R']):
                    d = self.directions[self.model.path[self.model.current_target]]
                    self.model.target_pos = Position(self.model.current_pos.x + 0.25*d[0], self.model.current_pos.y + 0.25*d[1])
                else:
                    self.model.target_pos = Position(*self.model.path[self.model.current_target])
                
                if(self.model.current_target == 0 or self.model.path[self.model.current_target - 1] not in ['U','D','L','R']): #Positions after UDLR are 'reset' positions (Character bounces against wall and comes back to its original position)
                    self.model.get_sequence().advance_instruction()
                self.model.current_target += 1
            elif(self.running): # Final target achieved
                self.model.end_game()
                self.set_gameover_state(game_loop)
        else:
            self.move_toward_target()
    
    def move_toward_target(self):
        delta_x = self.model.target_pos.x-self.model.current_pos.x
        delta_y = self.model.target_pos.y-self.model.current_pos.y
        self.model.current_pos.x += min(self.speed*(1 if delta_x > 0 else -1), delta_x, key=abs)
        self.model.current_pos.y += min(self.speed*(1 if delta_y > 0 else -1), delta_y, key=abs)

    def calculate_path(self):
        self.model.path.clear()
        visited = set()
        position = self.model.maze.start_position
        end_position = self.model.maze.end_position
        while (position not in visited and position != end_position):
            visited.add(position)
            for instruction in self.model.sequence.get_sequence():
                # Obtain next position
                if instruction == 'U':               
                    next_position = (position[0], position[1] - 1)
                elif instruction == 'D':
                    next_position = (position[0], position[1] + 1)
                elif instruction == 'L':
                    next_position = (position[0] - 1, position[1])
                elif instruction == 'R':
                    next_position = (position[0] + 1, position[1])
                
                self.model.path += [position]

                # Check if nextPosition is obtainable
                if self.model.maze.connected(position, next_position):
                    position = next_position
                    if(position == end_position):
                        self.model.path += [position]
                        break
                else:
                    self.model.path += [instruction]
        if(self.model.path[-1] in ['U','D','L','R']):
            self.model.path += [position]

class HumanGameController(GameController):
    actions = {
        Action.UP: 'U',
        Action.DOWN: 'D',
        Action.LEFT: 'L',
        Action.RIGHT: 'R'
    }

    def __init__(self, model):
        super().__init__(model)

    def handle_action(self, game_loop, action, elapsed_time):
        if not self.running:
            if action == Action.ENTER and self.model.sequence.full():
                self.calculate_path()
                self.running = True
            elif action in [Action.UP,Action.DOWN,Action.LEFT,Action.RIGHT]:
                self.model.add_instruction(self.actions[action])
            elif action == Action.BACKSPACE:
                self.model.pop_instruction()
        if self.model.gameover:
            if action == Action.ENTER:
                exit(0)
        
    
class AIGameController(GameController):
    def __init__(self, model, algorithm='bfs', max_depth=15):
        super().__init__(model)
        algorithms = {
            'bfs': self.solver.breath_first_search,
            'dfs': self.solver.depth_first_search,
            'ids': self.solver.iterative_deepening_search,
            'astar': self.solver.A_star_search,
            'greedy': self.solver.greedy_search
        }
        self.algorithm = algorithms[algorithm]
        self.algorithm_name = algorithm
        self.max_depth = max_depth
    
    def handle_action(self, game_loop, action, elapsed_time):
        if not self.running:
            if action == Action.ENTER:
                solution = self.algorithm(self.max_depth)
                last_state = solution[0][-1]
                self.visited_nodes = solution[1]
                self.model.set_instructions(last_state.get_instructions())
                self.calculate_path()
                self.running = True
        if self.model.gameover:
            if action == Action.ENTER:
                exit(0)
    
    def set_gameover_state(self, game_loop):
        game_loop.set_state(state.GameOverState(GameOverInformation(self.algorithm_name, self.visited_nodes)))


class GameOverController(Controller):
    def handle_action(self, game_loop, action, elapsed_time):
        if action == Action.ENTER:
            exit(0)
    
    def step(self, game_loop, elapsed_time):
        pass