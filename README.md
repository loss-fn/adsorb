### ADSORB

ADSORB is a simple turn-based game played on a 2D surface made up of a
number of squares. It's my submission to the [2019 Game Off Jam](
https://itch.io/jam/game-off-2019), the theme is _Leaps and Bounds_.

Players compete to occupy as much space on the board as possible. There are a
limited number of actions that can be made each turn. The player who occupy
the most squares when the board is full wins.

The game supports 1 - 4 players. If you play alone the object is to use as
few moves as possible to fill the board.

### Game play

A player can either `add` one (1) square, `remove` a square (1) or `copy` a
group of sqaures (1 - n) into adjacent empty squares. Copying can be done in
any direction, and from any square in the group, as long as all of the
destination squares are unoccupied. The square that is selected is considerd
the edge of the group in the direction the copying is performed, regardless of
whether or not it actually IS an edge.

### How to play

You'll need Python 3 installed and a terminal that supports colour.

Everything you need is in the `adsorb` folder. Open a terminal and type:
`python3 game.py ui` to open up the game in solitaire mode. You should see a
white, irregularly shaped, board. The play, simply click on a square. Note
that squares are 2 chars wide which is why you'll see `++` and not `+` once
you've clicked it. The `+`signs are there to mark which square you're about
to play on. If you click it it should turn green. If you click the green
square it should be marked with `--` and have arrows surrounding it. Clicking
the `-` signs removes the square and clicking either of the arrows `copies``
the group of squares in that direction.

If you want to play against the random cpu player you start the game with:
`python3 game.py ui cpu.Random` you can add up to 4 players in different
combinations. For example, `python3 game.py cpu.Random ui cpu.Random` starts
a 3 player game with P1 and P3 being random computer players and P2 being you.
You can also specify `python3 game.py cpu.Random cpu.Random` to start a 2
player game with only computer players. The board should flash by and present
the results almost directly.

```
Scores:
P1 42p, P2 45p

Board:
          
  12121111
1212121122
1211221222
2211222212
1221222112
2211211122
2122111122
1211122222
121211112
```

#### TODO

1. The `copy` function doesn't work as intended. It should not allow a `copy`
action in a blocked direction. But it does. I need to fix that.
2. ~~The board is just a square at the moment. I need to fix a shape generator.~~
3. The `cpu.Random` player is a bit boring to test the game against. I need
to upgrade that to something smarter.
4. Test the game on Windows and Linux platforms.