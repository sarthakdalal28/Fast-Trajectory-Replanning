import pygame
def drawGrid(grid, n, screen, black):
    blocksize = 10
    for x in range(0, n * 10, blocksize):
        for y in range(0, n * 10, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            pygame.draw.rect(screen, black, rect, 1)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '#':
                pygame.draw.rect(screen, black, pygame.Rect(j * 10, i * 10, blocksize, blocksize))