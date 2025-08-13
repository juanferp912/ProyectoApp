-- 1. DIM_CLIENTE
CREATE TABLE dim_cliente (
    cliente_key SERIAL PRIMARY KEY,
    id_cliente INT,
    nombre_cliente VARCHAR(100),
    correo VARCHAR(100),
    ciudad VARCHAR(50),
    fecha_registro DATE
);

-- 2. DIM_TIENDA
CREATE TABLE dim_tienda (
    tienda_key SERIAL PRIMARY KEY,
    id_tienda INT,
    nombre_tienda VARCHAR(100),
    tipo VARCHAR(50),
    ciudad VARCHAR(50),
    estado_tienda BOOLEAN
);

-- 3. DIM_REPARTIDOR
CREATE TABLE dim_repartidor (
    repartidor_key SERIAL PRIMARY KEY,
    id_repartidor INT,
    nombre_repartidor VARCHAR(100),
    zona VARCHAR(50),
    placa_moto VARCHAR(10)
);

-- 4. DIM_PRODUCTO
CREATE TABLE dim_producto (
    producto_key SERIAL PRIMARY KEY,
    id_producto INT,
    nombre_producto VARCHAR(100),
    descripcion TEXT,
    precio_base NUMERIC(6,2),
    categoria VARCHAR(50)
);

-- 5. DIM_PAGO
CREATE TABLE dim_pago (
    pago_key SERIAL PRIMARY KEY,
    metodo_pago VARCHAR(30),
    estado_pago VARCHAR(30)
);

-- 6. DIM_FECHA
CREATE TABLE dim_fecha (
    fecha_key SERIAL PRIMARY KEY,
    fecha DATE UNIQUE,
    ano INT,
    mes INT,
    dia INT,
    trimestre INT,
    dia_semana VARCHAR(10)
);


CREATE TABLE hechos_ventas (
    venta_key SERIAL PRIMARY KEY,
    fecha_key INT REFERENCES dim_fecha(fecha_key),
    cliente_key INT REFERENCES dim_cliente(cliente_key),
    producto_key INT REFERENCES dim_producto(producto_key),
    tienda_key INT REFERENCES dim_tienda(tienda_key),
    repartidor_key INT REFERENCES dim_repartidor(repartidor_key),
    pago_key INT REFERENCES dim_pago(pago_key),
    cantidad INT,
    precio_unitario NUMERIC(6,2),
    subtotal NUMERIC(8,2),
    total_pago NUMERIC(8,2),
    tiempo_entrega TEXT,
    estado_entrega VARCHAR(30)
);