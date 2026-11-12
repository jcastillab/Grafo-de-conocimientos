# Evaluar scripts y ejecutables antes de autorizarlos

Esta guía describe cómo preparar una solicitud de autorización en el entorno
que la persona usuaria indique. No contiene una lista de rutas, hashes,
ejecutables permitidos ni decisiones de seguridad tomadas para otros equipos.

## Inventario que debe recopilarse por proyecto

Para cada script o ejecutable que se quiera autorizar, documenta:

| Campo | Información que se debe verificar |
|---|---|
| Ruta | Ruta en el entorno actual. |
| Propósito | Qué tarea realiza y quién la inicia. |
| Momento de ejecución | Manual, hook, tarea programada o herramienta. |
| Permisos | Archivos que lee/escribe, red y procesos que inicia. |
| Dependencias | Paquetes o binarios requeridos y su procedencia. |
| Integridad | Hash calculado para el archivo actual, si la política lo exige. |
| Validación | Cómo probarlo en un entorno aislado y cómo revertirlo. |

No copies valores de otro inventario. Inspecciona los archivos actuales, explica
los efectos reales y solicita autorización a la persona responsable antes de
habilitar automatizaciones o instalar componentes.

## Procedimiento

1. Lee el código completo y sigue las llamadas a otros programas o archivos.
2. Identifica operaciones destructivas, acceso a secretos, red y escrituras.
3. Determina si puede probarse con datos temporales o en un sandbox.
4. Prepara la tabla anterior con rutas y hashes actuales, no estimados.
5. Espera aprobación antes de activar hooks, permisos o descargas.
6. Tras autorizar, prueba el caso normal y el de error; registra evidencia y
   documenta cómo desactivar la integración.
