from loop import GameLoop
from graphic import GUI

def main():
    game_gui = GUI(500, 500)
    game_loop = GameLoop(30, game_gui)
    game_loop.run()

if __name__ == '__main__':
    main()