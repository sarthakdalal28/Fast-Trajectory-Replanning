import pygame
import drawGrid
import pickle
import time
import custom_heapq as hq
import math


class Node:
    def __init__(self, pos=None, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.search = 0

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        if self.f == other.f:
            return self.g > other.g
        else:
            return self.f < other.f


def calculate_smallest_f(open__):
    nodee = hq.heappop(open__)
    ff = nodee.f
    hq.heappush(open__, nodee)
    return ff


def ComputePath(pos_a_x, pos_a_y, open_, closed_, direc, count, grid_, gval, all_nodes):
    while gval[pos_a_x][pos_a_y] > calculate_smallest_f(open_):
        if len(open_) == 0:
            print("Impossible")
            break
        curr = hq.heappop(open_)
        closed_.append(curr)
        nl = len(grid_)
        neighbours = []
        for d in direc:

            node_pos = (curr.pos[0] + d[0], curr.pos[1] + d[1])
            if node_pos[0] > nl - 1 or node_pos[0] < 0 or node_pos[1] > nl - 1 or node_pos[1] < 0:
                continue
            if grid_[node_pos[0]][node_pos[1]] == '#':
                continue

            found = False
            for an in all_nodes:
                if an.pos == node_pos:
                    found = True
                    new_node = an
            if not found:
                new_node = Node(node_pos, curr)
            neighbours.append(new_node)
        for n in neighbours:
            if n.search < count:
                n.g = math.inf
                gval[n.pos[0]][n.pos[1]] = math.inf
                n.search = count
            if n.g > curr.g + 1:
                n.g = curr.g + 1
                gval[n.pos[0]][n.pos[1]] = n.g
                n.parent = curr
                if n in open_:
                    open_.remove(n)
                n.h = abs(n.pos[0] - start_node.pos[0]) + abs(n.pos[1] - start_node.pos[1])
                n.f = n.g + n.h
                hq.heappush(open_, n)
                all_nodes.append(n)
    return open_, closed_, gval, curr, all_nodes


def reconstruct(curr):
    path = []
    current = curr
    while current is not None:
        path.append(current.pos)
        current = current.parent
    print("Length of path to be traversed: ", len(path)+1)
    return path

def moveA(aa, grid_, pos_a_x, pos_a_y):
    pygame.time.delay(50)
    pygame.draw.rect(screen, red, pygame.Rect(pos_a_y * 10, pos_a_x * 10, 10, 10))
    grid[pos_a_x][pos_a_y] = '.'
    pos_a_x = aa[0]
    pos_a_y = aa[1]
    grid_[pos_a_x][pos_a_y] = 'A'
    screen.blit(image_man, (pos_a_y * 10, pos_a_x * 10))
    pygame.display.update()
    return grid_, pos_a_x, pos_a_y

if __name__ == '__main__':
    l = 101
    pygame.init()
    screen = pygame.display.set_mode((l * 10, l * 10))
    white = (255, 255, 255)
    red = (255, 0, 0)
    black = (0, 0, 0)
    screen.fill(white)
    with open('Grids/Grid_1.data', 'rb') as f:
        grid = pickle.load(f)
    direc = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    for i in range(101):
        for j in range(101):
            if grid[i][j] == 'A':
                pos_a_x = i
                pos_a_y = j
            if grid[i][j] == 'T':
                pos_t_x = i
                pos_t_y = j
    drawGrid.drawGrid(grid, l, screen, black)
    image_man = pygame.image.load('neon_9x9.png')
    image_money = pygame.image.load('violet_9x9.png')
    screen.blit(image_man, (pos_a_y * 10, pos_a_x * 10))
    screen.blit(image_money, (pos_t_y * 10, pos_t_x * 10))
    pygame.display.update()
    count = 0
    start = [pos_a_x, pos_a_y]
    goal = [pos_t_x, pos_t_y]
    goal_node = Node(tuple(goal), None)
    start_node = Node(tuple(start), None)
    gval = [[math.inf]*l for i in range (l)]
    start_time = time.time()
    counter = 0
    start = time.time()
    all_nodes = []
    counter += 1
    count += 1
    gval[goal_node.pos[0]][goal_node.pos[1]] = 0
    goal_node.search = count
    start_node.g = math.inf
    gval[start_node.pos[0]][start_node.pos[1]] = math.inf
    start_node.search = count
    open = []
    closed = []
    hq.heapify(open)
    goal_node.h = abs(goal_node.pos[0] - start_node.pos[0]) + abs(goal_node.pos[1] - start_node.pos[1])
    goal_node.f = goal_node.g + goal_node.h
    hq.heappush(open, goal_node)
    open, closed, gval, goal_node, all_nodes = ComputePath(pos_a_x, pos_a_y, open, closed, direc, count, grid, gval, all_nodes)
    ans = reconstruct(goal_node)
    end = time.time()
    print("Time: ", end-start)
    for a in ans:
        grid, pos_a_x, pos_a_y = moveA(a, grid, pos_a_x, pos_a_y)
    grid, pos_a_x, pos_a_y = moveA([pos_t_x, pos_t_y], grid, pos_a_x, pos_a_y)
    pygame.time.delay(700)