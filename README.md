### ADSORB

ADSORB is a simple turn-based game played on a 2D surface made up of a
number of squares. It's my submission to the [2019 Game Off Jam](
https://itch.io/jam/game-off-2019), the theme is _Leaps and Bounds_.

Players compete to occupy as much space on the board as possible. There are a
limited number of actions that can be made each turn. The player who occupy
the most squares when the board is full wins.

### Game play variants

#### One

A player can either `add` one (1) square, `remove` a group of squares (1-n) or
`copy` a group of sqaures (1-n) into adjacent squares. Copying can be done in
any direction, and from any square in the group, as long as the destination
squares are unoccupied. The square that is selected is considerd the edge of
the group in the direction the copying is performed, regardless of whether or
not it actually IS an edge.

For example: Copying upwards from `B4` will have no effect at all, because it
will copy itself onto B3 and C3 (see below). Copying from `B3` however will
fill up empty adjacent squares. This goes for copying in any direction.
```
  A B C D                       A B C D                       A B C D
1 . . . .                     1 . . . .                     1 . * * .
2 . . . . ('COPY' B4, 'UP) => 2 . . . . ('COPY' B3, 'UP) => 2 . * * .
3 . * * .                     3 . * * .                     3 . * * .
4 . * * .                     4 . * * .                     4 . * * .
```

#### Two

Instead of being able to select _any_ square on the board the player is forced
to build a chain by selecting a _next_ square to occupy.