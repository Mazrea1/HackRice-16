"""
nav.py

Shared top navigation bar shown on every page (Home, Search, Routine).
Uses st.page_link, so clicking a link actually navigates -- unlike plain
markdown links, which can't trigger Streamlit's page routing.
"""

import streamlit as st

NAV_CSS = """
<style>
.navbar-brand {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: var(--chalk);
    font-size: 1rem;
    padding-top: 0.4rem;
}

div[data-testid="stPageLink"] a {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: var(--iron) !important;
}

div[data-testid="stPageLink"] a:hover {
    color: var(--chalk) !important;
}

div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
    border-bottom: 1px solid #2A2F34;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}
</style>
"""


def render_top_nav(active: str) -> None:
    """
    Render the horizontal top nav bar with links to every page.

    active: label of the current page (e.g. "Home", "Search", "Routine").
    Currently used only if you want to add a visual "you are here" cue
    later -- pass it in from every page now so that's a one-line change
    when you do.
    """
    st.markdown(NAV_CSS, unsafe_allow_html=True)

    brand_col, home_col, search_col, routine_col = st.columns([3, 1, 1, 1])

    with brand_col:
        st.markdown('<div class="navbar-brand">RERACK</div>', unsafe_allow_html=True)
    with home_col:
        st.page_link("Home.py", label="Home", icon="🏠")
    with search_col:
        st.page_link("pages/Search.py", label="Search", icon="🔍")
    with routine_col:
        st.page_link("pages/Routine.py", label="Routine", icon="📋")
