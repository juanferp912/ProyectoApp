# src/ui/components/charts.py
import plotly.graph_objects as go
import plotly.express as px

def line_ingreso_por_mes(df):
    if df.empty: 
        return None
    d = df.copy()
    d["anio_mes"] = d["ano"].astype(str) + "-" + d["mes"].astype(str)
    fig = px.line(d, x="anio_mes", y="ingreso_total", markers=True, title="Ingreso total por mes")
    return fig

def bar_unidades_por_mes(df):
    if df.empty:
        return None
    d = df.copy()
    d["anio_mes"] = d["ano"].astype(str) + "-" + d["mes"].astype(str)
    fig = px.bar(d, x="anio_mes", y="cantidad_total", title="Unidades por mes")
    return fig

def treemap_city_store_numbers_on_deep(df_cs):
    """
    df_cs: columnas ['ciudad','nombre_tienda','ingreso']
    Muestra números solo cuando el nodo tiene parent != "" (o sea, tiendas y niveles profundos).
    """
    if df_cs.empty: 
        return None

    # Preparamos nodos: ciudades (parents=""), tiendas (parent=ciudad)
    cities = df_cs["ciudad"].dropna().unique().tolist()
    labels, parents, values = [], [], []

    # Ciudades
    for c in cities:
        labels.append(c); parents.append(""); values.append(float(df_cs.loc[df_cs["ciudad"]==c, "ingreso"].sum()))

    # Tiendas
    for _, row in df_cs.iterrows():
        labels.append(row["nombre_tienda"])
        parents.append(row["ciudad"])
        values.append(float(row["ingreso"]))

    # Texto condicional: solo números cuando parent != ""
    text = []
    for l, p, v in zip(labels, parents, values):
        if p == "":  # ciudad (nivel raíz)
            text.append(f"{l}")
        else:        # tienda
            text.append(f"{l}<br>${v:,.2f}")

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        text=text,              # texto ya resuelto por nodo
        textinfo="text",        # usamos solo nuestro texto
        hovertemplate="<b>%{label}</b><br>Ingreso: $%{value:,.2f}<extra></extra>",
        branchvalues="total"    # suma de hijos = valor del padre
    ))
    fig.update_layout(
        title="Treemap por ciudad/tienda",
        height=720,
        margin=dict(t=60,l=6,r=6,b=6)
    )
    return fig
