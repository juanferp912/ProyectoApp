# src/reporting/pdf.py
from __future__ import annotations
import io
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

from src.services import trend, city_store, top_products
from src.ui.components.charts import line_ingreso_por_mes, bar_unidades_por_mes, treemap_city_store_numbers_on_deep

TZ = ZoneInfo("America/Guayaquil")

def _fmt_money(x) -> str:
    try:
        if isinstance(x, (int, float, Decimal)):
            return f"${float(x):,.2f}"
        # pandas numeric
        return f"${float(x):,.2f}"
    except Exception:
        return str(x)

def _df_to_table(df: pd.DataFrame, max_rows: int = 15):
    """Convierte un DataFrame a una tabla ReportLab (con encabezado repetible)."""
    if df is None or df.empty:
        return Paragraph("<i>No hay datos para mostrar.</i>", getSampleStyleSheet()["BodyText"])

    # Clon + slicing
    dfx = df.copy().head(max_rows)

    # Formateo básico de números
    for col in dfx.columns:
        if "ingreso" in col.lower() or "total" in col.lower() or "precio" in col.lower():
            dfx[col] = dfx[col].apply(_fmt_money)

    data = [list(dfx.columns)] + dfx.astype(str).values.tolist()
    tbl = Table(data, repeatRows=1, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F0F2F6")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#333333")),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.25, colors.HexColor("#DDDDDD")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#FCFCFD")]),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return tbl

def _fig_png(fig, scale: int = 2, width_cm: float | None = None):
    """Convierte un fig de Plotly a Image de ReportLab."""
    if fig is None:
        return None
    png_bytes = fig.to_image(format="png", scale=scale)
    bio = io.BytesIO(png_bytes)
    img = Image(bio)
    if width_cm:
        img.drawWidth = width_cm * cm
        img.drawHeight = img.imageHeight * (img.drawWidth / img.imageWidth)
    return img

def build_dashboard_pdf(filters: dict) -> bytes:
    """
    Genera un PDF (bytes) con:
      - Encabezado con fecha + filtros
      - KPIs (Ingreso, Unidades, Transacciones, Ticket)
      - Gráficos: línea, barras, treemap
      - Tabla: Top productos
    """
    # ------- Datos -------
    df_trend = trend(filters)
    df_ct = city_store(filters)
    df_top = top_products(filters, n=10)

    total_ingreso  = float(df_trend["ingreso_total"].sum()) if not df_trend.empty else 0.0
    total_unidades = int(df_trend["cantidad_total"].sum()) if not df_trend.empty else 0
    total_tx       = int(df_trend["transacciones"].sum())  if not df_trend.empty else 0
    ticket         = (total_ingreso / total_unidades) if total_unidades else 0.0

    # ------- Figuras -------
    fig_line = line_ingreso_por_mes(df_trend)
    fig_bar  = bar_unidades_por_mes(df_trend)
    fig_tree = treemap_city_store_numbers_on_deep(df_ct)

    img_line = _fig_png(fig_line, scale=2, width_cm=17)
    img_bar  = _fig_png(fig_bar,  scale=2, width_cm=17)
    img_tree = _fig_png(fig_tree, scale=2, width_cm=17)

    # ------- Documento -------
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=1.6*cm,
        rightMargin=1.6*cm,
        topMargin=1.2*cm,
        bottomMargin=1.2*cm,
        title="Reporte QuickDrop DW"
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="H1", fontSize=18, leading=22, spaceAfter=10, alignment=0))
    styles.add(ParagraphStyle(name="H2", fontSize=14, leading=18, spaceAfter=8, textColor=colors.HexColor("#333")))
    styles.add(ParagraphStyle(name="Small", fontSize=9, textColor=colors.HexColor("#666")))

    story = []

    # Título + fecha
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    story.append(Paragraph("Reporte de Analytics – QuickDrop DW", styles["H1"]))
    story.append(Paragraph(f"Generado: {now} (America/Guayaquil)", styles["Small"]))
    story.append(Spacer(1, 6))

    # Filtros aplicados
    f_ciudad = ", ".join(filters.get("ciudades", []) or []) or "Todas"
    f_cat    = ", ".join(filters.get("categorias", []) or []) or "Todas"
    f_metodo = ", ".join(filters.get("metodos", []) or []) or "Todos"
    f_fecha  = ""
    if filters.get("date_from") or filters.get("date_to"):
        dfm = filters.get("date_from")
        dtm = filters.get("date_to")
        f_fecha = f"{dfm or '—'} a {dtm or '—'}"
    else:
        f_fecha = "Sin restricción (todas las fechas)"

    story.append(Paragraph(f"<b>Filtros</b>: Fecha: {f_fecha} | Ciudades: {f_ciudad} | Categorías: {f_cat} | Métodos: {f_metodo}", styles["Small"]))
    story.append(Spacer(1, 10))

    # KPIs
    kpi_data = [
        ["Ingreso total", _fmt_money(total_ingreso)],
        ["Unidades", f"{total_unidades:,}"],
        ["Transacciones", f"{total_tx:,}"],
        ["Ticket promedio", _fmt_money(ticket)],
    ]
    kpi_tbl = Table(kpi_data, colWidths=[5*cm, 6*cm])
    kpi_tbl.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 11),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#222")),
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FAFBFD")),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#E5E7EB")),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(kpi_tbl)
    story.append(Spacer(1, 10))

    # Gráfico línea
    story.append(Paragraph("Ingreso total por mes", styles["H2"]))
    if img_line: story.append(img_line)
    story.append(Spacer(1, 8))

    # Gráfico barras
    story.append(Paragraph("Unidades por mes", styles["H2"]))
    if img_bar: story.append(img_bar)
    story.append(Spacer(1, 8))

    # Treemap
    story.append(Paragraph("Treemap por ciudad/tienda", styles["H2"]))
    if img_tree: story.append(img_tree)
    story.append(Spacer(1, 10))

    # Tabla Top productos
    story.append(Paragraph("Top 10 productos por ingreso", styles["H2"]))
    story.append(_df_to_table(df_top, max_rows=10))
    story.append(Spacer(1, 10))

    # --- Estados de entrega ---
    try:
        from src.services import delivery_status
        df_delivery = delivery_status(filters)
        story.append(Paragraph("Estados de entrega", styles["H2"]))
        story.append(_df_to_table(df_delivery, max_rows=15))
        story.append(Spacer(1, 10))
    except ImportError:
        pass
    except Exception as e:
        story.append(Paragraph(f"<i>Error cargando estados de entrega: {e}</i>", styles["Small"]))
        story.append(Spacer(1, 10))

    # --- Métodos de pago ---
    try:
        from src.services import payment_methods
        df_pay = payment_methods(filters)
        story.append(Paragraph("Métodos de pago", styles["H2"]))
        story.append(_df_to_table(df_pay, max_rows=15))
        story.append(Spacer(1, 10))
    except ImportError:
        pass
    except Exception as e:
        story.append(Paragraph(f"<i>Error cargando métodos de pago: {e}</i>", styles["Small"]))
        story.append(Spacer(1, 10))
    
    # Construir PDF
    doc.build(story)
    buf.seek(0)
    return buf.getvalue()
