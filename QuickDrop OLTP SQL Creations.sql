-- =========================
-- 📦 BASE DE DATOS OLTP: QUICKDROP
-- =========================

-- 1. Tabla: Cliente
CREATE TABLE cliente (
  id_cliente SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(100) UNIQUE,
  telefono VARCHAR(20),
  direccion TEXT NOT NULL,
  ciudad VARCHAR(50),
  fecha_registro DATE DEFAULT CURRENT_DATE
);

-- 2. Tabla: Tienda
CREATE TABLE tienda (
  id_tienda SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  tipo VARCHAR(50), 
  direccion TEXT NOT NULL,
  ciudad VARCHAR(50),
  estado BOOLEAN DEFAULT TRUE
);

-- 3. Tabla: Categoría
CREATE TABLE categoria (
  id_categoria SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);

-- 4. Tabla: Producto
CREATE TABLE producto (
  id_producto SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  precio NUMERIC(6,2) NOT NULL,
  stock INT NOT NULL,
  id_tienda INT REFERENCES tienda(id_tienda) ON DELETE CASCADE,
  id_categoria INT REFERENCES categoria(id_categoria)
);

-- 5. Tabla: Pedido
CREATE TABLE pedido (
  id_pedido SERIAL PRIMARY KEY,
  id_cliente INT REFERENCES cliente(id_cliente),
  fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  estado VARCHAR(30) DEFAULT 'pendiente' 
);

-- 6. Tabla: Detalle_Pedido
CREATE TABLE detalle_pedido (
  id_detalle SERIAL PRIMARY KEY,
  id_pedido INT REFERENCES pedido(id_pedido) ON DELETE CASCADE,
  id_producto INT REFERENCES producto(id_producto),
  cantidad INT NOT NULL,
  precio_unitario NUMERIC(6,2) NOT NULL
);

-- 7. Tabla: Repartidor
CREATE TABLE repartidor (
  id_repartidor SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  telefono VARCHAR(15),
  zona VARCHAR(50),
  placa_moto VARCHAR(10),
  disponible BOOLEAN DEFAULT TRUE
);

-- 8. Tabla: Entrega
CREATE TABLE entrega (
  id_entrega SERIAL PRIMARY KEY,
  id_pedido INT REFERENCES pedido(id_pedido) ON DELETE CASCADE,
  id_repartidor INT REFERENCES repartidor(id_repartidor),
  fecha_entrega TIMESTAMP,
  estado_entrega VARCHAR(30) DEFAULT 'en camino' 
);

-- 9. Tabla: Pago
CREATE TABLE pago (
  id_pago SERIAL PRIMARY KEY,
  id_pedido INT REFERENCES pedido(id_pedido) ON DELETE CASCADE,
  metodo_pago VARCHAR(30), 
  total NUMERIC(8,2) NOT NULL,
  estado_pago VARCHAR(30) DEFAULT 'pendiente' 
);



