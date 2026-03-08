# Se realizará la persistencia de datos de archivos

from pathlib import Path
import json
import csv

DATA_DIR = Path(__file__).parent / "data"
TXT_FILE = DATA_DIR / "datos.txt"
CSV_FILE = DATA_DIR / "datos.csv"
JSON_FILE = DATA_DIR / "datos.json"

# Asegurar la carpeta data
def asegurar_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# crear carpeta al iniciar
asegurar_data_dir()


# Guardar datos en un archivo de texto
def guardar_txt(registro: str):
    with open(TXT_FILE, "a", encoding="utf-8") as file:
        file.write(f"{registro}\n")


# Leer datos de un archivo de texto
def leer_txt():
    if not TXT_FILE.exists():
        return []
    with open(TXT_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


# Guardar datos en un archivo CSV
def guardar_csv(registro: dict):
    existe = CSV_FILE.exists()

    with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        if not existe:
            writer.writerow(['nombre', 'precio', 'cantidad', 'descripcion'])

        writer.writerow([
            registro["nombre"],
            registro["precio"],
            registro["cantidad"],
            registro["descripcion"]
        ])


# Leer datos de un archivo CSV
def leer_csv():
    if not CSV_FILE.exists():
        return []

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        return [row for row in reader if row]


# Leer el JSON
def leer_json():
    if not JSON_FILE.exists():
        return []

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# Guardar datos en un archivo JSON
def guardar_json(registro: dict):
    data = leer_json()
    data.append(registro)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)