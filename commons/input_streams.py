"""Module for defining the input streams that can be used by a binary."""

import typing
from dataclasses import dataclass
from enum import Enum


@dataclass
class Stream:
    long_name: str
    indicators: typing.List[str]


# On Linux/glibc, some stdio functions are macros that expand to internal
# _IO_* symbols at compile time. The binary's PLT contains the internal
# name, not the public one, so Ghidra extracts _IO_getc instead of getc.
GLIBC_MACRO_EXPANSIONS = {
    "getc":    "_IO_getc",
    "getchar": "_IO_getchar",
    "putc":    "_IO_putc",
    "putchar": "_IO_putchar",
}

def _with_glibc_aliases(indicators):
    result = []
    for name in indicators:
        result.append(name)
        if name in GLIBC_MACRO_EXPANSIONS:
            result.append(GLIBC_MACRO_EXPANSIONS[name])
    return result

class InputStreams(Enum):
    # At the moment, some libcalls and syscalls (for example, vfscanf) are
    # omitted due to an assumption that they are not frequently used in
    # practice. This list will anyway be continuously update
    STDIN = Stream(
        "standard input",
        _with_glibc_aliases([
            "read",
            "gets",
            "getc",
            "getchar", 
            "getline",
            "pread",
            "fread",
            "fgets",
            "fgetc",
            "fscanf",
            "scanf"
        ])
    )
    ARGUMENTS = Stream("program arguments", [])
    FILES = Stream(
        "files",
        [
            "read",
            "pread",
            "fread",
            "fgets",
            "fgetc",
            "fscanf",
            "fopen",
            "open",
            "openat"
        ]
    )
    ENVIRONMENT_VARIABLE = Stream(
        "environment variables", 
        [
            "getenv",
            "secure_getenv"
        ]
    )
    NETWORKING = Stream(
        "network packets", 
        [
            "recv", 
            "recvfrom", 
            "recvmsg",
            "connect",
            "send",
            "sendto",
            "sendmsg"
        ]
    )
