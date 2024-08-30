import os
from glob import glob
from typing import Optional, Set

import streamlit as st
from sqlitedict import SqliteDict

from sfm.data import DB_PATH
from sfm.types import Group, MoveItemType


def get_new_triggers(group: Optional[Group] = None) -> Optional[Set[str]]:
    existing_move_triggers = []
    if (
        group is not None
        and group.move_triggers is not None
        and len(group.move_triggers) > 0
    ):
        existing_move_triggers = sorted(list(group.move_triggers))
    move_triggers = sorted(
        s
        for s in st.text_input(
            label=f"Move Triggers (separate by space)",
            value=" ".join(existing_move_triggers),
            key=f"{group.name}_move_triggers" if group is not None else "move_triggers",
        ).split()
        if len(s) > 0
    )
    return set(move_triggers) if len(move_triggers) > 0 else None


@st.dialog("Confirm removal")
def confirm_removal(group: Group):
    st.write(f"Are you sure you want to remove group `{group.name}`?")
    if st.button("Yes"):
        with SqliteDict(DB_PATH, autocommit=True) as db:
            del db[group.name]
        st.rerun()


def render_group(
    group: Group, allow_removal: bool = True, show_existing_counts: bool = True
):
    st.markdown("---")
    st.markdown(
        f"Group`{group.name}` Moves **{group.move_item_type}s** From `{group.source_path}` to `{group.destination_path}`"
    )
    new_move_triggers = get_new_triggers(group)
    if new_move_triggers != group.move_triggers:
        if st.button("Update Move Triggers", key=f"{group.name}_update_move_triggers"):
            with SqliteDict(DB_PATH, autocommit=True) as db:
                group.move_triggers = new_move_triggers
                db[group.name] = group
            st.rerun()

    if show_existing_counts:
        if group.move_item_type == MoveItemType.FILE:
            paths = glob(os.path.join(group.destination_path, "*.*"))
        else:
            paths = glob(os.path.join(group.destination_path, "*", ""))
        with st.expander(
            f"{len(paths)} existing **{group.move_item_type}s** at `{group.destination_path}`"
        ):
            st.markdown("\n".join(paths))

    if allow_removal:
        if st.button("Remove group", key=f"{group.name}_remove"):
            confirm_removal(group)
