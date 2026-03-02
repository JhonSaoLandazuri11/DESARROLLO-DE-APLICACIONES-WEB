#Conexión a SQlite

import sqlite3
from sqlite3 import Error
from pathlib import Path

#Se creara el inventario en la carpeta data.
db_path = Path(__file__).parent/"data" / "inventario.db"

def get_connection():
    db_path.parent.mkdir(parents=True, exist_ok=True)
    Conn = sqlite3.connect(db_path)
    Conn.row_factory = sqlite3.Row
    return Conn

def init_db():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                descripcion TEXT
            )
        ''')
        conn.commit()