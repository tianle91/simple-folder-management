import os
import shutil
import time
from glob import glob

import pycron
import yaml


class SimpleFolderManagement:
    def __init__(self, config_path: str) -> None:
        # load from config_path
        self.config_path = config_path
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        # cron
        self.cron = self.config['meta']['cron']
        # get dump and managed dirs
        base_dir = self.config['meta']['base_dir']
        self.dump_dir = os.path.join(base_dir, self.config['meta']['dump_dir'])
        self.managed_dir = os.path.join(base_dir, self.config['meta']['managed_dir'])
        os.makedirs(self.dump_dir, exist_ok=True)
        os.makedirs(self.managed_dir, exist_ok=True)

    def parse_dump_dir(self):
        # glob pattern to get all top level directories: dumpdir/*/
        folders_in_dump = glob(os.path.join(self.dump_dir, '*', ''))
        folder_mapping = {
            # folder_name: (source_path, dest_path)
            p.split('/')[-2]: (p, None)
            for p in folders_in_dump
        }
        return folder_mapping
        # assert set(folder_mapping.keys()) == {'keyword_A', 'keyword_B', 'no_hits'}, folder_mapping

    def get_moves(self):
        folder_mapping = self.parse_dump_dir()
        for _, group_config in self.config['groups'].items():
            move_to_directory = os.path.join(self.managed_dir, group_config['name'])
            for folder_name in folder_mapping:
                source_dir, dest_dir = folder_mapping[folder_name]
                if dest_dir is not None:
                    continue
                else:
                    for kwd in group_config['keywords']:
                        if kwd in folder_name:
                            dest_dir = os.path.join(move_to_directory, folder_name)
                            folder_mapping[folder_name] = source_dir, dest_dir
                            break
        return folder_mapping
        # assert folder_mapping['keyword_A'][1] == 'tests/example_directory/managed/group_A_name/keyword_A'
        # assert folder_mapping['keyword_B'][1] == 'tests/example_directory/managed/group_A_name/keyword_B'
        # assert folder_mapping['no_hits'][1] is None


def execute_moves(folder_mapping: dict):
    for folder_name in folder_mapping:
        source_dir, dest_dir = folder_mapping[folder_name]
        if dest_dir is not None:
            shutil.move(source_dir, dest_dir)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='Simple Folder Management')
    parser.add_argument('config')
    args = parser.parse_args()

    sfm = SimpleFolderManagement(config_path=args.config)

    while True:
        if pycron.is_now(sfm.cron):
            folder_mapping = sfm.get_moves()
            execute_moves(folder_mapping=folder_mapping)
        time.sleep(60)
