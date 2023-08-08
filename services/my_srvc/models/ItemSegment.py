from dataclasses import dataclass, field
from typing import Union, Optional
from services.my_srvc.models.ItemChangeReq import ItemChange


@dataclass
class ItemSegment:
    id: Optional[int] = field(default=None)
    segment_type: Optional[str] = field(default=None)
    channel_name: Optional[str] = field(default=None)
    current_time: Optional[int] = field(default=None)
    segment_length: Optional[int] = field(default=None)
    updatedAt: Optional[str] = field(default=None)
    createdAt: Optional[str] = field(default=None)
    json: Union[dict, ItemChange] = field(default=None)
