def cap_score(score): return max(0, min(100, int(score)))
def risk_level(score):
    score=cap_score(score)
    if score<=24: return "Low"
    if score<=49: return "Medium"
    if score<=74: return "High"
    return "Critical"
def confidence_from_signals(signals):
    count=len(signals or [])
    return "High" if count>=6 else "Medium" if count>=3 else "Low"
