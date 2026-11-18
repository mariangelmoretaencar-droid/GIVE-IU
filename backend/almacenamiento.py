
import json
import os
from pathlib import Path
from flask import Flask, render_template, jsonify, request
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

@app.route("/api/donaciones", methods=["POST"])
def registrar_donacion():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "correcto": False,
            "mensaje": "Los datos enviados no son válidos."
        }), 400

    donante = str(datos.get("donante", "")).strip()
    telefono = str(datos.get("telefono", "")).strip()
    correo = str(datos.get("correo", "")).strip()
    observaciones = str(datos.get("observaciones", "")).strip()
    materiales = datos.get("materiales")

    if not donante:
        return jsonify({
            "correcto": False,
            "mensaje": "El nombre del donante es obligatorio."
        }), 400

    if not isinstance(materiales, list) or not materiales:
        return jsonify({
            "correcto": False,
            "mensaje": "Debes agregar al menos un útil."
        }), 400

    materiales_validos = []

    for material in materiales:
        if not isinstance(material, dict):
            return jsonify({
                "correcto": False,
                "mensaje": "Hay un material con datos inválidos."
            }), 400

        nombre = str(material.get("material", "")).strip()
        categoria = str(material.get("categoria", "")).strip()
        condicion = str(material.get("condicion", "")).strip()

        try:
            cantidad = int(material.get("cantidad"))
        except (ValueError, TypeError):
            cantidad = 0

        if not nombre or not categoria or not condicion or cantidad <= 0:
            return jsonify({
                "correcto": False,
                "mensaje": "Revisa los datos de cada útil y su cantidad."
            }), 400

        materiales_validos.append({
            "material": nombre,
            "categoria": categoria,
            "cantidad": cantidad,
            "condicion": condicion
        })

    nueva_donacion = {
        "id": str(uuid4()),
        "fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
        "donante": donante,
        "telefono": telefono,
        "correo": correo,
        "materiales": materiales_validos,
        "observaciones": observaciones,
        "estado": "pendiente_inspeccion"
    }

    try:
        donaciones = leer_datos("donaciones.json")
        donaciones.append(nueva_donacion)
        guardar_datos("donaciones.json", donaciones)

        return jsonify({
            "correcto": True,
            "mensaje": "Donación registrada correctamente.",
            "donacion": nueva_donacion
        }), 201

    except (OSError, ValueError, TypeError):
        app.logger.exception("Error al guardar la donación.")

        return jsonify({
            "correcto": False,
            "mensaje": "No se pudo guardar la donación."
        }), 500