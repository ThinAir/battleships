import enum


class Response(enum.Enum):
    NO_SHIP_HERE = 'NO_SHIP_HERE'
    HIT_A_SHIP_BUT_NOT_SUNK = 'HIT_A_SHIP_BUT_NOT_SUNK'
    SUNK_SHIP = 'SUNK_SHIP'
