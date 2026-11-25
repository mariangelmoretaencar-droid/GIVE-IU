# GIVE IU — Diagnóstico inicial (Fase 1)

Fecha de revisión: 25 de noviembre de 2026  
Base revisada: archivo `GIVE-IU-main(1).zip`, código y documentos PDF incluidos.

## 1. Decisión técnica acordada

Esta versión es una muestra/prototipo funcional con datos de demostración. Se conserva el stack existente:

- Python + Flask para el backend.
- HTML, CSS y JavaScript para la interfaz.
- Archivos JSON en `data/` para persistencia de muestra.

No se migra a PostgreSQL ni a React en esta etapa. Esta decisión evita una reescritura innecesaria y respeta el propósito de la muestra. Los archivos JSON no ofrecen transacciones ni control robusto de concurrencia; no deben considerarse una solución de producción multiusuario.

## 2. Estructura observada

- `app.py`: aplicación Flask, rutas, autenticación y registro de donaciones.
- `backend/almacenamiento.py`: lectura, escritura e inicialización de JSON.
- `frontend/templates/`: páginas HTML/Jinja.
- `frontend/static/css/`: estilos.
- `frontend/static/js/`: comportamiento del navegador.
- `data/`: usuarios, donaciones, inventario, solicitudes y entregas.
- `Planteamiento/`: documentos de definición del proyecto.

Se excluye `.venv/` del paquete de traslado. Cada computadora debe crear su propio entorno e instalar dependencias.

## 3. Funcionalidad encontrada

### Rutas existentes

| Ruta | Método | Función |
|---|---|---|
| `/` | GET | Página de inicio |
| `/donaciones` | GET | Formulario público de donaciones |
| `/admin` | GET | Entrada al panel |
| `/admin/configurar` | GET, POST | Configuración inicial de administrador |
| `/admin/ingresar` | GET, POST | Inicio de sesión |
| `/admin/salir` | POST | Cierre de sesión |
| `/admin/donaciones` | GET | Listado administrativo de donaciones |
| `/admin/donaciones/<id>/estado` | POST | Cambio controlado de estado |
| `/api/estado` | GET | Estado del servicio |
| `/api/almacenamiento` | GET | Conteo de registros JSON |
| `/api/donaciones` | POST | Registro de una donación |

### Datos JSON

Existen los archivos `usuarios.json`, `donaciones.json`, `inventario.json`, `solicitudes.json` y `entregas.json`. En la muestra revisada, donaciones y usuarios contienen registros; inventario, solicitudes y entregas están vacíos.

## 4. Brechas frente al alcance del proyecto

Todavía deben desarrollarse los flujos completos de:

1. Inspección detallada por artículo y aprobación de cantidades.
2. Alta de inventario únicamente desde artículos aprobados.
3. Movimientos y ajustes justificados de inventario.
4. Catálogo público basado exclusivamente en existencias disponibles.
5. Registro y administración de solicitudes.
6. Reservas, liberación de reservas y validación de disponibilidad.
7. Registro de entregas y descuento de existencias.
8. Dashboard y reportes calculados desde los datos reales.
9. Pruebas automatizadas del flujo completo.

## 5. Riesgos y mejoras técnicas detectadas

- `app.secret_key` usa una clave aleatoria cuando no se define `GIVE_IU_SECRET_KEY`; las sesiones dejan de ser válidas al reiniciar el proceso. Para desarrollo estable debe configurarse una clave fija mediante variable de entorno.
- `debug=True` debe mantenerse solo en desarrollo local y nunca en una publicación accesible públicamente.
- El servidor escucha en `127.0.0.1`; es adecuado para uso local, pero no para acceso desde otra computadora en una red sin cambiar la configuración.
- La escritura JSON utiliza un archivo temporal y `os.replace`, lo que reduce escrituras parciales, pero no evita conflictos entre escrituras simultáneas.
- La ruta `/api/almacenamiento` devuelve el texto de una excepción al cliente; conviene no exponer detalles internos.
- La dependencia está declarada como `Flask` sin versión fijada. Se debe comprobar el entorno objetivo antes de fijarla.
- No hay suite de pruebas automatizadas en el paquete revisado.

## 6. Validación realizada y limitaciones

- La sintaxis de `app.py` y `backend/almacenamiento.py` compila correctamente.
- No fue posible ejecutar pruebas de integración en el entorno de revisión porque Flask no está instalado en ese entorno (`ModuleNotFoundError: No module named 'flask'`).
- Por tanto, los códigos HTTP y el funcionamiento real de las páginas quedan pendientes de validación en una computadora con las dependencias instaladas.

## 7. Criterio de cierre de la Fase 1

La Fase 1 se considerará cerrada cuando:

- El proyecto se instale y ejecute en la computadora de trabajo.
- Se comprueben las rutas existentes con el servidor activo.
- Se confirme la lectura y escritura de los JSON.
- Se configure una clave de sesión estable para el entorno local.
- Se cree una copia de respaldo antes de iniciar cambios funcionales.

## 8. Próximo paso

Una vez validado el arranque local, iniciar la Fase 2 (autenticación y administración) solo si se detectan ajustes necesarios; de lo contrario, avanzar a completar la Fase 3 y mantener las funciones ya existentes.
