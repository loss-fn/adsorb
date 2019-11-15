## adsorb

import curses

import view
import model

def game(stdscr):
    h, w, board = model.gen_board(*stdscr.getmaxyx())
    py, px = view.init(stdscr, h, w, board)

    actions = { 27 : quit, # 27 is the <ESC> ASCII code
                curses.KEY_MOUSE : mouse, }

    # main loop
    while True:
        key = stdscr.getch()
        try:
            board = actions[key](board, py, px)
            view.update(stdscr, h, w, board)
        except KeyError: 
            # any key pressed that is not associated with
            # an action will end up here
            pass

def mouse(board, py, px):
    _, x, y, _, _ = curses.getmouse()

    # update board
    _x, _y = x - px, y - py
    v = model.get(_y, _x, board)
    if v == '0':
        board = model.place('1', _y, _x, board)
    else:
        board = model.remove('1', _y, _x, board)

    return board

def quit(*args):
    raise KeyboardInterrupt

if __name__ == "__main__":
    try:
        curses.wrapper(game)
    except KeyboardInterrupt:
        pass