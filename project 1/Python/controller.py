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
    def __init__(self, model): # TODO: Remove, it's only for debug
        super().__init__(model)
        self.model.path = [(1,4), (0,4), (0,3), (0,2), (1,2), (1,1), (1,0), (2,0), (3,0), (4,0), (4,1), (3,1)]
        self.current_target = -1
        self.speed = 0.05

    def handle_action(self, game_loop, action, elapsed_time):
        pass
    
    def step(self, game_loop, elapsed_time):
        if(abs(self.model.current_pos.x - self.model.target_pos.x) < 0.01 and
            abs(self.model.current_pos.y - self.model.target_pos.y) < 0.01):
            if(self.current_target < len(self.model.path)-1):
                self.current_target += 1
                self.model.target_pos = Position(*self.model.path[self.current_target])
        else:
            delta_x = self.model.target_pos.x-self.model.current_pos.x
            delta_y = self.model.target_pos.y-self.model.current_pos.y
            self.model.current_pos.x += min(self.speed*(1 if delta_x > 0 else -1), delta_x, key=abs)
            self.model.current_pos.y += min(self.speed*(1 if delta_y > 0 else -1), delta_y, key=abs)