"""Helpers for extracting architecture metadata from ELF binaries."""

import os

from elftools.elf.elffile import ELFError, ELFFile

from commons.arch import Architecture

_ELF_ARCH_MAP = {
    ("ELFCLASS32", "EM_386"): Architecture.X86,
    ("ELFCLASS64", "EM_X86_64"): Architecture.X86_64,
}

class UnsupportedArchitectureError(Exception):
    """Raised when an ELF architecture is not supported by OpenCRS."""


class InvalidELFError(Exception):
    """Raised when the given file is missing or not a valid ELF."""


def detect_binary_arch(binary_path: str) -> Architecture:
    if not os.path.isfile(binary_path):
        raise InvalidELFError(f"File does not exist: {binary_path}")

    with open(binary_path, "rb") as binary_file:
        try:
            elf = ELFFile(binary_file)
        except ELFError as exc:
            raise InvalidELFError(
                f"Invalid ELF file: {binary_path}"
            ) from exc

        elf_class = elf["e_ident"]["EI_CLASS"]
        machine = elf["e_machine"]

    arch = _ELF_ARCH_MAP.get((elf_class, machine))
    if arch is not None:
        return arch

    raise UnsupportedArchitectureError(
        "Unsupported ELF architecture "
        f"(class={elf_class}, machine={machine}) for {binary_path}"
    )
