
from flask import Flask, render_template, jsonify
from pathlib import Path

from backend.almacenamiento import (
    inicializar_archivos,
    leer_datos,
    guardar_datos
)
from datetime import datetime
from uuid import uuid4

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path="/static"
)


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/donaciones")
def pagina_donaciones():
    return render_template("donaciones.html")


@app.route("/api/estado", methods=["GET"])
def estado_sistema():
    return jsonify({
        "proyecto": "GIVE IU",
        "estado": "funcionando",
        "backend": "Python + Flask",
        "almacenamiento": "Archivos JSON",
        "version": "1.0.0"
    })


@app.route("/api/almacenamiento", methods=["GET"])
def estado_almacenamiento():
    """
    Consulta cuántos registros existen
    en cada archivo JSON.
    """

    archivos = [
        "usuarios.json",
        "donaciones.json",
        "inventario.json",
        "solicitudes.json",
        "entregas.json"
    ]

    resultado = {}

    try:
        for nombre in archivos:
            datos = leer_datos(nombre)
            resultado[nombre] = len(datos)

        return jsonify({
            "correcto": True,
            "mensaje": "Almacenamiento conectado correctamente.",
            "registros": resultado
        })

    except (OSError, ValueError, TypeError) as error:
        app.logger.exception("Error al consultar el almacenamiento.")

        return jsonify({
            "correcto": False,
            "mensaje": "No se pudo consultar el almacenamiento.",
            "error": str(error)
        }), 500


if __name__ == "__main__":
    inicializar_archivos()

    print("\n================================")
    print("             GIVE IU")
    print("     Útiles que transforman vidas")
    print("================================\n")
    print("Servidor iniciado:")
    print("http://127.0.0.1:5000\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
