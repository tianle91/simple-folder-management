import streamlit as st

from sfm.data import get_groups
from views.components import render_group

LIST_INTRO = """
# List Existing Groups

Here are the existing groups that are set up to automatically move files or directories when a move trigger is detected.
"""

st.markdown(LIST_INTRO)
groups = get_groups()
st.write(groups)
for group in groups.values():
    render_group(group)
