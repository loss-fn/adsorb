## adsorb

import curses

def gen_board(my, mx):
    return [['*' for _ in range(mx - 1)] for _ in range(my - 1)]

def game(stdscr):
    view(stdscr, gen_board(*stdscr.getmaxyx()))

def view(stdscr, board):
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