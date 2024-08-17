import logging
import os

import streamlit as st
from sqlitedict import SqliteDict

from sfm.types import Group
from views.create import render_create_new_group
from views.list import render_all_groups

CONFIG_DIR = os.getenv("CONFIG_DIR", "./config")
DB_PATH = os.path.join(CONFIG_DIR, "sfm.db")
log = logging.getLogger(__name__)


def get_groups() -> dict[str, Group]:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with SqliteDict(DB_PATH) as db:
        return {k: v for k, v in db.items()}


groups = get_groups()

list_tab, create_tab = st.tabs(["List Groups", "Create Group"])

with list_tab:
    render_all_groups(groups)

with create_tab:
    render_create_new_group()
