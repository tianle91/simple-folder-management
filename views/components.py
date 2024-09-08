from typing import Optional, Set

import streamlit as st
from sqlitedict import SqliteDict

from sfm.data import DB_PATH, Group
from sfm.path import get_top_level_files, get_top_level_folders


def get_new_triggers(group: Optional[Group] = None) -> Set[str]:
    existing_move_triggers = []
    if group is not None:
        existing_move_triggers = sorted(list(group.triggers))
    move_triggers = sorted(
        s.strip()
        for s in st.text_input(
            label=f"Move Triggers (separate by comma)",
            value=", ".join(existing_move_triggers),
            key=f"{group.name}_move_triggers" if group is not None else "move_triggers",
        ).split(",")
        if len(s) > 0
    )
    return set(move_triggers)


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
    st.markdown(
        ("📄" if group.move_files else "📁")
        + f" {group.name}: `{group.src}` → `{group.dst}`"
    )

    new_triggers = get_new_triggers(group)
    if new_triggers != group.triggers:
        if st.button("Update Move Triggers", key=f"{group.name}_update_move_triggers"):
            with SqliteDict(DB_PATH, autocommit=True) as db:
                group.triggers = new_triggers
                db[group.name] = group
            st.rerun()

    if show_existing_counts:
        paths = (
            get_top_level_files(path=group.src)
            if group.move_files
            else get_top_level_folders(path=group.src)
        )
        with st.expander(
            f"{len(paths)} existing `{('files' if group.move_files else 'folders')}` at `{group.dst}`"
        ):
            st.markdown("\n\n".join([f"`{p}`" for p, _ in paths]))

    if allow_removal:
        if st.button("Remove group", key=f"{group.name}_remove"):
            confirm_removal(group)

    st.markdown("---")
