# src/models.py
from __future__ import annotations
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, Text, ForeignKey

Base = declarative_base()

class DimCliente(Base):
    __tablename__ = "dim_cliente"
    cliente_key = Column(Integer, primary_key=True)
    id_cliente = Column(Integer)
    nombre_cliente = Column(String(100))
    correo = Column(String(100))
    ciudad = Column(String(50))
    fecha_registro = Column(Date)

class DimTienda(Base):
    __tablename__ = "dim_tienda"
    tienda_key = Column(Integer, primary_key=True)
    id_tienda = Column(Integer)
    nombre_tienda = Column(String(100))
    tipo = Column(String(50))
    ciudad = Column(String(50))
    estado_tienda = Column(Boolean)

class DimRepartidor(Base):
    __tablename__ = "dim_repartidor"
    repartidor_key = Column(Integer, primary_key=True)
    id_repartidor = Column(Integer)
    nombre_repartidor = Column(String(100))
    zona = Column(String(50))
    placa_moto = Column(String(10))

class DimProducto(Base):
    __tablename__ = "dim_producto"
    producto_key = Column(Integer, primary_key=True)
    id_producto = Column(Integer)
    nombre_producto = Column(String(100))
    descripcion = Column(Text)
    precio_base = Column(Numeric(6,2))
    categoria = Column(String(50))

class DimPago(Base):
    __tablename__ = "dim_pago"
    pago_key = Column(Integer, primary_key=True)
    metodo_pago = Column(String(30))
    estado_pago = Column(String(30))

class DimFecha(Base):
    __tablename__ = "dim_fecha"
    fecha_key = Column(Integer, primary_key=True)  # SERIAL en DB; aquí lo tratamos como int
    fecha = Column(Date, unique=True)
    ano = Column(Integer)
    mes = Column(Integer)
    dia = Column(Integer)
    trimestre = Column(Integer)
    dia_semana = Column(String(10))

class HechosVentas(Base):
    __tablename__ = "hechos_ventas"
    venta_key = Column(Integer, primary_key=True)
    fecha_key = Column(Integer, ForeignKey("dim_fecha.fecha_key"))
    cliente_key = Column(Integer, ForeignKey("dim_cliente.cliente_key"))
    producto_key = Column(Integer, ForeignKey("dim_producto.producto_key"))
    tienda_key = Column(Integer, ForeignKey("dim_tienda.tienda_key"))
    repartidor_key = Column(Integer, ForeignKey("dim_repartidor.repartidor_key"))
    pago_key = Column(Integer, ForeignKey("dim_pago.pago_key"))
    cantidad = Column(Integer)
    precio_unitario = Column(Numeric(6,2))
    subtotal = Column(Numeric(8,2))
    total_pago = Column(Numeric(8,2))
    tiempo_entrega = Column(Text)
    estado_entrega = Column(String(30))
