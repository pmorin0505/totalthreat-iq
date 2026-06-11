import streamlit as st

from config import RISK_COLORS


def inject_css():
    st.markdown(
        """
        <style>
        /* Hide Streamlit's automatic multipage navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Main app background */
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.25), transparent 35%),
                radial-gradient(circle at top right, rgba(239, 68, 68, 0.18), transparent 30%),
                linear-gradient(135deg, #071221 0%, #0f172a 55%, #111827 100%);
            color: #f8fafc;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #07111f 0%, #0b1220 100%);
            border-right: 1px solid #1f2a44;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1rem;
        }

        /* Logo */
        .sidebar-logo-wrap {
            margin-top: -0.5rem;
            margin-bottom: 0.5rem;
            text-align: center;
        }

        .sidebar-logo-wrap img {
            max-height: 115px;
            object-fit: contain;
            margin-bottom: 0.25rem;
        }

        .fallback-logo {
            font-size: 3rem;
            text-align: center;
        }

        .sidebar-title-block {
            margin-bottom: 1.25rem;
            padding: 0.75rem 0.65rem 1rem 0.65rem;
            border-bottom: 1px solid #1f2937;
        }

        .sidebar-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.2px;
        }

        .sidebar-subtitle {
            font-size: 0.78rem;
            color: #93c5fd;
            margin-top: 0.25rem;
            line-height: 1.2rem;
        }

        .sidebar-footer {
            margin-top: 1.2rem;
            padding: 0.9rem;
            border-radius: 14px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid #243047;
            color: #94a3b8;
            font-size: 0.8rem;
            line-height: 1.3rem;
        }

        /* Main content */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* Cards */
        .metric-card {
            background: linear-gradient(180deg, #111827 0%, #0b1220 100%);
            border: 1px solid #263249;
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.28);
        }

        .metric-card:hover {
            border-color: #3b82f6;
            transform: translateY(-1px);
            transition: 0.18s ease-in-out;
        }

        .result-card {
            background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
            border: 1px solid #263249;
            border-radius: 16px;
            padding: 16px;
            margin: 10px 0;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
        }

        .profile-card {
            background:
                radial-gradient(circle at top right, rgba(37, 99, 235, 0.22), transparent 35%),
                linear-gradient(180deg, #111827 0%, #0b1220 100%);
            border: 1px solid #334155;
            border-radius: 20px;
            padding: 24px;
            margin: 16px 0;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.32);
        }

        .profile-card h2 {
            margin-top: 0;
            color: #ffffff;
        }

        .profile-card p {
            color: #d1d5db;
            line-height: 1.65rem;
            font-size: 1rem;
        }

        .profile-link-row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 18px;
        }

        .profile-link {
            display: inline-block;
            padding: 10px 14px;
            border-radius: 999px;
            background: linear-gradient(90deg, #1d4ed8 0%, #7c3aed 100%);
            color: white !important;
            text-decoration: none !important;
            font-weight: 700;
            border: 1px solid #60a5fa;
        }

        .profile-link:hover {
            filter: brightness(1.12);
        }

        .small-muted {
            color: #94a3b8;
            font-size: 0.9rem;
        }

        .disclaimer {
            background: rgba(23, 32, 51, 0.95);
            border-left: 4px solid #38bdf8;
            padding: 12px 16px;
            border-radius: 12px;
            color: #dbeafe;
            line-height: 1.45rem;
        }

        /* Buttons */
        div.stButton > button {
            border-radius: 12px;
            border: 1px solid #334155;
            background: linear-gradient(90deg, #1d4ed8 0%, #7c3aed 100%);
            color: white;
            font-weight: 700;
            padding: 0.65rem 1rem;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.22);
        }

        div.stButton > button:hover {
            border-color: #93c5fd;
            filter: brightness(1.08);
            transform: translateY(-1px);
        }

        /* Inputs */
        textarea, input, select {
            border-radius: 10px !important;
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #1f2937;
        }

        h1, h2, h3 {
            color: #ffffff;
        }

        /* Fixed creator credit in bottom-right corner */
        .creator-credit {
            position: fixed;
            right: 18px;
            bottom: 14px;
            z-index: 9999;
            background: rgba(3, 7, 18, 0.88);
            border: 1px solid rgba(96, 165, 250, 0.35);
            color: #64748b;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.2px;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(8px);
        }

        .creator-credit a {
            color: #64748b !important;
            text-decoration: none !important;
        }

        .creator-credit a:hover {
            color: #93c5fd !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def app_credit_footer():
    st.markdown(
        """
        <div class="creator-credit">
            Built by <a href="https://github.com/pmorin0505" target="_blank">Paul Morin</a> • @pmorin0505
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_badge(risk):
    color = RISK_COLORS.get(risk, "#64748b")
    st.markdown(
        f"""
        <span style="
            background:{color};
            color:white;
            padding:6px 12px;
            border-radius:999px;
            font-weight:700;
            display:inline-block;
        ">
            {risk}
        </span>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, help_text=""):
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='small-muted'>{label}</div>
            <h2 style='margin:0.25rem 0;color:white'>{value}</h2>
            <div class='small-muted'>{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def result_card(title, body):
    st.markdown(
        f"""
        <div class='result-card'>
            <h4 style='margin-top:0;color:white'>{title}</h4>
            <p style='color:#d1d5db'>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def disclaimer_box(text):
    st.markdown(
        f"<div class='disclaimer'>{text}</div>",
        unsafe_allow_html=True,
    )
    