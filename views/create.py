import streamlit as st
from sqlitedict import SqliteDict

from sfm.data import DB_PATH
from sfm.types import Group
from views.components import get_new_triggers, render_group

CREATE_INTRO = """
# Create a new Group

Create a new group to automatically move files or directories in source path to destination path when a move trigger is detected.
"""


@st.dialog("Present created group")
def present_created_group(group: Group):
    st.markdown(f"## Group `{group.name}` created")
    st.write(group)
    st.page_link(page="views/pending.py", label="Go to pending moves")
    st.page_link(page="views/list.py", label="See existing groups")


def render_create_new_group():
    st.markdown(CREATE_INTRO)
    name = st.text_input("Name")
    source_path = st.text_input("Source Path")
    destination_base_path = st.text_input("Destination Base Path")
    move_item_type = st.radio("Move Item Type", ["file", "dir"], index=0)
    move_triggers = get_new_triggers()
    if len(source_path) == 0 or len(destination_base_path) == 0:
        st.error("Please set the default source and destination paths")
    elif st.button("Create Group"):
        group = Group(
            name=name,
            source_path=source_path,
            destination_base_path=destination_base_path,
            move_item_type=move_item_type,
            move_triggers=move_triggers,
        )
        with SqliteDict(DB_PATH) as db:
            if name in db:
                st.error(f"Group `{name}` already exists")
            else:
                db[name] = group
                db.commit()
                present_created_group(group)


render_create_new_group()
