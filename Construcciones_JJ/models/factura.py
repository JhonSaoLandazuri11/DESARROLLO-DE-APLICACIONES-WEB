from .db import db

class Factura(db.Model):
    __tablename__ = 'factura'

    id_factura = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    total = db.Column(db.Float)

    id_servicio = db.Column(
        db.Integer,
        db.ForeignKey('servicios.id_servicio')
    )