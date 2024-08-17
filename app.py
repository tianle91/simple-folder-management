import streamlit as st

HOME_INTRO = """
# Simple Folder Management

This app helps you manage your files and directories using keywords as move triggers.
"""

with st.sidebar:
    st.markdown(HOME_INTRO)

pg = st.navigation(
    pages=[
        st.Page("views/pending.py", title="Pending Moves"),
        st.Page("views/list.py", title="List Existing Groups"),
        st.Page("views/create.py", title="Create New Group"),
    ]
)
pg.run()
