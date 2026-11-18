# GIVE-IU
(Proyecto Mártires) plataforma digital de GIVE IU

1. ROL Y OBJETIVO
   
plataforma web completa, moderna, responsive y funcional para un emprendimiento
social llamado GIVE IU, cuyo eslogan es «Útiles que transforman vidas».
No quiero solamente una página de presentación ni un prototipo visual. Necesito una aplicación web
funcional, con frontend, backend, base de datos, autenticación, gestión de inventario y panel administrativo.

3. DESCRIPCIÓN DEL PROYECTO
   
GIVE IU es un emprendimiento social y ambiental que conecta a personas que desean donar útiles escolares con
estudiantes y familias que necesitan estos materiales.
GIVE IU actuará como intermediario responsable: recibirá físicamente los útiles, los inspeccionará, clasificará, registrará
en el inventario y posteriormente los pondrá a disposición de los beneficiarios.
Los beneficiarios podrán consultar un catálogo y enviar solicitudes gratuitas. El equipo administrativo aprobará
donaciones, inspeccionará materiales, gestionará el inventario, aprobará solicitudes y registrará entregas.
Importante: los útiles se entregan gratuitamente. Las solicitudes están sujetas a disponibilidad y aprobación
administrativa.

4. OBJETIVOS DE LA PLATAFORMA
   
• Registrar donaciones de útiles escolares.
• Administrar las donaciones recibidas.
• Inspeccionar y clasificar los materiales.
• Controlar el inventario.
• Publicar materiales disponibles en un catálogo.
• Permitir que los beneficiarios soliciten materiales.
• Gestionar y aprobar solicitudes.
• Registrar entregas.
• Consultar estadísticas e indicadores.
• Proteger la información personal de los usuarios.

5. IDENTIDAD VISUAL Y DISEÑO
   
Diseña una interfaz moderna, minimalista, tecnológica, profesional y amigable que transmita confianza, solidaridad,
educación, sostenibilidad y transparencia.

• Verde esperanza: #159B78 — botones principales y acciones positivas.
• Azul confianza: #2364AA — navegación, encabezados y elementos institucionales.
• Amarillo oportunidad: #F4C95D — detalles y elementos destacados.
• Blanco natural: #F5F7F4 — fondos.
• Gris oscuro: #243746 — texto principal.

Utiliza tipografía moderna y legible, iconografía sencilla, bordes suaves, sombras discretas, espacios amplios y
componentes visuales consistentes. El resultado debe parecer un producto digital profesional, no una plantilla genérica.
El sitio debe adaptarse correctamente a computadoras, tablets y teléfonos móviles. Utiliza el logotipo de GIVE IU si se
proporciona como archivo; si no está disponible, crea un espacio temporal para incorporarlo posteriormente.

6. TIPOS DE USUARIO Y PERMISOS
   
A. Visitantes y donantes

• Acceder a la página principal y conocer el proyecto.
• Consultar cómo funciona.
• Registrar donaciones y consultar instrucciones para entregar materiales.
• No podrán modificar directamente el inventario.

B. Beneficiarios

• Consultar el catálogo público.
• Buscar útiles por categoría y ver fotografías, estado y cantidades disponibles.
• Enviar solicitudes y proporcionar información de contacto.
• En la primera versión no es obligatorio tener una cuenta personal: se permite un formulario público.

C. Administradores

• Acceder a un panel privado protegido por autenticación.
• Administrar donaciones, inspecciones, inventario, catálogo, solicitudes y entregas.
• Aprobar o rechazar operaciones.
• Consultar estadísticas y gestionar estados y observaciones.
• Solo administradores autorizados podrán acceder a las funciones internas.

7. ESTRUCTURA DE LA PLATAFORMA PÚBLICA
   
6.1 Inicio

• Header con logotipo y navegación.
• Mensaje principal «Útiles que transforman vidas».
• Descripción breve de GIVE IU.
• Botones «Quiero donar» y «Necesito útiles».
• Secciones «¿Cómo funciona?», beneficios e impacto social y ambiental.
• Estadísticas obtenidas de datos reales cuando existan.
• Testimonios solo si se proporcionan testimonios reales.
• Footer con contacto y redes sociales.

6.2 Quiénes somos
   
Incluir descripción del proyecto, problema que busca resolver, misión, visión, valores y objetivos sociales y ambientales.

6.3 Cómo funciona
   
Explicar visualmente el flujo: donación fi recepción fi inspección y clasificación fi inventario fi catálogo fi solicitud fi
coordinación y registro de entrega.

6.4 Donar útiles
   
Crear un formulario con: nombre, correo, teléfono, categoría, nombre del material, cantidad aproximada, estado
declarado, descripción, fotografía opcional, zona o punto de entrega preferido y aceptación del aviso de privacidad.
Al enviarlo, validar campos, guardar la información en la base de datos, mostrar confirmación y crear un registro con
estado «Pendiente de revisión». El administrador debe poder gestionarlo desde su panel. No publicar automáticamente
los artículos en el catálogo.

6.5 Catálogo
   
Crear tarjetas con fotografía, nombre, categoría, descripción, estado de conservación, cantidad disponible, indicador de
disponibilidad y botón «Solicitar». Añadir buscador, filtros por categoría y estado, y paginación si es necesaria. Mostrar
exclusivamente productos aprobados y disponibles; no mostrar productos agotados como disponibles.

6.6 Solicitar útiles
   
Crear un formulario con nombre, correo, teléfono, materiales seleccionados del catálogo, cantidades requeridas,
descripción opcional de la necesidad, zona o punto de entrega preferido y aceptación del aviso de privacidad.
Al enviarse, guardar la solicitud, generar un identificador, asignar estado «Pendiente» y mostrar confirmación. Informar
que la solicitud está sujeta a disponibilidad y aprobación. No descontar inventario al registrar una solicitud pendiente.

8. PANEL ADMINISTRATIVO
9. 
Crear un dashboard moderno con menú lateral y estas secciones: Dashboard, Donaciones, Inspección, Inventario,
Catálogo, Solicitudes, Entregas, Reportes y Configuración.

7.1 Dashboard
   
Mostrar indicadores reales: total de donaciones, pendientes, aprobadas, útiles recibidos, disponibles, solicitudes
pendientes y aprobadas, y entregas completadas. Incluir gráficos de donaciones por categoría, útiles recibidos y
entregados, evolución de solicitudes y estados de donaciones.
No utilizar números inventados para simular resultados reales. Si la base de datos está vacía, mostrar cero o un estado
vacío bien diseñado.

7.2 Gestión de donaciones
   
Tabla con ID, donante, fecha, categoría, material, cantidad declarada, estado y acciones. Permitir ver detalles, aprobar,
rechazar, registrar recepción, agregar observaciones y cambiar estados.

7.3 Inspección
   
Registrar cantidad recibida, estado físico, limpieza, funcionalidad, cantidad aprobada, cantidad rechazada, observaciones
y responsable. Clasificaciones: Como nuevo, Muy buen estado, Buen estado y No apto. Solo materiales aprobados
ingresan al inventario.

7.4 Inventario
   
Tabla con ID, nombre, categoría, cantidad recibida, reservada y disponible, estado, fecha de ingreso y acciones. Permitir
crear y editar productos, consultar detalles, modificar cantidades mediante movimientos justificados, consultar historial,
retirar materiales y filtrar.

7.5 Solicitudes
   
Tabla con ID, solicitante, fecha, materiales, cantidades, estado y acciones. Permitir consultar detalles, aprobar, rechazar,
agregar observaciones, reservar materiales, cancelar solicitudes y pasar a coordinación de entrega.

7.6 Entregas
   
Permitir consultar solicitudes aprobadas, registrar fecha y cantidades entregadas, agregar observaciones, marcar la
entrega como completada y actualizar automáticamente el inventario.

7.7 Reportes
   
Mostrar útiles recuperados y entregados, donaciones, solicitudes, solicitudes atendidas, productos más solicitados y
materiales disponibles. Permitir filtrar por fechas y categorías.

9. ESTADOS DEL SISTEMA
   
Donaciones:
Pendiente de revisión; Contacto realizado; Recepción coordinada; Recibida; En inspección; Aprobada; Rechazada.
Productos:
Pendiente de inspección; Disponible; Reservado parcialmente; Agotado; Retirado.
Solicitudes:
Pendiente; En revisión; Aprobada; Rechazada; En coordinación de entrega; Entregada; Cancelada.
Los cambios de estado deben estar controlados por las reglas de negocio y los permisos de cada usuario

 REGLAS DE NEGOCIO OBLIGATORIAS
1. Ningún producto puede publicarse sin inspección y aprobación.
2. Ninguna solicitud puede aprobar más unidades de las disponibles.
3. Una solicitud pendiente no descuenta definitivamente el inventario.
4. Al aprobar una solicitud, las cantidades correspondientes deben reservarse.
5. Al registrar una entrega, deben descontarse las cantidades entregadas.
6. Si una solicitud se cancela o rechaza después de una reserva, se deben liberar las unidades reservadas.
7. El inventario nunca puede tener cantidades negativas.
8. Los beneficiarios no pagan por los materiales.
9. Solo administradores autorizados pueden modificar el inventario.
10. Registrar los movimientos de inventario.
11. Evitar que una misma cantidad se reserve simultáneamente para dos solicitudes diferentes.
12. Implementar transacciones en las operaciones de reserva y entrega.
13. Validar todos los datos también en el backend.

11. SEGURIDAD
• Autenticación segura.
• Contraseñas almacenadas con hash seguro.
• Control de permisos por rol.
• Protección de rutas administrativas.
• Validación frontend y backend.
• Protección contra SQL Injection y XSS.
• Validación del tipo y tamaño de archivos.
• Protección de datos personales.
• HTTPS en producción.
• Manejo seguro de sesiones.
• Copias de seguridad.
No mostrar públicamente nombres completos de donantes, teléfonos, correos, direcciones ni información personal de
beneficiarios.

12. TECNOLOGÍA

utilizar una arquitectura
moderna basada en:
• Frontend: React o Next.js.
• Lenguaje: TypeScript.
• Estilos: Tailwind CSS.
• Backend: API del propio framework o backend independiente.
• Base de datos: PostgreSQL.
• ORM: Prisma o equivalente.
• Autenticación: solución segura compatible con el stack.
• Almacenamiento de imágenes: servicio compatible con archivos privados y públicos según el caso.
No agregues dependencia

13. EXPERIENCIA DE USUARIO
    
• Navegación intuitiva.
• Formularios con validación.
• Mensajes de éxito y error.
• Estados de carga.
• Confirmaciones antes de operaciones importantes.
• Tablas con búsqueda y filtros.
• Diseño adaptable.
• Accesibilidad básica.
• Estados vacíos bien diseñados.
• Manejo de errores de servidor.

14. FUNCIONES FUERA DEL MVP
No priorizar en esta primera versión: aplicación móvil nativa, pagos en línea, donaciones monetarias, chat interno
complejo, geolocalización avanzada ni notificaciones automáticas complejas. La prioridad es tener un MVP estable y
funcional.

16. FORMA DE TRABAJO Y ENTREGABLES
    
Antes de comenzar a programar:
1. Analiza todos los requisitos.
2. Identifica posibles problemas técnicos.
3. Propón la arquitectura más adecuada.
4. Presenta la estructura de carpetas.
5. Explica las relaciones de la base de datos.
6. Identifica qué funciones dependen de otras.
Después comienza a implementar el proyecto por etapas. Si el proyecto es demasiado grande para una sola respuesta,
divídelo en etapas y mantén una lista de lo implementado y lo pendiente.
No generes únicamente código de ejemplo o pantallas estáticas. Quiero funcionalidades conectadas a una base de datos
real. No simules operaciones que deberían persistirse en la base de datos. No inventes estadísticas ni resultados.
Si falta información, toma decisiones técnicas razonables y documenta los supuestos. No elimines funcionalidades
importantes sin explicarlo. Prioriza código limpio, componentes reutilizables, seguridad, escalabilidad y facilidad de
mantenimiento.

17. RESULTADO FINAL ESPERADO

    Una plataforma web profesional y funcional para GIVE IU que permita gestionar todo el ciclo de vida de las
donaciones escolares: registro, recepción, inspección, inventario, catálogo, solicitudes, reservas y entregas El sistema debe ser fácil de utilizar, visualmente atractivo, seguro y preparado para crecer en futuras versiones.
Nombre del proyecto: GIVE IU
Eslogan: Útiles que transforman vidas










