# conexion/db.py

import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='metalmecanica_jj',
            user='root',
            password=''
        )
        return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


def init_db():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()

        # Tabla cliente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                telefono VARCHAR(15),
                email VARCHAR(100)
            )
        ''')

        # Tabla empresa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empresa (
                ruc VARCHAR(20) PRIMARY KEY,
                nombre VARCHAR(100),
                direccion VARCHAR(150),
                telefono VARCHAR(15)
            )
        ''')

        # Tabla servicios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicios (
                id_servicio INT AUTO_INCREMENT PRIMARY KEY,
                descripcion TEXT,
                costo DECIMAL(10,2),
                fecha_inicio DATE,
                fecha_fin DATE,
                estado VARCHAR(50),
                id_cliente INT,
                FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
            )
        ''')

        # Tabla factura
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS factura (
                id_factura INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE,
                total DECIMAL(10,2),
                id_servicio INT,
                FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
            )
        ''')

        # Tabla pago
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pago (
                id_pago INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE,
                monto DECIMAL(10,2),
                id_factura INT,
                FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()