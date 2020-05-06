#!/usr/bin/env python3
from pprint import pprint as pp
import numpy as np
from sudoku_test_grids import hard_grid, grid_easy


class PointXY:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def getInGrid(self, grid):
        return grid[self.y][self.x]
    def setInGrid(self, grid, value):
        grid[self.y][self.x] = value



def possible(grid, pos, value):
    for i in range(9):
        if grid[pos.y][i] == value:
            return False
    for i in range(9):
        if grid[i][pos.x] == value:
            return False
    x0 = (pos.x//3)*3
    y0 = (pos.y//3)*3
    for i in range(3):
        for j in range(3):
            if grid[y0+i][x0+j] == value:
                return False
    return True


def gridPositions(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            yield PointXY(x,y)



def solve(grid):
    for p in gridPositions(grid):
        if p.getInGrid(grid) == 0:
            for n in range(1, 10):
                if possible(grid, p, n):
                    p.setInGrid(grid, n)
                    solve(grid)
                    print('\n' * 10)
                    p.setInGrid(grid, 0)
            return
    pp(grid)
    input('...')
    return

solve(grid_easy)
