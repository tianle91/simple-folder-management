import os

CONFIG_DIR = os.getenv("CONFIG_DIR", "./config")
DB_PATH = os.path.join(CONFIG_DIR, "sfm.db")


def render_parsed_str_splits(s: str):
    return f"{' '.join([f'`{v}`' for v in s.split()])}"
