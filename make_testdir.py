import os

from tests.utils import make_files_at_dir

with open("tests/dump_globs.txt") as f:
    paths = f.read().splitlines()

os.makedirs("testdir", exist_ok=False)
make_files_at_dir("testdir", paths)
