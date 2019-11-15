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
            board, status = actions[key](player, board, py, px)
            if status == 1:
                view.update(stdscr, h, w, board)
                player = 1 - player

            else: # the player chose an invalid move
                view.invalid_move()

        except KeyError: 
            # any key pressed that is not associated with
            # an action will end up here
            pass

def mouse(player, board, py, px):
    _, x, y, _, _ = curses.getmouse()

    # update board
    _x, _y = x - px, y - py
    try:
        v = model.get(_y, _x, board)
        if v == '0':
            board, status = model.place(str(player + 1), _y, _x, board)
        else:
            board, status = model.remove(str(player + 1), _y, _x, board)
    except IndexError:
        status = 0

    return board, status

def _pass(player, board, *rest):
    status = 1
    return board, status

def quit(*args):
    raise KeyboardInterrupt

if __name__ == "__main__":
    try:
        curses.wrapper(game)
    except KeyboardInterrupt:
        pass