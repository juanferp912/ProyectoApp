# src/ui/dashboards.py
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

from src.services import trend, top_products, city_store
from src.ui.components.kpi import inject_css, kpi
from src.ui.components.tables import download_csv
from src.ui.components.charts import line_ingreso_por_mes, bar_unidades_por_mes, treemap_city_store_numbers_on_deep
from src.reporting.pdf import build_dashboard_pdf

TZ = ZoneInfo("America/Guayaquil")

def render_dashboard(filters: dict):
    inject_css()

    df_trend = trend(filters)
    total_ingreso  = float(df_trend["ingreso_total"].sum()) if not df_trend.empty else 0.0
    total_unidades = int(df_trend["cantidad_total"].sum()) if not df_trend.empty else 0
    total_tx       = int(df_trend["transacciones"].sum())  if not df_trend.empty else 0
    ticket         = (total_ingreso / total_unidades) if total_unidades else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi(f"${total_ingreso:,.2f}", "Ingreso total")
    with c2: kpi(f"{total_unidades:,}", "Unidades vendidas")
    with c3: kpi(f"{total_tx:,}", "Transacciones")
    with c4: kpi(f"${ticket:,.2f}", "Ticket promedio")

    colA, colB = st.columns((1.2, 1))
    with colA:
        st.subheader("Tendencia mensual")
        st.dataframe(df_trend, use_container_width=True)
        fig1 = line_ingreso_por_mes(df_trend)
        if fig1: st.plotly_chart(fig1, use_container_width=True)
    with colB:
        fig2 = bar_unidades_por_mes(df_trend)
        if fig2: st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Mapa de ingreso por Ciudad/Tienda")
    df_ct = city_store(filters)
    st.dataframe(df_ct, use_container_width=True)
    download_csv(df_ct, "ingreso_ciudad_tienda.csv", "Descargar CSV (Ciudad/Tienda)")
    fig = treemap_city_store_numbers_on_deep(df_ct)
    if fig: st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top productos por ingreso")
    n = st.slider("N", 5, 50, 10, 5, key="topN")
    df_top = top_products(filters, n=n)
    st.dataframe(df_top, use_container_width=True)
    download_csv(df_top, "top_productos.csv", "Descargar CSV (Top productos)")

    # ---- Reporte PDF ----
    st.divider()
    st.subheader("Reporte PDF")
    st.caption("Genera un PDF con los KPIs y gráficos mostrados, respetando los filtros actuales.")
    if st.button("📄 Generar PDF"):
        try:
            pdf_bytes = build_dashboard_pdf(filters)
            stamp = datetime.now(TZ).strftime("%Y%m%d_%H%M")
            st.download_button(
                label="Descargar reporte PDF",
                data=pdf_bytes,
                file_name=f"reporte_quickdrop_{stamp}.pdf",
                mime="application/pdf"
            )
            st.success("Reporte generado.")
        except Exception as e:
            st.error(f"Ocurrió un error generando el PDF: {e}\n\n"
                     "Verifica que 'kaleido' esté instalado correctamente.")
