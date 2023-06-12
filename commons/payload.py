"""Module for describing a payload that is sent to the program"""

import typing
from dataclasses import dataclass

from commons.input_streams import InputStreams


@dataclass
class SingleStreamPayload:
    content: bytes
    input_stream: InputStreams


@dataclass
class Payload:
    payloads_per_streams: typing.List[SingleStreamPayload]
