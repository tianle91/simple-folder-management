import streamlit as st
from sqlitedict import SqliteDict

from sfm.types import Group
from views.utils import DB_PATH, render_parsed_str_splits

CREATE_NEW_GROUP_INTRO = """
# Create a new Group

Create a new group to automatically move files or directories in source path to destination path when a move trigger is detected.
"""


def render_create_new_group():
    st.markdown(CREATE_NEW_GROUP_INTRO)
    name = st.text_input("Name")
    source_path = st.text_input("Source Path")
    destination_base_path = st.text_input("Destination Base Path")
    move_item_type = st.radio("Move Item Type", ["file", "dir"], index=0)
    move_triggers = st.text_input("Move Triggers (separate by blank spaces)")
    st.markdown(render_parsed_str_splits(move_triggers))

    if len(source_path) == 0 or len(destination_base_path) == 0:
        st.error("Please set the default source and destination paths")

    if st.button("Create Group"):
        group = Group(
            name=name,
            source_path=source_path,
            destination_base_path=destination_base_path,
            move_item_type=move_item_type,
            move_triggers=move_triggers,
        )
        with SqliteDict(DB_PATH) as db:
            db[name] = group
            db.commit()
        st.rerun()
