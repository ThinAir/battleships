import uuid

from .ships import Carrier, Battleship, Submarine, Cruiser, Destroyer
from .player import Player
from .errors import (
    GameOverError,
    TooManyPlayersError,
    NoSuchPlayerError,
    NotEnoughPlayersError,
    WrongTurnError,
)

SHIP_TYPES = (Carrier, Battleship, Submarine, Cruiser, Destroyer)


class Game(object):
    def __init__(self, board_size, **ship_counts):
        """starts a new 2-player game

        Args:
            board_size: the size of the board
            carrier: count of carriers
            battleship: count af battleships
            submarine: count of submarines
            cruiser: count of cruisers
            destroyer: count of destroyers
        """
        self.players = []
        self.turn = 0
        self.ship_counts = ship_counts
        self.winner = None

        if not isinstance(board_size, tuple):
            raise ValueError('board size must be a tuple of ints')

        x, y = board_size
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError('board size must be a tuple of ints')
        self.board_size = board_size

        if not any([isinstance(x, int) for x in ship_counts.values()]):
            raise ValueError('ship count must be int')

    def add_player(self, name):
        """add a new player

        Args:
            name: str

        Returns:
            uuid
        """
        if len(self.players) >= 2:
            raise TooManyPlayersError()
        _pid = uuid.uuid4()
        self.players.append(Player(
            name=name,
            pid=_pid,
            board_size=self.board_size,
            **self.ship_counts
        ))
        return _pid

    def _get_player(self, player_id):
        player = None
        for p in self.players:
            if player_id == p.pid:
                player = p
                break

        if player is None:
            raise NoSuchPlayerError()

        return player

    def place_ship(self, player_id, ship):
        """each player places their pieces"""
        if len(self.players) < 2:
            raise NotEnoughPlayersError()

        if self.winner:
            raise GameOverError()

        if not any([isinstance(ship, x) for x in SHIP_TYPES]):
            raise ValueError('ship must be one of {}'.format(SHIP_TYPES))

        player = self._get_player(player_id)

        player.place_ship(ship)

    def get_board(self):
        """return the board-states at any point in time (i.e. which cells are occupied/hit/sunk)"""
        return self.board

    def take_turn(self, shooting_player_id, target_cell, debug=False):
        """Allows players to take turns shooting at a 1x1 target cell.

        Args:
            player: the player who is shooting / hitting
            target_cell: (int, int) of the cell being hit
        """
        if shooting_player_id not in [p.pid for p in self.players]:
            raise ValueError('Invalid player id')
        players_id_turn = self.players[self.turn % 2].pid
        if shooting_player_id != players_id_turn:
            raise WrongTurnError()
        attacked_player = next(p for p in self.players if p.pid != shooting_player_id)
        max_r, max_c = self.board_size
        r, c = target_cell
        if any([r < 0, r >= max_r, c < 0, c >= max_c]):
            return ValueError('Invalid target cell')
        hit_response = attacked_player.set_hit(target_cell, debug)
        if attacked_player.has_lost():
            self.winner = shooting_player_id
        self.turn += 1
        return hit_response

    def get_winner(self):
        """Ability to signal when someone wins or loses"""
        return self.winner

    def print_board(self, player_id):
        self._get_player(player_id).print_board()
