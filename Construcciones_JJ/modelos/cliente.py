
from flask_login import UserMixin

class Clientes(UserMixin):
    def __init__(self, id_cliente, nombres, direccion, telefono, email, cedula, tipo_identificacion, tipo_cliente):
        self.id_cliente = id_cliente
        self.nombres = nombres
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.cedula = cedula
        self.tipo_identificacion = tipo_identificacion
        self.tipo_cliente = tipo_cliente

    # 🔴 CLAVE: Flask-Login usa este método
    def get_id(self):
        return str(self.id_cliente)

    # 🔴 opcional pero recomendado
    @property
    def id(self):
        return self.id_cliente