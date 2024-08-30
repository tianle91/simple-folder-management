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
    src = st.text_input("Source Path")
    dst = st.text_input("Destination Base Path")
    triggers = get_new_triggers()
    move_item_type = st.radio("Move Item Type", ["file", "dir"], index=0)

    if len(src) == 0 or len(dst) == 0:
        st.error("Please set the default source and destination paths")
    elif len(triggers) == 0:
        st.error("Please set at least one move trigger")
    elif st.button("Create Group"):
        group = Group(
            name=name,
            src=src,
            dst=dst,
            triggers=triggers,
            move_files=move_item_type == "file",
        )
        with SqliteDict(DB_PATH) as db:
            if name in db:
                st.error(f"Group `{name}` already exists")
            else:
                db[name] = group
                db.commit()
                present_created_group(group)


render_create_new_group()
