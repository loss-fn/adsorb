## adsorb - user interface for human player

import curses

def get_action(stdscr, player, board, py, px):
    while True:
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            _x, _y = x - px, y - py
            try:
                v = board[_y][_x]
                if v == '0':
                    return 'PLACE', _y, _x, 0

                elif v == str(player):
                    return 'REMOVE', _y, _x, 0

            except IndexError:
                # player clicked outside of the board area
                pass
            
        elif key == 32: # <SPACE> key is 'PASS'
            return 'PASS', 0, 0, 0

        elif key == 27: # <ESCAPE> key is 'QUIT'
            return 'QUIT', 0, 0, 0

