# PythonMouse2020
A rudimentary clone of CastleMouse 2000

# About
PythonMouse2020 is a terminal-based game where a player places animals on a grid in order to scare a mouse into a hole.
For example, a cat, C, placed next to a mouse, M, will scare the mouse in the direction opposite of the cat.

The animals in the game are a mouse, cats, dogs, bears, lions, elephants and pythons, represented by M, C, D, B, L, E, and P respectively. The hole is represented by O.

These animals scare each other in a big loop like so:

M < C < D < B < L < E < M.

Also there is a smaller loop where, C < P < L, the python being scared by the lion and scaring the cat.

There are 7 levels so far, levels 0-6.

When stepping through a level, press 'q' to quit and 'b' to break out of loops.

# Dependencies
Numpy

# Differences between CastleMouse 2000
CastleMouse 2000, an old Mac game, had more features like replay, a GUI, editor, and Puzzle of the Day.

The key difference in gameplay is how animals move.
I believe that in CastleMouse 2000, a space must be vacant before an animal can move to it.
Whereas in PythonMouse 2020, an animal can move to a space even when an animal was just occupying it.

Another difference is that I've added the python piece.
