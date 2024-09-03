import os
from dataclasses import dataclass
from typing import Dict, Set

from sqlitedict import SqliteDict

CONFIG_DIR = os.getenv("CONFIG_DIR", "./config")
DB_PATH = os.path.join(CONFIG_DIR, "sfm.db")


@dataclass
class Group:
    name: str
    src: str  # files/dirs will be moved from <src>
    dst: str  # files/dirs will be moved to <dst>
    triggers: Set[str]  # keywords to trigger move
    move_files: bool  # if False, then move directories


def get_groups() -> Dict[str, Group]:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with SqliteDict(DB_PATH) as db:
        # sort by dictionary keys
        return {k: v for k, v in sorted(db.items(), key=lambda item: item[0])}
