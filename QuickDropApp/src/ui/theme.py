# src/ui/theme.py
from __future__ import annotations
import streamlit as st
import plotly.io as pio

PALETTE = {
    "yellow": "#F7C948",   # Primario
    "yellow_dark": "#E0B800",
    "gray_900": "#1F2937",
    "gray_700": "#374151",
    "gray_500": "#6B7280",
    "gray_300": "#D1D5DB",
    "gray_200": "#E5E7EB",
    "gray_100": "#F3F4F6",
    "bg": "#F7F8FA",
    "panel": "#ECEFF4",
    "white": "#FFFFFF",
}

CSS = f"""
<style>
/* ====== Layout base ====== */
.block-container {{
  padding-top: 1.2rem;
  padding-bottom: 2rem;
}}

/* ====== Top header con logo ====== */
.app-header {{
  display: flex; align-items: center; gap: .8rem;
  padding: .6rem 1rem; margin-bottom: .6rem;
  border-radius: 12px;
  background: linear-gradient(90deg, {PALETTE["yellow"]}22, {PALETTE["panel"]} 70%);
  border: 1px solid {PALETTE["gray_200"]};
}}
.app-title {{
  font-size: 1.1rem; font-weight: 700; color: {PALETTE["gray_900"]}; margin: 0;
}}
.app-sub {{
  font-size: .85rem; color: {PALETTE["gray_500"]}; margin: 0;
}}

/* ====== KPI cards ====== */
.kpi-card {{
  padding: .9rem 1rem; border-radius: 14px;
  box-shadow: 0 1px 12px rgba(0,0,0,.06);
  border: 1px solid {PALETTE["gray_200"]};
  background: {PALETTE["white"]};
}}
.kpi-value {{ font-size: 1.6rem; font-weight: 800; margin: 0; color: {PALETTE["gray_900"]}; }}
.kpi-label {{ color: {PALETTE["gray_500"]}; margin: 0; font-size: .9rem; }}

/* ====== Botones y elementos de acción ====== */
.stButton>button, .stDownloadButton>button {{
  border-radius: 10px !important;
  border: 1px solid {PALETTE["gray_300"]} !important;
  background: {PALETTE["yellow"]} !important;
  color: #111 !important;
  font-weight: 700 !important;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
  filter: brightness(.95);
  border-color: {PALETTE["yellow_dark"]} !important;
}}

/* ====== Tablas ====== */
.stDataFrame, .stTable {{
  border-radius: 12px; overflow: hidden; border: 1px solid {PALETTE["gray_200"]};
}}
</style>
"""

def apply_global_theme():
    # Inyecta CSS
    st.markdown(CSS, unsafe_allow_html=True)

    # Plotly template (tipografía y colorway coherente)
    template = {
        "layout": {
            "font": {"family": "Inter, system-ui, Segoe UI, Roboto, sans-serif", "size": 13, "color": PALETTE["gray_900"]},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "margin": {"l": 30, "r": 20, "t": 40, "b": 30},
            "colorway": [
                PALETTE["yellow"], "#6B7280", "#F59E0B", "#9CA3AF",
                "#FDE68A", "#4B5563", "#D1D5DB"
            ],
            "xaxis": {"gridcolor": PALETTE["gray_200"]},
            "yaxis": {"gridcolor": PALETTE["gray_200"]},
            "legend": {"bgcolor": "rgba(255,255,255,0.6)", "bordercolor": PALETTE["gray_200"], "borderwidth": 1}
        }
    }
    pio.templates["quickdrop_yellow_gray"] = template
    pio.templates.default = "quickdrop_yellow_gray"
