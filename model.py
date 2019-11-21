## adsorb - model

import copy
import random

class Board(object):
    def __init__(self, shape = None, height = None, width = None):
        if shape is None: shape = 'SQUARE'
        if height is None: height = 12
        if width is None: width = 12
        self.size = (height, width)
        self.board = [['0' for _ in range(width)] for _ in range(height)]
        self.board_copy = None

    def get(self, y, x):
        return self.board[y][x]

    def mark_place(self, y, x):
        status = 10
        if self.board_copy is not None:
           self.board = copy.deepcopy(self.board_copy)
           self.board_copy = None

        self.board_copy = copy.deepcopy(self.board)
        self.board[y][x] = '+'
        return status

    def mark_copy_and_remove(self, y, x):
        status = 10
        if self.board_copy is not None:
           self.board = copy.deepcopy(self.board_copy)
           self.board_copy = None
           
        self.board_copy = copy.deepcopy(self.board)
        if y > 0:
            self.board[y-1][x] = '↑'
        if y < len(self.board) - 1:
            self.board[y+1][x] = '↓'
        if x > 0:
            self.board[y][x-1] = '←'
        if x < len(self.board[0]) - 1:
            self.board[y][x+1] = '→'

        self.board[y][x] = '-'
        return status

    def place(self, p, y, x):
        status = 0
        if self.board_copy is not None:
           self.board = copy.deepcopy(self.board_copy)
           self.board_copy = None

        if self.board[y][x] == '0':
            status = 100
            self.board[y][x] = str(p + 1)
        return status

    def remove(self, p, y, x):
        status = 0
        if self.board_copy is not None:
           self.board = copy.deepcopy(self.board_copy)
           self.board_copy = None
                
        if self.board[y][x] == str(p + 1):
            status = 100
            self.board[y][x] = '0'
        return status

    def copy(self, p, y, x, direction):
        status = 0
        if self.board_copy is not None:
           self.board = copy.deepcopy(self.board_copy)
           self.board_copy = None
                
        if self.board[y][x] == str(p + 1):
            if y > 0 and self.board[y-1][x] == '0':
                status = 100
                self.board[y-1][x] = str(p + 1)
        return status