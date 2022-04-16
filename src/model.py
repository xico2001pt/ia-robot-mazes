from turtle import position


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
    
class InstructionSequence:
    def __init__(self, size, sequence=[]):
        self.sequence = sequence
        self.size = size
        self.current_instruction = -2
    
    def get_sequence(self):
        return self.sequence
    
    def get_size(self):
        return self.size

    def get_current_instruction(self):
        return self.current_instruction
    
    def full(self):
        return self.size == len(self.sequence)
    
    def add_instruction(self, instruction):
        if len(self.sequence) < self.size:
            self.sequence.append(instruction)
    
    def pop_instruction(self):
        if len(self.sequence) > 0:
            self.sequence.pop()
    
    def set_instructions(self, instructions):
        self.sequence = instructions.copy()
        self.size = len(self.sequence)
    
    def advance_instruction(self):
        self.current_instruction = (self.current_instruction+1) % self.size


class Game:
    def __init__(self, maze, path=[]):
        self.maze = maze
        self.path = path
        self.sequence = InstructionSequence(self.maze.minimum_instructions)
        self.current_pos = Position(*maze.get_start_position())
        self.target_pos = Position(self.current_pos.x, self.current_pos.y) #TODO: Copy class is cleaner
        self.current_target = 0

    def get_maze(self):
        return self.maze
    
    def get_path(self):
        return self.path
    
    def get_sequence(self):
        return self.sequence
    
    def add_instruction(self, instruction):
        self.sequence.add_instruction(instruction)
    
    def set_instructions(self, instructions):
        self.sequence.set_instructions(instructions)
    
    def pop_instruction(self):
        self.sequence.pop_instruction()