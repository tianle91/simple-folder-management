from typing import Optional, Set

import streamlit as st
from sqlitedict import SqliteDict

from sfm.data import DB_PATH
from sfm.types import Group


def get_new_triggers(group: Optional[Group] = None) -> Optional[Set[str]]:
    existing_move_triggers = sorted(list(group.move_triggers)) if group else []
    move_triggers = sorted(
        st.text_input(
            label="Move Triggers",
            value=" ".join(existing_move_triggers),
            key=f"{group.name}_move_triggers" if group is not None else "move_triggers",
        ).split()
    )
    st.markdown("Parsed move triggers: " + " ".join([f"`{v}`" for v in move_triggers]))
    return set(move_triggers) if len(move_triggers) > 0 else None


@st.dialog("Confirm removal")
def confirm_removal(group: Group):
    st.write(f"Are you sure you want to remove group `{group.name}`?")
    if st.button("Yes"):
        with SqliteDict(DB_PATH, autocommit=True) as db:
            del db[group.name]
        st.rerun()


def render_group(group: Group, allow_removal: bool = True):
    st.markdown("---")
    st.markdown(f"## `{group.name}`")
    st.markdown(
        f"Moves **{group.move_item_type}s** from `{group.source_path}` to `{group.destination_base_path}/{group.name}`"
    )
    new_move_triggers = get_new_triggers(group)
    if new_move_triggers != group.move_triggers:
        if st.button("Update Move Triggers", key=f"{group.name}_update_move_triggers"):
            with SqliteDict(DB_PATH, autocommit=True) as db:
                group.move_triggers = new_move_triggers
                db[group.name] = group
            st.rerun()
    if allow_removal:
        if st.button("Remove group", key=f"{group.name}_remove"):
            confirm_removal(group)
