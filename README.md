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
to build a chain by selecting an adjacent, _next_, square to occupy. This would
create a different type of play where the initial position matters more.
Essentially all moves would be to grow 1 group of squares.

#### Variants

In what is outlined above there's no way to remove an opponent's square but in
order for the game not to become too simplistic we may have to introduce a way
to _kill_ the other player's squares. Say that a group ratio of `4:1` is
required to _copy over_ a group. That would at least avoid spread out squares
played only to block the other player.