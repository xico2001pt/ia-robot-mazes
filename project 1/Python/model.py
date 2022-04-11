class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def to_tuple(self):
        return (self.x, self.y)
    
    def get_up(self):
        return Position(self.x, self.y - 1)
    
    def get_down(self):
        return Position(self.x, self.y + 1)
    
    def get_left(self):
        return Position(self.x - 1, self.y)
    
    def get_right(self):
        return Position(self.x + 1, self.y)
    
    # TODO: __eq__()

class MainMenu:
    def __init__(self):
        self.x = 0
    
class Game:
    def __init__(self, maze):
        self.maze = maze

    def get_maze(self):
        return self.maze