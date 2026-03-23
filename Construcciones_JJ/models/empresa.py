from .db import db

class Empresa(db.Model):
    __tablename__ = 'empresa'

    ruc = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(150))
    telefono = db.Column(db.String(15))