from model import MainMenu
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
    def __init__(self):
        game_types = [("Player Input", HumanGameState), ("AI Input", AIGameState)]
        mazes = [(f"Maze {str(i).zfill(2)}", f"../assets/mazes/maze{str(i).zfill(2)}.txt") for i in range(1, 21)]
        main_menu = MainMenu(game_types, mazes)
        super().__init__(main_menu, MainMenuController(main_menu), MainMenuViewer(main_menu))

class GameState(State):
    def __init__(self, model, controller):
        super().__init__(model, controller, GameViewer(model))

class HumanGameState(GameState):
    def __init__(self, model):
        super().__init__(model, HumanGameController(model))

class AIGameState(GameState):
    def __init__(self, model):
        super.__init__(model, AIGameController(model, "bfs"))

if __name__ == "__main__":
    test = MainMenuState()