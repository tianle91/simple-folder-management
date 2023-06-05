import logging
from dataclasses import dataclass
from typing import Dict, List

logger = logging.getLogger(__name__)


@dataclass
class Group:
    path: str
    keywords: List[str]


@dataclass
class ManagedDir:
    base_dir: str
    groups: Dict[str, Group]
    move_files: bool = False


def parse_raw_group(raw_group: dict) -> Group:
    return Group(
        path=raw_group['path'],
        keywords=sorted(list(raw_group['keywords'])),
    )


def parse_raw_managed_dirs(raw_managed_dirs: dict) -> Dict[str, ManagedDir]:
    out: Dict[str, ManagedDir] = {}
    for k, raw_managed_dir in raw_managed_dirs.items():
        groups = {}
        for l, raw_group in raw_managed_dir['groups'].items():
            try:
                groups[l] = parse_raw_group(raw_group=raw_group)
            except Exception as e:
                logger.fatal(f'Failed to parse managed_dirs.{k}.{l}')
                raise e
        managed_dir = ManagedDir(
            base_dir=raw_managed_dir['base_dir'],
            move_files=raw_managed_dir.get('move_files', False),
            groups=groups
        )
        out[k] = managed_dir
    return out
