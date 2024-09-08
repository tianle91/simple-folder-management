import streamlit as st
from sqlitedict import SqliteDict

from sfm.data import DB_PATH, Group
from sfm.path import (
    get_token_to_file_names,
    get_token_to_folder_names,
    get_top_level_files,
    get_top_level_folders,
)
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
        token_to_names = (
            get_token_to_file_names(path=src)
            if move_files
            else get_token_to_folder_names(path=src)
        )
        most_tokens = [
            (k, token_to_names[k])
            for k in sorted(
                token_to_names.keys(),
                key=lambda k: len(token_to_names[k]),
                reverse=True,
            )
            if len(token_to_names[k]) > 1
        ]
        with st.expander(
            f"Found {len(most_tokens)} tokens from {'files' if move_files else 'folders'} in source path"
        ):
            for k, names in most_tokens:
                summary_md_str = f"* `{k}` appears in {len(names)} {'files' if move_files else 'folders'}: "
                if len(names) > 0:
                    for i, name in enumerate(names):
                        if i <= 5:
                            summary_md_str += f" `{name}`"
                        else:
                            summary_md_str += f"... and {len(names) - i} more"
                            break
                st.markdown(summary_md_str)

    dst = st.text_input("Destination Base Path")
    if dst == "":
        st.error("Please set destination path")
    else:
        paths = (
            get_top_level_files(path=src)
            if move_files
            else get_top_level_folders(path=src)
        )
        with st.expander(
            f"{len(paths)} existing `{('files' if move_files else 'folders')}` at `{dst}`"
        ):
            st.markdown("\n".join([p for p, _ in paths]))

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
