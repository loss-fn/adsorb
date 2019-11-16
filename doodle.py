## adsorb

import curses

import ui
import cpu
import view
import model

class Game(object):
    def __init__(self, p1, p2):
        self.board = model.Board()

        self.players = { 0 : p1,
                         1 : p2, }
        self.actions = { 'QUIT'  : self._quit,
                         'PASS'  : self._pass,
                         'PLACE' : self._place,
                         'REMOVE': self._remove,
                         'COPY'  : self._copy }

    def curses(self, stdscr):
        py, px = view.init(stdscr, self.board)

        # main loop
        player = 0
        while True:
            action, y, x, direction = self.players[player].get_action(stdscr, player, self.board, py, px)
            status = self.actions[action](player, y, x, direction)
            if status == 1:
                view.update(stdscr, self.board)
                player = 1 - player

    def _quit(self, *rest):
        raise KeyboardInterrupt

    def _pass(self, player, *rest):
        status = 1
        return status

    def _place(self, player, y, x, *rest):
        status = self.board.place(player, y, x)
        return status

    def _remove(self, player, y, x, *rest):
        status = self.board.remove(player, y, x)
        return status

    def _copy(self, player, y, x, direction, *rest):
        status = self.board.copy(player, y, x, direction)
        return status

if __name__ == "__main__":
    try:
        game = Game(p1 = ui, p2 = cpu)
        curses.wrapper(game.curses)
    except KeyboardInterrupt:
        pass