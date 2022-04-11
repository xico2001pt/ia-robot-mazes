class Maze:
    def __init__(self, filename):
        self.adjacencies = {}
        self.open_from_file(filename)
    
    def open_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.read().split('\n')
            self.size = tuple(int(i) for i in lines[0].split(' ')[1:])
            self.start_position = tuple(int(i) for i in lines[1].split(' ')[1:])
            self.end_position = tuple(int(i) for i in lines[2].split(' ')[1:])
            self.read_layout(lines[3:])

    def read_layout(self, lines):
        layout_list = [[i for i in line] for line in lines]
        board_width, board_height = self.size
        for i in range(2*board_height-1):
            for j in range(2*board_width-1):
                if(layout_list[i][j] == '#'):
                    x, y = j // 2, i // 2
                    self.adjacencies[(x,y)] = []

                    for offset_x, offset_y in [(-1,0),(1,0),(0,1),(0,-1)]:
                        wall_y, wall_x = i + offset_y, j + offset_x
                        k, q = i + offset_y*2, j + offset_x*2
                        if(k >= 0 and k < 2*board_height-1 and q >= 0 and q < 2*board_width-1 and layout_list[wall_y][wall_x] == ' '):
                            self.adjacencies[(x,y)].append((q // 2, k // 2))

    def get_adjacencies(self):
        return self.adjacencies

    def get_start_position(self):
        return self.start_position

    def get_end_position(self):
        return self.end_position
    
    def get_size(self):
        return self.size