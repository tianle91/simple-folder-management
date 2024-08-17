import os
from glob import glob
from typing import List, Tuple


def get_file_moves(
    source_path: str, destination_path: str, move_triggers: str
) -> List[Tuple[str, str, List[str]]]:
    move_triggers = move_triggers.split()
    moves = []
    for p in glob(os.path.join(source_path, "*.*")):
        # p is {source_path}/X.ext so this grabs X.ext
        file_name = p.split("/")[-1]
        move_trigger_hits = [kwd in file_name for kwd in move_triggers]
        if len(move_trigger_hits) > 0:
            moves.append((p, destination_path, move_trigger_hits))
    return moves


def get_folder_moves(
    source_path: str, destination_path: str, move_triggers: str
) -> List[Tuple[str, str, List[str]]]:
    move_triggers = move_triggers.split()
    moves = []
    for p in glob(os.path.join(source_path, "*", "")):
        # p is {dump_dir}/X/ so this grabs X
        folder_name = p.split("/")[-2]
        move_trigger_hits = [kwd in folder_name for kwd in move_triggers]
        if len(move_trigger_hits) > 0:
            moves.append((p, destination_path, move_trigger_hits))
    return moves
