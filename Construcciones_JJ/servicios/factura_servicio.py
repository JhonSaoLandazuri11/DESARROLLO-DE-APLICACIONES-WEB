from modelos.db import db
from MySQLdb.cursors import DictCursor

def guardar_factura(numero, subtotal, descuento, iva, total, forma_pago, estado_pago, id_servicio, id_cliente):
    cursor = db.connection.cursor()
    cursor.execute("""
        INSERT INTO factura (
            Numero_factura, Sub_total, Descuento, IVA, Total_pago,
            Forma_pago, Estado_pago, Id_servicio, Id_cliente
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (numero, subtotal, descuento, iva, total, forma_pago, estado_pago, id_servicio, id_cliente))
    
    db.connection.commit()


def obtener_factura(id):
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("""
        SELECT f.*, c.nombres, c.cedula, s.tipo_servicio, s.descripcion
        FROM factura f
        JOIN cliente c ON f.Id_cliente = c.id_cliente
        JOIN servicio s ON f.Id_servicio = s.id_servicio
        WHERE f.Id_factura = %s
    """, (id,))
    return cursor.fetchone()