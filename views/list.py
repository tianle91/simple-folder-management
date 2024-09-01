import streamlit as st

from sfm.data import get_groups
from views.components import render_group

LIST_INTRO = """
# List Existing Groups

Here are the existing groups that are set up to automatically move files or directories when a move trigger is detected.
"""

st.markdown(LIST_INTRO)
groups = get_groups()

file_groups = {}
dir_groups = {}
for k, g in groups.items():
    if g.move_files:
        file_groups[k] = g
    else:
        dir_groups[k] = g

file_tab, dir_tab = st.tabs(
    [f"File Groups ({len(file_groups)})", f"Directory Groups ({len(dir_groups)})"]
)
with file_tab:
    for group in file_groups.values():
        render_group(group)
with dir_tab:
    for group in dir_groups.values():
        render_group(group)
