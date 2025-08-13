# src/ui/operations.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.services import delivery_status, pay_mix, parse_delivery_minutes
from src.ui.components.tables import download_csv

def render_operations(filters: dict):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Estados de entrega")
        df = delivery_status(filters)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "estados_entrega.csv", "Descargar CSV")
        if not df.empty:
            fig = px.pie(df, names="estado_entrega", values="entregas", title="Distribución de estados de entrega")
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Métodos de pago")
        df = pay_mix(filters)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "metodos_pago.csv", "Descargar CSV")
        if not df.empty:
            fig = px.pie(df, names="metodo_pago", values="ingreso", title="Participación por método de pago")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Tiempos de entrega (min, si se pueden inferir)")
    serie = parse_delivery_minutes(filters)
    if not serie.empty:
        dfm = pd.DataFrame({"minutos": serie})
        fig = px.histogram(dfm, x="minutos", nbins=30, title="Histograma de tiempos de entrega (min)")
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"Promedio: **{serie.mean():.1f}** min, Mediana: **{serie.median():.1f}** min, N={len(serie)}")
    else:
        st.info("No se pudo inferir minutos desde `tiempo_entrega`. Considera guardarlo como entero.")
