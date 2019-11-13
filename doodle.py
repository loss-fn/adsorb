## adsorb

import curses

def gen_board(my, mx):
    sy, sx = my - 1, mx - 1
    if sy > sx:
        sy = sx
    elif sx > sy:
        sx = sy

    return sy, sx, [['*' for _ in range(sx)] for _ in range(sy)]

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