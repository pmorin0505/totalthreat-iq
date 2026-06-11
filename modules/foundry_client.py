import json
import os
from pathlib import Path


LOCAL_SECURITY_KNOWLEDGE_BASE = """
TotalThreat IQ cybersecurity knowledge base:

1. Credential phishing:
Messages asking users to verify accounts, reset passwords, sign in through unexpected links,
or provide credentials should be treated as suspicious.

2. MFA code theft:
Messages requesting one-time codes, verification codes, authenticator codes, or MFA approval
should be treated as high risk. Users should never share MFA codes.

3. Business email compromise:
Messages involving urgent payment changes, wire transfers, invoice changes, payroll updates,
or secrecy should be verified through a trusted out-of-band channel.

4. Suspicious links:
Unexpected links using HTTP, shortened URLs, suspicious top-level domains, IP-based URLs,
or unofficial brand-looking domains should not be clicked without verification.

5. Attachment risk:
Executable files, macro-enabled Office files, double extensions, compressed archives, and disk
image files can be used for malware delivery. This app only analyzes filenames and does not
open or execute files.

6. Safe user guidance:
Users should avoid clicking suspicious links, avoid opening unexpected attachments, avoid
replying with sensitive information, and verify through official channels.

7. Responsible AI:
This tool is educational and pattern-based. It does not guarantee that a message is safe or
malicious. Users should follow their organization’s security policies.
"""


def _load_env_file():
    """
    Loads .env if python-dotenv is available.
    The app still works if python-dotenv is missing.
    """
    try:
        from dotenv import load_dotenv

        env_path = Path(".env")
        if env_path.exists():
            load_dotenv(env_path)
    except Exception:
        pass


def get_foundry_config():
    _load_env_file()

    return {
        "azure_openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "").strip(),
        "azure_openai_api_key": os.getenv("AZURE_OPENAI_API_KEY", "").strip(),
        "azure_openai_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip(),
        "foundry_project_endpoint": os.getenv("FOUNDRY_PROJECT_ENDPOINT", "").strip(),
        "foundry_iq_knowledge_base": os.getenv("FOUNDRY_IQ_KNOWLEDGE_BASE", "").strip(),
    }


def is_foundry_configured():
    cfg = get_foundry_config()

    return bool(
        cfg["azure_openai_endpoint"]
        and cfg["azure_openai_api_key"]
        and cfg["azure_openai_deployment"]
    )


def foundry_status():
    cfg = get_foundry_config()

    if is_foundry_configured():
        return {
            "status": "Configured",
            "mode": "Connected mode available",
            "details": "Azure OpenAI / Microsoft Foundry endpoint variables are present.",
            "config": {
                "AZURE_OPENAI_ENDPOINT": "Set",
                "AZURE_OPENAI_API_KEY": "Set but hidden",
                "AZURE_OPENAI_DEPLOYMENT": cfg["azure_openai_deployment"],
                "FOUNDRY_PROJECT_ENDPOINT": cfg["foundry_project_endpoint"] or "Not set",
                "FOUNDRY_IQ_KNOWLEDGE_BASE": cfg["foundry_iq_knowledge_base"] or "Not set",
            },
        }

    return {
        "status": "Local fallback",
        "mode": "Foundry IQ-ready architecture",
        "details": (
            "Azure credentials are not configured yet. TotalThreat IQ will use a local "
            "grounding pack that mirrors the intended Foundry IQ workflow."
        ),
        "config": {
            "AZURE_OPENAI_ENDPOINT": "Not set",
            "AZURE_OPENAI_API_KEY": "Not set",
            "AZURE_OPENAI_DEPLOYMENT": "Not set",
            "FOUNDRY_PROJECT_ENDPOINT": cfg["foundry_project_endpoint"] or "Not set",
            "FOUNDRY_IQ_KNOWLEDGE_BASE": cfg["foundry_iq_knowledge_base"] or "Not set",
        },
    }


def build_structured_findings(result):
    signals = result.get("detected_signals", [])

    simplified_signals = []
    for signal in signals:
        simplified_signals.append(
            {
                "name": signal.get("name", "Unknown signal"),
                "weight": signal.get("weight", 0),
                "detail": signal.get("detail", ""),
                "source": signal.get("source", ""),
            }
        )

    return {
        "input_type": result.get("input_type"),
        "risk_level": result.get("risk_level"),
        "threat_score": result.get("threat_score"),
        "threat_category": result.get("threat_category"),
        "confidence_level": result.get("confidence_level"),
        "sender": result.get("sender"),
        "subject": result.get("subject"),
        "message_preview": result.get("message_preview"),
        "urls_found": result.get("urls_found", []),
        "attachments_found": result.get("attachments_found", []),
        "detected_signals": simplified_signals,
        "recommended_action": result.get("recommended_action"),
    }


def build_foundry_prompt(result):
    structured = build_structured_findings(result)

    return f"""
You are the Foundry IQ reasoning layer for TotalThreat IQ.

Use the cybersecurity knowledge base and the structured scan findings to create a grounded,
careful, security-analyst-style explanation. Do not claim certainty. Do not say the message is
definitely malicious or definitely safe.

Cybersecurity knowledge base:
{LOCAL_SECURITY_KNOWLEDGE_BASE}

Structured scan findings:
{json.dumps(structured, indent=2)}

Write:
1. A grounded analyst summary.
2. Why the detected signals matter.
3. Recommended next steps.
4. A short responsible AI safety note.
"""


def generate_local_grounded_summary(result):
    risk = result.get("risk_level", "Unknown")
    score = result.get("threat_score", 0)
    category = result.get("threat_category", "Unknown")
    signals = result.get("detected_signals", [])
    signal_names = [s.get("name", "Unknown signal") for s in signals]

    if signal_names:
        signal_text = ", ".join(signal_names[:8])
    else:
        signal_text = "no major indicators detected by the current rules"

    summary = (
        f"This scan produced a {risk} risk rating with a threat score of {score}/100. "
        f"The likely threat category is {category}. The main indicators were: {signal_text}. "
        f"Based on the local cybersecurity guidance pack, these indicators matter because phishing "
        f"and social engineering messages often combine pressure, impersonation, suspicious links, "
        f"credential requests, or risky attachment patterns to push a user into unsafe action. "
        f"The recommended next step is to avoid clicking links, avoid opening unexpected attachments, "
        f"avoid replying with sensitive information, and verify the message through an official channel."
    )

    return {
        "mode": "Local Foundry IQ-ready grounding",
        "connected": False,
        "summary": summary,
        "knowledge_source": "Local cybersecurity guidance pack",
        "note": (
            "Azure / Microsoft Foundry credentials are not configured yet. "
            "This fallback mirrors the intended Foundry IQ grounding workflow for the hackathon MVP."
        ),
    }


def generate_foundry_iq_summary(result):
    """
    Main function used by the Analyze page.

    If Azure OpenAI / Microsoft Foundry environment variables are configured,
    this function attempts to generate the grounded analyst summary through the configured model.

    If not configured, it returns a local Foundry IQ-ready grounded summary.
    """
    if not is_foundry_configured():
        return generate_local_grounded_summary(result)

    cfg = get_foundry_config()
    prompt = build_foundry_prompt(result)

    try:
        from openai import OpenAI

        endpoint = cfg["azure_openai_endpoint"].rstrip("/")

        if endpoint.endswith("/openai/v1"):
            base_url = endpoint
        else:
            base_url = endpoint + "/openai/v1"

        client = OpenAI(
            api_key=cfg["azure_openai_api_key"],
            base_url=base_url,
        )

        response = client.chat.completions.create(
            model=cfg["azure_openai_deployment"],
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful cybersecurity reasoning assistant for an educational "
                        "security awareness tool. Avoid certainty. Use grounded, responsible wording."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        summary = response.choices[0].message.content

        return {
            "mode": "Connected Microsoft Foundry / Azure OpenAI summary",
            "connected": True,
            "summary": summary,
            "knowledge_source": cfg["foundry_iq_knowledge_base"] or "Configured Microsoft Foundry / Azure OpenAI endpoint",
            "note": "Generated using configured Azure OpenAI / Microsoft Foundry settings.",
        }

    except Exception as exc:
        fallback = generate_local_grounded_summary(result)
        fallback["mode"] = "Local fallback after Foundry call failed"
        fallback["note"] = f"Foundry call failed, so local fallback was used. Error: {exc}"
        return fallback
    