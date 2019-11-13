## adsorb

import random

import curses

def gen_board(my, mx):
    sy, sx = my - 1, mx - 1
    if sy > sx:
        sy = sx
    elif sx > sy:
        sx = sy

    board = [['0' for _ in range(sx)] for _ in range(sy)]

    ## make the board irregular
    
    # TODO add some random sizes here instead of just removing
    # the square with a probability of 50%

    for y, x in [(0,0), (0,-1), (-1,-1), (-1,0)]:
        if random.random() >= 0.5:
            board[y][x] = ' '

    return sy, sx, board

def game(stdscr):
    view(stdscr, *gen_board(*stdscr.getmaxyx()))

def view(stdscr, sy, sx, board):
    # hide cursor
    curses.curs_set(0)

    # output the board on the screen
    y = 0
    for row in board:
        x = 0
        for col in row:
            stdscr.addch(y,x, col)
            x += 1
        y += 1

    stdscr.refresh()

    # wait for user to press <ESC>
    while True:
        key = stdscr.getch()
        if key == 27: # 27 is the <ESC> ASCII code
            raise Exception("%d %d" % (y, x))

if __name__ == "__main__":
    curses.wrapper(game)