from modelos.empresa import Empresa
from modelos.db import db

def obtener_empresas():
    return Empresa.query.all()