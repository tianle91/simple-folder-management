import os
from glob import glob
from typing import List, Tuple


def get_files(path: str) -> List[Tuple[str, str]]:
    out = []
    for p in glob(os.path.join(path, "*.*")):
        # p is {source_path}/X.ext so this grabs X.ext
        file_name = p.split("/")[-1]
        out.append((p, file_name))
    return out


def get_folders(path: str) -> List[Tuple[str, str]]:
    out = []
    for p in glob(os.path.join(path, "*", "")):
        # p is {dump_dir}/X/ so this grabs X
        folder_name = p.split("/")[-2]
        out.append((p, folder_name))
    return out
