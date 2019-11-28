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
        self.num_players = len(self.players.keys())
        if self.num_players == 1:
            self.moves = 0

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
            log_msg = "P%s %s (%s:%s) %s" % (player + 1, action, y, x, direction)
            try:
                status = self.actions[action](player, y, x, direction)
            except Exception:
                status = 0

            if self.log:
                self.log.write("[%s] %s\n" % \
                        (status, log_msg))

            if status == 0: # fail
                pass

            elif status == 10: # step 1 (of 2)
                view.update(stdscr, self.board)

            elif status == 100: # ok
                view.update(stdscr, self.board)
                player = player + 1
                if player >= self.num_players:
                    player = 0

                # in solitaire mode we count moves instead
                if self.num_players == 1:
                    self.moves += 1

        if self.log:
            for row in self.board.board:
                self.log.write("".join(row) + "\n")

            if self.num_players == 1:
                self.log.write("%s moves" % (self.moves))

            else:
                scores = self.board.score(self.num_players)
                p, msg = 1, ""
                for score in scores:
                    msg += "P%d %sp, " % (p, score)
                    p += 1
                self.log.write(msg[:-2])

            self.log.close()

        if self.num_players == 1:
            raise Result(self.board.board, None, self.moves)

        else:
            raise Result(self.board.board, self.board.score(self.num_players), None)

    def _quit(self, *rest):
        if self.num_players == 1:
            raise KeyboardInterrupt(self.board.board, None, self.moves)

        else:
            raise KeyboardInterrupt(self.board.board, self.board.score(self.num_players), None)

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
        try:
            mod, pl = player.split('.')
        except ValueError:
            mod, pl = player, None

        i = importlib.import_module(mod)
        _players[n] = i
        if pl:
            _players[n] = i.__dict__[pl]()

        n += 1

    try:
        game = Game(args.width, args.height, _players, args.log)
        curses.wrapper(game.curses)

    except Exception as result:
        args = result.args
        if type(result) == KeyboardInterrupt:
            print("User quit before game over.")
            print()

        if type(result) not in [KeyboardInterrupt, Result]:
            raise result

    finally:
        if n == 1:
            print("%s moves" % (args[2]))
            
        else:
            print("Scores:")
            p, msg = 1, ""
            for score in args[1]:
                msg += "P%d %sp, " % (p, score)
                p += 1
            print(msg[:-2])

            print()
            print("Board:")
            for row in args[0]:
                print("".join(row))
