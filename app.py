import logging
import os
import shutil
import time
from glob import glob
from typing import Dict, List, Tuple

import pycron
import yaml

from sfm.types import Group, ManagedDir, parse_raw_managed_dirs

log = logging.getLogger(__name__)


def get_file_moves(path: str, groups: Dict[str, Group]) -> List[Tuple[str, str]]:
    dump_dir = os.path.join(path, 'dump')
    moves = []
    for p in glob(os.path.join(dump_dir, '*.*')):
        # p is {dump_dir}/X.ext so this grabs X.ext
        file_name = p.split('/')[-1]
        for _, group in groups.items():
            move_to_directory = os.path.join(path, group.path)
            os.makedirs(move_to_directory, exist_ok=True)
            if any([kwd in file_name for kwd in group.keywords]):
                moves.append((p, move_to_directory))
                break
    return moves


def get_folder_moves(path: str, groups: Dict[str, Group]) -> List[Tuple[str, str]]:
    dump_dir = os.path.join(path, 'dump')
    mappings = []
    for p in glob(os.path.join(dump_dir, '*', '')):
        # p is {dump_dir}/X/ so this grabs X
        folder_name = p.split('/')[-2]
        for _, group in groups.items():
            move_to_directory = os.path.join(path, group.path)
            os.makedirs(move_to_directory, exist_ok=True)
            if any([kwd in folder_name for kwd in group.keywords]):
                dest_dir = os.path.join(move_to_directory, folder_name)
                mappings.append((p, dest_dir))
                break
    return mappings


class SimpleFolderManagement:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path

    @property
    def raw_config(self) -> dict:
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    @property
    def cron(self) -> str:
        return self.raw_config['cron']

    @property
    def managed_dirs(self) -> Dict[str, ManagedDir]:
        raw_managed_dirs = self.raw_config['managed_dirs']
        return parse_raw_managed_dirs(raw_managed_dirs=raw_managed_dirs)

    def get_all_moves(self) -> List[Tuple[str, str]]:
        all_moves = []
        for _, managed_dir in self.managed_dirs.items():
            if managed_dir.move_files:
                moves = get_file_moves(
                    path=managed_dir.base_dir,
                    groups=managed_dir.groups,
                )
            else:
                moves = get_folder_moves(
                    path=managed_dir.base_dir,
                    groups=managed_dir.groups,
                )
            log.info(
                f'In {managed_dir.base_dir}, '
                f'found {len(moves)} directories to be moved.'
            )
            all_moves.extend(moves)
        return all_moves


if __name__ == '__main__':
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(prog='Simple Folder Management')
    parser.add_argument('config')
    args = parser.parse_args()

    sfm_instance = SimpleFolderManagement(config_path=args.config)
    while True:
        if pycron.is_now(sfm_instance.cron):
            all_moves = sfm_instance.get_all_moves()
            for source_dir, dest_dir in all_moves:
                log.info(f'Moving {source_dir} -> {dest_dir}')                    
                if not os.path.isfile(source_dir) and os.path.exists(dest_dir):
                    log.info('Destination directory exists, clearing.')
                    shutil.rmtree(dest_dir)
                shutil.move(source_dir, dest_dir)
        time.sleep(60)
