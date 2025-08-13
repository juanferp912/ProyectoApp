# app.py
from src.ui.theme import apply_global_theme
import streamlit as st
from src.config import test_connection
from src.ui.filters import render_filters
from src.ui.dashboards import render_dashboard
from src.ui.operations import render_operations
from src.ui.people import render_people

st.set_page_config(
    page_title="QuickDrop DW – Analytics",
    page_icon="assets/logo.png",  
    layout="wide"
)
apply_global_theme()   

st.set_page_config(page_title="QuickDrop DW – Analytics", layout="wide")
st.title("QuickDrop DW – Analytics")

st.markdown(
    """
    <link rel="shortcut icon" href="/app/static/assets/logo.png">
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.image("assets/logo.png", width=140)
    st.header("Conexión")
    st.caption(test_connection())

# Filtros globales (devuelve un dict)
filters = render_filters()

tab_dash, tab_ops, tab_people = st.tabs(["Dashboard", "Operaciones", "Clientes & Repartidores"])

with tab_dash:
    render_dashboard(filters)

with tab_ops:
    render_operations(filters)

with tab_people:
    render_people(filters)
