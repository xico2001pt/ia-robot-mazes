from graphics import PygameSurfaceGUI
from model import InstructionSequence, Position
import graphics_consts as consts

class Viewer:
    def __init__(self, model):
        self.model = model    

    def draw_background(self, color, gui):
        gui.fill_screen(color)
    
    def draw(self, gui):
        raise NotImplementedError()

class MainMenuViewer(Viewer):
    def draw(self, gui):
        self.draw_background(consts.BACKGROUND_COLOR, gui)
        self.draw_title(gui)
        self.draw_credits(gui)
        self.draw_selections(gui)
    
    def draw_title(self, gui):
        gui.draw_centered_text("Robot Mazes", Position(gui.get_width()/2, gui.get_height()*0.2), consts.MENU_TITLE_COLOR, consts.MENU_TITLE_SIZE)

    def draw_credits(self, gui):
        lines = ["Members:", "Adriano Soares", "Filipe Campos", "Francisco Cerqueira"]
        for idx, line in enumerate(lines):
            gui.draw_text(line, Position(consts.MENU_CREDITS_PADDING, gui.get_height()-(len(lines)-idx)*consts.MENU_CREDITS_SIZE-consts.MENU_CREDITS_PADDING), consts.MENU_CREDITS_COLOR, consts.MENU_CREDITS_SIZE)
    
    def draw_selections(self, gui):
        selected_selection = self.model.get_selected_selection()
        options_selected = self.model.get_selected_options()
        if options_selected["state"] == "human":
            options_selected.pop("algorithm")
            options_selected.pop("heuristic")
        elif options_selected["state"] == "AI":
            algorithm_selected = options_selected["algorithm"]
            if not (algorithm_selected == "greedy" or algorithm_selected == "astar"):
                options_selected.pop("heuristic")
        
        spacing = consts.MENU_SELECTION_SIZE + consts.MENU_SELECTION_SPACING
        x, y = gui.get_width()/2, gui.get_height()/2 - (spacing * len(options_selected) - consts.MENU_SELECTION_SPACING)/2

        for selection, option in options_selected.items():
            color = consts.SELECTED_SELECTION_COLOR if selection == selected_selection else consts.UNSELECTED_SELECTION_COLOR
            self.draw_selection(gui, option, Position(x, y), color)
            y += spacing
        
        gui.draw_centered_text("Press ENTER to start", Position(x, y), consts.MENU_ENTER_COLOR, int(consts.MENU_SELECTION_SIZE*0.75))
        if options_selected["state"] == "human":
            y += spacing * 2 / 3
            gui.draw_centered_text("In game press H for a hint", Position(x, y), consts.MENU_ENTER_COLOR, int(consts.MENU_SELECTION_SIZE*0.75))

    def draw_selection(self, gui, option, position, color):
        gui.draw_centered_text("◄ " + str(option) + " ►", position, color, consts.MENU_SELECTION_SIZE)

class MazeViewer(Viewer):
    def __init__(self, model):
        super().__init__(model)

    def get_size(self):
        size = self.model.get_size()
        return (size[0] * consts.BLOCK_WIDTH + 2, size[1] * consts.BLOCK_WIDTH + 2)
    
    def draw(self, gui):
        adj = self.model.get_adjacencies()
        lines = []
        for pos in adj:
            self.draw_block(pos[0], pos[1], gui)
            for offset in [(-1,0), (1,0), (0,1), (0,-1)]:
                neighbour_pos = pos[0] + offset[0], pos[1] + offset[1]
                if(neighbour_pos not in adj[pos]): # Should draw wall between positions
                    lines.append(self.get_line_between_neighbours(pos, neighbour_pos))
        self.draw_walls(lines, gui)
        self.draw_start_and_end(gui)
    
    def get_line_between_neighbours(self, pos, neighbour_pos):
        delta_x, delta_y = neighbour_pos[0] - pos[0], neighbour_pos[1] - pos[1]
        if(delta_x == 0):
            if(delta_y < 0):
                start_position = Position(pos[0]*consts.BLOCK_WIDTH, pos[1]*consts.BLOCK_WIDTH)
            if(delta_y > 0):
                start_position = Position(neighbour_pos[0]*consts.BLOCK_WIDTH, neighbour_pos[1]*consts.BLOCK_WIDTH)
            end_position = Position(start_position.x + consts.BLOCK_WIDTH, start_position.y)
        if(delta_y == 0):
            if(delta_x < 0):
                start_position = Position(pos[0]*consts.BLOCK_WIDTH, pos[1]*consts.BLOCK_WIDTH)
            if(delta_x > 0):
                start_position = Position(neighbour_pos[0]*consts.BLOCK_WIDTH, neighbour_pos[1]*consts.BLOCK_WIDTH)
            end_position = Position(start_position.x, start_position.y + consts.BLOCK_WIDTH)
        return (start_position, end_position)

    def draw_walls(self, lines, gui):
        for start_pos, end_pos in lines:
            gui.draw_line(start_pos, end_pos, consts.WALL_COLOR, 6)
    
    def draw_block(self, x, y, gui):
        x, y = x * consts.BLOCK_WIDTH, y * consts.BLOCK_WIDTH
        gui.draw_rectangle(Position(x, y), consts.BLOCK_WIDTH, consts.BLOCK_WIDTH, consts.BACKGROUND_COLOR) # Draw fill TODO: Remove?
        gui.draw_rectangle(Position(x, y), consts.BLOCK_WIDTH, consts.BLOCK_WIDTH, consts.BORDER_COLOR, 1) # Draw grey border

    def draw_start_and_end(self, gui):
        self.draw_letter_on_block(*self.model.get_start_position(), 'S', gui)
        self.draw_letter_on_block(*self.model.get_end_position(), 'F', gui)
    
    def draw_letter_on_block(self, x, y, letter, gui):
        x = x * consts.BLOCK_WIDTH + consts.BLOCK_WIDTH/2
        y = y * consts.BLOCK_WIDTH + consts.BLOCK_WIDTH/2
        gui.draw_centered_text(letter, Position(x, y), consts.TEXT_COLOR, consts.BLOCK_WIDTH//2)

class GameViewer(Viewer):
    def __init__(self, model):
        super().__init__(model)
        self.OFFSET_X = 25
        self.OFFSET_Y = 25
        self.maze_viewer = MazeViewer(self.model.get_maze())
        self.instructions_viewer = InstructionSequenceViewer(self.model.get_sequence())
        self.path_viewer = PathViewer(self.model.get_path())
        self.character_viewer = CharacterViewer(self.model.current_pos)
    
    def get_size(self):
        maze_size = self.maze_viewer.get_size()
        instruction_size = self.instructions_viewer.get_size()
        return (max(maze_size[0],instruction_size[0])+self.OFFSET_X*2,
            maze_size[1]+instruction_size[1]+self.OFFSET_Y*3)

    def draw(self, gui):
        self.draw_background(consts.WHITE, gui)

        maze_surface = PygameSurfaceGUI(*self.maze_viewer.get_size())
        self.maze_viewer.draw(maze_surface)
        self.path_viewer.draw(maze_surface)
        self.character_viewer.draw(maze_surface)

        instructions_surface = PygameSurfaceGUI(*self.instructions_viewer.get_size())
        self.instructions_viewer.draw(instructions_surface)
        
        gui.blit(maze_surface, (self.OFFSET_X, self.OFFSET_Y))
        gui.blit(instructions_surface, (self.OFFSET_X, self.OFFSET_Y*2 + self.maze_viewer.get_size()[1]))

class InstructionSequenceViewer(Viewer):
    def __init__(self, model):
        super().__init__(model)

    def get_size(self):
        size = self.model.get_size()
        return (size*consts.INSTRUCTION_WIDTH, consts.INSTRUCTION_WIDTH)

    def draw(self, gui):
        size = self.model.get_size()
        gui.draw_rectangle(Position(0, 0), size*consts.INSTRUCTION_WIDTH, consts.INSTRUCTION_WIDTH, consts.BACKGROUND_COLOR)

        sequence = self.model.get_sequence()
        for i in range(self.model.get_size()):
            if(i < len(sequence)):
                pos = Position(consts.INSTRUCTION_WIDTH*i + consts.INSTRUCTION_WIDTH/2, consts.INSTRUCTION_WIDTH/2)
                color = consts.TEXT_COLOR if i != self.model.get_current_instruction() else consts.WALL_COLOR
                gui.draw_centered_text(sequence[i], pos, color, consts.BLOCK_WIDTH//2)
            gui.draw_rectangle(Position(consts.INSTRUCTION_WIDTH*i, 0), size*consts.INSTRUCTION_WIDTH, consts.INSTRUCTION_WIDTH, consts.WALL_COLOR, 5)

class PathViewer(Viewer):
    def __init__(self, model):
        super().__init__(model)
    
    def draw(self, gui):
        for i in range(len(self.model)-1):
            if(self.model[i] not in ['U','D','L','R']):
                start_pos = Position(self.model[i][0]*consts.BLOCK_WIDTH + consts.BLOCK_WIDTH/2, self.model[i][1]*consts.BLOCK_WIDTH + consts.BLOCK_WIDTH/2)
                j = 1
                while(i+j < len(self.model) and self.model[i+j] in ['U','D','L','R']):
                    j += 1

                if(i+j < len(self.model)):
                    end_pos = Position(self.model[i+j][0]*consts.BLOCK_WIDTH + consts.BLOCK_WIDTH/2, self.model[i+j][1]*consts.BLOCK_WIDTH + consts.BLOCK_WIDTH/2)
                    gui.draw_line(start_pos, end_pos, consts.PATH_COLOR, 3)

class CharacterViewer(Viewer):
    def __init__(self, model):
        super().__init__(model)
    
    def draw(self, gui):
        pos = Position(self.model.x*consts.BLOCK_WIDTH + consts.BLOCK_WIDTH/2 - consts.CHARACTER_WIDTH/2, self.model.y*consts.BLOCK_WIDTH + consts.BLOCK_WIDTH/2 - consts.CHARACTER_WIDTH/2)
        gui.draw_image(consts.ROBOT_IMG, pos, consts.CHARACTER_WIDTH, consts.CHARACTER_WIDTH)

class GameOverViewer(Viewer):
    def __init__(self, model):
        super().__init__(model)
    
    def draw(self, gui):
        self.draw_background(consts.BACKGROUND_COLOR, gui)
        width, height = gui.get_width(), gui.get_height()

        gui.draw_rectangle(Position(0,0), width, height, consts.GAMEOVER_BORDER_COLOR, consts.GAMEOVER_BORDER_THICKNESS)
    

        text_height = 20
        gui.draw_centered_text("Gameover", Position(width//2, consts.GAMEOVER_BORDER_THICKNESS*4), consts.GAMEOVER_TITLE_COLOR, consts.GAMEOVER_TITLE_SIZE)
        text_height += consts.GAMEOVER_TITLE_SIZE + 20
        if self.model.algorithm:
            gui.draw_text(f"Algorithm: {self.model.algorithm}", Position(consts.GAMEOVER_BORDER_THICKNESS*2, text_height), consts.GAMEOVER_INFO_COLOR, consts.GAMEOVER_INFO_SIZE)
            text_height += int(consts.GAMEOVER_INFO_SIZE * 1.5)
        if self.model.visited_nodes:
            gui.draw_text(f"Visited: {self.model.visited_nodes}", Position(consts.GAMEOVER_BORDER_THICKNESS*2, text_height), consts.GAMEOVER_INFO_COLOR, consts.GAMEOVER_INFO_SIZE)
            text_height += int(consts.GAMEOVER_INFO_SIZE * 1.5)
        if self.model.time:
            gui.draw_text(f"Time: {self.model.time:.2f} seconds", Position(consts.GAMEOVER_BORDER_THICKNESS*2, text_height), consts.GAMEOVER_INFO_COLOR, consts.GAMEOVER_INFO_SIZE)
            text_height += int(consts.GAMEOVER_INFO_SIZE * 1.5)
        text_height += consts.GAMEOVER_INFO_SIZE * 2
        gui.draw_centered_text("Press ENTER to continue",Position(width//2, text_height), consts.GAMEOVER_INFO_COLOR, consts.GAMEOVER_INFO_SIZE)