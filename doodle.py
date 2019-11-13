## adsorb

import curses

def game(stdscr):
    # wait for user to press <ESC>
    while True:
        key = stdscr.getch()
        if key == 27: # 27 is the <ESC> ASCII code
            break

if __name__ == "__main__":
    curses.wrapper(game)