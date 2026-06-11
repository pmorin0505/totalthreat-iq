# TotalThreat IQ

**A multi-signal cybersecurity reasoning application for suspicious emails, messages, links, domains, and attachment names.**

TotalThreat IQ is a local cybersecurity reasoning app built for the **Microsoft Agents League Hackathon / Microsoft AI Fest** under the **Reasoning Agents** track. The app analyzes suspicious communication, detects common phishing and social engineering indicators, assigns a threat score, explains the reasoning, recommends safe actions, saves scan history locally, and generates downloadable security reports.

---
## Live Demo

Try TotalThreat IQ here: https://totalthreat-iq.streamlit.app/

## Public Demo Data Notice

The Streamlit demo is a shared public demo environment. Scan history may be visible to other users while the app instance is running, and history may reset when the app restarts or redeploys. Do not enter confidential, personal, employer, customer, employee, or sensitive information. Use fictional or test examples only.

## Project Summary

TotalThreat IQ is inspired by tools like VirusTotal, but instead of scanning executable malware, it focuses on suspicious communication.

The app can analyze:

* Emails
* Text messages
* Chat / DM messages
* Links and domains
* Attachment names
* Mixed suspicious communication

It checks for threat signals such as urgency, credential requests, MFA code theft attempts, suspicious URLs, brand impersonation, payment scams, gift card scams, risky attachment names, and social engineering language.

---

## Hackathon Track

**Track:** Reasoning Agents
**Microsoft IQ Direction:** Foundry IQ / Microsoft Foundry
**Project Type:** Local Streamlit cybersecurity reasoning app
**Developer:** Paul Morin
**GitHub:** https://github.com/pmorin0505
**LinkedIn:** https://www.linkedin.com/in/paul-morin-6526422b0/

---

## Why This Fits the Reasoning Agents Track

TotalThreat IQ performs multi-step reasoning instead of only returning a basic keyword match.

The app:

1. Accepts suspicious communication from the user.
2. Extracts message text, sender context, URLs, domains, and attachment names.
3. Detects multiple threat signals.
4. Applies weighted scoring rules.
5. Classifies the risk level as Low, Medium, High, or Critical.
6. Identifies the likely threat category.
7. Explains why the message may be suspicious.
8. Recommends safe next steps.
9. Generates a downloadable report.
10. Saves the scan to local history.

---

## Foundry IQ Integration Approach

TotalThreat IQ includes a **Foundry IQ-ready grounding layer**.

The local MVP produces structured cybersecurity findings and passes them into a Microsoft IQ-style grounding layer that creates an analyst-style explanation. This mirrors the Foundry IQ pattern from the Microsoft IQ Series: using knowledge sources and grounding to help agents produce more reliable, contextual, and useful answers.

The current version includes:

* A local cybersecurity grounding knowledge pack
* A Foundry IQ / Microsoft IQ summary section in scan results
* A dedicated Foundry IQ Integration page
* Optional Azure / Microsoft Foundry environment variable configuration
* A clear path for connecting the project to a full Foundry IQ knowledge base in the future

A full cloud version would connect the grounding layer to a Microsoft Foundry Agent and a Foundry IQ knowledge base backed by Azure AI Search.

---

## Azure / Foundry Access Note

I attempted to configure Azure / Microsoft Foundry access using both a personal Microsoft account and a school account. During setup, Azure repeatedly returned the following access error:

```text
AADSTS53003: Access has been blocked by Conditional Access policies.
```

This appeared to be related to account or tenant access restrictions during sign-in/token retrieval. Because of that, I could not complete a live Azure Foundry deployment before submission.

Rather than stop the project, I built the full local application and implemented a Foundry IQ-ready architecture with a local grounding knowledge pack, optional Azure configuration, and clear documentation showing how the full Foundry IQ version would connect when Azure access is available.

This was a frustrating but valuable part of the project. The goal was not just to make a demo screen, but to keep building despite the access limitation and still produce a working, safe, organized, and demo-ready cybersecurity reasoning tool.

---

## Features

* Suspicious message scanner
* Link and domain analyzer
* Attachment name analyzer
* Full threat scan mode
* Weighted threat scoring system
* Risk levels: Low, Medium, High, Critical
* Threat category classification
* Security analyst-style reasoning
* Plain-English explanation
* Foundry IQ / Microsoft IQ-style grounded summary
* Downloadable TXT report
* Downloadable JSON report
* SQLite scan history
* Dashboard with charts and metrics
* Risk distribution visualization
* Common threat signal visualization
* Responsible AI and safety disclaimers
* Synthetic demo data only

---

## Risk Scoring

TotalThreat IQ uses a weighted scoring model.

Example signal weights:

| Signal                         | Weight |
| ------------------------------ | -----: |
| Urgency or pressure            |    +15 |
| Credential request             |    +25 |
| MFA code request               |    +25 |
| Suspicious link                |    +20 |
| Brand impersonation            |    +15 |
| Account shutdown threat        |    +20 |
| Payment or banking request     |    +20 |
| Gift card request              |    +20 |
| Dangerous attachment extension |    +25 |
| Macro-enabled Office file      |    +20 |
| Double extension               |    +25 |
| HTTP link                      |    +10 |
| Shortened URL                  |    +15 |
| IP-based URL                   |    +20 |

Scores are capped at 100.

Risk levels:

| Score Range | Risk Level |
| ----------: | ---------- |
|        0–24 | Low        |
|       25–49 | Medium     |
|       50–74 | High       |
|      75–100 | Critical   |

---

## Threat Categories

TotalThreat IQ can classify scans into categories such as:

* Credential phishing
* MFA code theft
* Business email compromise
* Invoice/payment scam
* Payroll scam
* Gift card scam
* Malware delivery attempt
* Fake job scam
* Package delivery scam
* Brand impersonation
* General social engineering
* Low-confidence suspicious message

---

## Tech Stack

* Python
* Streamlit
* SQLite
* Pandas
* Plotly
* CSV / Excel data layer
* Local rule-based cybersecurity analysis
* Foundry IQ-ready grounding layer
* Optional Azure / Microsoft Foundry configuration

---

## Folder Structure

```text
totalthreat-iq/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── launch_totalthreat.bat
├── assets/
│   └── totalthreat_logo.png
├── data/
│   ├── sample_messages.csv
│   ├── threat_rules.csv
│   ├── suspicious_patterns.csv
│   ├── attachment_patterns.csv
│   └── totalthreat_scans.db
├── modules/
│   ├── analyzer.py
│   ├── attachment_analyzer.py
│   ├── charts.py
│   ├── database.py
│   ├── demo_data.py
│   ├── foundry_client.py
│   ├── report_generator.py
│   ├── scoring.py
│   ├── ui_components.py
│   ├── url_analyzer.py
│   └── utils.py
└── pages/
    ├── about.py
    ├── analyze.py
    ├── dashboard.py
    ├── foundry_iq.py
    ├── history.py
    ├── reports.py
    └── threat_intel.py
```
## Demo Instructions

When you first open TotalThreat IQ, the dashboard may be empty because scan history is generated locally.

To test the app:

1. Go to the **Analyze** page.
2. Load a demo example, such as the fake Microsoft password reset.
3. Click **Analyze Message**.
4. Review the threat score, risk level, detected signals, reasoning summary, and Foundry IQ / Microsoft IQ-style summary.
5. Go to the **Dashboard** page.
6. Watch the charts and metrics update based on the scans you create.
7. Try multiple demo messages to see how the scoring changes in real time.

The app intentionally starts with no saved scan history so users can experiment with the scanner and see the scoring system work from a clean state.

---

## How to Run Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the app:

```bash
python -m streamlit run app.py
```

Or on Windows, run:

```text
launch_totalthreat.bat
```

---

## Optional Azure / Microsoft Foundry Configuration

The local app runs without Azure credentials.

For a future connected deployment, create a `.env` file in the project root:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini

FOUNDRY_PROJECT_ENDPOINT=https://your-ai-services-account-name.services.ai.azure.com/api/projects/your-project-name
FOUNDRY_IQ_KNOWLEDGE_BASE=totalthreat-cybersecurity-knowledge-base
```

Do **not** upload `.env` to GitHub.

---

## Responsible AI and Safety

TotalThreat IQ is an educational cybersecurity awareness and reasoning tool. It does not guarantee that a message is safe or malicious. Users should verify suspicious messages through official channels and follow their organization’s security policies.

This project uses fictional and synthetic examples only. No employer, customer, employee, confidential, or real organizational data was used.

TotalThreat IQ does not:

* Execute files
* Open attachments
* Sandbox malware
* Scan real malware
* Claim certainty
* Replace professional security review

The app uses careful wording such as:

* “This message may be suspicious because…”
* “Risk appears low based on detected indicators.”
* “Verify through official channels.”

---

## Demo Flow

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

---

## About the Creator

My name is **Paul Morin**. I am a college student studying cybersecurity and technology. I built TotalThreat IQ for the Microsoft Agents League Hackathon / Microsoft AI Fest as a practical cybersecurity reasoning project.

This project also represents how I use AI as a learning and development accelerator. AI helped me move faster, but I still reviewed the code, tested the app, fixed errors, made design decisions, and shaped the project into a working tool.

* GitHub: https://github.com/pmorin0505
* LinkedIn: https://www.linkedin.com/in/paul-morin-6526422b0/

---

## Future Improvements

* Full Microsoft Foundry Agent integration
* Live Foundry IQ knowledge base backed by Azure AI Search
* More advanced typosquatting detection
* PDF report export
* Admin settings page
* More demo scenarios
* Expanded threat intelligence rules
* Safer organization-specific deployment mode
* Better accessibility support

---

## License

This project is for educational and hackathon demonstration purposes.
