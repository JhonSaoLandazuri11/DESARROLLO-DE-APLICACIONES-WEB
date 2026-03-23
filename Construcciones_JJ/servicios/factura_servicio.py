from modelos.factura import Factura
from modelos.db import db

def crear_factura(fecha, total, id_servicio):
    factura = Factura(
        fecha=fecha,
        total=total,
        id_servicio=id_servicio
    )
    db.session.add(factura)
    db.session.commit()
    return factura

def obtener_facturas():
    return Factura.query.all()