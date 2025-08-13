# src/ui/components/kpi.py
import streamlit as st

def inject_css():
    # Ya no necesitamos CSS aquí: lo inyecta theme.apply_global_theme()
    pass

def kpi(value, label):
    st.markdown(
        f'<div class="kpi-card"><p class="kpi-value">{value}</p><p class="kpi-label">{label}</p></div>',
        unsafe_allow_html=True
    )
