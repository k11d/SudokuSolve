#-*-coding: utf-8-*-
import numpy as np
from lib.sudoku_test_grids import hard_grid, grid_easy, grid_easy_1
import sys
import random
import pygame
from pygame.locals import *

# from lib.profiling import profile


pygame.init()


class SudokuSolver:

    QUIT = False
    SOLVED =False

    class PointXY:
        def __init__(self, x, y):
            self.x, self.y = x, y
        def getInGrid(self, grid):
            return grid[self.y][self.x]
        def setInGrid(self, grid, value):
            grid[self.y][self.x] = value

    def __init__(self, grid):
        self.grid = grid
        self._original_grid = [
            [v for v in line]
            for line in self.grid
        ]
        self._modif_stack = []

    def gridPositions(self, randomized=False):
        def _iter():
            for y in range(len(self.grid)):
                for x in range(len(self.grid[0])):
                    yield SudokuSolver.PointXY(x, y)
        if randomized:
            pos = list(_iter())
            random.shuffle(pos)
            yield from pos
        else:
            yield from _iter()

    def possible(self, pos, value):
        for i in range(9):
            if self.grid[pos.y][i] == value:
                return False
        for i in range(9):
            if self.grid[i][pos.x] == value:
                return False
        x0 = (pos.x//3)*3
        y0 = (pos.y//3)*3
        for i in range(3):
            for j in range(3):
                if self.grid[y0+i][x0+j] == value:
                    return False
        return True


    def solve(self, screen_update_handle):
        if not self.SOLVED:
            for p in self.gridPositions():
                if p.getInGrid(self.grid) == 0:
                    for n in range(9, 0, -1):
                        if self.possible(p, n):
                            if self.QUIT:
                                return
                            SG.set_state(p.x, p.y, 'solved')
                            p.setInGrid(self.grid, n)
                            self.solve(screen_update_handle)
                            if not self.SOLVED:
                                p.setInGrid(self.grid, 0)
                                SG.set_state(p.x, p.y, 'wrong')
                    screen_update_handle()
                    return
            self.SOLVED = True
            self.solve(screen_update_handle)
        else:
            screen_update_handle()

class NumberLabels:

    DEFAULT_FONT = "assets/Anonymous_Pro.ttf"

    def __init__(self, size, colors=[], fontname=None):
        if not fontname:
            fontname = self.DEFAULT_FONT
        self.font_engine =  pygame.font.Font(fontname, size)
        self.labels = {
            color : {
                value : self.font_engine.render(str(value), True, color)
                for value in range(0, 10)
            } for color in colors
        }

    def blit(self, number, color, surface, position):
        if color in self.labels:
            surface.blit(self.labels[color][number], position)

class SurfaceGrid:
    def __init__(self, cell_width, edge_width, grid):
        self.cell_width = cell_width
        self.edge_width = edge_width
        self._rects = {}
        self._states = {}
        self._surfaces = []
        self._selected = None
        self.background = (250, 250, 250)
        self.rects_color = (50, 50, 50)
        #
        self.given = (120, 120, 120)
        self.empty = self.rects_color
        self.wrong = (255, 0, 0)
        self.solved = (0, 255, 0)
        #
        self.grid = grid
        self._changed_rects = []
        self._numbers = NumberLabels(cell_width, [self.given, self.wrong, self.solved])
        self._init_states()
        self._make_rects()

    def _init_states(self):
        for x,y,val in self._pull_values(self.grid):
            if val == 0:
                self._states[(x,y)] = 'empty'
            else:
                self._states[(x,y)] = 'given'

    def _make_rects(self):
        for row, line in enumerate(self.grid):
            for col, n in enumerate(line):
                rec = pygame.Rect(col*self.cell_width + edge_width, row*self.cell_width + edge_width, self.cell_width - edge_width, self.cell_width - edge_width)
                self._rects[(col,row)] = rec
                self._changed_rects.append(rec)

    def _pull_values(self, grid):
        for y, line in enumerate(self.grid):
            for x, value in enumerate(line):
                yield x, y, value

    def set_state(self, x, y, state):
        self._changed_rects.append(self._rects[(x,y)])
        self._states[(x,y)] = state


    def get_state(self, x, y):
        if (x,y) in self._states:
            return self._states[(x,y)]


    def _render_grid_rect(self, surface, rect):
        pygame.draw.rect(surface, self.rects_color, rect)


    def render(self, grid, surface):
        _changed_rects = []
        pv = self._pull_values(grid)
        for rect in self._rects.values():
            x, y, val = next(pv)
            if rect not in self._changed_rects:
                continue
            _changed_rects.append(rect)
            self._render_grid_rect(surface, rect)
            if (x,y) in self._states:
                color = getattr(self, self._states[(x,y)])
            w, h = self._numbers.font_engine.size('0')
            self._numbers.blit(val, color, surface, (rect.x + w // 2, rect.y))
        self._changed_rects.clear()
        return _changed_rects


def _mainloop():
    def _handle_events():
        for event in pygame.event.get():
            if event.type == QUIT:
                SS.QUIT = True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                SS.QUIT = True
    def _update():
        screen.fill(SG.background)
        updated_rects = SG.render(GRID, screen)
        pygame.display.update(updated_rects)

    if SS.SOLVED:
        _update()
        while not SS.QUIT:
            _handle_events()
    else:
        _update()
        _handle_events()

# @profile
def run():
    try:
        SS.solve(screen_update_handle=_mainloop)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':

    edge_width = 2
    cell_width = 100
    GRID = grid_easy
    screen = pygame.display.set_mode((cell_width * 9, cell_width * 9))
    pygame.display.set_caption("Sudoku Solver")
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))

    SG = SurfaceGrid(cell_width, edge_width, GRID)
    SS = SudokuSolver(GRID)

    run()
