# modelos/servicio.py

class Servicio:
    def __init__(self, id_servicio, descripcion, costo, fecha_inicio, fecha_fin, estado, id_cliente):
        self.id_servicio = id_servicio
        self.descripcion = descripcion
        self.costo = costo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.id_cliente = id_cliente

    # =========================
    # 🔹 Convertir a TUPLA
    # =========================
    def to_tuple(self):
        return (
            self.id_servicio,
            self.descripcion,
            self.costo,
            self.fecha_inicio,
            self.fecha_fin,
            self.estado,
            self.id_cliente
        )

    # =========================
    # 🔹 Convertir a DICCIONARIO
    # =========================
    def to_dict(self):
        return {
            'id_servicio': self.id_servicio,
            'descripcion': self.descripcion,
            'costo': self.costo,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'estado': self.estado,
            'id_cliente': self.id_cliente
        }

    # =========================
    # 🔹 Convertir a LISTA
    # =========================
    def to_list(self):
        return [
            self.id_servicio,
            self.descripcion,
            self.costo,
            self.fecha_inicio,
            self.fecha_fin,
            self.estado,
            self.id_cliente
        ]