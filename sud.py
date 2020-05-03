from pprint import pprint as pp

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
                    p.setInGrid(grid, 0)
            return
    global sol
    pp(grid)


#grid = [
#    [5,3,0,0,7,0,0,0,0], 
#    [6,0,0,1,9,5,0,0,0], 
#    [0,9,8,0,0,0,0,6,0], 
#    [8,0,0,0,6,0,0,0,3], 
#    [4,0,0,8,0,3,0,0,1], 
#    [7,0,0,0,2,0,0,0,6], 
#    [0,6,0,0,0,0,2,8,0], 
#    [0,0,0,4,1,9,0,0,5], 
#    [0,0,0,0,8,0,0,7,9],
#]

grid = [
    [5,0,0,6,7,0,9,0,0],
    [0,4,0,8,0,0,0,0,0],
    [8,0,0,5,0,0,6,1,3],
    [0,6,2,4,0,0,0,7,0],
    [1,0,0,0,0,3,0,2,0],
    [3,7,4,9,0,8,0,0,0],
    [0,9,6,1,0,7,8,0,2],
    [2,1,8,0,0,6,0,4,5],
    [0,5,0,0,8,0,0,9,0]
]

sol = None
solve(grid)

# for p in gridPositions(grid):
#     print(p, p.getInGrid(grid))

