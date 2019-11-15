## adsorb - cpu player

import random

import curses

def get_action(_, player, board, py, px, max_attempts = 10):
    attempt = 0
    while True:
        attempt += 1
        h, w = len(board), len(board[0])
        y, x = random.randint(0, h-1), random.randint(0, w-1)

        if board[y][x] == '0':
            return 'PLACE', y, x, 0

        if attempt >= max_attempts:
            return 'PASS', 0, 0, 0