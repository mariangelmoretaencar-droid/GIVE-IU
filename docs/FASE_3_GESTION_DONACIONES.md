# Fase 3 — Gestión de donaciones

## Implementado

- Listado administrativo de donaciones con datos del donante y materiales declarados.
- Búsqueda por código, donante, teléfono, correo y nombre de material.
- Filtros por estado, categoría y rango de fechas.
- Resumen real de donaciones por estado.
- Observaciones administrativas internas, separadas de las observaciones del donante.
- Historial de transiciones de estado con fecha y usuario responsable.
- Encabezados HTTP para evitar que el navegador reutilice una lista desactualizada.
- Validación en backend de las transiciones permitidas y protección CSRF.
- Las nuevas donaciones registran su estado inicial en el historial.
- Los registros antiguos siguen siendo compatibles; si no tienen historial, el panel lo indica.

## Reglas respetadas

- Los datos continúan almacenándose en archivos JSON de muestra.
- Las observaciones internas solo se muestran dentro del panel administrativo.
- Cambiar el estado no incorpora materiales al inventario.
- La aprobación de materiales y su incorporación al inventario se desarrollarán en la Fase 4 (inspección).

## Archivos modificados

- `app.py`
- `frontend/templates/admin_donaciones.html`
- `frontend/static/js/main.js`
- `frontend/static/css/styles.css`

## Pruebas realizadas en la preparación

- Compilación sintáctica de `app.py`.
- Validación de sintaxis JSON de los archivos de muestra.
- Verificación de que el ZIP conserva los archivos de datos originales.

## Pruebas pendientes en la computadora de desarrollo

1. Registrar una donación desde el formulario público.
2. Verificar que aparece en el panel administrativo.
3. Probar búsqueda por donante, código y material.
4. Probar filtros por estado, categoría y fechas.
5. Guardar una observación administrativa y comprobar que persiste tras recargar.
6. Cambiar el estado y comprobar que se registra fecha y usuario en el historial.
7. Verificar que una cuenta sin sesión no puede guardar observaciones ni cambiar estados.
8. Confirmar que el archivo `data/donaciones.json` conserva los registros existentes.
