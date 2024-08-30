from typing import List
import os

def make_files_at_dir(dir: str, paths: List[str]) -> None:
    if not os.path.exists(dir):
        raise FileNotFoundError(f"Directory {dir} does not exist")
    for p in paths:
        absolute_p = os.path.join(dir, p)
        os.makedirs(os.path.dirname(absolute_p), exist_ok=True)
        with open(absolute_p, 'w') as f:
            f.write('')
