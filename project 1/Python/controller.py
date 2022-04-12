from graphics import Action
from model import Position

class Controller:
    def __init__(self, model):
        self.model = model
    
    def update(self, game_loop, actions, elapsed_time):
        for action in actions: # TODO: QUIT SHOULD BE HANDLED HERE, BECAUSE IT DOES THE SAME THING EVERYTIME
            self.handle_action(game_loop, action, elapsed_time)
        self.step(game_loop, elapsed_time)

    def handle_action(self, game_loop, action, elapsed_time):
        raise NotImplementedError()
    
    def step(self, game_loop, elapsed_time):
        raise NotImplementedError()

class MainMenuController(Controller):
    def handle_action(self, game_loop, action, elapsed_time):
        if action == Action.QUIT:
            print("Bye")
            game_loop.stop()
        elif action == Action.ENTER:
            self.model.x = 0
    
    def step(self, game_loop, elapsed_time):
        self.model.x += 1

class GameController(Controller):
    directions = {
        'U': (0,-1),
        'D': (0, 1),
        'R': (1,0),
        'L': (-1,0)
    }
    actions = {
        Action.UP: 'U',
        Action.DOWN: 'D',
        Action.LEFT: 'L',
        Action.RIGHT: 'R'
    }

    def __init__(self, model):
        super().__init__(model)
        self.speed = 0.05
        self.running = False

    def handle_action(self, game_loop, action, elapsed_time):
        if not self.running:
            if action == Action.ENTER and self.model.sequence.full():
                self.calculate_path()
                self.running = True
            if action in [Action.UP,Action.DOWN,Action.LEFT,Action.RIGHT] and not self.model.sequence.full():
                self.model.add_instruction(self.actions[action])
    
    def step(self, game_loop, elapsed_time):
        if(abs(self.model.current_pos.x - self.model.target_pos.x) < 0.01 and
            abs(self.model.current_pos.y - self.model.target_pos.y) < 0.01):
            if(self.model.current_target < len(self.model.path)):
                if(self.model.path[self.model.current_target] in ['U','D','L','R']):
                    d = self.directions[self.model.path[self.model.current_target]]
                    self.model.target_pos = Position(self.model.current_pos.x + 0.25*d[0], self.model.current_pos.y + 0.25*d[1])
                else:
                    self.model.target_pos = Position(*self.model.path[self.model.current_target])
                self.model.current_target += 1
        else:
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