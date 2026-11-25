
import json
import os
from pathlib import Path
# Ruta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta donde se guardan los datos
DATA_DIR = BASE_DIR / "data"

# Archivos disponibles en el sistema
ARCHIVOS = [
    "usuarios.json",
    "donaciones.json",
    "inventario.json",
    "solicitudes.json",
    "entregas.json"
]


def inicializar_archivos():
    """
    Crea la carpeta y los archivos JSON
    si todavía no existen.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for nombre in ARCHIVOS:
        ruta = DATA_DIR / nombre

        if not ruta.exists():
            guardar_datos(nombre, [])


def leer_datos(nombre):
    """
    Lee y devuelve la información de un archivo JSON.
    """

    if nombre not in ARCHIVOS:
        raise ValueError("Archivo JSON no permitido.")

    ruta = DATA_DIR / nombre

    if not ruta.exists():
        guardar_datos(nombre, [])

    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, list):
        raise ValueError(
            f"El contenido de {nombre} debe ser una lista."
        )

    return datos


def guardar_datos(nombre, datos):
    """
    Guarda información en un archivo JSON.
    Utiliza un archivo temporal para reducir
    el riesgo de dejar datos escritos a medias.
    """

    if nombre not in ARCHIVOS:
        raise ValueError("Archivo JSON no permitido.")

    if not isinstance(datos, list):
        raise ValueError("Los datos deben ser una lista.")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    ruta = DATA_DIR / nombre
    temporal = DATA_DIR / f"{nombre}.tmp"

    with open(temporal, "w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    os.replace(temporal, ruta)

