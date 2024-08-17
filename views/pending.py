import streamlit as st

from sfm.data import get_groups

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
