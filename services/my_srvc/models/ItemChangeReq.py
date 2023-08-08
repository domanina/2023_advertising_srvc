import time

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from random import randint
from typing import Union


class SegmentType(Enum):
    PROGRAM = "program"
    UNKNOWN = "unknown"



@dataclass
class ItemChangeSegment:
    segmentType: Optional[str] = field(default=None)
    channel: Optional[str] = field(default=None)
    currentTime: int = field(default_factory=lambda: int(time.time()), init=True)
    segmentLength: int = field(default_factory=lambda: randint(-1, 1000000), init=True)


@dataclass
class ItemChange:
    itemChange: Union[ItemChangeSegment, dict]
