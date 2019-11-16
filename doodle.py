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
                'PLACE' : _place,
                'REMOVE': _remove,
                'COPY'  : _copy }

    # main loop
    player = 0
    while True:
        action, y, x, direction = players[player].get_action(stdscr, player, board, py, px)
        board, status = actions[action](player, board, y, x, direction)
        if status == 1:
            view.update(stdscr, h, w, board)
            player = 1 - player

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

def _copy(player, board, y, x, direction, *rest):
    board, status = model.copy(str(player + 1), y, x, direction, board)
    return board, status

if __name__ == "__main__":
    try:
        curses.wrapper(game)
    except KeyboardInterrupt:
        pass