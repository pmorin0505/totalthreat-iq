import streamlit as st
import pandas as pd
from modules.database import fetch_history, clear_history
def render():
    st.title('Analysis History'); history=fetch_history()
    if not history: st.info('No saved scan history yet.'); return
    df=pd.DataFrame(history); risk=st.multiselect('Filter by Risk',['Low','Medium','High','Critical'],default=['Low','Medium','High','Critical']); search=st.text_input('Search message preview'); view=df[df['risk_level'].isin(risk)]
    if search: view=view[view['message_preview'].str.contains(search,case=False,na=False)]
    st.dataframe(view[['id','timestamp','input_type','risk_level','threat_score','threat_category','message_preview']], use_container_width=True, hide_index=True); st.download_button('Export History CSV', view.to_csv(index=False), 'totalthreat_scan_history.csv')
    with st.expander('Clear local history'):
        if st.button('Clear History'): clear_history(); st.warning('Local scan history cleared. Refresh the page to update the table.')
