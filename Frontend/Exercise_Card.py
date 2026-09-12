"""
exercise_card.py

Renders a single exercise as an expandable card: name + short tag line
collapsed, full explanation when expanded. Built to be reused anywhere an
exercise needs to be shown -- the Search page today, the Routine page
next.

WHY IT'S SPLIT INTO SMALL _render_x() FUNCTIONS:
Each piece of the expanded content (description, video, etc.) has its own
function. render_exercise_card() just calls them in order. To add a new
piece later -- e.g. a demo video once exercises have a `video_url` field --
write a new _render_x() function and add one line calling it. Nothing
else about the card needs to change.
"""

from typing import Any, Dict

import streamlit as st


def _render_description(exercise: Dict[str, Any]) -> None:
    """The exercise's full written explanation."""
    st.markdown(
        f'<div class="exercise-detail-text">{exercise.get("instructions", "")}</div>',
        unsafe_allow_html=True,
    )


def _render_video(exercise: Dict[str, Any]) -> None:
    """
    Placeholder for a future demo video. Renders nothing today. Once an
    exercise dict has a `video_url` field, this will embed it automatically
    -- no changes needed anywhere else.
    """
    video_url = exercise.get("video_url")
    if video_url:
        st.video(video_url)


def render_exercise_card(exercise: Dict[str, Any]) -> None:
    """
    Render one exercise as a collapsed row (name + short tag line) that
    expands to show the full explanation.
    """
    tag_line = f'{exercise.get("equipment", "")} • {exercise.get("muscle_group", "")}'
    label = f'{exercise.get("name", "Unnamed exercise")}  —  {tag_line}'

    with st.expander(label):
        _render_description(exercise)
        _render_video(exercise)  # no-op until exercises have a video_url