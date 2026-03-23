# modelos/orm.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# =========================
# 👤 CLIENTE
# =========================
class ClienteORM(db.Model):
    __tablename__ = 'cliente'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(100))

    # Relación: un cliente tiene muchos servicios
    servicios = db.relationship('ServicioORM', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellido}>'

# =========================
# 🧩 SERVICIOS
# =========================
class ServicioORM(db.Model):
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

    def __repr__(self):
        return f'<Servicio {self.descripcion}>'

# =========================
# 🧾 FACTURA
# =========================
class FacturaORM(db.Model):
    __tablename__ = 'factura'

    id_factura = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    total = db.Column(db.Float)

    id_servicio = db.Column(
        db.Integer,
        db.ForeignKey('servicios.id_servicio')
    )

    def __repr__(self):
        return f'<Factura {self.id_factura}>'

# =========================
# 💳 PAGO
# =========================
class PagoORM(db.Model):
    __tablename__ = 'pago'

    id_pago = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    monto = db.Column(db.Float)

    id_factura = db.Column(
        db.Integer,
        db.ForeignKey('factura.id_factura')
    )

    def __repr__(self):
        return f'<Pago {self.id_pago}>'

# =========================
# 🏢 EMPRESA
# =========================
class EmpresaORM(db.Model):
    __tablename__ = 'empresa'

    ruc = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(150))
    telefono = db.Column(db.String(15))

    def __repr__(self):
        return f'<Empresa {self.nombre}>'