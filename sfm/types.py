import logging
from dataclasses import dataclass
from typing import Set

logger = logging.getLogger(__name__)


@dataclass
class Group:
    name: str
    src: str  # files/dirs will be moved from <src>
    dst: str  # files/dirs will be moved to <dst>
    triggers: Set[str]  # keywords to trigger move
    move_files: bool  # if False, then move directories
