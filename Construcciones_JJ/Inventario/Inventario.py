#Creación de clase Inventario
from .productos import Producto
from .Base_datos import init_db, get_connection

class Inventario:
    def __init__(self):
        self.productos = {}

    def cargar_productos(self):
        init_db()
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM productos")
            for row in cursor:
                producto = Producto(
                    id=row["id"],
                    nombre=row["nombre"],
                    precio=row["precio"],
                    cantidad=row["cantidad"],
                    descripcion=row["descripcion"]
                )
                self.productos[producto.id] = producto   # ✅ usar ID

    def listar_productos(self):
        return [p.to_tuple() for p in self.productos.values()]

    def agregar_producto(self, nombre, precio, cantidad, descripcion):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio, cantidad, descripcion) VALUES (?, ?, ?, ?)",
                (nombre, precio, cantidad, descripcion)
            )
            conn.commit()

    # ✅ EDITAR POR ID
    def editar_producto(self, id, nombre, precio, cantidad, descripcion):
        with get_connection() as conn:
            conn.execute("""
                UPDATE productos 
                SET nombre = ?, precio = ?, cantidad = ?, descripcion = ?
                WHERE id = ?
            """, (nombre, precio, cantidad, descripcion, id))
            conn.commit()

        # Actualizar también en el diccionario local
        if id in self.productos:
            producto = self.productos[id]
            producto.nombre = nombre
            producto.precio = precio
            producto.cantidad = cantidad
            producto.descripcion = descripcion

    # ✅ ELIMINAR POR ID
    def eliminar_producto(self, id):
        id = int(id)  # asegurar que sea entero
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM productos WHERE id = ?", (id,))
            conn.commit()
            print(f"Filas afectadas en la DB: {cursor.rowcount}")  # opcional debug

        # Eliminar también del diccionario local
        if id in self.productos:
            del self.productos[id]
            print(f"Producto con id {id} eliminado del diccionario local")