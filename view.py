## adsorb - view

import curses

def init(stdscr, board):
    # hide cursor
    curses.curs_set(0)

    # turn on mouse events
    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    # initialize colors
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)

    return update(stdscr, board)

def log(stdscr, line, msg):
    stdscr.move(line,1)
    stdscr.addstr(msg)

def update(stdscr, board):
    my, mx = stdscr.getmaxyx()
    h, w = board.size
    py, px = int((my - h) / 2), int((mx - (2 * w)) / 2)
    # output the board on the screen
    # since the x/y pixel ratio is close to 2/1 the view will
    # look better if we use two chars per square on the board 
    y = 0
    for row in board.board:
        x = 0
        for col in row:
            if col != ' ':
                if col in ['0', '1', '2', '3', '4']:
                    stdscr.addstr(y + py, x + px, '  ', curses.color_pair(int(col) + 1))
                else:
                    stdscr.addstr(y + py, x + px, col + col, curses.color_pair(6))
            x += 2
        y += 1

    stdscr.refresh()

    return py, px