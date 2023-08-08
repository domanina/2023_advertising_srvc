from dataclasses import dataclass
from typing import List
from services.my_srvc.models.ItemSegment import ItemSegment


@dataclass
class ItemSegmentsList:
    _items: List[ItemSegment]
