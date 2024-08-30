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

    with st.expander(
        f"Found {len(files)} files and {len(folders)} folders in `{source_path}`.",
        expanded=False,
    ):
        st.markdown(f"Files ({len(files)})")
        for p, obj in files:
            st.markdown(f"- `{p}`")
        st.markdown(f"Folders ({len(folders)})")
        for p, obj in folders:
            st.markdown(f"- `{p}`")

    hits = {}
    for group in groups.values():
        paths_and_objects = (
            files if group.move_item_type == MoveItemType.FILE.value else folders
        )
        for p, obj in paths_and_objects:
            move_triggers_found = [
                trigger for trigger in group.move_triggers if trigger in obj
            ]
            if len(move_triggers_found) > 0:
                hits_candidates = hits.get(p, {})
                hits_candidates[group.name] = move_triggers_found
                hits[p] = hits_candidates

    selected_moves = []
    for p, possible_matched_groups in hits.items():
        if len(possible_matched_groups) == 1:
            group_name = list(possible_matched_groups.keys())[0]
            group = groups[group_name]
            selected_moves.append((p, group.destination_path, group_name))
        else:
            # TODO: Handle multiple matches
            multiple_group_names_formatted = ", ".join(
                [f"`{s}`" for s in possible_matched_groups.keys()]
            )
            st.error(
                f"Skipping `{p}` as it matches multiple groups: {multiple_group_names_formatted}"
            )

    selected_moves_markdown = ""
    for p, dest_p, group_name in selected_moves:
        selected_moves_markdown += (
            f"* `{p}` → `{dest_p}` (matched group: `{group_name}`)\n"
        )
    st.markdown(selected_moves_markdown)
