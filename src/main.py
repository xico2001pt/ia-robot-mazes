from loop import GameLoop
from graphics import PygameScreenGUI
from state import MainMenuState

def main():
    game_gui = PygameScreenGUI(500, 500)
    game_loop = GameLoop(30, game_gui, MainMenuState())
    game_loop.run()
    game_gui.close()

if __name__ == '__main__':
    main()