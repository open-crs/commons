"""Module for defining the mitigations that can be used by a binary."""

from enum import Enum, auto


class Mitigations(Enum):
    ASLR = auto()
    NX = auto()
    CANARIES = auto()
    RELRO = auto()
    PIE = auto()
    FORTIFY = auto()
    ASAN = auto()
