## adsorb

import random

import curses

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

def game(stdscr):
    bx, by, board = gen_board(*stdscr.getmaxyx())
    view(stdscr, bx, by, board)

    # main loop (quit using <ESC>)
    while True:
        key = stdscr.getch()
        if key == 27: # 27 is the <ESC> ASCII code
            raise Exception("%d %d" % (y, x))


def view(stdscr, sy, sx, board):
    # hide cursor
    curses.curs_set(0)

    my, mx = stdscr.getmaxyx()
    py, px = int((my - sy) / 2), int((mx - sx) / 2)
    # output the board on the screen
    y = 0
    for row in board:
        x = 0
        for col in row:
            stdscr.addch(y + py, x + px, col)
            x += 1
        y += 1

    stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(game)