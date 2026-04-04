class Pago:
    def __init__(self, id_pago=None, fecha_pago=None, monto=None, id_factura=None):
        self.id_pago = id_pago
        self.fecha_pago = fecha_pago
        self.monto = monto
        self.id_factura = id_factura