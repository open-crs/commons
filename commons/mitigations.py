"""Module for defining the mitigations that can be used by a binary."""

import typing
from enum import Enum, auto

from pwn import ELF

from commons.binary import _get_members_from_loaded_elf


class Mitigations(Enum):
    ASLR = auto()
    NX = auto()
    CANARIES = auto()
    RELRO = auto()
    PIE = auto()
    FORTIFY = auto()
    ASAN = auto()


def get_mitigations(binary: ELF) -> typing.List[Mitigations]:
    yield from _get_members_from_loaded_elf(binary, Mitigations)
