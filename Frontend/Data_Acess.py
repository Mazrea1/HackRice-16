"""
data_access.py

Thin bridge between the Streamlit frontend and the backend's logic.py, so
pages don't need to deal with import paths or reload the JSON file on
every rerun.
"""

import os
import sys

import streamlit as st

# Make Backend/ importable from any page in this Frontend/ folder
_BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Backend")
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from logic import load_exercises  # noqa: E402

_EXERCISES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "Data", "exercises.json"
)


@st.cache_data
def get_all_exercises():
    """Load and cache the full exercise catalog for the session."""
    return load_exercises(_EXERCISES_PATH)