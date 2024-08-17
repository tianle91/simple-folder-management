import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set

logger = logging.getLogger(__name__)


class MoveItemType(Enum):
    FILE = "file"
    DIR = "dir"


@dataclass
class Group:
    name: str
    source_path: str  # file/dir will be moved from source_path
    destination_base_path: str  # file/dir will be moved to destination_base_path/<group_name>
    move_item_type: MoveItemType  # file or dir
    move_triggers: Optional[Set[str]] = None  # keywords that trigger move
