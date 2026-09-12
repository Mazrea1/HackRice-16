"""Saved workout routine page."""

import streamlit as st

from Theme import inject_theme
from Nav import render_top_nav
from Data_Acess import get_saved_exercises, remove_saved_exercise
from Exercise_Card import render_exercise_card

st.set_page_config(page_title="ReRack — Routine", page_icon="📋", layout="wide")

inject_theme()
render_top_nav("Routine")

st.markdown('<div class="page-title">Your Routine</div>', unsafe_allow_html=True)

saved_exercises = get_saved_exercises()

with st.expander("Saved Workouts", expanded=False):
    if not saved_exercises:
        st.info("Save exercises from the Search page to build your routine.")
    else:
        st.markdown(
            f"{len(saved_exercises)} saved exercise"
            f"{'s' if len(saved_exercises) != 1 else ''}"
        )
        for exercise in saved_exercises:
            render_exercise_card(exercise, expandable=False)
            if st.button("Remove from routine", key=f"remove-{exercise['id']}"):
                _, message = remove_saved_exercise(exercise["id"])
                st.success(message)
                st.rerun()