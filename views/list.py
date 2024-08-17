from typing import Dict

import streamlit as st
from sqlitedict import SqliteDict

from sfm.types import Group
from views.utils import DB_PATH, render_parsed_str_splits


def render_group(group: Group):
    st.markdown(f"## `{group.name}`")
    st.markdown(
        f"Moves **{group.move_item_type}s** from `{group.source_path}` to `{group.destination_base_path}/{group.name}`"
    )
    st.markdown(f"Move Triggers: {render_parsed_str_splits(group.move_triggers)}")
    with st.expander(f"Update Move Triggers"):
        new_move_triggers = st.text_input(
            "New Move Triggers (separate by blank spaces)",
            value=group.move_triggers,
            key=f"{group.name}_new_move_triggers",
        )
        st.markdown(render_parsed_str_splits(s=new_move_triggers))
        if st.button("Update Move Triggers", key=f"{group.name}_update_move_triggers"):
            with SqliteDict(DB_PATH, autocommit=True) as db:
                group.move_triggers = new_move_triggers
                db[group.name] = group
            st.rerun()
    with st.expander(f"Remove Group"):
        if st.button("Confirm?", key=f"{group.name}_remove"):
            with SqliteDict(DB_PATH, autocommit=True) as db:
                del db[group.name]
            st.rerun()


LIST_GROUPS_INTRO = """
# List Existing Groups

Here are the existing groups that are set up to automatically move files or directories when a move trigger is detected.
"""


def render_all_groups(groups: Dict[str, Group]):
    st.markdown("# List existing Groups")
    for group in groups.values():
        render_group(group)
