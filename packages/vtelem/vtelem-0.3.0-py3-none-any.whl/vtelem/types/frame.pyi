from enum import IntEnum
from typing import NamedTuple, Optional

class FrameType(IntEnum):
    INVALID: int
    DATA: int
    EVENT: int
    MESSAGE: int
    STREAM: int

class FrameHeader(NamedTuple):
    app_id: int
    type: FrameType
    timestamp: int
    size: int

class FrameFooter(NamedTuple):
    crc: Optional[int]

class ParsedFrame(NamedTuple):
    header: FrameHeader
    body: dict
    footer: FrameFooter
