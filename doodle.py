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
                         
                         'MARK_PLACE'           : self._mark_place,
                         'MARK_COPY_AND_REMOVE' : self._mark_copy_and_remove,

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
            view.log(stdscr, 1, "".join(self.board.board[0]))
            if status == 10:
                view.update(stdscr, self.board)

            elif status == 100:
                view.update(stdscr, self.board)
                player = 1 - player

    def _quit(self, *rest):
        raise KeyboardInterrupt

    def _pass(self, player, *rest):
        status = 100
        return status

    def _mark_place(self, player, y, x, *rest):
        status = self.board.mark_place(y, x)
        return status

    def _mark_copy_and_remove(self, player, y, x, *rest):
        status = self.board.mark_copy_and_remove(y, x)
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