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

from logic import (  # noqa: E402
    add_saved_exercise,
    delete_saved_exercise,
    load_exercises,
    load_saved_exercises,
)

_EXERCISES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "Data", "exercises.json"
)


@st.cache_data
def get_all_exercises():
    """Load and cache the full exercise catalog for the session."""
    return load_exercises(_EXERCISES_PATH)


def get_saved_exercises():
    """Load the exercises saved from the Search page."""
    return load_saved_exercises()


def save_exercise(exercise_id, exercises):
    """Save one catalog exercise for the user's routine."""
    return add_saved_exercise(exercise_id, exercises)


def remove_saved_exercise(exercise_id):
    """Remove one exercise from the user's routine."""
    return delete_saved_exercise(exercise_id)