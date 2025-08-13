# src/queries.py
from __future__ import annotations

def where_and_params(years, months, ciudades, categorias, metodos, date_from=None, date_to=None):
    # Nota: dejamos years/months por compatibilidad (puedes retirarlos luego si no los usas)
    where, params = [], {}
    if years:      where.append("df.ano = ANY(:years)");              params["years"] = years
    if months:     where.append("df.mes = ANY(:months)");             params["months"] = months
    if ciudades:   where.append("dt.ciudad = ANY(:ciudades)");        params["ciudades"] = ciudades
    if categorias: where.append("dp.categoria = ANY(:categorias)");   params["categorias"] = categorias
    if metodos:    where.append("dpg.metodo_pago = ANY(:metodos)");   params["metodos"]  = metodos
    if date_from:  where.append("df.fecha >= :date_from");            params["date_from"] = date_from
    if date_to:    where.append("df.fecha <= :date_to");              params["date_to"]   = date_to
    return ("WHERE " + " AND ".join(where)) if where else "", params

SQL = {
    "trend": """
        SELECT df.ano, df.mes,
               SUM(hv.total_pago)::numeric(14,2) AS ingreso_total,
               SUM(hv.cantidad)                  AS cantidad_total,
               COUNT(*)                           AS transacciones
        FROM hechos_ventas hv
        JOIN dim_fecha df   ON hv.fecha_key   = df.fecha_key
        JOIN dim_tienda dt  ON hv.tienda_key  = dt.tienda_key
        JOIN dim_producto dp ON hv.producto_key = dp.producto_key
        JOIN dim_pago dpg   ON hv.pago_key    = dpg.pago_key
        {where}
        GROUP BY df.ano, df.mes
        ORDER BY df.ano, df.mes;
    """,
    "top_products": """
        SELECT dp.categoria, dp.nombre_producto,
               SUM(hv.cantidad)                  AS unidades,
               SUM(hv.total_pago)::numeric(14,2) AS ingreso
        FROM hechos_ventas hv
        JOIN dim_producto dp ON hv.producto_key = dp.producto_key
        JOIN dim_fecha df    ON hv.fecha_key    = df.fecha_key
        JOIN dim_tienda dt   ON hv.tienda_key   = dt.tienda_key
        JOIN dim_pago dpg    ON hv.pago_key     = dpg.pago_key
        {where}
        GROUP BY dp.categoria, dp.nombre_producto
        ORDER BY ingreso DESC
        LIMIT :limit;
    """,
    "city_store": """
        SELECT dt.ciudad, dt.nombre_tienda,
               SUM(hv.total_pago)::numeric(14,2) AS ingreso,
               SUM(hv.cantidad)                  AS unidades
        FROM hechos_ventas hv
        JOIN dim_tienda dt ON hv.tienda_key = dt.tienda_key
        JOIN dim_fecha  df ON hv.fecha_key  = df.fecha_key
        JOIN dim_producto dp ON hv.producto_key = dp.producto_key
        JOIN dim_pago dpg ON hv.pago_key = dpg.pago_key
        {where}
        GROUP BY dt.ciudad, dt.nombre_tienda
        ORDER BY dt.ciudad, ingreso DESC;
    """,
    "pay_mix": """
        SELECT dpg.metodo_pago,
               SUM(hv.total_pago)::numeric(14,2) AS ingreso,
               COUNT(*) AS transacciones
        FROM hechos_ventas hv
        JOIN dim_pago dpg ON hv.pago_key = dpg.pago_key
        JOIN dim_fecha df ON hv.fecha_key = df.fecha_key
        JOIN dim_tienda dt ON hv.tienda_key = dt.tienda_key
        JOIN dim_producto dp ON hv.producto_key = dp.producto_key
        {where}
        GROUP BY dpg.metodo_pago
        ORDER BY ingreso DESC;
    """,
    "delivery_status": """
        SELECT hv.estado_entrega,
               COUNT(*) AS entregas,
               SUM(hv.total_pago)::numeric(14,2) AS ingreso
        FROM hechos_ventas hv
        JOIN dim_fecha df ON hv.fecha_key = df.fecha_key
        JOIN dim_tienda dt ON hv.tienda_key = dt.tienda_key
        JOIN dim_producto dp ON hv.producto_key = dp.producto_key
        JOIN dim_pago dpg ON hv.pago_key = dpg.pago_key
        {where}
        GROUP BY hv.estado_entrega
        ORDER BY entregas DESC;
    """,
    "top_clients": """
        SELECT dc.nombre_cliente, dc.ciudad,
               COUNT(*) AS pedidos,
               SUM(hv.total_pago)::numeric(14,2) AS ingreso
        FROM hechos_ventas hv
        JOIN dim_cliente dc ON hv.cliente_key = dc.cliente_key
        JOIN dim_fecha df   ON hv.fecha_key   = df.fecha_key
        JOIN dim_tienda dt  ON hv.tienda_key  = dt.tienda_key
        JOIN dim_producto dp ON hv.producto_key = dp.producto_key
        JOIN dim_pago dpg   ON hv.pago_key    = dpg.pago_key
        {where}
        GROUP BY dc.nombre_cliente, dc.ciudad
        ORDER BY ingreso DESC
        LIMIT :limit;
    """,
    "top_couriers": """
        SELECT dr.nombre_repartidor, dr.zona, dr.placa_moto,
               COUNT(*) AS entregas,
               SUM(hv.total_pago)::numeric(14,2) AS ingreso
        FROM hechos_ventas hv
        JOIN dim_repartidor dr ON hv.repartidor_key = dr.repartidor_key
        JOIN dim_fecha df   ON hv.fecha_key   = df.fecha_key
        JOIN dim_tienda dt  ON hv.tienda_key  = dt.tienda_key
        JOIN dim_producto dp ON hv.producto_key = dp.producto_key
        JOIN dim_pago dpg   ON hv.pago_key    = dpg.pago_key
        {where}
        GROUP BY dr.nombre_repartidor, dr.zona, dr.placa_moto
        ORDER BY entregas DESC, ingreso DESC
        LIMIT :limit;
    """,
    "clients_by_city": """
        SELECT dc.ciudad,
               COUNT(DISTINCT dc.cliente_key) as clientes_unicos,
               SUM(hv.total_pago)::numeric(14,2) as ingreso
        FROM hechos_ventas hv
        JOIN dim_cliente dc ON hv.cliente_key = dc.cliente_key
        JOIN dim_fecha df   ON hv.fecha_key   = df.fecha_key
        JOIN dim_tienda dt  ON hv.tienda_key  = dt.tienda_key
        JOIN dim_producto dp ON hv.producto_key = dp.producto_key
        JOIN dim_pago dpg   ON hv.pago_key    = dpg.pago_key
        {where}
        GROUP BY dc.ciudad
        ORDER BY ingreso DESC;
    """,
}
