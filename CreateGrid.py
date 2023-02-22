import random
import pickle


dRow = [0, 1, 0, -1]
dCol = [-1, 0, 1, 0]


def setT(grid, n):
    pos_t_x = int((random.random()) * n)
    pos_t_y = int((random.random()) * n)
    grid[pos_t_x][pos_t_y] = 'T'
    return grid


def setA(grid, n):
    pos_a_x = int((random.random()) * n)
    pos_a_y = int((random.random()) * n)
    grid[pos_a_x][pos_a_y] = 'A'
    return grid

def isValid(row, col,n):
    global ROW
    global COL
    global vis

    # If cell is out of bounds
    if (row < 0 or col < 0 or row >= n or col >= n):
        return False

    # If the cell is already visited
    if (vis[row][col]):
        return False


    return True


def createGrid(row, col, grid, n):
    global dRow
    global dCol
    global vis

    vis = [[False for i in range(n)] for j in range(n)]
    st = []
    st.append([row, col])

    while (len(st) > 0):
        curr = st[len(st) - 1]
        st.remove(st[len(st) - 1])
        row = curr[0]
        col = curr[1]

        if (isValid(row, col, n) == False):
            continue

        vis[row][col] = True

        num = random.random()
        if num >= 0.3:
            grid[row][col] = '.'

        for i in range(4):
            adjx = row + dRow[i]
            adjy = col + dCol[i]
            st.append([adjx, adjy])

    return grid


for i in range(1, 51):
    grid = [['#'] * 101 for i in range(101)]
    grid = createGrid(0, 0, grid, 101)
    grid = setA(grid, 101)
    grid = setT(grid, 101)
    with open ('Grids/Grid_%s.data'%i, 'wb') as f:
        pickle.dump(grid, f)