import streamlit as st

pg = st.navigation(
    pages=[
        st.Page("views/pending.py", title="Pending"),
        st.Page("views/list.py", title="List Existing Groups"),
        st.Page("views/create.py", title="Create New Group"),
    ]
)
pg.run()
