## adsorb - user interface for human player

import math

import curses

def get_action(stdscr, player, board, py, px):
    while True:
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            _x, _y = x - px, y - py
            _x = math.floor(_x / 2)
            try:
                # since -1 is a valid index the player can click
                # on a square above or to the left of the board
                # and still have it count as a move
                if _x < 0 or _y < 0:
                    raise IndexError

                v = board.get(_y, _x)
                if v == '0':
                    return 'PLACE', _y, _x, 0

                elif v == str(player + 1):
                    return 'REMOVE', _y, _x, 0

            except IndexError:
                # player clicked outside of the board area
                pass
            
        elif key == 32: # <SPACE> key is 'PASS'
            return 'PASS', 0, 0, 0

        elif key == 27: # <ESCAPE> key is 'QUIT'
            return 'QUIT', 0, 0, 0

