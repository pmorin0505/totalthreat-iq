import streamlit as st

from config import APP_NAME, LOGO_PATH


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def initialize_database():
    from modules.database import init_db

    init_db()
    return True


def load_global_ui():
    from modules.ui_components import inject_css

    inject_css()


def render_sidebar():
    with st.sidebar:
        st.markdown("<div class='sidebar-logo-wrap'>", unsafe_allow_html=True)

        try:
            st.image(LOGO_PATH, use_container_width=True)
        except Exception:
            st.markdown("<div class='fallback-logo'>🛡️</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="sidebar-title-block">
                <div class="sidebar-title">TotalThreat IQ</div>
                <div class="sidebar-subtitle">Suspicious communication reasoning scanner</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            from streamlit_option_menu import option_menu

            page = option_menu(
                menu_title=None,
                options=[
                    "Analyze",
                    "Dashboard",
                    "Reports",
                    "History",
                    "Threat Intelligence",
                    "About / Responsible AI",
                ],
                icons=[
                    "search",
                    "speedometer2",
                    "file-earmark-text",
                    "clock-history",
                    "shield-lock",
                    "info-circle",
                ],
                default_index=0,
                styles={
                    "container": {
                        "padding": "16px 14px",
                        "background-color": "#07111f",
                        "border-radius": "0px",
                        "border": "1px solid #07111f",
                        "box-shadow": "none",
                    },
                    "icon": {
                        "color": "#7dd3fc",
                        "font-size": "18px",
                    },
                    "nav-link": {
                        "font-size": "15px",
                        "font-weight": "700",
                        "text-align": "left",
                        "margin": "10px 0px",
                        "padding": "15px 16px",
                        "border-radius": "16px",
                        "color": "#f8fafc",
                        "background-color": "#0f172a",
                        "border": "1px solid #1e293b",
                        "box-shadow": "0 4px 14px rgba(0, 0, 0, 0.22)",
                    },
                    "nav-link:hover": {
                        "background-color": "#132238",
                        "color": "#ffffff",
                        "border": "1px solid #334155",
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(90deg, #10243d 0%, #16385c 55%, #10243d 100%)",
                        "color": "#ffffff",
                        "border": "1px solid #38bdf8",
                        "box-shadow": "0 0 14px rgba(56, 189, 248, 0.16)",
                    },
                },
            )

        except Exception:
            page = st.radio(
                "Navigate",
                [
                    "Analyze",
                    "Dashboard",
                    "Reports",
                    "History",
                    "Threat Intelligence",
                    "About / Responsible AI",
                ],
                index=0,
                label_visibility="collapsed",
            )

        st.markdown(
            """
            <div class="sidebar-footer">
                <strong>Local MVP</strong><br>
                Pattern-based scanner<br>
                No malware execution
            </div>
            """,
            unsafe_allow_html=True,
        )

    return page


def render_page(page):
    if page == "Analyze":
        from pages import analyze

        analyze.render()

    elif page == "Dashboard":
        from pages import dashboard

        dashboard.render()

    elif page == "Reports":
        from pages import reports

        reports.render()

    elif page == "History":
        from pages import history

        history.render()

    elif page == "Threat Intelligence":
        from pages import threat_intel

        threat_intel.render()

    elif page == "About / Responsible AI":
        from pages import about

        about.render()


def main():
    initialize_database()
    load_global_ui()

    page = render_sidebar()
    render_page(page)

    from modules.ui_components import app_credit_footer

    app_credit_footer()


if __name__ == "__main__":
    main()
    