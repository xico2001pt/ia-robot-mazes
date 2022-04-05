from loop import GameLoop
from graphics import PygameGUI

def main():
    game_gui = PygameGUI(500, 500)
    game_loop = GameLoop(30, game_gui)
    game_loop.run()

if __name__ == '__main__':
    main()