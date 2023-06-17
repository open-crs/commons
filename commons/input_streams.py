"""Module for defining the input streams that can be used by a binary."""

import typing
from dataclasses import dataclass
from enum import Enum


@dataclass
class Stream:
    long_name: str
    indicators: typing.List[str]


class InputStreams(Enum):
    # At the moment, some libcalls and syscalls (for example, vfscanf) are
    # omitted due to an assumption that they are not frequently used in
    # practice. This list will anyway be continuously update
    STDIN = Stream(
        "standard input",
        [
            "read",
            "gets",
            "pread",
            "fread",
            "fgets",
            "fgetc",
            "fscanf",
            "read",
            "pread",
            "fread",
            "fgets",
            "fgetc",
            "fscanf",
        ],
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
        ],
    )
    ENVIRONMENT_VARIABLE = Stream("environment variables", ["getenv"])
    NETWORKING = Stream("network packets", ["recv", "recvfrom", "recvmsg"])
