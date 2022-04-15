# Robot Mazes Quick Guide

## Function Calls Description

1. **main**()

   1. m = **Maze**("../assets/mazes/maze10.txt") `Initializes a maze from an input file.`

      1. **open_from_file**("../assets/mazes/maze10.txt") `Reads maze dimensions, initial and final position and minimum number of instructions needed to complete the maze (admitting they're in the correct order, meaning, no error detection is implemented).`
         1. **read_layout**(lines) `Reads the maze layout from the input file and puts it in an adjancencies list e.g. {(0,0): [(1,0),(0,1)]}.`

   2. game_gui = **PygameScreenGUI**(*GameViewer(Game(m)).get_size()) `Initializes Pygame, screen mode with the given size and font (default: monospace 64).`

      > **Note:** This will be changed in the future since we're wastefully creating a GameViewer just to calculate the screen size needed.

      1. **GameViewer**(Game(m))**.get_size()** `Initializes a Viewer for the Game instantiated inside of it, it contains a MazeViewer, an InstructionsSequenceViewer, a PathViewer and a CharacterViewer. The size returned is calculated with the Maze size and Instructions size.`
         1.  **Game**(m) `Initializes a game Model, containing the maze and path that can be empty. It keeps information about the Instructions Sequence (basically a stack with a defined size equal to the minimum number of instructions from the file), the current position (initially the start) and a target position and current target.`

   3. game_loop = **GameLoop**(30, game_gui, GameState(Game(m))) `Initializes the game loop, receives the fps at which the game will be run, the game GUI initialized above and a State, respectively.`

      > **Note:** self.gui.close() shouldn't be in run().

      1. **GameState**(Game(m)) `Initializes a GameState containing a Model. In its contructor a Viewer and Controller (MVC) are instanciated (further explanation available bellow).`

   4. game_loop.**run()** `Initially the GameLoop isn't "running", a run() function must be called. This function is responsible for advancing a Step in the controller (present in the State given in the constructor of the GameLoop) and for waiting if the the Step took less time than a frame time (1/30 seconds per frame in our case).`

## MVC Explanation

The State has a Model, Viewer and Controller. Furthermore, it has a `step(game_loop, gui, elapsed_time)` function that receives the GameLoop, the GUI and the elapsed time. This function is called by the GameLoop each seconds per frame elapsed. `step()` is responsible for:

1. Getting actions from the GUI;
2. Updating the Controller with the actions received and the time elapsed;
3. Clearing, drawing (responsibility of the Viewer) and refreshing the GUI.

> **Note:** The Controller handles the modification of the Model, since both the Controller and the Viewer maintain a copy of it its modification will reflect on a modification in the Viewer.

In the current version we have two States implemented: *MainMenuState* and *GameState*. They both create their Controller and Viewer in their constructor and pass to them the Model received as the constructor's argument (e.g. `super().__init__(model, AIGameController(model), GameViewer(model))`).

The Controller receives a Model. It has an `update()`, `handle_action()` and `step()` functions:

- `update(game_loop, actions, elapsed_time)` - It's implemented in the parent class. For each action received it calls the `handle_action()` method, after all the actions have been handled the `step()` method is executed;
- `handle_action(game_loop, action, elapsed_time)` - It needs to be implemented by the child classes. It's responsible for analysing the action requested and execute the command(s) it's instructed to do when they happen (e.g. in the AIGameController, when it's not running and the action is ENTER it must calculate the solution of the maze, modify the current instructions in the Model, calculate the path it takes and make itself run).
- `step()` - It needs to be implemented by the child classes. It's responsible to modify the visual aspect of the Model that'll be displayed in the next frame.