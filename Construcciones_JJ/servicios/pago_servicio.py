from modelos.pago import Pago
from modelos.db import db

def crear_pago(fecha, monto, id_factura):
    pago = Pago(
        fecha=fecha,
        monto=monto,
        id_factura=id_factura
    )
    db.session.add(pago)
    db.session.commit()
    return pago

def obtener_pagos():
    return Pago.query.all()