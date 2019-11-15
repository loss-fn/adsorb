## adsorb

import curses

import view
import model

def game(stdscr):
    bx, by, board = model.gen_board(*stdscr.getmaxyx())
    view.init(stdscr, bx, by, board)

    actions = { 27 : quit, # 27 is the <ESC> ASCII code
                curses.KEY_MOUSE : mouse, }

    # main loop
    while True:
        key = stdscr.getch()
        try:
            actions[key](board)
        except KeyError: 
            # any key pressed that is not associated with
            # an action will end up here
            pass

def mouse(board):
    _, x, y, _, btn_state = curses.getmouse()
    raise Exception("%s:%s %s" % (x,y,btn_state))

def quit(_):
    raise KeyboardInterrupt

if __name__ == "__main__":
    try:
        curses.wrapper(game)
    except KeyboardInterrupt:
        pass