#!/usr/bin/env python

import unittest

from battleship import (
    Game,
    Response,

    BoardError,
    TooManyPlayersError,
    NoRoomForThisShipError,
    WrongTurnError,

    Carrier,
    Battleship,
    Submarine,
    Cruiser,
    Destroyer,
)


class TestGameB(unittest.TestCase):
    def setUp(self):
        self.game = Game(
            board_size=(10, 10),
            carrier=1,
            battleship=1,
            submarine=1,
            cruiser=1,
            destroyer=1,
        )

        self.p1_id = self.game.add_player(name='Bob')
        self.p2_id = self.game.add_player(name='Ana')

        # Player 1 places a Carrier (5 cells long) on their board at x=1, y=1
        self.game.place_ship(self.p1_id, Carrier(1, 1))

        # Player 2 places a ship on their board
        self.game.place_ship(self.p2_id, Carrier(4, 4))

        # Player 1 takes their turn and shots target cell at x=2, y=2
        self.assertIs(self.game.take_turn(self.p1_id, (2, 2)), Response.NO_SHIP_HERE)

    def test_take_turn_and_hit_on_occupied_cell_and_sinks(self):
        P1 = self.p1_id
        P2 = self.p2_id

        # Player 1 already took a turn.  Now player 2 shoots at x=1, y=1
        self.assertIs(self.game.take_turn(P2, (1, 1), debug=True), Response.HIT_A_SHIP_BUT_NOT_SUNK)

        self.assertIs(self.game.take_turn(P1, (2, 3)), Response.NO_SHIP_HERE)
        self.assertIs(self.game.take_turn(P2, (1, 1)), Response.HIT_A_SHIP_BUT_NOT_SUNK)

        self.assertIs(self.game.take_turn(P1, (2, 4)), Response.NO_SHIP_HERE)
        self.assertIs(self.game.take_turn(P2, (1, 2)), Response.HIT_A_SHIP_BUT_NOT_SUNK)

        self.assertIs(self.game.take_turn(P1, (2, 5)), Response.NO_SHIP_HERE)
        self.assertIs(self.game.take_turn(P2, (1, 3)), Response.HIT_A_SHIP_BUT_NOT_SUNK)

        self.assertIs(self.game.take_turn(P1, (2, 2)), Response.NO_SHIP_HERE)
        self.assertIs(
            self.game.take_turn(P2, (1, 4), debug=True),
            Response.HIT_A_SHIP_BUT_NOT_SUNK,  # expect for the boat to be still ok
            'We seemed to have sunk a boat, which is not true'
        )
        self.assertIs(self.game.take_turn(P1, (2, 6)), Response.NO_SHIP_HERE)
        self.assertIsNone(self.game.get_winner())
        self.assertIs(self.game.take_turn(P2, (1, 5)), Response.SUNK_SHIP)
        self.game.print_board(P1)
        self.assertEqual(self.game.get_winner(), P2)


if __name__ == '__main__':
    unittest.main()
