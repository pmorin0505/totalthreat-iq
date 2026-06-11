import pandas as pd
from config import SAMPLE_MESSAGES_PATH
def load_samples():
    try: return pd.read_csv(SAMPLE_MESSAGES_PATH)
    except Exception: return pd.DataFrame()
def sample_by_label(label):
    df=load_samples()
    if df.empty: return None
    row=df[df['Subject'].astype(str).str.contains(label, case=False, na=False)]
    if row.empty: row=df.head(1)
    return row.iloc[0].to_dict()
