# persistencia/archivos.py

from pathlib import Path
import json
from json import JSONDecodeError
import csv

# 📁 Rutas de archivos
DATA_DIR = Path(__file__).parent / "data"
TXT_FILE = DATA_DIR / "servicios.txt"
CSV_FILE = DATA_DIR / "servicios.csv"
JSON_FILE = DATA_DIR / "servicios.json"

# 🔧 Asegurar carpeta
def asegurar_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# 📄 TXT
# =========================

def guardar_txt(registro: str):
    asegurar_data_dir()
    with open(TXT_FILE, 'a', encoding="utf-8") as f:
        f.write(registro + '\n')


def leer_txt():
    asegurar_data_dir()
    if not TXT_FILE.exists():
        return []
    with open(TXT_FILE, 'r', encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# =========================
# 🧾 JSON
# =========================

def guardar_json(dic):
    asegurar_data_dir()

    data = leer_json()
    data.append(dic)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def leer_json():
    asegurar_data_dir()

    if not JSON_FILE.exists():
        return []

    if JSON_FILE.stat().st_size == 0:
        return []

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except JSONDecodeError:
            return []

# =========================
# 📊 CSV
# =========================

def guardar_csv(dic: dict):
    """
    Guarda un servicio en CSV
    """
    asegurar_data_dir()

    campos = ["descripcion", "costo", "fecha_inicio", "fecha_fin", "estado", "id_cliente"]
    existe = CSV_FILE.exists()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)

        if not existe:
            writer.writeheader()

        writer.writerow({
            "descripcion": dic.get("descripcion", ""),
            "costo": dic.get("costo", ""),
            "fecha_inicio": dic.get("fecha_inicio", ""),
            "fecha_fin": dic.get("fecha_fin", ""),
            "estado": dic.get("estado", ""),
            "id_cliente": dic.get("id_cliente", "")
        })


def leer_csv():
    if not CSV_FILE.exists():
        return []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)