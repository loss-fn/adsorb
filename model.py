## adsorb - model

import copy
import random

class Board(object):
    def __init__(self, shape = None, height = None, width = None):
        if shape is None: shape = 'SQUARE'
        if height is None: height = 12
        if width is None: width = 12

        self.size = (height, width)
        self.board = self.generate_board(height, width)
        
        self._board_copy, self._board_copy_2 = None, None
        self._pos_conns= {} # (y,x) -> [(y,x), (y,x)]

    def generate_board(self, height, width):
        result = [[' ' for _ in range(width)] for _ in range(height)]
        for _ in range(random.choice([2,3,4])):
            h = random.choice([0.6, 0.7, 0.8, 0.9])
            w = random.choice([0.6, 0.7, 0.8, 0.9])

            y = random.randrange(0, int(height / 2))
            x = random.randrange(0, int(width / 2))

            # plot box on board
            yy = y
            for _ in range(int(height * h)):
                xx = x
                for _ in range(int(width * w)):
                    try:
                        result[yy][xx] = '0'
                    except IndexError:
                        pass
                    xx += 1
                yy += 1

        return result

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

    def mark_copy_and_remove(self, p, y, x):
        status = 10
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None
           
        self._board_copy_2 = copy.deepcopy(self.board)
        self._board_copy = copy.deepcopy(self.board)
        if y > 0 and self.copy(p, y, x, 'UP', test = True) == 100:
            self.board[y-1][x] = '↑'

        if y < len(self.board) - 1 and \
                self.copy(p, y, x, 'DOWN', test = True) == 100:
            self.board[y+1][x] = '↓'

        if x > 0 and self.copy(p, y, x, 'LEFT', test = True) == 100:
            self.board[y][x-1] = '←'

        if x < len(self.board[0]) - 1 and \
                self.copy(p, y, x, 'RIGHT', test = True) == 100:
            self.board[y][x+1] = '→'

        self.board[y][x] = '-'

        self._board_copy = self._board_copy_2
        self._board_copy_2 = None
        return status

    def place(self, p, y, x):
        status = 0
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None

        if self.board[y][x] == '0':
            status = 100
            self.board[y][x] = str(p + 1)

        return status

    def remove(self, p, y, x):
        status = 0
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None
                
        if self.board[y][x] == str(p + 1):
            status = 100
            self.board[y][x] = '0'

        return status

    def within_bounds(self, y, x):
        if y < 0 or x < 0 or y >= self.size[0] or x >= self.size[1]:
            return False
        return True

    def copy(self, p, y, x, direction, test = False):
        status = 0
        if self._board_copy is not None:
           self.board = copy.deepcopy(self._board_copy)
           self._board_copy = None
                
        my, mx = y, x # mirrored coords

        if direction == 'UP': my = y - 1
        if direction == 'DOWN': my = y + 1
        if direction == 'LEFT': mx = x - 1
        if direction == 'RIGHT': mx = x + 1
        
        # keep original mirrored coords
        omy, omx = my, mx
        if not self.within_bounds(my, mx):
            return status

        group, copied = self._get_group(p, y, x), []
        while len(group) > 0:
            cy, cx = group.pop(0) # current coords

            if (cy,cx) not in copied:  # make sure not to copy a position
                copied.append((cy,cx)) # more than once

                # figure out where the mirrored position (my,mx) for current is
                dy, dx = cy - y, cx - x # diff between current and original

                if direction in ['UP', 'DOWN']: my, mx = omy + (-1 * dy), omx + dx
                if direction in ['LEFT', 'RIGHT']: my, mx = omy + dy, omx + (-1 * dx)

                try:
                    if test:
                        if self.board[my][mx] != '0':
                            return 0
                    else:
                        if self.board[my][mx] == '0':
                            self.board[my][mx] = self.board[y][x]
                            copied.append((my,mx))

                except IndexError:
                    pass

        status = 100
        return status

    def _get_group(self, p, y, x):
        todo, done, result = [(y,x),], [], []
        while len(todo) > 0:
            cy, cx = todo.pop() # current coords
            if (cy,cx) not in done: # make sure not to copy a position
                done.append((cy,cx)) # more than once

                # is this position part of the group?
                if self.board[cy][cx] == str(p + 1):
                    result.append((cy,cx))

                # check left, up, right and down
                if cx > 0: todo.append((cy,cx-1))
                if cy > 0: todo.append((cy-1,cx))
                if cx < self.size[1] - 1: todo.append((cy,cx+1))
                if cy < self.size[0] - 1: todo.append((cy+1,cx))

        return result
