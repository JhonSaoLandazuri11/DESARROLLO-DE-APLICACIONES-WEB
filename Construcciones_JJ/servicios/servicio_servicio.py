from modelos.db import db
from MySQLdb.cursors import DictCursor

# =========================
# LISTAR SERVICIOS
# =========================
def obtener_servicios():
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("""
        SELECT 
            s.id_servicio,
            s.tipo_identificacion,
            s.tipo_servicio,
            s.estado_servicio,
            s.costo_estimado,
            s.fecha_solicitud,
            s.fecha_estimada,
            s.fecha_inicio,
            s.descripcion,
            s.RUC_empresa,
            s.id_cliente,
            c.nombres AS cliente_nombre,
            c.cedula AS cliente_cedula
        FROM servicio s
        LEFT JOIN cliente c ON s.id_cliente = c.id_cliente
        WHERE s.estado_servicio = 1
        ORDER BY s.id_servicio DESC
    """)
    
    return cursor.fetchall()
# =========================
# GUARDAR SERVICIO
# =========================
def guardar_servicio(tipo_identificacion, tipo_servicio, estado_servicio,
                     costo_estimado, fecha_solicitud, fecha_estimada,
                     fecha_inicio, descripcion, RUC_empresa, id_cliente):

    cursor = db.connection.cursor()

    cursor.execute("""
        INSERT INTO servicio (
            tipo_identificacion,
            tipo_servicio,
            estado_servicio,
            costo_estimado,
            fecha_solicitud,
            fecha_estimada,
            fecha_inicio,
            descripcion,
            RUC_empresa,
            id_cliente
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        tipo_identificacion,
        tipo_servicio,
        estado_servicio,
        costo_estimado,
        fecha_solicitud,
        fecha_estimada,
        fecha_inicio,
        descripcion,
        RUC_empresa,
        id_cliente
    ))

    db.connection.commit()

# =========================
# OBTENER SERVICIO POR ID
# =========================
def obtener_servicios():
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("""
        SELECT 
            s.id_servicio,
            s.Tipo_Identificacion AS tipo_identificacion,
            s.Tipo_servicio AS tipo_servicio,
            s.Estado_Servicio AS estado_servicio,
            s.Costo_estimado AS costo_estimado,
            s.Fecha_solicitud AS fecha_solicitud,
            s.Fecha_estimada AS fecha_estimada,
            s.Fecha_inicio AS fecha_inicio,
            s.Descripcion AS descripcion,
            s.RUC_empresa AS ruc_empresa,
            s.id_cliente,
            c.nombres AS cliente_nombre,
            c.cedula AS cliente_cedula
        FROM servicio s
        LEFT JOIN cliente c ON s.id_cliente = c.id_cliente
        WHERE s.Estado_Servicio = 1
        ORDER BY s.id_servicio DESC
    """)
    return cursor.fetchall()
# =========================
# ACTUALIZAR SERVICIO
# =========================
def actualizar_servicio(id, tipo_identificacion, tipo_servicio, estado_servicio,
                       costo_estimado, fecha_solicitud, fecha_estimada,
                       fecha_inicio, descripcion, RUC_empresa, id_cliente):

    cursor = db.connection.cursor()

    cursor.execute("""
        UPDATE servicio SET
            tipo_identificacion=%s,
            tipo_servicio=%s,
            estado_servicio=%s,
            costo_estimado=%s,
            fecha_solicitud=%s,
            fecha_estimada=%s,
            fecha_inicio=%s,
            descripcion=%s,
            RUC_empresa=%s,
            id_cliente=%s
        WHERE id_servicio=%s
    """, (
        tipo_identificacion,
        tipo_servicio,
        estado_servicio,
        costo_estimado,
        fecha_solicitud,
        fecha_estimada,
        fecha_inicio,
        descripcion,
        RUC_empresa,
        id_cliente,
        id
    ))

    db.connection.commit()

# =========================
# ELIMINAR SERVICIO (Borrado lógico)
# =========================
def eliminar_servicio(id):
    cursor = db.connection.cursor()
    cursor.execute("UPDATE servicio SET estado_servicio = 0 WHERE id_servicio = %s", (id,))
    db.connection.commit()