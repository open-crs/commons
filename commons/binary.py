"""Module for statically analyzing binaries."""

import logging
import typing
from enum import Enum, auto

from pwn import ELF

from commons.mitigations import Mitigations


class ContextAspects(Enum):
    EXECSTACK = auto()
    RWX_SEGMENTS = auto()


def get_mitigations(binary: ELF) -> typing.List[Mitigations]:
    yield from __get_members_from_loaded_elf(binary, Mitigations)


def get_context_aspects(binary: ELF) -> typing.List[ContextAspects]:
    yield from __get_members_from_loaded_elf(binary, ContextAspects)


def __get_members_from_loaded_elf(
    binary: ELF, members_enum: Enum
) -> typing.Generator[Enum, None, None]:
    for member in members_enum:
        member_name = member.name
        if getattr(binary, member_name.lower(), False):
            logging.info("Found set member of binary: %s", member_name)

            yield members_enum[member_name]
