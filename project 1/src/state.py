from controller import HumanGameController, AIGameController, MainMenuController
from viewer import GameViewer, MainMenuViewer

class State:
    def __init__(self, model, controller, viewer):
        self.model = model
        self.controller = controller
        self.viewer = viewer
    
    def get_model(self):
        return self.model
    
    def step(self, game_loop, gui, elapsed_time):
        actions = gui.get_actions()

        self.controller.update(game_loop, actions, elapsed_time)

        gui.clear()
        self.viewer.draw(gui)
        gui.refresh()

class MainMenuState(State):
    def __init__(self, main_menu):
        super().__init__(main_menu, MainMenuController(main_menu), MainMenuViewer(main_menu))

class GameState(State):
    def __init__(self, model):
        super().__init__(model, AIGameController(model), GameViewer(model))