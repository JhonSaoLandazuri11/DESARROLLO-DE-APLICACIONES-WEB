from conexion.db import get_connection
from decimal import Decimal

class Servicios:
    def __init__(self):
        self.servicios = {}

    # cargar servicios desde la BD
    def cargar_desde_db(self):
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM servicios')

            for row in cursor.fetchall():
                self.servicios[row['id_servicio']] = row

            cursor.close()
            conn.close()

    # listar servicios
    def listar_servicios(self):
        return list(self.servicios.values())

    # buscar por descripción
    def buscar_por_descripcion(self, texto):
        texto = texto.lower().strip()
        resultados = []

        for servicio in self.servicios.values():
            if texto in servicio['descripcion'].lower():
                resultados.append(servicio)

        return resultados

    # agregar servicio
    def agregar_servicio(self, descripcion, costo, fecha_inicio, fecha_fin, estado, id_cliente):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO servicios (descripcion, costo, fecha_inicio, fecha_fin, estado, id_cliente)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (descripcion, float(costo), fecha_inicio, fecha_fin, estado, id_cliente))

            conn.commit()
            nuevo_id = cursor.lastrowid

            # guardar en memoria
            self.servicios[nuevo_id] = {
                'id_servicio': nuevo_id,
                'descripcion': descripcion,
                'costo': float(costo),
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'estado': estado,
                'id_cliente': id_cliente
            }

            cursor.close()
            conn.close()

    # actualizar servicio
    def actualizar_servicio(self, id_servicio, descripcion, costo, fecha_inicio, fecha_fin, estado, id_cliente):
        id_servicio = int(id_servicio)

        if id_servicio not in self.servicios:
            return False

        conn = get_connection()
        if conn:
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE servicios 
                SET descripcion=%s, costo=%s, fecha_inicio=%s, fecha_fin=%s, estado=%s, id_cliente=%s
                WHERE id_servicio=%s
            ''', (descripcion, float(costo), fecha_inicio, fecha_fin, estado, id_cliente, id_servicio))

            conn.commit()

            # actualizar en memoria
            self.servicios[id_servicio].update({
                'descripcion': descripcion,
                'costo': float(costo),
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'estado': estado,
                'id_cliente': id_cliente
            })

            cursor.close()
            conn.close()
            return True

    # eliminar servicio
    def eliminar_servicio(self, id_servicio):
        if id_servicio in self.servicios:
            conn = get_connection()
            if conn:
                cursor = conn.cursor()

                cursor.execute('DELETE FROM servicios WHERE id_servicio=%s', (id_servicio,))
                conn.commit()

                self.servicios.pop(id_servicio)

                cursor.close()
                conn.close()