"""Module for statically analyzing binaries."""

import logging
import typing
from enum import Enum, auto

from commons.mitigations import Mitigations
from pwn import ELF

SENSITIVE_STRINGS = ["win", "secret", "shell", "system", "flag"]


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


def get_sensitive_functions_names(
    elf_filename: str,
) -> typing.Generator[str, None, None]:
    binary = ELF(elf_filename)
    funcs = [name for name in binary.symbols.keys() if __is_sensitive(name)]

    for name in funcs.items():
        logging.info(
            "Found sensitive function: %s (%s)", name, hex(binary.symbols[name])
        )

    yield from funcs


def __is_sensitive(function_name: str) -> bool:
    return any([string in function_name for string in SENSITIVE_STRINGS])
