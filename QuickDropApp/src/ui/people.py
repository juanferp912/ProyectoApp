# src/ui/people.py
import streamlit as st
import plotly.express as px
from src.services import top_clients, clients_by_city, top_couriers
from src.ui.components.tables import download_csv

def render_people(filters: dict):
    st.subheader("Clientes")
    c1, c2 = st.columns(2)
    with c1:
        df = top_clients(filters, n=15)
        st.caption("Top 15 clientes por ingreso")
        st.dataframe(df, use_container_width=True)
        download_csv(df, "top_clientes.csv", "Descargar CSV")
    with c2:
        df2 = clients_by_city(filters)
        st.caption("Clientes únicos e ingreso por ciudad")
        st.dataframe(df2, use_container_width=True)
        if not df2.empty:
            fig = px.bar(df2, x="ciudad", y="clientes_unicos", title="Clientes únicos por ciudad")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Repartidores")
    df3 = top_couriers(filters, n=20)
    st.dataframe(df3, use_container_width=True)
    download_csv(df3, "repartidores.csv", "Descargar CSV")
    if not df3.empty:
        fig = px.bar(df3, x="nombre_repartidor", y="entregas",
                     hover_data=["zona","placa_moto","ingreso"], title="Entregas por repartidor (Top 20)")
        fig.update_layout(xaxis_tickangle=-35, height=520)
        st.plotly_chart(fig, use_container_width=True)
