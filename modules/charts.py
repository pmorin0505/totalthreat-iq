import pandas as pd
import plotly.express as px
def risk_distribution(history):
    df=pd.DataFrame(history)
    if df.empty: return None
    counts=df['risk_level'].value_counts().reset_index(); counts.columns=['Risk Level','Count']
    return px.pie(counts, names='Risk Level', values='Count', title='Risk Distribution')
def signal_frequency(history):
    import json
    rows=[]
    for h in history:
        try: sigs=json.loads(h.get('detected_signals') or '[]')
        except Exception: sigs=[]
        for s in sigs: rows.append(s.get('name','Unknown'))
    if not rows: return None
    df=pd.Series(rows).value_counts().head(10).reset_index(); df.columns=['Signal','Count']
    return px.bar(df, x='Signal', y='Count', title='Common Threat Signals')
