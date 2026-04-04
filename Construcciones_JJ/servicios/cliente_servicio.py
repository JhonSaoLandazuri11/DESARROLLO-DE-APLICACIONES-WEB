from modelos.db import db
from modelos.cliente import Clientes
from MySQLdb.cursors import DictCursor

# =========================
# LISTAR CLIENTES
# =========================
def listar_clientes():
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM cliente")
    datos = cursor.fetchall()

    print("DATOS BD:", datos)  # 🔥 AQUI

    clientes = []
    for fila in datos:
        cliente = Clientes(
            id_cliente=fila.get('id_cliente'),
            nombres=fila.get('nombres'),
            direccion=fila.get('direccion'),
            telefono=fila.get('telefono'),
            email=fila.get('email'),
            cedula=fila.get('cedula'),
            tipo_identificacion=fila.get('tipo_identificacion'),
            tipo_cliente=fila.get('tipo_cliente')
        )
        clientes.append(cliente)

    print("CLIENTES OBJETOS:", clientes)  # 🔥 AQUI

    return clientes

# =========================
# OBTENER CLIENTE POR EMAIL
# =========================
def obtener_cliente_por_email(email):
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM cliente WHERE email = %s", (email,))
    return cursor.fetchone()

# =========================
# CREAR CLIENTE (REGISTRO)
# =========================
def crear_cliente(nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente, password):
    cursor = db.connection.cursor()
    cursor.execute("""
        INSERT INTO cliente (nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente, password))
    db.connection.commit()

# =========================
# GUARDAR CLIENTE (CRUD)
# =========================
def guardar_cliente(nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente):
    cursor = db.connection.cursor()
    cursor.execute("""
        INSERT INTO cliente (nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente))
    db.connection.commit()

# =========================
# OBTENER CLIENTE POR ID
# =========================
def obtener_cliente(id):
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (id,))
    return cursor.fetchone()

# =========================
# ACTUALIZAR CLIENTE
# =========================
def actualizar_cliente_db(id, nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente):
    cursor = db.connection.cursor()
    cursor.execute("""
        UPDATE cliente
        SET nombres=%s, direccion=%s, telefono=%s, email=%s, cedula=%s, tipo_identificacion=%s, tipo_cliente=%s
        WHERE id_cliente=%s
    """, (nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente, id))
    db.connection.commit()

# =========================
# ELIMINAR CLIENTE
# =========================
def eliminar_cliente_db(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id,))
    db.connection.commit()