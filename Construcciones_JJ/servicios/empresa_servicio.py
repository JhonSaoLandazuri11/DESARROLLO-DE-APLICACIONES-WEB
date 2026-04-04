from modelos.db import db
from MySQLdb.cursors import DictCursor

def listar_empresas():
    cursor = db.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM empresa")
    return cursor.fetchall()