## adsorb - model

import random

def gen_board(my, mx):
    h, w = my - 2, mx - 2
    if h > w:
        h = w
    elif w > h:
        w = h

    board = [['0' for _ in range(w)] for _ in range(h)]

    ## make the board irregular

    # TODO add some random sizes here instead of just removing
    # the square with a probability of 50%

    for y, x in [(0,0), (0,-1), (-1,-1), (-1,0)]:
        if random.random() >= 0.5:
            board[y][x] = ' '

    return h, w, board

def get(y, x, board):
    return board[y][x]

def place(p, y, x, board):
    status = 0
    if board[y][x] == '0':
        status = 1
        board[y][x] = p
    return board, status

def remove(p, y, x, board):
    status = 0
    if board[y][x] == p:
        status = 1
        board[y][x] = '0'
    return board, status
