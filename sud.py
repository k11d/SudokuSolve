#!/usr/bin/env python3
from pprint import pprint as pp
import numpy as np
from lib.sudoku_test_grids import hard_grid, grid_easy
import sys
import pygame
from pygame.locals import *

pygame.init()


class SudokuSolver:

    QUIT = False

    class PointXY:
        def __init__(self, x, y):
            self.x, self.y = x, y
        def getInGrid(self, grid):
            return grid[self.y][self.x]
        def setInGrid(self, grid, value):
            grid[self.y][self.x] = value

    def __init__(self, grid):
        self.grid = grid

    def gridPositions(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                # yield SudokuSolver.PointXY(x,y)
                yield SudokuSolver.PointXY(x,y)

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
    
    def count_possibles(self, pos):
        possibles = 0
        for n in range(1, 10):
            if self.possible(self.grid, pos, n):
                possibles += 1
        return possibles
    


    def solve(self, screen_update_handle):
        for p in self.gridPositions():
            if p.getInGrid(self.grid) == 0:
                SG.set_state(p.x, p.y, 'selected')
                for n in range(1, 10):
                    if self.possible(p, n):
                        SG.set_state(p.x, p.y, 'found')
                        p.setInGrid(self.grid, n)
                        if self.QUIT:
                            return
                        self.solve(screen_update_handle)
                        p.setInGrid(self.grid, 0)
                        SG.set_state(p.x, p.y, 'wrong')
                screen_update_handle()
                return
        screen_update_handle()
        input('...')
        


class TextLabel:

    DEFAULT_FONT = "Anonymous_Pro.ttf"
    def __init__(self, value, size, color, fontname=None):
        if not fontname:
            fontname = self.DEFAULT_FONT
        self.font_engine =  pygame.font.Font(fontname, size)
        self.surface = self.font_engine.render(value, True, color)

    def blit(self, surface, position):
        surface.blit(self.surface, position)


class SurfaceGrid:
    QUIT = False
    def __init__(self, cell_width, edge_width, grid):
        self.cell_width = cell_width
        self.edge_width = edge_width
        self._rects = []
        self._states = {}
        self._surfaces = []
        self._selected = None
        self.background = (50,50,50)
        #
        self.empty = (200, 180, 0)
        self.given = (240,240,240)
        self.wrong = (255, 0, 0)
        self.found = (0, 0, 255)
        self.solved = (0, 255, 0)
        self.selected = (0, 150, 200)
        #
        self.grid = grid
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
                self._rects.append(pygame.Rect(col*self.cell_width + edge_width, row*self.cell_width + edge_width, self.cell_width - edge_width, self.cell_width - edge_width))

    def _pull_values(self, grid):
        for y, line in enumerate(self.grid):
            for x, value in enumerate(line):
                yield x, y, value


    def set_state(self, x, y, state):
        """ one of:
            empty given wrong found solved selected
        """
        self._states[(x,y)] = state


    def get_state(self, x, y):
        if (x,y) in self._states:
            return self._states[(x,y)]

    def render_grid_cells(self, surface):
        for rect in self._rects:
            pygame.draw.rect(surface, self.background, rect)

    def render_values(self, grid, surface):
        pv = self._pull_values(grid)
        for rect in self._rects:
            x, y, val = next(pv)
            if (x,y) in self._states:
                color = getattr(self, self._states[(x,y)])
            txt = TextLabel(str(val), cell_width, color)
            w, h = txt.font_engine.size('0')
            txt.blit(surface, (rect.x + w // 2, rect.y))




edge_width = 2
cell_width = 100
screen = pygame.display.set_mode((cell_width*9, cell_width*9))


SG = SurfaceGrid(cell_width, edge_width, grid_easy)
SS = SudokuSolver(grid_easy)


def mainloop():
    for event in pygame.event.get():
        if event.type == QUIT:
            SS.QUIT = True
            SG.QUIT = True
    #     if event.type == MOUSEBUTTONDOWN:
    #         x, y = event.pos
    #         col, row= x // (cell_width + edge_width), y // (cell_width + edge_width)
    #         print(row, col)
    #         if SG._selected:
    #             SG.set_state(*SG._selected, 'given')
    #             SG._selected = None
    #         else:
    #             SG._selected = (col, row)
    #             SG.set_state(col, row, 'selected')

    screen.fill(SG.background)
    SG.render_grid_cells(screen)
    SG.render_values(grid_easy, screen)
    pygame.display.update(SG._rects)

try:
    SS.solve(screen_update_handle=mainloop)
except KeyboardInterrupt:
    pass
