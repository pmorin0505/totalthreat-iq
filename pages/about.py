import streamlit as st

from modules.ui_components import disclaimer_box, result_card


def render():
    st.title("About TotalThreat IQ")
    st.caption("Microsoft Agents League Hackathon / Microsoft AI Fest • Reasoning Agents • Foundry IQ Direction")

    st.markdown(
        """
        <div class="profile-card">
            <h2>TotalThreat IQ</h2>
            <p>
                <strong>TotalThreat IQ</strong> is a local cybersecurity reasoning application that analyzes
                suspicious emails, messages, links, domains, and attachment names. It detects common phishing
                and social engineering indicators, assigns a threat score, explains the reasoning, recommends
                safe actions, saves scan history locally, and generates downloadable security reports.
            </p>
            <p>
                The project was built for the <strong>Microsoft Agents League Hackathon / Microsoft AI Fest</strong>
                under the <strong>Reasoning Agents</strong> track. It is designed to show how a cybersecurity
                tool can reason across multiple signals instead of only matching one keyword or one indicator.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.header("Project Identity")

    col1, col2, col3 = st.columns(3)

    with col1:
        result_card(
            "Hackathon Track",
            "Reasoning Agents — TotalThreat IQ performs multi-step reasoning by detecting indicators, scoring risk, explaining findings, and recommending safe actions.",
        )

    with col2:
        result_card(
            "Microsoft IQ Direction",
            "Foundry IQ / Microsoft Foundry — the project includes a Foundry IQ-ready grounding layer and optional Azure / Foundry configuration path.",
        )

    with col3:
        result_card(
            "Project Type",
            "Local Streamlit cybersecurity reasoning app using Python, SQLite, CSV data, Plotly charts, and a structured analysis engine.",
        )

    st.header("What the App Scans")

    st.markdown(
        """
        TotalThreat IQ can analyze:

        - Suspicious emails
        - Text messages
        - Chat / DM messages
        - Links and domains
        - Attachment names
        - Mixed suspicious communication
        """
    )

    st.header("Why This Fits the Reasoning Agents Track")

    st.markdown(
        """
        TotalThreat IQ performs a full reasoning workflow:

        1. Accepts suspicious communication from the user.
        2. Extracts message text, sender context, URLs, domains, and attachment names.
        3. Detects multiple threat signals.
        4. Applies weighted scoring rules.
        5. Classifies the risk level as Low, Medium, High, or Critical.
        6. Identifies the likely threat category.
        7. Explains why the message may be suspicious.
        8. Recommends safe next steps.
        9. Generates a downloadable security report.
        10. Saves the scan to local history.
        """
    )

    st.header("Foundry IQ Integration Approach")

    st.markdown(
        """
        TotalThreat IQ includes a **Foundry IQ-ready grounding layer**.

        The local MVP produces structured cybersecurity findings and passes them into a Microsoft IQ-style
        grounding layer that creates an analyst-style explanation. This mirrors the Foundry IQ pattern from
        the Microsoft IQ Series: using knowledge sources and grounding to help agents produce more reliable,
        contextual, and useful answers.

        The current version includes:

        - A local cybersecurity grounding knowledge pack
        - A Foundry IQ / Microsoft IQ summary section in scan results
        - A dedicated Foundry IQ Integration page
        - Optional Azure / Microsoft Foundry environment variable configuration
        - A clear path for connecting the project to a full Foundry IQ knowledge base in the future

        A full cloud version would connect the grounding layer to a Microsoft Foundry Agent and a Foundry IQ
        knowledge base backed by Azure AI Search.
        """
    )

    st.header("Azure / Foundry Access Note")

    st.markdown(
        """
        I attempted to configure Azure / Microsoft Foundry access using both a personal Microsoft account and
        a school account. During setup, Azure repeatedly returned the following access error:
        """
    )

    st.code(
        "AADSTS53003: Access has been blocked by Conditional Access policies.",
        language="text",
    )

    st.markdown(
        """
        This appeared to be related to account or tenant access restrictions during sign-in/token retrieval.
        Because of that, I could not complete a live Azure Foundry deployment before submission.

        Rather than stop the project, I finished the full local application and implemented a Foundry IQ-ready
        architecture with a local grounding knowledge pack, optional Azure configuration, and clear documentation
        showing how the full Foundry IQ version would connect when Azure access is available.

        This was a frustrating but valuable part of the project. The goal was not just to create a demo screen,
        but to keep building despite the access limitation and still produce a working, safe, organized, and
        demo-ready cybersecurity reasoning tool.
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
        - Security analyst-style reasoning
        - Plain-English explanation
        - Foundry IQ / Microsoft IQ-style grounded summary
        - Downloadable TXT report
        - Downloadable JSON report
        - SQLite scan history
        - Dashboard with charts and metrics
        - Risk distribution visualization
        - Common threat signal visualization
        - Responsible AI and safety disclaimers
        - Synthetic demo data only
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
        | 0–24 | Low |
        | 25–49 | Medium |
        | 50–74 | High |
        | 75–100 | Critical |
        """
    )

    st.header("Threat Categories")

    st.markdown(
        """
        TotalThreat IQ can classify scans into categories such as:

        - Credential phishing
        - MFA code theft
        - Business email compromise
        - Invoice/payment scam
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

    st.header("Responsible AI and Safety")

    disclaimer_box(
        "TotalThreat IQ is an educational cybersecurity awareness and reasoning tool. "
        "It does not guarantee that a message is safe or malicious. Users should verify suspicious messages "
        "through official channels and follow their organization’s security policies."
    )

    st.markdown("")

    disclaimer_box(
        "This project uses fictional and synthetic examples only. No employer, customer, employee, confidential, "
        "or real organizational data was used."
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

        - “This message may be suspicious because…”
        - “Risk appears low based on detected indicators.”
        - “Verify through official channels.”
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
        6. Show the Critical risk score.
        7. Review detected threat signals.
        8. Review the reasoning summary.
        9. Show the Foundry IQ / Microsoft IQ-style summary.
        10. Download the security report.
        11. Show the scan saved in history.
        12. End with the responsible AI and fictional-data disclaimer.
        """
    )

    st.header("About the Creator")

    st.markdown(
        """
        <div class="profile-card">
            <h2>Paul Morin</h2>
            <p>
                My name is <strong>Paul Morin</strong>. I am a college student studying cybersecurity and technology.
                I built TotalThreat IQ for the Microsoft Agents League Hackathon / Microsoft AI Fest as a practical
                cybersecurity reasoning project.
            </p>
            <p>
                This project also represents how I use AI as a learning and development accelerator. AI helped me move
                faster, but I still reviewed the code, tested the app, fixed errors, made design decisions, and shaped
                the project into a working tool.
            </p>
            <div class="profile-link-row">
                <a class="profile-link" href="https://github.com/pmorin0505" target="_blank">GitHub: pmorin0505</a>
                <a class="profile-link" href="https://www.linkedin.com/in/paul-morin-6526422b0/" target="_blank">LinkedIn: Paul Morin</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
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