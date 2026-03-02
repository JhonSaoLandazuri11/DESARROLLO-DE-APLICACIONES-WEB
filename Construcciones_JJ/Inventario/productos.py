#Creacion de Clase Producto

class Producto:
    def __init__(self, id=None, nombre="", precio=0.0, cantidad=0, descripcion=""):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.descripcion = descripcion

    def __str__(self):
        return f"Producto: {self.nombre}, Precio: {self.precio}, Cantidad: {self.cantidad}, Descripción: {self.descripcion}"
    
    # Para INSERT en la BD (NO incluye el id porque es AUTOINCREMENT)
    def to_tuple(self):
        return (self.nombre, self.precio, self.cantidad, self.descripcion)
    
    # Para trabajar como diccionario (útil en templates o APIs)
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "descripcion": self.descripcion
        }