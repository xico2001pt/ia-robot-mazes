from model import MainMenu, Option
from controller import HumanGameController, AIGameController, MainMenuController, GameOverController
from viewer import GameOverViewer, GameViewer, MainMenuViewer

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
        game_types = [
            Option("Player Input", "human"),
            Option("AI Input", "AI")
        ]
        mazes = [Option(f"Maze {str(i).zfill(2)}", f"../assets/mazes/maze{str(i).zfill(2)}.txt") for i in range(1, 21)]
        algorithms = [
            Option("Breadth First Search", "bfs"),
            Option("Depth First Search", "dfs"),
            Option("Iterative Deepening Search", "ids"),
            Option("A-Star", "astar"),
            Option("Greedy", "greedy")
        ]
        heuristics = [
            Option("Directions Heuristic", "direction"),
            Option("LTP Heuristic", "ltp")
        ]
        main_menu = MainMenu(game_types, mazes, algorithms, heuristics)
        super().__init__(main_menu, MainMenuController(main_menu), MainMenuViewer(main_menu))

class GameState(State):
    def __init__(self, model, controller):
        super().__init__(model, controller, GameViewer(model))

class HumanGameState(GameState):
    def __init__(self, model):
        super().__init__(model, HumanGameController(model))

class AIGameState(GameState):
    def __init__(self, model, algorithm, heuristic):
        super().__init__(model, AIGameController(model, algorithm, heuristic))

class GameOverState(State):
    def __init__(self, model):
        super().__init__(model, GameOverController(model), GameOverViewer(model))

if __name__ == "__main__":
    test = MainMenuState()