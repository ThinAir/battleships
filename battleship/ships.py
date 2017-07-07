class AbstractPiece(object):
    busted_cells = []  # keep track of the destroyed cells of this piece
    dimension = None  # how manycells are occupied
    name = None  # name of the piece
    _symbol = None  # unicode symbol used to visualise the piece

    def __init__(self, target_row, target_col):
        if not any([isinstance(target_row, int), isinstance(target_col, int)]):
            raise ValueError('target row and column must be ints')
        self.target_row = target_row
        self.target_col = target_col

    def is_sunk(self):
        return len(self.busted_cells) >= self.dimension[0] * self.dimension[1]

    def set_hit(self, target_cell):
        self.busted_cells.append(target_cell)
        return self.is_sunk()

    @property
    def symbol(self):
        if self.is_sunk():
            return '{}{}{}'.format('\033[4m', self._symbol, '\033[0m')
        return self._symbol


class Carrier(AbstractPiece):
    dimension = (1, 5)
    name = 'carrier'
    _symbol = 'a'


class Battleship(AbstractPiece):
    dimension = (1, 4)
    name = 'battleship'
    _symbol = 'b'


class Submarine(AbstractPiece):
    dimension = (1, 3)
    name = 'submarine'
    _symbol = 's'


class Cruiser(AbstractPiece):
    dimension = (1, 2)
    name = 'cruiser'
    _symbol = 'u'


class Destroyer(AbstractPiece):
    dimension = (1, 2)
    name = 'destroyer'
    _symbol = 'd'
