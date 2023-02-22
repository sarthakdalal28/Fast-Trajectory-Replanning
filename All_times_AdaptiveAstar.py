import heapq
import pickle
import custom_heapq as hq
import math
import time

class Node:
    def __init__(self, pos=None, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.s = 0

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        if self.f == other.f:
            return self.g > other.g
        else:
            return self.f < other.f


def calc_h(start, goal):
    return abs(start.pos[0] - goal.pos[0]) + abs(start.pos[1] - goal.pos[1])


def InitializeState(state, count, pathcost, deltah, goal_state):
    if state.s != count and state.s != 0:
        if state.g + state.h < pathcost[state.s]:
            state.h = pathcost[state.s] - state.g
        state.h = state.h - (deltah[count] - deltah[state.s])
        state.h = max(state.h, calc_h(state, goal_state))
        state.g = math.inf
    elif state.s == 0:
        state.g = math.inf
        state.h = calc_h(state, goal_state)
    state.s = count
    return state



def find_min_f(open_):
    n = hq.heappop(open_)
    ff = n.f
    open = heapq.heappush(open_, n)
    return ff


def ComputePath(pos_t_x, pos_t_y, open_, closed_, direc, count, grid_, gval, goal_node, pathcost, deltah, all_nodes):
    while gval[pos_t_x][pos_t_y] > find_min_f(open_):
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
            InitializeState(n, count, pathcost, deltah, goal_node)
            if n.g > curr.g + 1:
                n.g = curr.g + 1
                gval[n.pos[0]][n.pos[1]] = n.g
                n.parent = curr
                if n in open_:
                    open_.remove(n)
                n.f = n.g + n.h
                hq.heappush(open_, n)
                all_nodes.append(n)
    end = time.time()
    return gval, curr, all_nodes, end

if __name__ == '__main__':
    l = 101
    direc = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    sum_ = 0
    for iter in range(1, 51):
        with open('Grids/Grid_%s.data' % iter, 'rb') as f:
            grid = pickle.load(f)

        for i in range(101):
            for j in range(101):
                if grid[i][j] == 'A':
                    pos_a_x = i
                    pos_a_y = j
                if grid[i][j] == 'T':
                    pos_t_x = i
                    pos_t_y = j

        count = 1
        deltah = [0]
        start = [pos_a_x, pos_a_y]
        goal = [pos_t_x, pos_t_y]
        goal_node = Node(tuple(goal), None)
        start_node = Node(tuple(start), None)
        gval = [[math.inf] * l for i in range(l)]
        pathcost = [0]
        all_nodes = []
        start_node = InitializeState(start_node, count, pathcost, deltah, goal_node)
        goal_node = InitializeState(goal_node, count, pathcost, deltah, goal_node)
        start_node.g = 0
        gval[start_node.pos[0]][start_node.pos[1]] = 0
        goal_node.g = math.inf
        gval[goal_node.pos[0]][goal_node.pos[1]] = math.inf
        open_ = []
        hq.heapify(open_)
        closed = []
        start_node.h = abs(start_node.pos[0] - goal_node.pos[0]) + abs(start_node.pos[1] - goal_node.pos[1])
        start_node.f = start_node.g + start_node.h
        hq.heappush(open_, start_node)
        start_time = time.time()
        gval, start_node, all_nodes, end = ComputePath(pos_t_x, pos_t_y, open_, closed, direc, count, grid, gval, goal_node, pathcost, deltah, all_nodes)
        sum_ += end-start_time
        print("Time_%s: " % iter, end - start_time)
    print("Average Time: ", sum_/50)