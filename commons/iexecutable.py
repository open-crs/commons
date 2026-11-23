import abc
import typing

from commons.arch import Architecture
from commons.elf_utils import detect_binary_arch


class IExecutable(abc.ABC):
    identifier: str
    full_path: str
    cwes: typing.List[int]
    architecture: typing.Optional[Architecture] = None

    def resolve_architecture(self) -> Architecture:
        if self.architecture is None:
            self.architecture = detect_binary_arch(self.full_path)
        return self.architecture
