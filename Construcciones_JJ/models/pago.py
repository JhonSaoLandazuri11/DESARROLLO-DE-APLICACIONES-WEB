from .db import db

class Pago(db.Model):
    __tablename__ = 'pago'

    id_pago = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    monto = db.Column(db.Float)

    id_factura = db.Column(
        db.Integer,
        db.ForeignKey('factura.id_factura')
    )