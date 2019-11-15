## adsorb

import curses

import view
import model

def game(stdscr):
    bx, by, board = model.gen_board(*stdscr.getmaxyx())
    view.init(stdscr, bx, by, board)

    actions = { 27 : quit, } # 27 is the <ESC> ASCII code

    # main loop
    while True:
        key = stdscr.getch()
        try:
            actions[key](board)
        except KeyError: 
            pass

def quit(_):
    raise KeyboardInterrupt

if __name__ == "__main__":
    try:
        curses.wrapper(game)
    except KeyboardInterrupt:
        pass