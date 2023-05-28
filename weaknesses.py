"""Module for defining the weaknesses that a binary may have."""

from enum import Enum, auto


class Weaknesses(Enum):
    STACK_OUT_OF_BOUND_WRITE = auto()
    HEAP_OUT_OF_BOUND_WRITE = auto()
    TYPE_OVERFLOW = auto()
    TAINTED_FORMAT_STRING = auto()
