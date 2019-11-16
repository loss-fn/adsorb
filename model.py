## adsorb - model

import random
import collections.abc

class Board(object):
    def __init__(self, shape = None, height = None, width = None):
        if shape is None: shape = 'SQUARE'
        if height is None: height = 12
        if width is None: width = 12
        self.size = (height, width)
        self.board = [['0' for _ in range(width)] for _ in range(height)]

    def get(self, y, x):
        return self.board[y][x]

    def place(self, p, y, x):
        status = 0
        if self.board[y][x] == '0':
            status = 1
            self.board[y][x] = p
        return status

    def remove(self, p, y, x):
        status = 0
        if self.board[y][x] == p:
            status = 1
            self.board[y][x] = '0'
        return status

    def copy(self, p, y, x, direction):
        raise NotImplementedError