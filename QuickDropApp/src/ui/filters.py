# src/ui/filters.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from src.config import get_engine

TZ = ZoneInfo("America/Guayaquil")

@st.cache_data(ttl=300)
def _load_filters():
    engine = get_engine()
    with engine.connect() as conn:
        df_tienda= pd.read_sql("SELECT tienda_key, nombre_tienda, ciudad FROM dim_tienda ORDER BY ciudad, nombre_tienda;", conn)
        df_prod  = pd.read_sql("SELECT DISTINCT categoria FROM dim_producto ORDER BY categoria;", conn)
        df_pago  = pd.read_sql("SELECT DISTINCT metodo_pago FROM dim_pago ORDER BY metodo_pago;", conn)
    return df_tienda, df_prod, df_pago

def _preset_range(preset: str):
    today = datetime.now(TZ).date()
    if preset == "Últimos 7 días":
        return today - timedelta(days=7), today
    if preset == "Últimos 30 días":
        return today - timedelta(days=30), today
    if preset == "Últimos 60 días":
        return today - timedelta(days=60), today
    if preset == "Últimos 90 días":
        return today - timedelta(days=90), today
    if preset == "Último año":
        return today - timedelta(days=365), today
    return None, None  # Personalizado

def render_filters():
    df_tienda, df_prod, df_pago = _load_filters()

    st.sidebar.header("Filtros")

    # Presets de fecha
    preset = st.sidebar.selectbox(
        "Rango de fechas",
        ["Últimos 7 días", "Últimos 30 días", "Últimos 60 días", "Últimos 90 días", "Último año", "Personalizado"],
        index=1
    )
    date_from, date_to = _preset_range(preset)
    if preset == "Personalizado":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            date_from = st.date_input("Desde", value=date_from or (datetime.now(TZ).date() - timedelta(days=30)))
        with col2:
            date_to   = st.date_input("Hasta", value=date_to or datetime.now(TZ).date())

    ciudades   = st.sidebar.multiselect("Ciudad (tienda)", sorted(df_tienda["ciudad"].dropna().unique().tolist()))
    categorias = st.sidebar.multiselect("Categoría", df_prod["categoria"].dropna().tolist())
    metodos    = st.sidebar.multiselect("Método de pago", df_pago["metodo_pago"].dropna().tolist())

    st.sidebar.caption("Los filtros aplican a todas las pestañas.")
    return {
        "date_from": pd.to_datetime(date_from).date() if date_from else None,
        "date_to":   pd.to_datetime(date_to).date()   if date_to   else None,
        "ciudades": ciudades,
        "categorias": categorias,
        "metodos": metodos
    }
