from utils.enum import IntEnum


class OrderType(IntEnum):
    UNIT = 0
    NAME = 1
    CREATED = 2
    CHANGED = 3
    DONE = 4
