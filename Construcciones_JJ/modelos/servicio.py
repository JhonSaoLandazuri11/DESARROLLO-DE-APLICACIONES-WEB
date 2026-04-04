class Servicio:
    def __init__(self, id_servicio=None, descripcion=None, costo=None,
                 fecha_inicio=None, fecha_fin=None, estado=None, id_cliente=None):
        
        self.id_servicio = id_servicio
        self.descripcion = descripcion
        self.costo = costo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.id_cliente = id_cliente