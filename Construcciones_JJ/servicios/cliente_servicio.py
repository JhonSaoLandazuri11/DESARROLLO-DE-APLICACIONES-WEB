from modelos.cliente import Cliente
from modelos.db import db

def obtener_clientes():
    return Cliente.query.all()

def obtener_cliente(id):
    return Cliente.query.get(id)

def crear_cliente(nombre, apellido, telefono, email):
    nuevo = Cliente(
        nombre=nombre,
        apellido=apellido,
        telefono=telefono,
        email=email
    )
    db.session.add(nuevo)
    db.session.commit()
    return nuevo

def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()