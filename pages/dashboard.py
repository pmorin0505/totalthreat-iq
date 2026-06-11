import json
from collections import Counter

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from modules.database import fetch_history
from modules.ui_components import metric_card, disclaimer_box


RISK_ORDER = ["Low", "Medium", "High", "Critical"]

RISK_COLORS = {
    "Low": "#22c55e",       # green
    "Medium": "#eab308",    # yellow
    "High": "#f97316",      # orange
    "Critical": "#ef4444",  # red
}

SIGNAL_COLORS = [
    "#ef4444",  # red
    "#f97316",  # orange
    "#eab308",  # yellow
    "#22c55e",  # green
    "#ef4444",
    "#f97316",
    "#eab308",
    "#22c55e",
    "#ef4444",
    "#f97316",
]


def _load_history_dataframe():
    rows = fetch_history()

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    if "threat_score" in df.columns:
        df["threat_score"] = pd.to_numeric(df["threat_score"], errors="coerce").fillna(0)

    return df


def _extract_signal_counts(df):
    signal_counter = Counter()

    if df.empty or "detected_signals" not in df.columns:
        return signal_counter

    for value in df["detected_signals"].dropna():
        try:
            parsed = json.loads(value)

            if isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict):
                        signal_name = (
                            item.get("signal")
                            or item.get("name")
                            or item.get("Signal")
                            or "Unknown Signal"
                        )
                        signal_counter[signal_name] += 1
                    else:
                        signal_counter[str(item)] += 1
            else:
                signal_counter[str(parsed)] += 1

        except Exception:
            parts = [x.strip() for x in str(value).split(",") if x.strip()]
            for part in parts:
                signal_counter[part] += 1

    return signal_counter


def _risk_distribution_chart(df):
    counts = (
        df["risk_level"]
        .value_counts()
        .reindex(RISK_ORDER, fill_value=0)
        .reset_index()
    )
    counts.columns = ["Risk Level", "Count"]

    counts = counts[counts["Count"] > 0]

    fig = px.pie(
        counts,
        names="Risk Level",
        values="Count",
        title="Risk Distribution",
        color="Risk Level",
        color_discrete_map=RISK_COLORS,
        category_orders={"Risk Level": RISK_ORDER},
        hole=0.35,
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title=dict(font=dict(size=20)),
        margin=dict(l=20, r=20, t=55, b=20),
        height=420,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=13),
        ),
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        marker=dict(
            line=dict(color="#0f172a", width=2)
        ),
        pull=[0.03 if risk in ["High", "Critical"] else 0 for risk in counts["Risk Level"]],
    )

    return fig


def _score_gauge(avg_score):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_score,
            number={"suffix": "/100"},
            title={"text": "Average Threat Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#e5e7eb"},
                "steps": [
                    {"range": [0, 24], "color": "#22c55e"},
                    {"range": [25, 49], "color": "#eab308"},
                    {"range": [50, 74], "color": "#f97316"},
                    {"range": [75, 100], "color": "#ef4444"},
                ],
                "threshold": {
                    "line": {"color": "#ffffff", "width": 4},
                    "thickness": 0.75,
                    "value": avg_score,
                },
            },
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        margin=dict(l=20, r=20, t=45, b=20),
        height=420,
    )

    return fig


def _common_signals_chart(signal_counter):
    if not signal_counter:
        return None

    common = signal_counter.most_common(10)
    chart_df = pd.DataFrame(common, columns=["Signal", "Count"])

    colors = SIGNAL_COLORS[: len(chart_df)]

    fig = go.Figure(
        data=[
            go.Bar(
                x=chart_df["Signal"],
                y=chart_df["Count"],
                text=chart_df["Count"],
                textposition="outside",
                marker=dict(
                    color=colors,
                    line=dict(color="#111827", width=1),
                ),
            )
        ]
    )

    fig.update_layout(
        title="Common Threat Signals",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=20),
        margin=dict(l=20, r=20, t=55, b=120),
        height=420,
        xaxis=dict(
            title="Signal",
            tickangle=35,
            gridcolor="rgba(148, 163, 184, 0.22)",
        ),
        yaxis=dict(
            title="Count",
            gridcolor="rgba(148, 163, 184, 0.22)",
        ),
        showlegend=False,
    )

    return fig


def render():
    st.title("TotalThreat IQ Dashboard")
    st.caption("Local cybersecurity reasoning dashboard for suspicious communication analysis.")

    df = _load_history_dataframe()

    if df.empty:
        st.markdown(
            """
            <div class="result-card">
                <h3 style="margin-top:0;">No scans yet</h3>
                <p style="color:#d1d5db;">
                    Run a few demo scans from the Analyze page first. Once scans are saved,
                    this dashboard will show risk distribution, average threat score,
                    common threat signals, and recent scan history.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        disclaimer_box(
            "TotalThreat IQ uses fictional demo data and pattern-based analysis. "
            "It does not guarantee that a message is safe or malicious."
        )
        return

    total_scans = len(df)
    high_critical = df[df["risk_level"].isin(["High", "Critical"])].shape[0]

    if "threat_score" in df.columns:
        avg_score = round(df["threat_score"].mean(), 1)
    else:
        avg_score = 0

    if "timestamp" in df.columns:
        last_scan = df.sort_values("timestamp", ascending=False).iloc[0]
    else:
        last_scan = df.iloc[-1]

    signal_counter = _extract_signal_counts(df)
    most_common_signal = signal_counter.most_common(1)[0][0] if signal_counter else "None detected"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Scans", total_scans, "Saved locally in SQLite")

    with col2:
        metric_card("High / Critical", high_critical, "Scans needing attention")

    with col3:
        metric_card("Average Score", f"{avg_score}/100", "Average threat score")

    with col4:
        metric_card("Top Signal", most_common_signal, "Most frequent indicator")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.plotly_chart(_risk_distribution_chart(df), use_container_width=True)

    with right:
        signal_fig = _common_signals_chart(signal_counter)
        if signal_fig:
            st.plotly_chart(signal_fig, use_container_width=True)
        else:
            st.markdown(
                """
                <div class="result-card">
                    <h3 style="margin-top:0;">No threat signals yet</h3>
                    <p style="color:#d1d5db;">
                        Run more scans to populate the common threat signals chart.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.plotly_chart(_score_gauge(avg_score), use_container_width=True)

    st.subheader("Recent Scan History")

    recent_cols = [
        "timestamp",
        "input_type",
        "message_preview",
        "risk_level",
        "threat_score",
        "threat_category",
    ]

    available_cols = [col for col in recent_cols if col in df.columns]

    if "timestamp" in df.columns:
        recent_df = (
            df.sort_values("timestamp", ascending=False)
            .head(10)[available_cols]
            .copy()
        )
    else:
        recent_df = df.head(10)[available_cols].copy()

    st.dataframe(recent_df, use_container_width=True, hide_index=True)

    st.subheader("Latest Scan Summary")

    latest_risk = last_scan.get("risk_level", "Unknown")
    latest_score = last_scan.get("threat_score", 0)
    latest_category = last_scan.get("threat_category", "Unknown")
    latest_preview = last_scan.get("message_preview", "")

    latest_color = RISK_COLORS.get(latest_risk, "#64748b")

    st.markdown(
        f"""
        <div class="result-card" style="border-left: 5px solid {latest_color};">
            <h3 style="margin-top:0; color:white;">
                {latest_risk} Risk • Score {latest_score}/100
            </h3>
            <p style="color:#d1d5db;">
                <strong>Category:</strong> {latest_category}
            </p>
            <p style="color:#d1d5db;">
                <strong>Preview:</strong> {latest_preview}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    disclaimer_box(
        "Dashboard results are based on local pattern detection and saved scan history. "
        "Verify suspicious messages through official channels and follow organization security policies."
    )
    