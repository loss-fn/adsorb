## adsorb - model

import random

def gen_board(my, mx):
    by, bx = my - 2, mx - 2
    if by > bx:
        by = bx
    elif bx > by:
        bx = by

    board = [['0' for _ in range(bx)] for _ in range(by)]

    ## make the board irregular

    # TODO add some random sizes here instead of just removing
    # the square with a probability of 50%

    for y, x in [(0,0), (0,-1), (-1,-1), (-1,0)]:
        if random.random() >= 0.5:
            board[y][x] = ' '

    return by, bx, board

