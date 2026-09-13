"""Saved workout routine page."""

import streamlit as st

from Theme import inject_theme
from Nav import render_top_nav
from Data_Acess import (
    find_replacement,
    generate_workout_plan,
    get_all_exercises,
    get_saved_exercises,
    remove_saved_exercise,
)
from Exercise_Card import render_exercise_card

st.set_page_config(page_title="ReRack — Routine", page_icon="📋", layout="wide")

inject_theme()
render_top_nav("Routine")

st.markdown('<div class="page-title">Your Routine</div>', unsafe_allow_html=True)

saved_exercises = get_saved_exercises()
all_exercises = get_all_exercises()

st.markdown("### Build a workout plan")
num_days = st.radio(
    "How many days should your plan have?",
    options=[3, 5],
    format_func=lambda days: f"{days} days",
    horizontal=True,
)

if st.button("Generate workout plan"):
    plan, message = generate_workout_plan(num_days, get_all_exercises())
    st.session_state["workout_plan"] = plan
    st.success(message)

workout_plan = st.session_state.get("workout_plan")
if workout_plan:
    st.markdown("### Your workout plan")
    for day in workout_plan:
        muscle_groups = ", ".join(day["muscle_groups"])
        with st.expander(f"Day {day['day']} — {muscle_groups}", expanded=True):
            if day["exercises"]:
                for exercise in day["exercises"]:
                    st.markdown(f"- {exercise['name']}")
            else:
                st.info("No exercises available for this day.")

with st.expander("Saved Workouts", expanded=False):
    if not saved_exercises:
        st.info("Save exercises from the Search page to build your routine.")
    else:
        st.markdown(
            f"{len(saved_exercises)} saved exercise"
            f"{'s' if len(saved_exercises) != 1 else ''}"
        )

        def find_exercise_replacement(exercise_id):
            return find_replacement(exercise_id, all_exercises)

        for exercise in saved_exercises:
            render_exercise_card(
                exercise,
                replacement_callback=find_exercise_replacement,
                expandable=False,
            )
            if st.button("Remove from routine", key=f"remove-{exercise['id']}"):
                _, message = remove_saved_exercise(exercise["id"])
                st.success(message)
                st.rerun()