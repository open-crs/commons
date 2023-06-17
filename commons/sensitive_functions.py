"""Module for retrieving sensitive functions from binaries."""

import logging
import typing
from dataclasses import dataclass

from pwn import ELF

SENSITIVE_STRINGS = ["win", "secret", "shell", "system", "flag"]


@dataclass
class SensitiveFunction:
    name: str
    address: int


def get_sensitive_functions_names(
    elf_filename: str,
) -> typing.Generator[SensitiveFunction, None, None]:
    binary = ELF(elf_filename, checksec=False)
    funcs = [name for name in binary.symbols.keys() if __is_sensitive(name)]

    for name in funcs:
        logging.info(
            "Found sensitive function: %s (%s)",
            name,
            hex(binary.symbols[name]),
        )

        yield SensitiveFunction(name, binary.symbols[name])


def __is_sensitive(function_name: str) -> bool:
    return any([string in function_name for string in SENSITIVE_STRINGS])
