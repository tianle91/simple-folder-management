import os
import re
from glob import glob
from typing import Dict, List, Set


def get_tokens_from_string(s: str) -> Set[str]:
    toks = s.split() + s.split("_") + s.split("-")
    for regex in [r"\(.*?\)", r"\[.*?\]"]:
        toks += re.findall(regex, s)
    return set(toks)


def get_token_to_file_names(path: str) -> Dict[str, List[str]]:
    toks_to_file_names: Dict[str, List[str]] = {}
    for p in glob(os.path.join(path, "*.*")):
        # p is {source_path}/X.ext so this grabs X
        file_name: str = p.split("/")[-1].split(".")[0]
        toks = get_tokens_from_string(s=file_name)
        for tok in toks:
            tok_file_names = toks_to_file_names.get(tok, [])
            tok_file_names.append(file_name)
            toks_to_file_names[tok] = tok_file_names
    return toks_to_file_names


def get_token_to_folder_names(path: str) -> Dict[str, List[str]]:
    toks_to_folder_names: Dict[str, List[str]] = {}
    for p in glob(os.path.join(path, "*", "")):
        # p is {dump_dir}/X/ so this grabs X
        folder_name = p.split("/")[-2]
        toks = get_tokens_from_string(s=folder_name)
        for tok in toks:
            tok_folder_names = toks_to_folder_names.get(tok, [])
            tok_folder_names.append(folder_name)
            toks_to_folder_names[tok] = tok_folder_names
    return toks_to_folder_names
