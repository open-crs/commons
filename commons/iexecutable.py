import abc
import typing


class IExecutable(abc.ABC):
    identifier: str
    full_path: str
    cwes: typing.List[int]
