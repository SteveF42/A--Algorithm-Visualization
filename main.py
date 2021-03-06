import pygame
from queue import PriorityQueue
from tkinter import *
from cube import Cube
import math
import random


ROWS = 63
target_resolution = 900 // ROWS
WIDTH = target_resolution * ROWS

SCREEN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Path Finding Visualization")

#colors
RED = (255,0,0)
GREEN = (0,255,0)
PURPLE = (100,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,100,0)
BLUE = (0,0,255)
GREY = (50,50,50)

'''
Description: makes the internal grid which holds each Node
Type rows: int
Type width: int
'''
def make_grid(rows,width):
    gap = width // rows

    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Cube(i,j,gap,rows))

    return grid

'''
Description: prints out a grid like picture
Type window: pygame.display.set_mode()
Type width: int
Type rows: int
'''
def print_grid(window,width,rows):
    gap = width // rows
    
    for row in range(rows):
        pygame.draw.line(window,GREY,(0,row * gap),(width,row*gap))
        for col in range(rows):  
            pygame.draw.line(window,GREY,(col * gap,0),(col*gap,width))

'''
Description: draws everything out, helper function for print_grid and make_grid
Type window: pygame.display.set_mode()
Type rows: int
Type grid: 2D array(list)
'''
def draw(window,width,rows,grid):
    for row in grid:
        for node in row:
            node.draw(window)

    print_grid(window,width,rows)
    pygame.display.update()

'''
Description: returns a location within the 2D array 
Type mousePos: (x,y) Tuple
Type width: int
Type rows: int
Rtype Tuple(x,y)
'''
def get_clicked_pos(mousePos,width,rows):
    gap = width // rows
    x, y = mousePos
    row = x // gap
    col = y // gap
    return row, col

'''
Description: Draws a path after the algorithm figures out a viable path
Type draw: Lambda function
Type current: Cube
Type ls: Array(list)
'''
def make_path(draw,current, ls):
    while current in ls:
        current = ls[current]
        current.make_path()
        draw()

'''
Description: A* (A star) Algorithm, figures out what the best possible path is from a starting point an ending point
Type draw: Lambda function
Type start: Cube
Type end: Cube
'''
def Astar(draw,start,end):
    count = 0
    open_set = PriorityQueue() #priority queue to keep things sorted
    closed_set = []
    start_f = h(start.get_pos(),end.get_pos()) #starting F score
    open_set.put((start_f,start)) #first object to be put inside the queue
    start.G_score = 0
    parents = {}

    open_set_hash = [start]
    
    #loop while something is in queue
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #gets node and remoes it from queue
        current = open_set.get()[1]
        open_set_hash.remove(current)
        
        #puts it in a closed set where it can no longer be read from once its visited
        closed_set.append(current)
        if current != start:
            current.make_closed()

        #once we find the end node draw path and break
        if current == end:
            make_path(draw,end,parents)
            end.make_end()
            start.make_start()
            return True

        #goes through the current nodes neighbors determining their score
        for neighbor in current.neighbors:
            if neighbor in closed_set:
                continue
            
            #the current nodes cost is plus 1 from the previous
            temp_g_cost = current.get_G_score() + 1 

            # if ther neighboring cost is less than the current cost then set 
            # current node to the parent of the neighboring cost then put it in a queue to be explorered later
            if temp_g_cost < neighbor.get_G_score() or neighbor not in open_set_hash:
                temp_f_cost = h(neighbor.get_pos(),end.get_pos()) + temp_g_cost
                neighbor.set_F_score(temp_f_cost)
                neighbor.set_G_score(temp_g_cost)
                # make current parent node of its neighbor
                parents[neighbor] = current

                #if neighbor isn't already in the open set, put it in 
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((neighbor.F_score,neighbor))
                    open_set_hash.append(neighbor)
                    neighbor.make_open()
        draw()

    return False


'''
Description: calculates the H(n) value
Type start: Cube
Type end: Cube
'''
def h(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1-x2) + abs(y1-y2)

'''
Description: uses BFS Breadth First Search to determin the location of the ending node
Type draw: lambda
Type start: Cube
Type end: Cube
Type rows: int
'''
def BFS(draw,start,end,rows):
    stack = [start]
    visited = []
    x = rows // 2
    y = rows // 2
    parents = {}

    start.make_open()
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop(0)
        if current in visited:

            continue
        visited.append(current)
        
        if current == end:
            end = end.make_end()
            make_path(draw,current,parents)
            start = start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                neighbor.make_open()
                parents[neighbor] = current
        current.make_closed()
        draw()
    return False

'''
Description: Main function which holds the pygame loop, takes care of running the actual program
Type window: pygame.display.set_mode
Type width: int
'''


# def TkinterWindow():
#     def callback():
        
#         ROWS = int(E1.get())
#         if ROWS:
#             while ROWS % 5 != 0:
#                 ROWS -= 1
#             top.destroy()
#             print(ROWS)


#     top = Tk()
#     top.title('Grid Size')
#     top.geometry("250x80")
#     L1 = Label(top, text="Grid Size")
#     L1.grid(row=0, column=0)
#     E1 = Entry(top, bd = 5)
#     E1.grid(row=0, column=1)

#     MyButton1 = Button(top, text="Submit", width=10, command=callback)
#     MyButton1.grid(row=1, column=1)

    
#     top.mainloop()

'''
Description: uses prims algorithm to generate a self made maze
Type grid: lambda function of draw function
Type grid: 2D list
Type rows: int
'''
def generate_maze(draw,grid,rows):
    # Prim's algorithm
    # makes everything a wall
    for row in grid:
        for node in row:
            node.make_wall()
    # gets first node somewhere in the middle
    x = rows //2
    y = rows // 2
    first = grid[x][y]
    part_of_maze = [first]

    # Tuple of node and opposite direction
    walls = [first.cross_neighbors[i] for i in range(0,len(first.cross_neighbors)-1)]
    first.make_white()

    #while there are walls in the list
    while walls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #get random wall from the wall list
        randInt = random.randint(0,len(walls)-1)
        current_value = walls[randInt]
        current_wall = current_value[0]
        came_from = current_value[1]

        #if the chosen wall happens to be in the path section continue
        if current_wall in part_of_maze:
            walls.remove(current_value)
            continue

        # In my case I had to travel to path sizes and get the direction to connect the path back to the main path
        fill_wall = None
        try:
            if came_from == 'up':
                fill_wall = current_wall.neighbors[1]
            elif came_from == 'down':
                fill_wall = current_wall.neighbors[0]
            elif came_from == 'right':
                fill_wall = current_wall.neighbors[3]
            elif came_from == 'left':
                fill_wall = current_wall.neighbors[2]
        except:
            pass
        
        #create a path with that connection if its not an edge
        if fill_wall != None:
            fill_wall.make_white()
            part_of_maze.append(fill_wall)

        current_wall.make_white()
        part_of_maze.append(current_wall)
        walls.remove(current_value)

        #gets all the neighbors of the current wall and puts them into the wall list if they weren't already turned into paths
        for neighbor in current_wall.cross_neighbors:
            if neighbor[0] not in part_of_maze:
                walls.append(neighbor)

        draw()

    # draws out edges
    for i in range(rows):
        grid[0][i].make_wall()
        grid[i][0].make_wall()
        grid[rows-1][i].make_wall()
        grid[i][rows-1].make_wall()
        draw()

    pygame.event.clear()

'''
Description: helper function to clear the board before executing an algorithm
Type start: Cube
Type end: Cube
Type grid: 2D array
'''
def board_reset(start, end,grid):
    if start == None or end == None:
        return

    for row in grid: #clears previous simulation
        for node in row:
            if node.color == RED or node.color == GREEN or node.color == PURPLE:
                node.color = WHITE 

    for row in grid: # clears all values in case new walls are to be placed/destroyed
        for node in row:
            node.reset()

    for node in grid:#calculates all neighboring nodes
        for cube in node:
            cube.update_neighbors(grid)

'''
Description: main game window, controls the bulk of the application
Type window: pygame.display.set_mode()
Type width: int
'''

def main(window, width):
    # TkinterWindow()
    global ROWS
    run = True

    start = None
    end = None

    grid = make_grid(ROWS,width)
    memory_grid = grid.copy()

    started = False
    mouseClicked = False


    while run:
        draw(window,width,ROWS,grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: #left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos,width,ROWS)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    node.make_start()

                elif not end and node != start:
                    end = node
                    node.make_end()

                elif node != start and node != end:
                    node.make_wall()
            if pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos,width,ROWS)
                node = grid[row][col]
                if node.is_start():
                    start = None
                    node.reset(True)

                elif node.is_end():
                    end = None
                    node.reset(True)
                    
                elif node.is_wall():
                    node.reset(True)

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE: #space to start simulation
                    board_reset(start,end,grid)
                    Astar(lambda: draw(window,width,ROWS,grid),start,end)

                if event.key == pygame.K_b: #start BFS simulation
                    board_reset(start,end,grid)
                    BFS(lambda: draw(window,width,ROWS,grid),start,end,ROWS)

                if event.key == pygame.K_c: # completely clears the board
                    start = None
                    end = None
                    for row in grid:
                        for node in row:
                            node.reset(True)
                
                if event.key == pygame.K_m:
                    start = None
                    end = None
                    for row in grid: # clears all values in case new walls are to be placed/destroyed
                        for node in row:
                            node.reset(True)

                    for node in grid:#calculates all neighboring nodes
                        for cube in node:
                            cube.update_neighbors(grid)
                            cube.update_cross_neighbors(grid)

                    generate_maze(lambda: draw(window,width,ROWS,grid),grid,ROWS)


    pygame.quit()


if __name__ == '__main__':
    main(SCREEN, WIDTH)  