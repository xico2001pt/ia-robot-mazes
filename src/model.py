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
        self.current_instruction = (self.current_instruction+1) % len(self.sequence)

class Option:
    def __init__(self, description, value=None):
        self.description = description
        self.value = value if value != None else description

    def __str__(self):
        return self.description

    def __eq__(self, description):
        return self.description == description
    
    def get_value(self):
        return self.value

class Selection:
    def __init__(self, options):
        self.options = {i : option for i, option in enumerate(options)}
        self.selected = 0
    
    def get_selected_option(self):
        return self.options[self.selected]
    
    def get_selected_index(self):
        return self.selected

    def previous_option(self):
        self.selected = (self.selected - 1) % len(self.options)
    
    def next_option(self):
        self.selected = (self.selected + 1) % len(self.options)

    def get_options(self):
        return list(self.options.values())
    
    def __len__(self):
        return len(self.options)

class MainMenu:
    def __init__(self, game_states, mazes, algorithms):
        self.selections = Selection([Selection(game_states), Selection(mazes), Selection(algorithms)])
    
    def get_selections(self):
        return self.selections
    
    def is_human_game_type(self):
        return self.selections.get_options()[0].get_selected_option().get_value() == "human"

class Game:
    def __init__(self, maze, path=[]):
        self.maze = maze
        self.path = path
        self.sequence = InstructionSequence(self.maze.minimum_instructions)
        self.current_pos = Position(*maze.get_start_position())
        self.target_pos = Position(self.current_pos.x, self.current_pos.y) #TODO: Copy class is cleaner
        self.current_target = 0
        self.gameover = False

    def is_gameover(self):
        return self.gameover
    
    def end_game(self):
        self.gameover = True

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

class GameOverInformation:
    def __init__(self, algorithm=None, visited_nodes=None, time=None):
        self.algorithm = algorithm
        self.visited_nodes = visited_nodes
        self.time = time