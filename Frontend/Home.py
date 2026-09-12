"""
Home.py

Landing page for the app. Streamlit's multipage convention picks up any
files placed in a sibling `pages/` folder automatically -- this file is
the entry point, run with `streamlit run Home.py`.
"""

import streamlit as st

from Theme import inject_theme
from Nav import render_top_nav

st.set_page_config(
    page_title="ReRack",
    page_icon="🏋️",
    layout="wide",
)

inject_theme()
render_top_nav("Home")

# ---------------------------------------------------------------------------
# Hero-specific styles (only used on this page, so kept local rather than
# in the shared theme.py)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .hero-headline {
        font-family: 'Oswald', sans-serif;
        font-weight: 700;
        font-size: 4rem;
        line-height: 1.05;
        color: var(--chalk);
        margin-bottom: 1.2rem;
        max-width: 15ch;
    }

    .hero-sub {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--iron);
        max-width: 48ch;
        margin-bottom: 2rem;
    }

    .panel {
        padding: 1.8rem 1.6rem;
        height: 100%;
    }

    .panel-search {
        border-left: 3px solid var(--ember);
        background-color: var(--slate);
    }

    .panel-routine {
        border-top: 3px solid var(--iron);
        background-color: transparent;
    }

    .panel-title {
        font-family: 'Oswald', sans-serif;
        font-weight: 600;
        font-size: 1.5rem;
        color: var(--chalk);
        margin-bottom: 0.6rem;
    }

    .panel-body {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: var(--iron);
        line-height: 1.5;
    }

    .footnote {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: var(--iron);
        opacity: 0.6;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="hero-headline">Your Gym Backup Plan In Your Pocket</div>',
    unsafe_allow_html=True,
)

st.markdown(
    "<div class=\"hero-sub\">"
    "When the machine you need is taken, ReRack finds a free-weight or "
    "bodyweight move that hits the same muscle group -- so your workout "
    "never stalls waiting in line."
    "</div>",
    unsafe_allow_html=True,
)

st.button("Make your routine")

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Preview panels for the other two pages
# ---------------------------------------------------------------------------
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown(
        """
        <div class="panel panel-search">
            <div class="panel-title">Search Exercises</div>
            <div class="panel-body">
                Browse the full catalog by muscle group and equipment type,
                and see which free-weight or bodyweight move to reach for
                when a machine is already busy.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="panel panel-routine">
            <div class="panel-title">Your Routine</div>
            <div class="panel-body">
                Save exercises you like and pull up your list anytime
                you're back at the gym.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footnote">Built for HackRice 16</div>',
    unsafe_allow_html=True,
)