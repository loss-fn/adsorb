## adsorb

import argparse
import importlib

import curses

import view
import model

class Result(Exception):
    pass

class Game(object):
    def __init__(self, width, height, players, log):
        self.board = model.Board(height = height, width = width)
        self.players = players
        self.log = log
        if log is not None:
            self.log = open(log, 'w')
            self.log.write("Starting %sH x %sW game with %s players.\n" % \
                (height, width, len(players)))

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
            action, y, x, direction = \
                    self.players[player].get_action(stdscr, player,
                                                    self.board,
                                                    py, px)
            status = self.actions[action](player, y, x, direction)
            if self.log:
                self.log.write("[%s] P%s %s (%s:%s) %s\n" % \
                        (status, player + 1, action, y, x, direction))

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
    parser = argparse.ArgumentParser(description = 'ADSORB v 0.1 (curses)')
    parser.add_argument('players', metavar = 'player', nargs = '+',
                        help = 'list of players (ui = human, cpu = computer,' + \
                        ' <filename> = your AI player)')
    parser.add_argument('--width', default = 10, type = int,
                        choices = range(8, 25, 4), help = 'width of board')
    parser.add_argument('--height', default = 10, type = int,
                        choices = range(8, 25, 4), help = 'height of board')
    parser.add_argument('--log', default = None, type = str,
                        help = 'filename to log game state to')
    args = parser.parse_args()

    if len(args.players) > 4:
        raise argparse.ArgumentTypeError("")

    n = 0
    _players = {}
    for player in args.players:
        i = importlib.import_module(player)
        _players[n] = i
        n += 1

    try:
        game = Game(args.width, args.height, _players, args.log)
        curses.wrapper(game.curses)

    except KeyboardInterrupt as quit:
        board, p1_score, p2_score = quit.args

        print("User quit before game over.")
        print("P1 %dp - P2 %dp" % (p1_score, p2_score))

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
