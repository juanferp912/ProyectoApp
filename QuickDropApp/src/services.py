# src/services.py
from __future__ import annotations
import re
import pandas as pd
import streamlit as st
from sqlalchemy import text
from src.config import get_engine
from src.queries import where_and_params, SQL

engine = get_engine()

def _apply_filters(filters):
    # Compat con antiguos keys years/months; ahora enfocamos en rango real:
    return where_and_params(
        filters.get("years"),      # opcional
        filters.get("months"),     # opcional
        filters.get("ciudades"),
        filters.get("categorias"),
        filters.get("metodos"),
        filters.get("date_from"),
        filters.get("date_to"),
    )

def _run(sql_key: str, filters: dict, extra_params: dict | None = None):
    where_sql, params = _apply_filters(filters)
    sql = SQL[sql_key].format(where=where_sql)
    if extra_params:
        params = {**params, **extra_params}
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)
    
@st.cache_data(ttl=300)
def trend(filters):                return _run("trend", filters)
@st.cache_data(ttl=300)
def top_products(filters, n=10):   return _run("top_products", filters, {"limit": n})
@st.cache_data(ttl=300)
def city_store(filters):           return _run("city_store", filters)
@st.cache_data(ttl=300)
def pay_mix(filters):              return _run("pay_mix", filters)
@st.cache_data(ttl=300)
def delivery_status(filters):      return _run("delivery_status", filters)
@st.cache_data(ttl=300)
def top_clients(filters, n=15):    return _run("top_clients", filters, {"limit": n})
@st.cache_data(ttl=300)
def top_couriers(filters, n=20):   return _run("top_couriers", filters, {"limit": n})
@st.cache_data(ttl=300)
def clients_by_city(filters):      return _run("clients_by_city", filters)

@st.cache_data(ttl=300)
def parse_delivery_minutes(filters):
    # Si luego quieres consultar directo, crea una SQL específica. Aquí reuso city_store() solo para filtros.
    where_sql, params = where_and_params(
        filters.get("years"), filters.get("months"),
        filters.get("ciudades"), filters.get("categorias"), filters.get("metodos")
    )
    sql = f"""
    SELECT hv.tiempo_entrega
    FROM hechos_ventas hv
    JOIN dim_fecha df ON hv.fecha_key = df.fecha_key
    JOIN dim_tienda dt ON hv.tienda_key = dt.tienda_key
    JOIN dim_producto dp ON hv.producto_key = dp.producto_key
    JOIN dim_pago dpg ON hv.pago_key = dpg.pago_key
    {where_sql}
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn, params=params)
    mins = []
    for v in df["tiempo_entrega"].dropna().astype(str):
        m = re.search(r"(\d+)", v)
        if m:
            try: mins.append(int(m.group(1)))
            except: pass
    return pd.Series(mins, name="minutos")
