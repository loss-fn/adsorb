## adsorb - view

import curses

def init(stdscr, h, w, board):
    # hide cursor
    curses.curs_set(0)

    # turn on mouse events
    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    # initialize colors
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)

    py, px = update(stdscr, h, w, board)

    return py, px 

def update(stdscr, h, w, board):
    my, mx = stdscr.getmaxyx()
    py, px = int((my - h) / 2), int((mx - w) / 2)
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

    return py, px

def invalid_move():
    curses.flash()