from loop import GameLoop
from graphics import PygameScreenGUI
from state import GameState, MainMenuState
from model import MainMenu, Game
from viewer import GameViewer

def main():
    from maze import Maze

    m = Maze("../assets/mazes/maze06.txt")
    game_gui = PygameScreenGUI(*GameViewer(Game(m)).get_size()) #TODO: This is absolutely stupid
    game_loop = GameLoop(30, game_gui, MainMenuState(MainMenu()))
    #game_loop = GameLoop(30, game_gui, GameState(Game(m)))
    game_loop.run()

if __name__ == '__main__':
    main()