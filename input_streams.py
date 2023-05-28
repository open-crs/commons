"""Module for defining the input streams that can be used by a binary."""

from enum import Enum, auto


class InputStreams(Enum):
    STANDARD_INPUT = auto()
    ARGUMENTS = auto()
    FILES = auto()
