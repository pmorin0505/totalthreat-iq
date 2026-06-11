import streamlit as st

from modules.ui_components import disclaimer_box, result_card


def render():
    st.title("About TotalThreat IQ")
    st.caption("Microsoft Agents League Hackathon / Microsoft AI Fest • Reasoning Agents • Foundry IQ Direction")
st.markdown(
    """
    **TotalThreat IQ** is a cybersecurity reasoning app that analyzes suspicious emails, messages,
    links, domains, and attachment names. It looks for common phishing and social engineering warning
    signs, assigns a threat score, explains the findings, recommends safe next steps, saves scan history,
    and generates downloadable reports.

    I built this project for the **Microsoft Agents League Hackathon / Microsoft AI Fest** under the
    **Reasoning Agents** track. The goal was to create a practical tool that reviews multiple risk signals
    instead of relying on one keyword or one indicator.
    """
)

st.header("Project Identity")

col1, col2, col3 = st.columns(3)

with col1:
    result_card(
        "Hackathon Track",
        "Reasoning Agents — the app reviews multiple signals, scores risk, explains findings, and recommends safe next steps.",
    )

with col2:
    result_card(
        "Microsoft IQ Direction",
        "Foundry IQ / Microsoft Foundry — the app includes a Foundry IQ-ready grounding layer and an optional Azure configuration path.",
    )

with col3:
    result_card(
        "Project Type",
        "Streamlit cybersecurity app built with Python, SQLite, CSV data, Plotly charts, and a structured analysis engine.",
    )

st.header("What the App Scans")

st.markdown(
    """
    TotalThreat IQ can review:

    - Suspicious emails
    - Text messages
    - Chat or DM messages
    - Links and domains
    - Attachment names
    - Mixed suspicious communication
    """
)

st.header("How the App Works")

st.markdown(
    """
    TotalThreat IQ follows a structured analysis process:

    1. The user enters a suspicious message, link, domain, or attachment name.
    2. The app extracts useful details such as URLs, sender context, domains, and filenames.
    3. The scanner checks for phishing, impersonation, social engineering, and attachment-risk indicators.
    4. Weighted rules are applied to calculate a threat score.
    5. The result is classified as Low, Medium, High, or Critical.
    6. The app explains which signals were detected and why they matter.
    7. A recommended safe action is provided.
    8. The result can be saved, reviewed in history, shown on the dashboard, or downloaded as a report.
    """
)

st.header("Main Features")

st.markdown(
    """
    - Suspicious message scanner
    - Link and domain analyzer
    - Attachment name analyzer
    - Full threat scan mode
    - Weighted threat scoring system
    - Risk levels: Low, Medium, High, Critical
    - Threat category classification
    - Plain-English explanation
    - Recommended safe action
    - Foundry IQ / Microsoft IQ-style summary
    - Dashboard charts and metrics
    - Scan history
    - Downloadable TXT report
    - Downloadable JSON report
    - Responsible-use and safety disclaimers
    - Fictional demo examples
    """
)

st.header("Foundry IQ Integration Approach")

st.markdown(
    """
    TotalThreat IQ includes a **Foundry IQ-ready grounding layer**.

    The current version runs locally and uses a built-in cybersecurity knowledge pack to produce
    analyst-style summaries from structured scan findings. This mirrors the Foundry IQ pattern of
    grounding responses in organized knowledge sources.

    The current version includes:

    - A local cybersecurity grounding knowledge pack
    - A Foundry IQ / Microsoft IQ-style summary in scan results
    - A dedicated Foundry IQ Integration page
    - Optional Azure / Microsoft Foundry environment variable configuration
    - Documentation for how a future cloud-connected version could work

    A full cloud version could connect this workflow to a Microsoft Foundry Agent and a Foundry IQ
    knowledge base backed by Azure AI Search.
    """
)

st.header("Azure / Foundry Access Note")

st.markdown(
    """
    I attempted to configure Azure / Microsoft Foundry access using both a personal Microsoft account
    and a school account. During setup, Azure repeatedly returned this access error:
    """
)

st.code(
    "AADSTS53003: Access has been blocked by Conditional Access policies.",
    language="text",
)

st.markdown(
    """
    This appeared to be related to account or tenant access restrictions during sign-in or token retrieval.
    Because of that, I could not complete a live Azure Foundry deployment before submission.

    Instead of stopping there, I finished the working local app and built the project so it has a clear
    path for future Foundry / Azure integration when access is available. The current version is still
    demo-ready, organized, and safe to test with fictional examples.
    """
)

st.header("Risk Scoring")

st.markdown(
    """
    TotalThreat IQ uses weighted scoring rules. Scores are capped at 100.

    | Signal | Weight |
    |---|---:|
    | Urgency or pressure | +15 |
    | Credential request | +25 |
    | MFA code request | +25 |
    | Suspicious link | +20 |
    | Brand impersonation | +15 |
    | Account shutdown threat | +20 |
    | Payment or banking request | +20 |
    | Gift card request | +20 |
    | Dangerous attachment extension | +25 |
    | Macro-enabled Office file | +20 |
    | Double extension | +25 |
    | HTTP link | +10 |
    | Shortened URL | +15 |
    | IP-based URL | +20 |
    """
)

st.markdown(
    """
    | Score Range | Risk Level |
    |---:|---|
    | 0-24 | Low |
    | 25-49 | Medium |
    | 50-74 | High |
    | 75-100 | Critical |
    """
)

st.header("Threat Categories")

st.markdown(
    """
    TotalThreat IQ can classify scans into categories such as:

    - Credential phishing
    - MFA code theft
    - Business email compromise
    - Invoice or payment scam
    - Payroll scam
    - Gift card scam
    - Malware delivery attempt
    - Fake job scam
    - Package delivery scam
    - Brand impersonation
    - General social engineering
    - Low-confidence suspicious message
    """
)

st.header("Technology Stack")

st.markdown(
    """
    - Python
    - Streamlit
    - SQLite
    - Pandas
    - Plotly
    - CSV / Excel data layer
    - Local rule-based cybersecurity analysis
    - Foundry IQ-ready grounding layer
    - Optional Azure / Microsoft Foundry configuration
    """
)

st.header("Optional Azure / Microsoft Foundry Configuration")

st.markdown(
    """
    The local app runs without Azure credentials. For a future connected deployment, a `.env`
    file can be added to the project root with Azure / Microsoft Foundry values.
    """
)

st.code(
    """

AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini

FOUNDRY_PROJECT_ENDPOINT=https://your-ai-services-account-name.services.ai.azure.com/api/projects/your-project-name
FOUNDRY_IQ_KNOWLEDGE_BASE=totalthreat-cybersecurity-knowledge-base
""".strip(),
language="text",
)

disclaimer_box(
    "Do not upload .env files, API keys, access tokens, secrets, or credentials to GitHub."
)

st.header("Responsible Use and Safety")

disclaimer_box(
    "TotalThreat IQ is an educational cybersecurity awareness and reasoning tool. "
    "It does not guarantee that a message is safe or malicious. Users should verify suspicious messages "
    "through official channels and follow their organization's security policies."
)

st.markdown("")

disclaimer_box(
    "This project uses fictional and synthetic examples only. No employer, customer, employee, confidential, "
    "or real organizational data was used."
)

st.markdown("")

disclaimer_box(
    "The public Streamlit demo is a shared demo environment. Do not enter confidential, personal, work, "
    "customer, employee, financial, or sensitive information."
)

st.markdown(
    """
    TotalThreat IQ does **not**:

    - Execute files
    - Open attachments
    - Sandbox malware
    - Scan real malware
    - Claim certainty
    - Replace professional security review

    The app uses careful wording such as:

    - "This message may be suspicious because..."
    - "Risk appears low based on detected indicators."
    - "Verify through official channels."
    """
)

st.header("Demo Flow")

st.markdown(
    """
    1. Open TotalThreat IQ.
    2. View the dashboard.
    3. Go to Analyze.
    4. Load the fake Microsoft password reset example.
    5. Run the scan.
    6. Review the risk score and detected threat signals.
    7. Review the reasoning summary.
    8. Show the Foundry IQ / Microsoft IQ-style summary.
    9. Download the security report.
    10. Show the scan saved in history.
    11. End with the fictional-data and public-demo safety notice.
    """
)

st.header("About the Creator")

st.subheader("Paul Morin")

st.markdown(
    """
    My name is **Paul Morin**. I am a college student studying cybersecurity and technology.
    I built TotalThreat IQ for the Microsoft Agents League Hackathon / Microsoft AI Fest as a practical
    cybersecurity reasoning project.

    This project gave me a chance to turn an idea into a working application with threat scoring,
    dashboard metrics, scan history, report downloads, and a cleaner user interface. It also helped
    me practice organizing code, debugging, working with Python libraries, and connecting different
    parts of an application into one finished project.

    TotalThreat IQ was inspired by tools like VirusTotal, but with a different focus: suspicious
    communication, phishing indicators, links, domains, and attachment names.
    """
)

col_a, col_b = st.columns(2)

with col_a:
    st.link_button("GitHub: pmorin0505", "https://github.com/pmorin0505")

with col_b:
    st.link_button(
        "LinkedIn: Paul Morin",
        "https://www.linkedin.com/in/paul-morin-6526422b0/",
    )

st.header("Future Improvements")

st.markdown(
    """
    - Full Microsoft Foundry Agent integration
    - Live Foundry IQ knowledge base backed by Azure AI Search
    - More advanced typosquatting detection
    - PDF report export
    - Admin settings page
    - More demo scenarios
    - Expanded threat intelligence rules
    - Safer organization-specific deployment mode
    - Better accessibility support
    """
)

st.header("Creator Links")

st.markdown(
    """
    **Paul Morin**  
    GitHub: [pmorin0505](https://github.com/pmorin0505)  
    LinkedIn: [Paul Morin](https://www.linkedin.com/in/paul-morin-6526422b0/)
    """
)
