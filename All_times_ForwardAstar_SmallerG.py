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
            return self.g < other.g
        else:
            return self.f < other.f


def calculate_smallest_f(open__):
    nodee = hq.heappop(open__)
    ff = nodee.f
    hq.heappush(open__, nodee)
    return ff


def ComputePath(pos_t_x, pos_t_y, open_, closed_, direc, count, grid_, gval, all_nodes):
    while gval[pos_t_x][pos_t_y] > calculate_smallest_f(open_):
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
                n.h = abs(n.pos[0] - goal_node.pos[0]) + abs(n.pos[1] - goal_node.pos[1])
                n.f = n.g + n.h
                hq.heappush(open_, n)
                all_nodes.append(n)
    return open_, closed_, gval, curr, all_nodes


if __name__ == '__main__':
    l = 101
    direc = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    sum_ = 0
    for iter in range(1, 51):
        with open('Grids/Grid_%s.data' %iter, 'rb') as f:
            grid = pickle.load(f)
        for i in range(101):
            for j in range(101):
                if grid[i][j] == 'A':
                    pos_a_x = i
                    pos_a_y = j
                if grid[i][j] == 'T':
                    pos_t_x = i
                    pos_t_y = j
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
        gval[start_node.pos[0]][start_node.pos[1]] = 0
        start_node.search = count
        goal_node.g = math.inf
        gval[goal_node.pos[0]][goal_node.pos[1]] = math.inf
        goal_node.search = count
        open_ = []
        closed = []
        hq.heapify(open_)
        start_node.h = abs(start_node.pos[0] - goal_node.pos[0]) + abs(start_node.pos[1] - goal_node.pos[1])
        start_node.f = start_node.g + start_node.h
        hq.heappush(open_, start_node)
        open_, closed, gval, start_node, all_nodes = ComputePath(pos_t_x, pos_t_y, open_, closed, direc, count, grid, gval, all_nodes)
        end = time.time()
        sum_ += end - start
        print("Time_%s: " %iter, end-start)
    print("Average Time: ", sum_/50)