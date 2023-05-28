"""Module for defining the outcomes that an attack may have."""

from enum import Enum


class Outcome(Enum):
    CODE_EXECUTION = 0
    CALL_TO_WIN_FUNCTION = CODE_EXECUTION + 1
    INTERACTIVE_SHELL = CODE_EXECUTION + 2

    INFORMATION_LEAK = 10
    DENIAL_OF_SERVICE = 20
