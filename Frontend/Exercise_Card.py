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

from io import BytesIO
from typing import Any, Callable, Dict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image, UnidentifiedImageError
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


@st.cache_data(show_spinner=False)
def _fetch_image(url: str) -> bytes | None:
    """Download and validate an exercise image, returning None if unavailable."""
    if not url or url.strip().upper() == "N/A":
        return None

    try:
        request = Request(url, headers={"User-Agent": "ReRack"})
        with urlopen(request, timeout=10) as response:
            image_data = response.read()

        with Image.open(BytesIO(image_data)) as image:
            image.verify()

        return image_data
    except (HTTPError, URLError, TimeoutError, UnidentifiedImageError, OSError, ValueError):
        return None


def _render_image(url: Any, caption: str) -> None:
    """Render an image or a clear fallback when its URL cannot be loaded."""
    if not isinstance(url, str):
        image_data = None
    else:
        image_data = _fetch_image(url.strip())

    if image_data is None:
        st.caption(f"{caption}: Image not available")
    else:
        st.image(image_data, caption=caption, use_container_width=True)


def _render_images(exercise: Dict[str, Any]) -> None:
    """Show the exercise's starting and ending positions side by side."""
    start_image_url = exercise.get("start_image_url")
    end_image_url = exercise.get("end_image_url")

    start_col, end_col = st.columns(2)

    with start_col:
        _render_image(start_image_url, "Starting position")

    with end_col:
        _render_image(end_image_url, "Ending position")


def render_exercise_card(
    exercise: Dict[str, Any],
    action_label: str | None = None,
    action_key: str | None = None,
    action_callback: Callable[[str], str] | None = None,
    expandable: bool = True,
) -> None:
    """
    Render one exercise as a collapsed row (name + short tag line) that
    expands to show the full explanation.
    """
    tag_line = f'{exercise.get("equipment", "")} • {exercise.get("muscle_group", "")}'
    label = f'{exercise.get("name", "Unnamed exercise")}  —  {tag_line}'

    def render_contents() -> None:
        _render_description(exercise)
        _render_images(exercise)
        _render_video(exercise)  # no-op until exercises have a video_url
        if action_label and action_key and action_callback:
            if st.button(action_label, key=action_key):
                st.success(action_callback(exercise["id"]))

    if expandable:
        with st.expander(label):
            render_contents()
    else:
        st.markdown(f"**{label}**")
        render_contents()