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

    def game_over(self):
        # game is not over if there are empty squares left
        for row in self.board:
            for col in row:
                if col in ['0', '↑', '↓', '←', '→', '-', '+']:
                    return False

        return True

    def score(self, num_players):
        p1, p2, p3, p4 = 0, 0, 0, 0
        for row in self.board:
            for col in row:
                if col == '1': p1 += 1
                if col == '2': p2 += 1
                if col == '3': p3 += 1
                if col == '4': p4 += 1

        return [p1, p2, p3, p4][:num_players]

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
            my, mx = y, x # mirrored coords

            if direction == 'UP': my = y - 1
            if direction == 'DOWN': my = y + 1
            if direction == 'LEFT': mx = x - 1
            if direction == 'RIGHT': mx = x + 1
            
            # keep original mirrored coords
            omy, omx = my, mx

            copied = []
            # copy starting position
            if self.board[my][mx] == '0':
                self.board[my][mx] = self.board[y][x]
                self._add_connections(p, my, mx)
                copied.append((my,mx))

            # copy all connected positions recursively
            pos = self._pos_conns[p][(y,x)]
            while len(pos) > 0:
                cy, cx = pos.pop() # current coords

                if (cy,cx) not in copied: # make sure not to copy a position
                    copied.append((cy,cx)) # more than once

                    # figure where the mirrored position (my,mx) for current is
                    dy, dx = cy - y, cx - x # diff between current and original

                    if direction in ['UP', 'DOWN']: my, mx = omy + (-1 * dy), omx + dx
                    if direction in ['LEFT', 'RIGHT']: my, mx = omy + dy, omx + (-1 * dx)

                    try:
                        if self.board[my][mx] == '0':
                            self.board[my][mx] = self.board[y][x]
                            self._add_connections(p, my, mx)
                            copied.append((my,mx))

                            pos += self._pos_conns[p][(cy,cx)]
                    except IndexError:
                        pass

            status = 100
            
        return status

    def _add_connections(self, p, y, x, updated = None):
        if updated is None:
            updated = [(y,x),]

        if p not in self._pos_conns.keys():
            self._pos_conns[p] = {}

        if (y,x) not in self._pos_conns[p].keys():
            self._pos_conns[p][(y,x)] = []
            
        for _y, _x in [(y-1,x), (y+1,x), (y,x-1), (y,x+1)]:
            try:
                if self.board[_y][_x] == str(p + 1):
                    self._pos_conns[p][(y,x)].append((_y,_x))
                    if (_y,_x) not in updated:
                        updated.append((_y,_x))
                        self._add_connections(p, _y, _x, updated)

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
