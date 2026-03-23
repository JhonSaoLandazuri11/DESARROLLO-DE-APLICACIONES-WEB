from .db import db

class Servicio(db.Model):
    __tablename__ = 'servicios'

    id_servicio = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(50))

    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey('cliente.id_cliente'),
        nullable=False
    )