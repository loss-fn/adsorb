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

                # updating the board is a two-step process. First
                # player's select a square and second they decide
                # what action to take.
                v = board.get(_y, _x)
                if v == '0':
                    # player clicked on an empty square
                    # add a '+' sign to indicate that 'place'
                    # is a valid next move
                    return 'MARK_PLACE', _y, _x, 0

                elif v == '+':
                    return 'PLACE', _y, _x, 0

                elif v == str(player + 1):
                    # player clicked on an own square
                    # add a '-' sign and arrows to indicate that
                    # 'remove' and 'copy' are valid next moves
                    return 'MARK_COPY_AND_REMOVE', _y, _x, 0

                elif v == '-':
                    return 'REMOVE', _y, _x, 0

                elif v == '↑':
                    return 'COPY', _y, _x, 'UP'

                elif v == '↓':
                    return 'COPY', _y, _x, 'DOWN'

                elif v == '←':
                    return 'COPY', _y, _x, 'LEFT'

                elif v == '→':
                    return 'COPY', _y, _x, 'RIGHT'

            except IndexError:
                # player clicked outside of the board area
                pass
            
        elif key == 32: # <SPACE> key is 'PASS'
            return 'PASS', 0, 0, 0

        elif key == 27: # <ESCAPE> key is 'QUIT'
            return 'QUIT', 0, 0, 0

