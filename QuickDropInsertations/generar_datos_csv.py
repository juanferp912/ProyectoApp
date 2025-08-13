import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker('es_ES')
carpeta_salida = "csv_quickdrop"
os.makedirs(carpeta_salida, exist_ok=True)

# ================================================
# 1. CLIENTES (500)
# ================================================
clientes_ids = list(range(1, 501))
with open(f"{carpeta_salida}/clientes.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['nombre', 'correo', 'telefono', 'direccion', 'ciudad', 'fecha_registro'])
    for _ in clientes_ids:
        writer.writerow([
            fake.name(),
            fake.unique.email(),
            fake.phone_number(),
            fake.address().replace("\n", ", "),
            fake.city(),
            datetime.now().date()
        ])

# ================================================
# 2. TIENDAS (500)
# ================================================
tipos_tienda = ['Restaurante', 'Farmacia', 'Papelería', 'Ferretería', 'Ropa', 'Tecnología', 'MiniMarket']
tiendas_ids = list(range(1, 501))
with open(f"{carpeta_salida}/tiendas.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['nombre', 'tipo', 'direccion', 'ciudad', 'estado'])
    for _ in tiendas_ids:
        writer.writerow([
            f"Tienda {fake.last_name()}",
            random.choice(tipos_tienda),
            fake.street_address(),
            fake.city(),
            True
        ])

# ================================================
# 3. CATEGORÍAS (FIJO: 10)
# ================================================
categorias = ['Comida', 'Salud', 'Oficina', 'Electrónica', 'Hogar', 'Mascotas', 'Libros', 'Ropa', 'Bebidas', 'Limpieza']
categorias_ids = list(range(1, len(categorias)+1))
with open(f"{carpeta_salida}/categorias.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['nombre'])
    for nombre in categorias:
        writer.writerow([nombre])

# ================================================
# 4. PRODUCTOS (500)
# ================================================
productos_ids = list(range(1, 501))
with open(f"{carpeta_salida}/productos.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['nombre', 'descripcion', 'precio', 'stock', 'id_tienda', 'id_categoria'])
    for _ in productos_ids:
        writer.writerow([
            fake.word().capitalize(),
            fake.sentence(),
            round(random.uniform(1.0, 100.0), 2),
            random.randint(5, 100),
            random.choice(tiendas_ids),
            random.choice(categorias_ids)
        ])

# ================================================
# 5. REPARTIDORES (500)
# ================================================
repartidores_ids = list(range(1, 501))
with open(f"{carpeta_salida}/repartidores.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['nombre', 'telefono', 'zona', 'placa_moto', 'disponible'])
    for _ in repartidores_ids:
        writer.writerow([
            fake.name(),
            fake.phone_number(),
            fake.city(),
            f"{fake.random_uppercase_letter()}{random.randint(100,999)}{fake.random_uppercase_letter()}",
            True
        ])

# ================================================
# 6. PEDIDOS (500)
# ================================================
pedidos_ids = list(range(1, 501))
estado_pedidos = ['pendiente', 'aceptado', 'entregado', 'cancelado']
with open(f"{carpeta_salida}/pedidos.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['id_cliente', 'fecha_pedido', 'estado'])
    for _ in pedidos_ids:
        writer.writerow([
            random.choice(clientes_ids),
            datetime.now() - timedelta(days=random.randint(0, 30)),
            random.choice(estado_pedidos)
        ])

# ================================================
# 7. DETALLE_PEDIDO (500)
# ================================================
with open(f"{carpeta_salida}/detalle_pedido.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['id_pedido', 'id_producto', 'cantidad', 'precio_unitario'])
    for _ in range(500):
        producto_id = random.choice(productos_ids)
        writer.writerow([
            random.choice(pedidos_ids),
            producto_id,
            random.randint(1, 5),
            round(random.uniform(1.0, 100.0), 2)
        ])

# ================================================
# 8. ENTREGAS (500)
# ================================================
estado_entrega = ['en camino', 'entregado', 'fallido']
with open(f"{carpeta_salida}/entregas.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['id_pedido', 'id_repartidor', 'fecha_entrega', 'estado_entrega'])
    for pid in pedidos_ids:
        writer.writerow([
            pid,
            random.choice(repartidores_ids),
            datetime.now() - timedelta(days=random.randint(0, 10)),
            random.choice(estado_entrega)
        ])

# ================================================
# 9. PAGOS (500)
# ================================================
metodos_pago = ['efectivo', 'tarjeta', 'transferencia']
estado_pago = ['pendiente', 'pagado', 'fallido']
with open(f"{carpeta_salida}/pagos.csv", "w", newline='', encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['id_pedido', 'metodo_pago', 'total', 'estado_pago'])
    for pid in pedidos_ids:
        writer.writerow([
            pid,
            random.choice(metodos_pago),
            round(random.uniform(5.0, 300.0), 2),
            random.choice(estado_pago)
        ])

print("✅ TODOS los archivos CSV fueron generados en la carpeta 'csv_quickdrop'")
