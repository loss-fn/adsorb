## adsorb

import curses

import ui
import cpu
import view
import model

def game(stdscr):
    h, w, board = model.gen_board(*stdscr.getmaxyx())
    py, px = view.init(stdscr, h, w, board)

    players = { 0 : ui,
                1 : cpu, }

    actions = { 'QUIT'  : _quit,
                'PASS'  : _pass,
                'PLACE'  : _place,
                'REMOVE': _remove,
                'UNFOLD': _unfold }

    # main loop
    player = 0
    while True:
        action, y, x, direction = players[player].get_action(stdscr, player, board, py, px)
        board, status = actions[action](player, board, y, x, direction)
        if status == 1:
            view.update(stdscr, h, w, board)
            player = 1 - player

        else: # the player chose an invalid move
            view.invalid_move()

def _quit(*rest):
    raise KeyboardInterrupt

def _pass(player, board, *rest):
    status = 1
    return board, status

def _place(player, board, y, x, *rest):
    board, status = model.place(str(player + 1), y, x, board)
    return board, status

def _remove(player, board, y, x, *rest):
    board, status = model.remove(str(player + 1), y, x, board)
    return board, status

def _unfold(player, board, y, x, direction, *rest):
    raise NotImplementedError

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


if __name__ == "__main__":
    try:
        curses.wrapper(game)
    except KeyboardInterrupt:
        pass