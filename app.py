
from datetime import datetime, timedelta
from functools import wraps
import os
from pathlib import Path
import secrets
from uuid import uuid4

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from backend.almacenamiento import (
    inicializar_archivos,
    leer_datos,
    guardar_datos,
)

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
app.secret_key = os.environ.get("GIVE_IU_SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("GIVE_IU_COOKIE_SECURE", "0") == "1",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
)

ESTADOS_DONACION = {
    "pendiente_inspeccion": "Pendiente de inspección",
    "contacto_realizado": "Contacto realizado",
    "recepcion_coordinada": "Recepción coordinada",
    "recibida": "Recibida",
    "en_inspeccion": "En inspección",
    "aprobada": "Aprobada",
    "rechazada": "Rechazada",
}

TRANSICIONES_DONACION = {
    "pendiente_inspeccion": {"contacto_realizado", "recepcion_coordinada", "rechazada"},
    "contacto_realizado": {"recepcion_coordinada", "rechazada"},
    "recepcion_coordinada": {"recibida", "rechazada"},
    "recibida": {"en_inspeccion", "rechazada"},
    "en_inspeccion": {"rechazada"},
    "aprobada": set(),
    "rechazada": set(),
}

CATEGORIAS_DONACION = {
    "escritura": "Escritura",
    "papeleria": "Papelería",
    "mochilas": "Mochilas y bolsos",
    "otros": "Otros",
}


def administradores():
    # Los registros antiguos no tienen el campo "activo"; se consideran activos
    # para mantener compatibilidad con los datos de muestra existentes.
    return [
        usuario for usuario in leer_datos("usuarios.json")
        if usuario.get("rol") == "admin" and usuario.get("activo", True)
    ]


def usuario_actual():
    nombre = session.get("admin_usuario")
    return next((u for u in administradores() if u.get("usuario") == nombre), None)


def csrf_valido():
    token_formulario = request.form.get("csrf_token", "")
    token_sesion = session.get("csrf_token", "")
    return bool(token_formulario and token_sesion and secrets.compare_digest(token_formulario, token_sesion))


def requiere_admin(vista):
    @wraps(vista)
    def protegida(*args, **kwargs):
        if not usuario_actual():
            session.clear()
            flash("Tu sesión no está activa. Inicia sesión nuevamente.", "error")
            return redirect(url_for("admin_login"))
        return vista(*args, **kwargs)
    return protegida


@app.context_processor
def variables_plantilla():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return {"csrf_token": session["csrf_token"]}


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/donaciones")
def pagina_donaciones():
    return render_template("donaciones.html")


@app.route("/admin")
def admin_inicio():
    if not administradores():
        return redirect(url_for("admin_configurar"))
    if not session.get("admin_usuario"):
        return redirect(url_for("admin_login"))
    return redirect(url_for("admin_donaciones"))


@app.route("/admin/configurar", methods=["GET", "POST"])
def admin_configurar():
    if administradores():
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        if not csrf_valido():
            flash("La sesión del formulario venció. Intenta nuevamente.", "error")
        else:
            usuario = request.form.get("usuario", "").strip()
            contrasena = request.form.get("contrasena", "")
            confirmar = request.form.get("confirmar", "")

            if len(usuario) < 4 or len(usuario) > 50:
                flash("El usuario debe tener entre 4 y 50 caracteres.", "error")
            elif len(contrasena) < 12:
                flash("La contraseña debe tener al menos 12 caracteres.", "error")
            elif contrasena != confirmar:
                flash("Las contraseñas no coinciden.", "error")
            else:
                usuarios = leer_datos("usuarios.json")
                usuarios.append({
                    "id": str(uuid4()),
                    "usuario": usuario,
                    "password_hash": generate_password_hash(contrasena),
                    "rol": "admin",
                    "activo": True,
                    "creado": datetime.now().astimezone().isoformat(timespec="seconds"),
                })
                guardar_datos("usuarios.json", usuarios)
                session.clear()
                session.permanent = True
                session["admin_usuario"] = usuario
                flash("Cuenta administrativa creada.", "success")
                return redirect(url_for("admin_donaciones"))

    return render_template("admin_configurar.html")


@app.route("/admin/ingresar", methods=["GET", "POST"])
def admin_login():
    if not administradores():
        return redirect(url_for("admin_configurar"))

    if request.method == "POST":
        if not csrf_valido():
            flash("La sesión del formulario venció. Intenta nuevamente.", "error")
        else:
            usuario = request.form.get("usuario", "").strip()
            contrasena = request.form.get("contrasena", "")
            cuenta = next((item for item in administradores() if item.get("usuario", "").casefold() == usuario.casefold()), None)

            if cuenta and check_password_hash(cuenta.get("password_hash", ""), contrasena):
                session.clear()
                session.permanent = True
                session["admin_usuario"] = cuenta["usuario"]
                flash("Sesión iniciada.", "success")
                return redirect(url_for("admin_donaciones"))

            flash("Usuario o contraseña incorrectos.", "error")

    return render_template("admin_login.html")


@app.route("/admin/salir", methods=["POST"])
@requiere_admin
def admin_salir():
    if not csrf_valido():
        flash("La sesión del formulario venció. Intenta nuevamente.", "error")
        return redirect(url_for("admin_donaciones"))
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin/usuarios", methods=["GET", "POST"])
@requiere_admin
def admin_usuarios():
    if request.method == "POST":
        if not csrf_valido():
            flash("La sesión del formulario venció. Intenta nuevamente.", "error")
            return redirect(url_for("admin_usuarios"))

        nombre = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")
        confirmar = request.form.get("confirmar", "")
        usuarios = leer_datos("usuarios.json")

        if len(nombre) < 4 or len(nombre) > 50:
            flash("El usuario debe tener entre 4 y 50 caracteres.", "error")
        elif any(u.get("usuario", "").casefold() == nombre.casefold() for u in usuarios):
            flash("Ya existe una cuenta con ese nombre de usuario.", "error")
        elif len(contrasena) < 12:
            flash("La contraseña debe tener al menos 12 caracteres.", "error")
        elif contrasena != confirmar:
            flash("Las contraseñas no coinciden.", "error")
        else:
            usuarios.append({
                "id": str(uuid4()),
                "usuario": nombre,
                "password_hash": generate_password_hash(contrasena),
                "rol": "admin",
                "activo": True,
                "creado": datetime.now().astimezone().isoformat(timespec="seconds"),
            })
            guardar_datos("usuarios.json", usuarios)
            flash("Cuenta administrativa creada correctamente.", "success")
            return redirect(url_for("admin_usuarios"))

    # Leer nuevamente el JSON en cada petición y normalizar el rol para
    # admitir registros de muestra antiguos con espacios o mayúsculas.
    usuarios_json = leer_datos("usuarios.json")
    usuarios = [
        u for u in usuarios_json
        if isinstance(u, dict)
        and str(u.get("rol", "")).strip().casefold() in {"admin", "administrador"}
    ]
    usuarios.sort(key=lambda u: str(u.get("usuario", "")).casefold())

    respuesta = app.make_response(render_template(
        "admin_usuarios.html",
        usuarios=usuarios,
        usuario_sesion=session.get("admin_usuario"),
        total_usuarios=len(usuarios),
    ))
    # Evita que el navegador reutilice una lista antigua tras crear usuarios.
    respuesta.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    respuesta.headers["Pragma"] = "no-cache"
    respuesta.headers["Expires"] = "0"
    return respuesta


@app.route("/admin/usuarios/<usuario_id>/estado", methods=["POST"])
@requiere_admin
def admin_usuario_estado(usuario_id):
    if not csrf_valido():
        flash("La sesión del formulario venció. Intenta nuevamente.", "error")
        return redirect(url_for("admin_usuarios"))

    usuarios = leer_datos("usuarios.json")
    cuenta = next((u for u in usuarios if u.get("id") == usuario_id and u.get("rol") == "admin"), None)
    if not cuenta:
        flash("No se encontró la cuenta administrativa.", "error")
        return redirect(url_for("admin_usuarios"))

    if str(cuenta.get("usuario", "")).casefold() == str(session.get("admin_usuario", "")).casefold():
        flash("No puedes desactivar la cuenta con la que tienes la sesión abierta.", "error")
        return redirect(url_for("admin_usuarios"))

    activos = [u for u in usuarios if u.get("rol") == "admin" and u.get("activo", True)]
    nuevo_estado = not cuenta.get("activo", True)
    if not nuevo_estado and len(activos) <= 1:
        flash("Debe permanecer al menos una cuenta administradora activa.", "error")
        return redirect(url_for("admin_usuarios"))

    cuenta["activo"] = nuevo_estado
    cuenta["actualizado"] = datetime.now().astimezone().isoformat(timespec="seconds")
    guardar_datos("usuarios.json", usuarios)
    flash("Cuenta activada." if nuevo_estado else "Cuenta desactivada.", "success")
    return redirect(url_for("admin_usuarios"))


@app.route("/admin/donaciones")
@requiere_admin
def admin_donaciones():
    donaciones = leer_datos("donaciones.json")
    donaciones.sort(key=lambda item: item.get("fecha", ""), reverse=True)
    resumen = {estado: 0 for estado in ESTADOS_DONACION}
    categorias_presentes = set()

    for donacion in donaciones:
        estado = donacion.get("estado", "pendiente_inspeccion")
        resumen[estado] = resumen.get(estado, 0) + 1
        for material in donacion.get("materiales", []):
            categoria = material.get("categoria", "")
            if categoria:
                categorias_presentes.add(categoria)

    respuesta = app.make_response(render_template(
        "admin_donaciones.html",
        donaciones=donaciones,
        resumen=resumen,
        etiquetas_estado=ESTADOS_DONACION,
        transiciones=TRANSICIONES_DONACION,
        categorias=CATEGORIAS_DONACION,
        categorias_presentes=sorted(categorias_presentes),
        donacion_destacada=request.args.get("donacion", ""),
    ))
    respuesta.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    respuesta.headers["Pragma"] = "no-cache"
    respuesta.headers["Expires"] = "0"
    return respuesta


@app.route("/admin/donaciones/<donacion_id>/observaciones", methods=["POST"])
@requiere_admin
def admin_guardar_observaciones_donacion(donacion_id):
    if not csrf_valido():
        flash("La sesión del formulario venció. Intenta nuevamente.", "error")
        return redirect(url_for("admin_donaciones"))

    observacion = request.form.get("observacion_admin", "").strip()
    if len(observacion) > 1500:
        flash("La observación administrativa no puede superar 1,500 caracteres.", "error")
        return redirect(url_for("admin_donaciones"))

    donaciones = leer_datos("donaciones.json")
    donacion = next((item for item in donaciones if item.get("id") == donacion_id), None)
    if not donacion:
        flash("No se encontró esa donación.", "error")
        return redirect(url_for("admin_donaciones"))

    donacion["observacion_admin"] = observacion
    donacion["observacion_admin_actualizada"] = datetime.now().astimezone().isoformat(timespec="seconds")
    donacion["observacion_admin_usuario"] = session.get("admin_usuario")

    try:
        guardar_datos("donaciones.json", donaciones)

        # Verificar la escritura leyendo nuevamente el archivo JSON.
        donaciones_guardadas = leer_datos("donaciones.json")
        donacion_guardada = next(
            (item for item in donaciones_guardadas if str(item.get("id")) == str(donacion_id)),
            None
        )
        if donacion_guardada is None or donacion_guardada.get("observacion_admin", "") != observacion:
            raise OSError("La observación no pudo verificarse en donaciones.json.")
    except (OSError, ValueError, TypeError):
        app.logger.exception("No se pudo guardar la observación administrativa de la donación %s.", donacion_id)
        flash("No se pudo guardar la observación. Comprueba que data/donaciones.json tenga permisos de escritura.", "error")
        return redirect(url_for("admin_donaciones", donacion=donacion_id, _anchor=f"donacion-{donacion_id}"))

    flash("Observación administrativa guardada correctamente.", "success")
    return redirect(url_for("admin_donaciones", donacion=donacion_id, _anchor=f"donacion-{donacion_id}"))


@app.route("/admin/donaciones/<donacion_id>/estado", methods=["POST"])
@requiere_admin
def admin_cambiar_estado(donacion_id):
    if not csrf_valido():
        flash("La sesión del formulario venció. Intenta nuevamente.", "error")
        return redirect(url_for("admin_donaciones"))

    nuevo_estado = request.form.get("estado", "")
    donaciones = leer_datos("donaciones.json")
    donacion = next((item for item in donaciones if item.get("id") == donacion_id), None)

    if not donacion:
        flash("No se encontró esa donación.", "error")
        return redirect(url_for("admin_donaciones"))

    estado_actual = donacion.get("estado", "pendiente_inspeccion")
    if nuevo_estado not in TRANSICIONES_DONACION.get(estado_actual, set()):
        flash("Ese cambio de estado no está permitido.", "error")
        return redirect(url_for("admin_donaciones"))

    fecha_cambio = datetime.now().astimezone().isoformat(timespec="seconds")
    historial = donacion.setdefault("historial_estados", [])
    if not isinstance(historial, list):
        historial = []
        donacion["historial_estados"] = historial

    historial.append({
        "estado_anterior": estado_actual,
        "estado_nuevo": nuevo_estado,
        "fecha": fecha_cambio,
        "usuario": session.get("admin_usuario"),
    })
    donacion["estado"] = nuevo_estado
    donacion["actualizado"] = fecha_cambio
    guardar_datos("donaciones.json", donaciones)
    flash("Estado de la donación actualizado.", "success")
    return redirect(url_for("admin_donaciones"))


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

    except (OSError, ValueError, TypeError):
        app.logger.exception("Error al consultar el almacenamiento.")

        return jsonify({
            "correcto": False,
            "mensaje": "No se pudo consultar el almacenamiento. Revisa los registros del servidor."
        }), 500


@app.route("/api/donaciones", methods=["POST"])
def registrar_donacion():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"correcto": False, "mensaje": "Los datos enviados no son válidos."}), 400

    donante_recibido = datos.get("donante")
    telefono_recibido = datos.get("telefono")
    correo_recibido = datos.get("correo", "")
    observaciones_recibidas = datos.get("observaciones", "")
    materiales = datos.get("materiales")

    if not isinstance(donante_recibido, str) or not isinstance(telefono_recibido, str):
        return jsonify({"correcto": False, "mensaje": "El nombre y el teléfono deben ser texto."}), 400
    if not isinstance(correo_recibido, str) or not isinstance(observaciones_recibidas, str):
        return jsonify({"correcto": False, "mensaje": "El correo y las observaciones deben ser texto."}), 400

    donante = donante_recibido.strip()
    telefono = telefono_recibido.strip()
    correo = correo_recibido.strip()
    observaciones = observaciones_recibidas.strip()

    if not donante or len(donante) > 100:
        return jsonify({"correcto": False, "mensaje": "Indica el nombre del donante (máximo 100 caracteres)."}), 400
    if not telefono or len(telefono) > 20:
        return jsonify({"correcto": False, "mensaje": "Indica un teléfono de contacto válido."}), 400
    if len(correo) > 120 or len(observaciones) > 1000:
        return jsonify({"correcto": False, "mensaje": "Revisa el correo y las observaciones; exceden el máximo permitido."}), 400
    if correo and (correo.count("@") != 1 or "." not in correo.rsplit("@", 1)[1]):
        return jsonify({"correcto": False, "mensaje": "El correo electrónico no tiene un formato válido."}), 400
    if not isinstance(materiales, list) or not materiales:
        return jsonify({"correcto": False, "mensaje": "Agrega al menos un útil a la donación."}), 400

    categorias = {"escritura", "papeleria", "mochilas", "otros"}
    condiciones = {"nuevo", "buen_estado", "regular"}
    materiales_validos = []

    for material in materiales:
        if not isinstance(material, dict):
            return jsonify({"correcto": False, "mensaje": "Hay un material con datos inválidos."}), 400

        nombre_recibido = material.get("material")
        categoria_recibida = material.get("categoria")
        condicion_recibida = material.get("condicion")
        cantidad_recibida = material.get("cantidad")

        if not all(isinstance(valor, str) for valor in (nombre_recibido, categoria_recibida, condicion_recibida)):
            return jsonify({"correcto": False, "mensaje": "El nombre, categoría y condición deben ser texto."}), 400

        nombre = nombre_recibido.strip()
        categoria = categoria_recibida.strip()
        condicion = condicion_recibida.strip()

        try:
            cantidad = int(cantidad_recibida)
        except (ValueError, TypeError, OverflowError):
            cantidad = 0

        if (
            isinstance(cantidad_recibida, bool)
            or (isinstance(cantidad_recibida, float) and not cantidad_recibida.is_integer())
            or not nombre
            or len(nombre) > 100
            or categoria not in categorias
            or condicion not in condiciones
            or cantidad <= 0
        ):
            return jsonify({"correcto": False, "mensaje": "Revisa el nombre, categoría, condición y cantidad de cada útil."}), 400

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
        "estado": "pendiente_inspeccion",
        "historial_estados": [{
            "estado_anterior": None,
            "estado_nuevo": "pendiente_inspeccion",
            "fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
            "usuario": "Sistema",
        }]
    }

    try:
        donaciones = leer_datos("donaciones.json")
        donaciones.append(nueva_donacion)
        guardar_datos("donaciones.json", donaciones)
    except (OSError, ValueError, TypeError):
        app.logger.exception("Error al guardar una donación.")
        return jsonify({"correcto": False, "mensaje": "No se pudo guardar la donación. Intenta nuevamente."}), 500

    return jsonify({
        "correcto": True,
        "mensaje": "Donación registrada. Quedó pendiente de inspección.",
        "donacion": {"id": nueva_donacion["id"], "estado": nueva_donacion["estado"]}
    }), 201


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
        debug=os.environ.get("FLASK_DEBUG", "0") == "1"
    )
