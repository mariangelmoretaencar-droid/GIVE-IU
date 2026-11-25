# GIVE IU
**Útiles que transforman vidas**

Plataforma web de muestra para gestionar donaciones de útiles escolares, inspección, inventario, catálogo, solicitudes y entregas.

## Stack de esta versión de muestra

- Python + Flask
- HTML, CSS y JavaScript
- Archivos JSON como almacenamiento de demostración

> Los JSON se utilizan intencionalmente porque esta versión trabaja con datos de muestra. No se está usando PostgreSQL. El almacenamiento JSON es apropiado para una demostración local, pero no ofrece transacciones ni concurrencia segura para una operación multiusuario de producción.

## Requisitos

- Python 3.11 o posterior
- pip

## Instalación en Windows (PowerShell)

1. Descomprime el proyecto.
2. Abre PowerShell dentro de la carpeta `GIVE-IU-main`.
3. Crea un entorno virtual:

   ```powershell
   py -3 -m venv .venv
   ```

4. Activa el entorno:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación, puedes ejecutar los comandos usando `.venv\Scripts\python.exe` directamente.

5. Instala las dependencias:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Define una clave local para las sesiones:

   ```powershell
   $env:GIVE_IU_SECRET_KEY = "cambia-esto-por-una-clave-larga-y-aleatoria"
   ```

7. Inicia el servidor:

   ```powershell
   python app.py
   ```

8. Abre `http://127.0.0.1:5000` en el navegador.

## Instalación en macOS o Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export GIVE_IU_SECRET_KEY="cambia-esto-por-una-clave-larga-y-aleatoria"
python app.py
```

Abre `http://127.0.0.1:5000`.

## Datos de muestra

Los archivos JSON están en `data/`:

- `usuarios.json`
- `donaciones.json`
- `inventario.json`
- `solicitudes.json`
- `entregas.json`

Haz una copia de la carpeta `data/` antes de probar operaciones que modifiquen información. No incluyas datos personales reales en muestras compartidas.

## Estructura

```text
GIVE-IU-main/
├── app.py
├── backend/
│   └── almacenamiento.py
├── data/
├── docs/
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   └── templates/
├── Planteamiento/
├── requirements.txt
└── README.md
```

## Funcionalidades administrativas

- Configuración inicial de la primera cuenta administradora.
- Inicio y cierre de sesión.
- Contraseñas almacenadas mediante hash.
- Sesiones con duración máxima de 8 horas.
- Administración de cuentas: creación, activación y desactivación.
- Protección CSRF en formularios administrativos.
- Una cuenta inactiva no puede iniciar sesión ni continuar usando una sesión anterior.
- No se permite desactivar la cuenta actual ni dejar el sistema sin administradores activos.

Los registros de usuarios antiguos que no incluyan el campo `activo` se interpretan como activos para conservar compatibilidad con los datos de muestra.

## Documentación

Consulta `docs/DIAGNOSTICO_FASE_1.md` para conocer el estado inicial y `docs/FASE_2_AUTENTICACION.md` para las mejoras de autenticación y administración de usuarios.

## Importante

- `.venv/` no se comparte entre computadoras; cada equipo crea su propio entorno.
- No uses `debug=True` en un servidor público.
- La clave `GIVE_IU_SECRET_KEY` debe ser estable en el entorno para conservar sesiones entre reinicios.
- El servidor actual está configurado para uso local (`127.0.0.1`).


## Acceso al área de administración

La página principal incluye ahora el enlace **Administración** en el menú superior. Este enlace dirige a `/admin`, que conserva el control de acceso: si no hay una sesión iniciada, redirige al inicio de sesión; si aún no existe una cuenta administradora, dirige a la configuración inicial.


## Fase 3 — Gestión de donaciones

El panel administrativo permite buscar y filtrar donaciones por texto, estado, categoría y fecha. También permite guardar observaciones internas y consultar el historial de cambios de estado. Las notas internas no se muestran en el formulario público. Los materiales no ingresan al inventario desde este módulo: primero deben pasar por inspección en la Fase 4.

Consulta `docs/FASE_3_GESTION_DONACIONES.md` para el detalle y las pruebas pendientes.


## Corrección de observaciones administrativas

Al guardar una observación interna, el servidor verifica que el texto haya quedado escrito en `data/donaciones.json`. Después redirige a la donación correspondiente y mantiene abierta la sección de observaciones e historial para que el administrador pueda confirmar el resultado. Si ocurre un error de escritura, se muestra un mensaje y se registra el detalle en el log del servidor.
