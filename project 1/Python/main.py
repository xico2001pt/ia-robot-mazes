from loop import GameLoop
from graphics import PygameGUI
from state import MainMenuState
from model import MainMenu
from RobotMazeSolver import RobotMazeSolver, RobotMazeState

def main():
    from maze import Maze
    m = Maze("example_maze.txt")
    state = RobotMazeState(['R','U','U','U','R'])   # Solution: ['R','U','U','U','R','R']
    solver = RobotMazeSolver(state, m)
    print(solver.is_final_state(state))

    """
    game_gui = PygameGUI(500, 500)
    game_loop = GameLoop(30, game_gui, MainMenuState(MainMenu()))
    game_loop.run()
    """

if __name__ == '__main__':
    main()