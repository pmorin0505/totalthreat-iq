import streamlit as st
from modules.database import fetch_history
def render():
    st.title('Reports'); history=fetch_history()
    if not history: st.info('No reports yet. Run a scan first.'); return
    selected=st.selectbox('Select report', history, format_func=lambda h: f"#{h['id']} • {h['timestamp']} • {h['risk_level']} • {h['threat_category']}")
    st.text_area('Latest / Selected Report', selected.get('report_text',''), height=520)
    st.download_button('Download Selected TXT Report', selected.get('report_text',''), file_name=f"totalthreat_report_{selected['id']}.txt")
