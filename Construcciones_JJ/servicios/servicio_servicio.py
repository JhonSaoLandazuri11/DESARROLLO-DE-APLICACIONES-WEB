from modelos.servicio import Servicio
from modelos.db import db

def obtener_servicios():
    return Servicio.query.all()

def crear_servicio(descripcion, costo, fecha_inicio, fecha_fin, estado, id_cliente):
    nuevo = Servicio(
        descripcion=descripcion,
        costo=costo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado=estado,
        id_cliente=id_cliente
    )
    db.session.add(nuevo)
    db.session.commit()
    return nuevo

def eliminar_servicio(id):
    servicio = Servicio.query.get(id)
    if servicio:
        db.session.delete(servicio)
        db.session.commit()