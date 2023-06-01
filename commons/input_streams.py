"""Module for defining the input streams that can be used by a binary."""

from enum import Enum, auto


class InputStreams(Enum):
    STDIN = auto()
    ARGUMENTS = auto()
    FILES = auto()
    ENVIRONMENT_VARIABLE = auto()
    NETWORKING = auto()
