import copy

from .errors import (
    BoardError,
    NoRoomForThisShipError,
)
from .response import Response


class Player(object):

    def __init__(self, name, pid, board_size, **ship_counts):
        self.ship_counts = ship_counts
        self.ships = []
        self.name = name
        self.pid = pid
        self.board_size = board_size
        columns_count, row_count = board_size
        self.board = []
        for _ in range(0, row_count):
            self.board.append([None for _ in range(0, columns_count)])

    def place_ship(self, ship):
        """Place a ship on the Player's board
        Raises:
            BoardError: if the target cell is occupied or too close to edge or
                        not on board
        """
        if self.ship_counts.get(ship.name, 0) == 0:
            raise NoRoomForThisShipError()

        max_row_count, max_column_count = self.board_size

        board_copy = copy.copy(self.board)
        rows, columns = ship.dimension
        for r in range(ship.target_row, ship.target_row + rows):
            for c in range(ship.target_col, ship.target_col + columns):
                if board_copy[r][c] is not None:
                    raise BoardError('Target is already occupied')
                if any([r >= max_row_count, c >= max_column_count]):
                    raise BoardError('Target cell too close to edge')

                board_copy[r][c] = ship

        self.board = board_copy
        self.ship_counts[ship.name] -= 1
        self.ships.append(ship)

    def set_hit(self, target_cell, debug=False):
        row, col = target_cell
        is_ship = self.board[row][col] is not None
        if is_ship:
            ship = self.board[row][col]
            is_sunk = ship.set_hit(target_cell)
        if debug:
            self.print_board(ship)
        if is_ship:
            return Response.SUNK_SHIP if is_sunk else Response.HIT_A_SHIP_BUT_NOT_SUNK
        else:
            return Response.NO_SHIP_HERE

    def has_lost(self):
        return all(ship.is_sunk() for ship in self.ships)

    def print_board(self, ship=None):
        """ascii art viz for the board"""
        print '\n'
        for r in range(0, self.board_size[0]):
            for c in range(0, self.board_size[1]):
                current_ship = self.board[r][c]
                if current_ship is None:
                    print u'\u25A1',  # empty square
                else:
                    print current_ship.symbol,
            print ''
        if ship:
            print 'hit cells ->', ship.busted_cells
        else:
            print '\n'
