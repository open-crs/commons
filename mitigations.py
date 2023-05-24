from enum import Enum, auto


class Mitigations(Enum):
    NX = auto()
    CANARIES = auto()
    PIE = auto()
    ASLR = auto()
