import json

from config import DISCLAIMER, DATA_DISCLAIMER
from modules.utils import list_to_string


def report_text(result):
    signals = "\n".join(
        [
            f"- {s.get('name')} (+{s.get('weight')}): {s.get('detail', '')}"
            for s in result.get("detected_signals", [])
        ]
    ) or "- No major indicators detected by current rules."

    foundry = result.get("foundry_iq", {})

    foundry_mode = foundry.get("mode", "Not generated")
    foundry_summary = foundry.get(
        "summary",
        "Foundry IQ summary was not generated for this report.",
    )
    foundry_source = foundry.get("knowledge_source", "Not provided")
    foundry_note = foundry.get("note", "")

    return f"""TotalThreat IQ Security Report
Generated: {result.get('timestamp')}
Input Type: {result.get('input_type')}
Sender: {result.get('sender') or 'Not provided'}
Subject: {result.get('subject') or 'Not provided'}
Message Preview: {result.get('message_preview')}

Threat Score: {result.get('threat_score')}/100
Risk Level: {result.get('risk_level')}
Threat Category: {result.get('threat_category')}
Confidence: {result.get('confidence_level')}

URLs Found: {list_to_string(result.get('urls_found')) or 'None'}
Attachments Found: {list_to_string(result.get('attachments_found')) or 'None'}

Detected Signals:
{signals}

Reasoning Summary:
{result.get('reasoning_summary')}

Plain-English Explanation:
{result.get('plain_english_explanation')}

Recommended Action:
{result.get('recommended_action')}

Foundry IQ / Microsoft IQ Summary:
Mode: {foundry_mode}
Knowledge Source: {foundry_source}

{foundry_summary}

Foundry Note:
{foundry_note}

Security Analyst Summary:
Risk appears {result.get('risk_level')} based on detected communication, URL/domain, and attachment-name indicators. This assessment is pattern-based and should support, not replace, human verification.

Disclaimer:
{DISCLAIMER}
{DATA_DISCLAIMER}
"""


def report_json(result):
    return json.dumps(result, indent=2)
