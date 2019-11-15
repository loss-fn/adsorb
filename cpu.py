## adsorb - cpu player

import random

import curses

def action(_, board, py, px, max_attempts = 10):
    attempt = 0
    while True:
        attempt += 1
        h, w = len(board), len(board[0])
        y, x = random.randint(0, h-1), random.randint(0, w-1)

        if board[y][x] == '0':
            curses.ungetmouse(0, px + x, py + y, 0, curses.BUTTON1_CLICKED)
            return curses.KEY_MOUSE

        if attempt >= max_attempts:
            return ord(' ') # <SPACE> is pass