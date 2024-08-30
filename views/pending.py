import streamlit as st

from sfm.data import get_groups
from sfm.moves import get_top_level_files, get_top_level_folders
from sfm.types import MoveItemType

PENDING_INTRO = """
# Pending

Pending file or directory moves will be triggered by keywords you specify.
"""

st.markdown(PENDING_INTRO)

groups = get_groups()

st.markdown(f"Currently tracking {len(groups)} groups.")
if st.button("List Existing Groups"):
    st.switch_page("views/list.py")

if len(groups) == 0:
    st.info("No groups found. Create a new group to get started.")
    if st.button("Create New Group"):
        st.switch_page("views/create.py")

source_paths = set(group.source_path for group in groups.values())
st.markdown(f"Currently tracking {len(source_paths)} source paths.")
for source_path in source_paths:
    st.markdown(f"## Pending moves in `{source_path}`")
    files = get_top_level_files(source_path)
    folders = get_top_level_folders(source_path)
    st.markdown(
        f"Found {len(files)} files and {len(folders)} folders in `{source_path}`."
    )
    hits = {}
    for group in groups.values():
        for p, obj in files if group.move_item_type == MoveItemType.FILE else folders:
            move_triggers_found = [
                trigger for trigger in group.move_triggers if trigger in obj
            ]
            if len(move_triggers_found) > 0:
                hits_candidates = hits.get(p, {})
                hits_candidates[group.name] = move_triggers_found
                hits[p] = hits_candidates
    st.write(hits)
