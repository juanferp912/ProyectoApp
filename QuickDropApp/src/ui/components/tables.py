# src/ui/components/tables.py
import io
import streamlit as st

def download_csv(df, filename, label):
    if df is None or df.empty: 
        return
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button(label=label, data=buf.getvalue(), file_name=filename, mime="text/csv")
