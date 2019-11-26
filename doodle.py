## adsorb

import curses

import ui
import cpu
import view
import model

class Result(Exception):
    pass

class Game(object):
    def __init__(self, p1, p2):
        self.board = model.Board(height=4, width=4)

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
        while self.board.game_over() is not True:
            action, y, x, direction = self.players[player].get_action(stdscr, player, self.board, py, px)
            view.log(stdscr, 1, "%s (%s:%s) %s. " % (action, y, x, direction))
            try:
                view.log(stdscr, 3, ",".join("%s:%s" % (_y,_x) for (_y,_x) in self.board._pos_conns[player][(y,x)]))
            except KeyError:
                pass
            status = self.actions[action](player, y, x, direction)
            view.log(stdscr, 8, "status : %s. " % (status))
            view.log(stdscr, 9, "".join(self.board.board[0]))
            view.log(stdscr, 10, "".join(self.board.board[1]))
            view.log(stdscr, 11, "".join(self.board.board[2]))
            view.log(stdscr, 12, "".join(self.board.board[3]))
            if status == 10:
                view.update(stdscr, self.board)

            elif status == 100:
                view.update(stdscr, self.board)
                player = 1 - player

        raise Result(self.board.board, *self.board.score())

    def _quit(self, *rest):
        raise KeyboardInterrupt(self.board.board, *self.board.score())

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
    except KeyboardInterrupt as quit:
        board, p1_score, p2_score = quit.args

        print("User quit before game over.")
        print("P1 %d p - P2 %d p" % (p1_score, p2_score))

        print()
        print("Board when quitting:")
        for row in board:
            print("".join(row))

    except Result as result:
        board, p1_score, p2_score = result.args
        if p1_score > p2_score:
            print("P1 wins. (%d-%d p)" % (p1_score, p2_score))
        elif p1_score < p2_score:
            print("P2 wins. (%d-%d p)" % (p2_score, p1_score))
        else:
            print("Draw. (%d-%d p)" % (p2_score, p1_score))

        print()
        print("Board at game-over:")
        for row in board:
            print("".join(row))
