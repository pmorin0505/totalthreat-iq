from datetime import datetime
import re

def now_iso(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def clean_text(text): return re.sub(r"\s+", " ", (text or "")).strip()
def preview(text, limit=140):
    text = clean_text(text)
    return text[:limit] + ("..." if len(text) > limit else "")
def list_to_string(items):
    if not items: return ""
    if isinstance(items, str): return items
    return "; ".join(str(x) for x in items)
