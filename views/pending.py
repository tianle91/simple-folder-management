import os
import shutil
from typing import Dict, List

import streamlit as st

from sfm.data import Group, get_groups
from sfm.path import get_top_level_files, get_top_level_folders

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

srcs_to_groups_mapping: Dict[str, List[Group]] = {}
for group in groups.values():
    src_groups = srcs_to_groups_mapping.get(group.src, [])
    src_groups.append(group)
    srcs_to_groups_mapping[group.src] = src_groups

st.markdown(f"Currently tracking {len(srcs_to_groups_mapping)} source paths.")
for src_path, src_groups in srcs_to_groups_mapping.items():
    st.markdown(f"## Pending moves in `{src_path}`")
    files = get_top_level_files(src_path)
    folders = get_top_level_folders(src_path)

    with st.expander(
        f"Found {len(files)} files and {len(folders)} folders in `{src_path}`.",
        expanded=False,
    ):
        st.markdown(f"Files ({len(files)})")
        for p, obj in files:
            st.markdown(f"- `{p}`")
        st.markdown(f"Folders ({len(folders)})")
        for p, obj in folders:
            st.markdown(f"- `{p}`")

    with st.expander(
        f"There are {len(src_groups)} groups monitoring `{src_path}`",
        expanded=False,
    ):
        for group in src_groups:
            st.write(group)

    hits = {}
    for group in src_groups:
        if (group.triggers is None) or (len(group.triggers) == 0):
            st.error(f"Skipping group `{group.name}` as it has no move triggers.")
            continue
        files_or_folders = files if group.move_files else folders
        for p, obj in files_or_folders:
            triggers_found = [trigger for trigger in group.triggers if trigger in obj]
            if len(triggers_found) > 0:
                hits_candidates = hits.get(p, {})
                hits_candidates[group.name] = triggers_found
                hits[p] = hits_candidates

    selected_moves = []
    for p, possible_matched_groups in hits.items():
        if len(possible_matched_groups) == 1:
            # format the source and destination paths for use in shutil.move
            group_name = list(possible_matched_groups.keys())[0]
            group = groups[group_name]
            # make sure dst_folder_path ends with "/" so that it's a directory
            # also make sure it exists so that src is moved inside that directory
            # https://docs.python.org/3/library/shutil.html#shutil.move
            dst_folder_path = os.path.join(group.dst, "")
            selected_moves.append((p, dst_folder_path))
        else:
            # TODO: Handle multiple matches
            multiple_group_names_formatted = ", ".join(
                [f"`{s}`" for s in possible_matched_groups.keys()]
            )
            st.error(
                f"Skipping `{p}` as it matches multiple groups: {multiple_group_names_formatted}"
            )

    selected_moves_markdown = "\n".join(
        [f"* `{p}` → `{dest_p}`" for p, dest_p in selected_moves]
    )
    st.markdown(selected_moves_markdown)
    if len(selected_moves) > 0:
        if st.button("Trigger Moves"):
            for p, dst_folder_path in selected_moves:
                # make sure dst_folder_path ends with "/" so that it's a directory
                # also make sure it exists so that src is moved inside that directory
                # https://docs.python.org/3/library/shutil.html#shutil.move
                os.makedirs(dst_folder_path, exist_ok=True)
                shutil.move(p, dst_folder_path)
                st.success(f"Moved `{p}` to `{dst_folder_path}`")
            st.success("Moves ran successfully. Refresh to continue.")
            st.stop()
