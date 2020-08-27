import pygame


RED = (255,0,0)
GREEN = (0,255,0)
PURPLE = (100,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,100,0)
BLUE = (0,0,255)
GREY = (50,50,50)

class Cube:
    def __init__(self, row, col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.color = WHITE
        self.neighbors = []
        self.F_score = float('inf')
        self.G_score = float('inf')
        self.parent = None

    def get_G_score(self):
        return self.G_score

    def set_G_score(self, score):
        self.G_score = score

    def get_F_score(self):
        return self.F_score

    def set_F_score(self, score):
        self.F_score = score

    def get_pos(self):
        return self.row,self.col

    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.x,self.y, self.width,self.width))

    def reset(self,clear_color = False):
        self.F_score = float('inf')
        self.G_score = float('inf')
        self.neighbors = []
        self.color = WHITE if clear_color else self.color

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = BLUE

    def make_open(self):
        self.color = GREEN
    
    def make_closed(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE

    def make_wall(self):
        self.color = BLACK

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == BLUE

    def is_wall(self):
        return self.color == BLACK
    
    def is_open(self):
        return self.color == GREEN

    def is_closed(self):
        return self.color == RED

    def __lt__(self,other):
        return True


    def update_neighbors(self,grid):
        #home node
        home = grid[self.row][self.col]
        #up
        
        # for row in range(-1,2):
        #     for col in range(-1,2): 
                
        #         if (self.row + row) < 0 or (self.col + col) < 0:
        #             continue
        #         elif (self.row + row) > self.total_rows-1 or (self.col + col) > self.total_rows-1:
        #             continue
        #         elif grid[self.row + row][self.col + col] == home:
        #             continue
        #         elif grid[self.row + row][self.col + col].is_wall():
        #             continue

        #         neighbor = grid[self.row + row][self.col + col]
                
        #         self.neighbors.append(neighbor)

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # up
            self.neighbors.append(grid[self.row-1][self.col])
        
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): #down
            self.neighbors.append(grid[self.row+1][self.col])

        if self.col < self.total_rows - 1  and not grid[self.row][self.col + 1].is_wall(): #right
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): #left
            self.neighbors.append(grid[self.row][self.col - 1])


