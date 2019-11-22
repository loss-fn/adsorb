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
        
        self._board_copy = None
        self._pos_conns= {} # (y,x) -> [(y,x), (y,x)]

    def get(self, y, x):
        return self.board[y][x]

    def mark_place(self, y, x):
        status = 10
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None

        self._board_copy = copy.deepcopy(self.board)
        self.board[y][x] = '+'
        return status

    def mark_copy_and_remove(self, y, x):
        status = 10
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None
           
        self._board_copy = copy.deepcopy(self.board)
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
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None

        if self.board[y][x] == '0':
            status = 100
            self.board[y][x] = str(p + 1)

            self._add_connections(p, y, x)

        return status

    def remove(self, p, y, x):
        status = 0
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None
                
        if self.board[y][x] == str(p + 1):
            status = 100
            self.board[y][x] = '0'

            self._del_connections(p, y, x)

        return status

    def copy(self, p, y, x, direction):
        status = 0
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None
                
        if self.board[y][x] == str(p + 1):
            if y > 0 and self.board[y-1][x] == '0':
                status = 100
                self.board[y-1][x] = str(p + 1)
        return status

    def _add_connections(self, p, y, x):
        if p not in self._pos_conns.keys():
            self._pos_conns[p] = {}

        if (y,x) not in self._pos_conns[p].keys():
            self._pos_conns[p][(y,x)] = []
            
        for _y, _x in [(y-1,x), (y+1,x), (y,x-1), (y,x+1)]:
            try:
                if self.board[_y][_x] == str(p + 1):
                    self._pos_conns[p][(y,x)].append((_y,_x))
                    try:
                        self._pos_conns[p][(_y,_x)].append((y,x))
                    except KeyError:
                        self._pos_conns[p][(_y,_x)] = [(y,x),]
            except IndexError:
                pass

    def _del_connections(self, p, y, x):
        if p not in self._pos_conns.keys():
            raise Exception("This can't happen!(TM)")

        for _y, _x in self._pos_conns[p][(y,x)]:
            try:
                self._pos_conns[p][(_y,_x)].remove((y,x))
            except Exception:
                raise Exception("This can't happen!(TM)")
        del self._pos_conns[p][(y,x)]
