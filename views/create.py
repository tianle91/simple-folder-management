import os
from glob import glob

import streamlit as st
from sqlitedict import SqliteDict

from sfm.data import DB_PATH
from sfm.path import get_token_to_file_names, get_token_to_folder_names
from sfm.types import Group
from views.components import get_new_triggers, render_group

CREATE_INTRO = """
# Create a new Group

Create a new group to automatically move files or directories in source path to destination path when a move trigger is detected.
"""


@st.dialog("Present created group")
def present_created_group(group: Group):
    st.markdown(f"## Group `{group.name}` created")
    render_group(group=group)
    st.page_link(page="views/pending.py", label="Go to pending moves")
    st.page_link(page="views/list.py", label="See existing groups")


def render_create_new_group():
    st.markdown(CREATE_INTRO)

    name = st.text_input("Name")
    move_files = st.radio("Move Item Type", ["file", "dir"], index=0) == "file"

    src = st.text_input("Source Path")
    if src == "":
        st.error("Please set source path")
    else:
        if move_files:
            st.write(get_token_to_file_names(path=src))
        else:
            st.write(get_token_to_folder_names(path=src))

    dst = st.text_input("Destination Base Path")
    if dst == "":
        st.error("Please set destination path")
    else:
        pattern = os.path.join(dst, "*.*") if move_files else os.path.join(dst, "*", "")
        paths = glob(pattern)
        with st.expander(
            f"{len(paths)} existing `{('files' if move_files else 'folders')}` at `{dst}`"
        ):
            st.markdown("\n".join(paths))

    triggers = get_new_triggers()
    if len(triggers) == 0:
        st.error("Please set at least one trigger")
    else:
        pass

    if (
        name != ""
        and src != ""
        and dst != ""
        and len(triggers) > 0
        and st.button("Create Group")
    ):
        group = Group(
            name=name,
            src=src,
            dst=dst,
            triggers=triggers,
            move_files=move_files,
        )
        with SqliteDict(DB_PATH) as db:
            if name in db:
                st.error(f"Group `{name}` already exists")
            else:
                db[name] = group
                db.commit()
                present_created_group(group)


render_create_new_group()
