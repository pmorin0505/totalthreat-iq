import streamlit as st
import pandas as pd
from config import THREAT_RULES_PATH, SUSPICIOUS_PATTERNS_PATH, ATTACHMENT_PATTERNS_PATH
def render():
    st.title('Threat Intelligence / Rules'); st.write('This page explains the local pattern-based rules TotalThreat IQ uses for educational threat communication analysis.')
    for title,path in [('Scoring Rules',THREAT_RULES_PATH),('Suspicious URL / Message Patterns',SUSPICIOUS_PATTERNS_PATH),('Attachment Patterns',ATTACHMENT_PATTERNS_PATH)]:
        st.subheader(title)
        try: st.dataframe(pd.read_csv(path), use_container_width=True, hide_index=True)
        except Exception as e: st.error(f'Could not load {path}: {e}')
