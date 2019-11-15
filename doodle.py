## adsorb

import curses

import ui
import view
import model

def game(stdscr):
    h, w, board = model.gen_board(*stdscr.getmaxyx())
    py, px = view.init(stdscr, h, w, board)

    players = { 0 : ui,
                1 : ui, }

    actions = { 27 : quit, # 27 is the <ESC> ASCII code
                32 : _pass, # 32 is the <SPACE> ASCII code
                curses.KEY_MOUSE : mouse, }

    # main loop
    player = 0
    while True:
        key = players[player].action(stdscr, board, py, px)
        try:
            board = actions[key](player, board, py, px)
            view.update(stdscr, h, w, board)
            player = 1 - player
            
        except KeyError: 
            # any key pressed that is not associated with
            # an action will end up here
            pass

def mouse(player, board, py, px):
    _, x, y, _, _ = curses.getmouse()

    # update board
    _x, _y = x - px, y - py
    v = model.get(_y, _x, board)
    if v == '0':
        board = model.place(str(player + 1), _y, _x, board)
    else:
        board = model.remove(str(player + 1), _y, _x, board)

    return board

def _pass(player, board, *rest):
    return board

def quit(*args):
    raise KeyboardInterrupt

if __name__ == "__main__":
    try:
        curses.wrapper(game)
    except KeyboardInterrupt:
        pass