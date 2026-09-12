"""
pages/1_Search.py

Search Exercises page: filter the catalog by muscle group and equipment
type, then browse results as expandable cards.
"""

import streamlit as st

from Theme import inject_theme
from Nav import render_top_nav
from Data_Acess import get_all_exercises, save_exercise
from Exercise_Card import render_exercise_card

st.set_page_config(page_title="ReRack — Search", page_icon="🔍", layout="wide")

inject_theme()
render_top_nav("Search")

st.markdown('<div class="page-title">Search Exercises</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-sub">Filter by muscle group and equipment to find your next move.</div>',
    unsafe_allow_html=True,
)

exercises = get_all_exercises()

# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------
muscle_groups = sorted({ex["muscle_group"] for ex in exercises if ex.get("muscle_group")})

filter_col1, filter_col2 = st.columns([2, 1])

with filter_col1:
    selected_groups = st.multiselect(
        "Muscle group",
        options=muscle_groups,
        placeholder="All muscle groups",
    )

with filter_col2:
    equipment_filter = st.selectbox(
        "Equipment",
        options=["All", "Machine only", "Free weight / Bodyweight only"],
    )

filtered = exercises

if selected_groups:
    filtered = [ex for ex in filtered if ex.get("muscle_group") in selected_groups]

if equipment_filter == "Machine only":
    filtered = [ex for ex in filtered if ex.get("is_machine")]
elif equipment_filter == "Free weight / Bodyweight only":
    filtered = [ex for ex in filtered if not ex.get("is_machine")]

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
count_label = f'{len(filtered)} exercise{"s" if len(filtered) != 1 else ""}'
st.markdown(f'<div class="result-count">{count_label}</div>', unsafe_allow_html=True)

if not filtered:
    st.info("No exercises match those filters.")
else:
    def save_to_routine(exercise_id):
        _, message = save_exercise(exercise_id, exercises)
        return message

    for exercise in filtered:
        render_exercise_card(
            exercise,
            action_label="Save to routine",
            action_key=f"save-{exercise['id']}",
            action_callback=save_to_routine,
        )