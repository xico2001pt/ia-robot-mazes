from loop import GameLoop
from graphics import PygameGUI
from state import GameState, MainMenuState
from model import MainMenu, Game

def main():
    from maze import Maze
    m = Maze("example_maze.txt")

    dimensions = m.get_size()
    game_gui = PygameGUI(dimensions[0]*150, dimensions[1]*150) #TODO: Remove hardcoded width
    #game_loop = GameLoop(30, game_gui, MainMenuState(MainMenu()))
    game_loop = GameLoop(30, game_gui, GameState(Game(m)))
    game_loop.run()

if __name__ == '__main__':
    main()