from dataclasses import dataclass
from enum import Enum
import typing


class Architecture(str, Enum):
    X86 = "x86"
    X86_64 = "x86_64"

    @classmethod
    def _missing_(cls, value: object) -> typing.Optional["Architecture"]:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in ("i386", "i486", "i586", "i686", "ia32", "x86_32"):
                return cls.X86
            if normalized in ("amd64", "x64", "x86-64"):
                return cls.X86_64
        return None


@dataclass(frozen=True)
class ArchConfig:
    architecture: Architecture
    bits: int
    pointer_size_bytes: int
    ip_register: str
    sp_register: str
    bp_register: str


_ARCH_CONFIGS: typing.Dict[Architecture, ArchConfig] = {
    Architecture.X86: ArchConfig(
        architecture=Architecture.X86,
        bits=32,
        pointer_size_bytes=4,
        ip_register="eip",
        sp_register="esp",
        bp_register="ebp",
    ),
    Architecture.X86_64: ArchConfig(
        architecture=Architecture.X86_64,
        bits=64,
        pointer_size_bytes=8,
        ip_register="rip",
        sp_register="rsp",
        bp_register="rbp",
    ),
}


def get_arch_config(arch: Architecture) -> ArchConfig:
    return _ARCH_CONFIGS[arch]
