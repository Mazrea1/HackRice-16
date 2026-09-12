"""
theme.py

Shared design tokens and global CSS for the ReRack app. Import and call
inject_theme() once near the top of every page so Home, Search, and
Routine all look consistent instead of each page redefining its own
fonts and colors.
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Inter:wght@400;500&display=swap');

:root {
    --graphite: #14171A;
    --slate: #1E2226;
    --chalk: #F5F3EE;
    --iron: #9AA0A6;
    --ember: #FF5A36;
}

#MainMenu, footer {visibility: hidden;}

.stApp {
    background-color: var(--graphite);
}

.block-container {
    padding-top: 2.5rem;
    max-width: 1100px;
}

/* -- Buttons -- */
div[data-testid="stButton"] > button {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    background-color: var(--ember);
    color: var(--graphite);
    border: none;
    border-radius: 3px;
    padding: 0.6rem 1.6rem;
    font-size: 1rem;
}

div[data-testid="stButton"] > button:hover {
    background-color: #ff7654;
    color: var(--graphite);
}

/* -- Page headers (used on Search / Routine) -- */
.page-title {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 2.2rem;
    color: var(--chalk);
    margin-bottom: 0.4rem;
}

.page-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: var(--iron);
    margin-bottom: 1.5rem;
}

.result-count {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--iron);
    margin: 0.5rem 0 1rem 0;
}

/* -- Exercise cards (expanders) -- */
div[data-testid="stExpander"] {
    background-color: var(--slate);
    border: 1px solid #2A2F34;
    border-radius: 3px;
    margin-bottom: 0.6rem;
}

div[data-testid="stExpander"] summary {
    font-family: 'Inter', sans-serif;
    color: var(--chalk) !important;
    font-weight: 500;
}

.exercise-detail-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: var(--iron);
    line-height: 1.6;
    padding-top: 0.4rem;
}
</style>
"""


def inject_theme() -> None:
    """Inject the shared font/color CSS. Call once near the top of each page."""
    st.markdown(CSS, unsafe_allow_html=True)