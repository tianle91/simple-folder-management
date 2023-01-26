from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Group:
    path: str
    keywords: List[str]


@dataclass
class ManagedDir:
    base_dir: str
    groups: Dict[str, Group]


def parse_raw_group(raw_group: dict) -> Group:
    return Group(
        path=raw_group['path'],
        keywords=sorted(list(raw_group['keywords'])),
    )


def parse_raw_managed_dirs(raw_managed_dirs: dict) -> Dict[str, ManagedDir]:
    out: Dict[str, ManagedDir] = {}
    for k, raw_managed_dir in raw_managed_dirs.items():
        managed_dir = ManagedDir(
            base_dir=raw_managed_dir['base_dir'],
            groups={
                l: parse_raw_group(raw_group=raw_group)
                for l, raw_group in raw_managed_dir['groups'].items()
            }
        )
        out[k] = managed_dir
    return out
