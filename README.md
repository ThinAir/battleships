## Battleships Game Engine

This is a working implementation of a game engine for the Battleships game in Python.

The rules of the game are here:  https://en.wikipedia.org/wiki/Battleship_(game)

1. Clone the repo:  `git clone git@github.com:ThinAir/battleships.git`
2. Run the unit tests:  `make test`

There is a bug in the game engine, which is the reason why the tests are not passing.

Find the bug and submit a PR.

### TODO:
 - A recent refactoring seems to have broken the unit tests - find out why and fix the bug that broke the test. (It seems that we are sinking a boat earlier than expected)
