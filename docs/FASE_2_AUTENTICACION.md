# GIVE IU — Fase 2: Autenticación y administración de usuarios

## Objetivo

Completar el acceso administrativo y permitir gestionar las cuentas que pueden acceder al panel.

## Cambios realizados

1. Se conserva la configuración inicial de la primera cuenta administradora.
2. Se incorpora la pantalla `/admin/usuarios` para crear cuentas administrativas adicionales.
3. Las contraseñas nuevas se guardan mediante `generate_password_hash`; nunca se almacenan en texto plano.
4. Se permite activar y desactivar cuentas.
5. Se impide desactivar la cuenta que mantiene la sesión actual.
6. Se impide dejar el sistema sin ninguna cuenta administradora activa.
7. El inicio de sesión compara nombres de usuario sin distinguir mayúsculas y minúsculas.
8. Las cuentas desactivadas no pueden iniciar sesión. Si una cuenta se desactiva, su sesión deja de superar la validación de las rutas protegidas.
9. Los formularios administrativos mantienen protección CSRF.
10. Las sesiones tienen una duración máxima de ocho horas.
11. La opción `FLASK_DEBUG` controla el modo depuración y queda desactivado por defecto.
12. Los errores de almacenamiento no exponen el texto interno de la excepción en la respuesta de la API.

## Compatibilidad con los JSON de muestra

Los usuarios anteriores que no tengan el atributo `activo` se consideran activos. No se modifica ni se elimina ningún registro de `data/usuarios.json`.

## Pruebas manuales de aceptación

- [ ] Iniciar sesión con la cuenta administradora existente.
- [ ] Abrir «Administrar usuarios» desde el panel de donaciones.
- [ ] Crear un segundo usuario con contraseña de al menos 12 caracteres.
- [ ] Cerrar sesión e iniciar sesión con el nuevo usuario.
- [ ] Desactivar el segundo usuario desde la primera cuenta.
- [ ] Confirmar que el usuario desactivado ya no puede iniciar sesión.
- [ ] Confirmar que el usuario desactivado pierde acceso al intentar abrir una ruta protegida con una sesión anterior.
- [ ] Confirmar que no se puede desactivar la cuenta de la sesión actual.
- [ ] Confirmar que el sistema impide desactivar al último administrador activo.
- [ ] Confirmar que cerrar sesión invalida el acceso al panel.

## Configuración recomendada en desarrollo local

PowerShell:

```powershell
$env:GIVE_IU_SECRET_KEY = "una-clave-local-larga-y-aleatoria"
$env:FLASK_DEBUG = "1"
python app.py
```

Para una ejecución sin depurador, omite `FLASK_DEBUG` o asígnale `0`. No habilites el modo debug en un servidor público.

## Limitaciones conocidas

- Los roles de esta versión de muestra siguen siendo únicamente `admin`; todavía no hay permisos granulares.
- Los archivos JSON no proporcionan transacciones ni control de concurrencia multiusuario.
- La aplicación utiliza una clave de sesión local; debe mantenerse estable mediante `GIVE_IU_SECRET_KEY` para conservar sesiones entre reinicios.
- La validación integral con navegador y servidor debe realizarse en la computadora donde se instalarán las dependencias. En el entorno de preparación no fue posible instalar Flask por falta de acceso a Internet.

## Criterio de cierre

La fase se considera funcionalmente implementada en código, pero su aceptación final requiere completar la lista de pruebas manuales en el equipo local.
