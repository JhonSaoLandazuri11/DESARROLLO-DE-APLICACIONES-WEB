from .db import db

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(100))

    servicios = db.relationship('Servicio', backref='cliente', lazy=True)