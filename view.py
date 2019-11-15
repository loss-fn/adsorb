## adsorb - view

import curses

def init(stdscr, sy, sx, board):
    # hide cursor
    curses.curs_set(0)

    # initialize colors
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)

    update(stdscr, sy, sx, board)

def update(stdscr, sy, sx, board):
    my, mx = stdscr.getmaxyx()
    py, px = int((my - sy) / 2), int((mx - sx) / 2)
    # output the board on the screen
    y = 0
    for row in board:
        x = 0
        for col in row:
            if col != ' ':
                stdscr.addstr(y + py, x + px, ' ', curses.color_pair(int(col) + 1))
            x += 1
        y += 1

    stdscr.refresh()

