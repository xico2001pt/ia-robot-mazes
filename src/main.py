from loop import GameLoop
from graphics import PygameScreenGUI
from state import MainMenuState
from model import MainMenu, Game
from viewer import GameViewer

def main():
    from maze import Maze

    m = Maze("../assets/mazes/maze06.txt")
    print(GameViewer(Game(m)).get_size())
    game_gui = PygameScreenGUI(500, 500) #TODO: This is absolutely stupid
    game_loop = GameLoop(30, game_gui, MainMenuState())
    game_loop.run()
    game_gui.close()

if __name__ == '__main__':
    main()