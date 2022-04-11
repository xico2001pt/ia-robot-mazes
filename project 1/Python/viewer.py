from model import Position

class Viewer:
    def __init__(self, model):
        self.model = model
    
    def get_model(self): # TODO: IS IT NECESSARY?
        return self.model
    
    def draw(self, gui):
        raise NotImplementedError()

class MainMenuViewer(Viewer):
    def draw(self, gui):
        gui.draw_rectangle(Position(10, 10+self.model.x), 50, 50, (0, 255, 0))
        gui.draw_text("Robot Mazes!", Position(10+self.model.x, 10), (255, 0, 0))

class GameViewer(Viewer):
    def __init__(self, model):
        super().__init__(model)
        self.SQUARE_WIDTH = 150
        self.BLOCK_COLOR = '#F2EFEA'
        self.BLOCK_BORDER_COLOR = '#E6E6E6'
        self.WALL_COLOR = '#FC7753'
        self.TEXT_COLOR = '#403D58'

    def draw(self, gui):
        adj = self.model.get_maze().get_adjacencies()
        lines = []
        for pos in adj:
            self.draw_block(pos[0], pos[1], gui)
            for offset in [(-1,0), (1,0), (0,1), (0,-1)]:
                neighbour_pos = pos[0] + offset[0], pos[1] + offset[1]
                if(neighbour_pos not in adj[pos]): # Should draw wall between positions
                    lines.append(self.get_line_between_neighbours(pos, neighbour_pos))
        self.draw_walls(lines, gui)
        self.draw_start_and_end(gui)
    
    # TODO: Refactor code so it looks cleaner
    def get_line_between_neighbours(self, pos, neighbour_pos):
        delta_x, delta_y = neighbour_pos[0] - pos[0], neighbour_pos[1] - pos[1]
        if(delta_x == 0):
            if(delta_y < 0):
                start_position = Position(pos[0]*self.SQUARE_WIDTH, pos[1]*self.SQUARE_WIDTH)
            if(delta_y > 0):
                start_position = Position(neighbour_pos[0]*self.SQUARE_WIDTH, neighbour_pos[1]*self.SQUARE_WIDTH)
            end_position = Position(start_position.x + self.SQUARE_WIDTH, start_position.y)
        if(delta_y == 0):
            if(delta_x < 0):
                start_position = Position(pos[0]*self.SQUARE_WIDTH, pos[1]*self.SQUARE_WIDTH)
            if(delta_x > 0):
                start_position = Position(neighbour_pos[0]*self.SQUARE_WIDTH, neighbour_pos[1]*self.SQUARE_WIDTH)
            end_position = Position(start_position.x, start_position.y + self.SQUARE_WIDTH)
        return (start_position, end_position)

    def draw_walls(self, lines, gui):
        for start_pos, end_pos in lines:
            gui.draw_line(start_pos, end_pos, self.WALL_COLOR, 6)
    
    def draw_block(self, x, y, gui):
        x, y = x * self.SQUARE_WIDTH, y * self.SQUARE_WIDTH
        gui.draw_rectangle(Position(x, y), self.SQUARE_WIDTH, self.SQUARE_WIDTH, self.BLOCK_COLOR) # Draw fill
        gui.draw_rectangle(Position(x, y), self.SQUARE_WIDTH, self.SQUARE_WIDTH, self.BLOCK_BORDER_COLOR, 1) # Draw grey border

    def draw_start_and_end(self, gui):
        maze = self.model.get_maze()
        start_pos = maze.get_start_position()
        font_pos = Position(start_pos[0] * self.SQUARE_WIDTH + self.SQUARE_WIDTH/2, start_pos[1] * self.SQUARE_WIDTH  + self.SQUARE_WIDTH/2)
        gui.draw_centered_text('S', font_pos, self.TEXT_COLOR)
        end_pos = maze.get_end_position()
        font_pos = Position(end_pos[0] * self.SQUARE_WIDTH + self.SQUARE_WIDTH/2, end_pos[1] * self.SQUARE_WIDTH  + self.SQUARE_WIDTH/2)
        gui.draw_centered_text('E', font_pos, self.TEXT_COLOR)