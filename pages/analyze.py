import math

import streamlit as st

from config import DISCLAIMER
from modules.analyzer import analyze_message
from modules.database import save_scan
from modules.demo_data import load_samples
from modules.foundry_client import generate_foundry_iq_summary
from modules.report_generator import report_json, report_text
from modules.ui_components import disclaimer_box, result_card, risk_badge


def clean_optional_value(value):
    """
    Prevents pandas demo data blanks from showing as 'nan' in the app.
    """
    if value is None:
        return ""

    if isinstance(value, float) and math.isnan(value):
        return ""

    value = str(value)

    if value.lower() == "nan":
        return ""

    return value


def enrich_with_foundry(result):
    """
    Adds the Foundry IQ / Microsoft IQ summary to every scan result.
    """
    result["foundry_iq"] = generate_foundry_iq_summary(result)
    return result


def render_result(result):
    st.subheader("Analysis Result")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Threat Score", f"{result['threat_score']}/100")
    c2.metric("Signals", len(result["detected_signals"]))
    c3.metric("Category", result["threat_category"])
    c4.metric("Confidence", result["confidence_level"])

    risk_badge(result["risk_level"])
    st.write("")

    with st.expander("Detected Threat Signals", expanded=True):
        if result["detected_signals"]:
            for signal in result["detected_signals"]:
                st.markdown(
                    f"- **{signal.get('name')}** (+{signal.get('weight')}): "
                    f"{signal.get('detail', '')}"
                )
        else:
            st.write("No major indicators detected by current rules.")

    result_card("Reasoning Summary", result["reasoning_summary"])
    result_card("Plain-English Explanation", result["plain_english_explanation"])
    result_card("Recommended Action", result["recommended_action"])

    foundry = result.get("foundry_iq", {})

    st.markdown(
        f"""
        <div class="result-card" style="border-left: 5px solid #38bdf8;">
            <h3 style="margin-top:0;">Foundry IQ / Microsoft IQ Summary</h3>
            <p style="color:#93c5fd;">
                <strong>Mode:</strong> {foundry.get("mode", "Not generated")}
            </p>
            <p style="color:#d1d5db; line-height:1.6rem;">
                {foundry.get("summary", "No Foundry IQ summary available.")}
            </p>
            <p style="color:#94a3b8;">
                <strong>Knowledge Source:</strong> {foundry.get("knowledge_source", "Not provided")}
            </p>
            <p style="color:#94a3b8;">
                {foundry.get("note", "")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("URL / Domain Details"):
        for url_result in result["url_results"] or []:
            st.json(url_result)

        if not result["url_results"]:
            st.write("No URLs detected.")

    with st.expander("Attachment Name Details"):
        for attachment_result in result["attachment_results"] or []:
            st.json(attachment_result)

        if not result["attachment_results"]:
            st.write("No attachment names analyzed.")

    txt = report_text(result)
    js = report_json(result)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download TXT Report",
            txt,
            file_name="totalthreat_report.txt",
        )

    with col2:
        st.download_button(
            "Download JSON Report",
            js,
            file_name="totalthreat_report.json",
        )

    st.text_area(
        "Copyable Security Report Summary",
        txt,
        height=360,
    )


def analyze_and_save(input_type, sender, subject, body, attachment):
    sender = clean_optional_value(sender)
    subject = clean_optional_value(subject)
    body = clean_optional_value(body)
    attachment = clean_optional_value(attachment)

    result = analyze_message(input_type, sender, subject, body, attachment)
    result = enrich_with_foundry(result)
    result["scan_id"] = save_scan(result)
    return result


def render():
    st.title("Analyze Suspicious Communication")

    st.caption(
        "Scan suspicious emails, messages, links, domains, and attachment names using "
        "local reasoning plus a Foundry IQ-ready grounded summary layer."
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Analyze Message",
            "Link / Domain Analyzer",
            "Attachment Name Analyzer",
            "Full Threat Scan",
        ]
    )

    samples = load_samples()

    with tab1:
        demo_label = None

        if not samples.empty:
            demo_label = st.selectbox(
                "Load demo example",
                ["None"] + samples["Subject"].astype(str).tolist(),
            )

        defaults = {}

        if demo_label and demo_label != "None":
            defaults = (
                samples[samples["Subject"].astype(str) == demo_label]
                .iloc[0]
                .to_dict()
            )

        input_type = st.selectbox(
            "Message Type",
            [
                "Email",
                "Text message",
                "Chat / DM",
                "Link only",
                "Mixed content",
            ],
        )

        sender = st.text_input(
            "Sender (optional)",
            value=clean_optional_value(defaults.get("Sender Email / Handle", "")) if defaults else "",
        )

        subject = st.text_input(
            "Subject (optional)",
            value=clean_optional_value(defaults.get("Subject", "")) if defaults else "",
        )

        body = st.text_area(
            "Message Body",
            value=clean_optional_value(defaults.get("Message Body", "")) if defaults else "",
            height=190,
        )

        attachment = st.text_input(
            "Attachment Name(s), optional",
            value=clean_optional_value(defaults.get("Attachment Name", "")) if defaults else "",
        )

        if st.button("Analyze Message", type="primary"):
            result = analyze_and_save(input_type, sender, subject, body, attachment)
            st.success(f"Scan saved to local history as ID {result['scan_id']}.")
            render_result(result)

    with tab2:
        urltext = st.text_area(
            "Paste URL, domain, or message containing URLs",
            height=160,
            key="urltext",
        )

        if st.button("Analyze Link / Domain"):
            result = analyze_and_save("Link only", "", "", urltext, "")
            st.success(f"Scan saved to local history as ID {result['scan_id']}.")
            render_result(result)

    with tab3:
        names = st.text_area(
            "Enter one or more attachment names",
            "invoice.pdf.exe\npayroll_update.zip\nbenefits_form.docm",
            height=160,
        )

        if st.button("Analyze Attachment Name"):
            result = analyze_and_save(
                "Attachment name",
                "",
                "",
                "Attachment filename review",
                names,
            )

            st.success(f"Scan saved to local history as ID {result['scan_id']}.")
            render_result(result)

            disclaimer_box(
                "TotalThreat IQ does not open, execute, sandbox, or deeply scan files. "
                "It only checks filenames and metadata-style indicators."
            )

    with tab4:
        full = st.text_area(
            "Paste full communication",
            height=220,
            key="fullscan",
        )

        full_att = st.text_input("Attachment names for full scan")

        if st.button("Run Full Threat Scan"):
            result = analyze_and_save(
                "Full Threat Scan",
                "",
                "",
                full,
                full_att,
            )

            cats = {
                "Message Scan": len(
                    [s for s in result["detected_signals"] if not s.get("source")]
                ),
                "URL / Domain Scan": len(result["url_results"]),
                "Attachment Scan": len(result["attachment_results"]),
                "Overall Scan": len(result["detected_signals"]),
            }

            for name, count in cats.items():
                result_card(
                    name,
                    f'{count} finding(s) or item(s) reviewed. Overall risk: {result["risk_level"]}.',
                )

            st.success(f"Scan saved to local history as ID {result['scan_id']}.")
            render_result(result)

    disclaimer_box(DISCLAIMER)
    