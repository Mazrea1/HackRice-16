"""
pages/2_Routine.py

Your Routine page -- placeholder for now. We'll build this out next to
show saved exercises using add_saved_exercise() / delete_saved_exercise()
from the backend.
"""

import streamlit as st

from Theme import inject_theme
from Nav import render_top_nav

st.set_page_config(page_title="ReRack — Routine", page_icon="📋", layout="wide")

inject_theme()
render_top_nav("Routine")

st.markdown('<div class="page-title">Your Routine</div>', unsafe_allow_html=True)
st.info("Coming soon.")