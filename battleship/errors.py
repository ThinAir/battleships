class TooManyPlayersError(Exception):
    pass


class NoSuchPlayerError(Exception):
    pass


class BoardError(Exception):
    pass


class NoRoomForThisShipError(Exception):
    pass


class GameOverError(Exception):
    pass


class NotEnoughPlayersError(Exception):
    pass


class WrongTurnError(Exception):
    pass
