# conexion/db.py

import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Servicios_m_mecanica',  # Ajustar al nombre real
            user='root',
            password='123456'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()