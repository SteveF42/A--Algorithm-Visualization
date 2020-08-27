import pygame
from queue import PriorityQueue
from cube import Cube

WIDTH = 900
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

def make_grid(rows,width):
    gap = width // rows

    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Cube(i,j,gap,rows))

    return grid

def print_grid(window,width,rows):
    gap = width // rows
    
    for row in range(rows):
        pygame.draw.line(window,GREY,(0,row * gap),(width,row*gap))
        for col in range(rows):  
            pygame.draw.line(window,GREY,(col * gap,0),(col*gap,width))


def draw(window,width,rows,grid):
    for row in grid:
        for node in row:
            node.draw(window)

    print_grid(window,width,rows)
    pygame.display.update()

def get_clicked_pos(mousePos,width,rows):
    gap = width // rows
    x, y = mousePos
    row = x // gap
    col = y // gap
    return row, col

def make_path(draw,current, ls):
    while current in ls:
        current = ls[current]
        current.make_path()
        draw()

def Astar(draw,start,end):
    count = 0
    open_set = PriorityQueue()
    closed_set = []
    start_f = h(start.get_pos(),end.get_pos())
    open_set.put((start_f,start))
    start.G_score = 0
    parents = {}

    open_set_hash = [start]
    

    while not open_set.empty():
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        open_set_hash.remove(current)
        
        closed_set.append(current)
        if current != start:
            current.make_closed()


        if current == end:
            make_path(draw,end,parents)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor in closed_set:
                continue

            temp_g_cost = current.get_G_score() + 1 

            if temp_g_cost < neighbor.get_G_score() or neighbor not in open_set_hash:
                temp_f_cost = h(neighbor.get_pos(),end.get_pos()) + temp_g_cost
                neighbor.set_F_score(temp_f_cost)
                neighbor.set_G_score(temp_g_cost)
                parents[neighbor] = current

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((neighbor.F_score,neighbor))
                    open_set_hash.append(neighbor)
                    neighbor.make_open()
        draw()

    return False


def h(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1-x2) + abs(y1-y2)
     

def main(window, width):
    ROWS = 50
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
            if pygame.mouse.get_pressed()[2]:
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
                if event.key == pygame.K_SPACE:
                    if start == None or end == None:
                        continue

                    for row in grid:
                        for node in row:
                            if node.color == RED or node.color == GREEN or node.color == PURPLE:
                                node.color = WHITE 

                    for node in grid:
                        for cube in node:
                            cube.update_neighbors(grid)

                    started = False
                    Astar(lambda: draw(window,width,ROWS,grid),start,end)

                    for row in grid:
                        for node in row:
                            node.reset()

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    for row in grid:
                        for node in row:
                            node.reset(True)


    pygame.quit()


if __name__ == '__main__':
    main(SCREEN, WIDTH)