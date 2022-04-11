from graphics import Action

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
    def handle_action(self, game_loop, action, elapsed_time):
        pass
    
    def step(self, game_loop, elapsed_time):
        pass # TODO