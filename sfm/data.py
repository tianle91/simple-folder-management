import os

from sqlitedict import SqliteDict

from sfm.types import Group

CONFIG_DIR = os.getenv("CONFIG_DIR", "./config")
DB_PATH = os.path.join(CONFIG_DIR, "sfm.db")


def get_groups() -> dict[str, Group]:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with SqliteDict(DB_PATH) as db:
        return {k: v for k, v in db.items()}
