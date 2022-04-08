from loop import GameLoop
from graphics import PygameGUI
from state import MainMenuState
from model import MainMenu

def main():
    from maze import Maze
    m = Maze()
    m.open_from_file("example_maze.txt")

    game_gui = PygameGUI(500, 500)
    game_loop = GameLoop(30, game_gui, MainMenuState(MainMenu()))
    game_loop.run()

if __name__ == '__main__':
    main()