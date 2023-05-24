from enum import Enum, auto


class InputStreams(Enum):
    STANDARD_INPUT = auto()
    ARGUMENTS = auto()
    FILES = auto()
