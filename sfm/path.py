import os
from glob import glob
from pathlib import Path
from typing import Dict, List, Set, Tuple

PARENTHESES = ["(", ")", "[", "]", "{", "}"]
SEPARATORS = [".", "-", "_", "/", "#", "\\"]


def get_top_level_files(path: str) -> List[Tuple[str, str]]:
    out = []
    for p in glob(os.path.join(path, "*.*")):
        # p is {source_path}/X.ext so this grabs X.ext
        file_name = p.split("/")[-1]
        out.append((p, file_name))
    return out


def get_top_level_folders(path: str) -> List[Tuple[str, str]]:
    out = []
    for p in glob(os.path.join(path, "*", "")):
        # p is {dump_dir}/X/ so this grabs X
        folder_name = p.split("/")[-2]
        out.append((p, folder_name))
    return out


def tokenize(s: str) -> Set[str]:
    for c in SEPARATORS + PARENTHESES:
        s = s.replace(c, " ")
    return set(s.split())


def get_token_to_file_names(path: str) -> Dict[str, List[str]]:
    toks_to_file_names: Dict[str, List[str]] = {}
    for _, file_name in get_top_level_files(path=path):
        # only tokenize the file name, not the extension
        toks = tokenize(s=Path(file_name).stem)
        for tok in toks:
            tok_file_names = toks_to_file_names.get(tok, [])
            tok_file_names.append(file_name)
            toks_to_file_names[tok] = tok_file_names
    return toks_to_file_names


def get_token_to_folder_names(path: str) -> Dict[str, List[str]]:
    toks_to_folder_names: Dict[str, List[str]] = {}
    for _, folder_name in get_top_level_folders(path=path):
        toks = tokenize(s=folder_name)
        for tok in toks:
            tok_folder_names = toks_to_folder_names.get(tok, [])
            tok_folder_names.append(folder_name)
            toks_to_folder_names[tok] = tok_folder_names
    return toks_to_folder_names
