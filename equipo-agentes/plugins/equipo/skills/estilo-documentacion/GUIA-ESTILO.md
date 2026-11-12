# Guía general de documentación

Este método no presupone marca, tecnología, estructura ni contenido de un
proyecto. Antes de escribir, inspecciona solo el proyecto indicado por la
persona usuaria y adapta el resultado a sus convenciones verificadas.

## Principios

- Escribe para el rol que realizará la tarea; explica cada término técnico la
  primera vez que aparezca.
- Describe únicamente comportamientos comprobables en el código o en la
  aplicación. No inventes botones, mensajes, cifras, rutas ni capacidades.
- Respeta la identidad visual local si existe. Si no existe, utiliza una
  presentación neutral o solicita preferencias; no copies logos, colores ni
  activos de otros proyectos.
- Mantén documentación existente y actualiza solo las partes afectadas.

## Elegir documentos

- Manual de usuario: tareas habituales, requisitos, pasos, resultados y ayuda.
- Manual de administración: instalación, configuración, operación y resolución
  técnica de problemas.
- README: propósito, requisitos, inicio rápido, validación y enlaces a la
  documentación local.
- Proyecto sin interfaz: documenta comandos, entradas, salidas y ejemplos que
  existan en el proyecto.

## Estructura sugerida

1. Título, audiencia, alcance y fecha de revisión.
2. Requisitos previos y preparación.
3. Procedimientos en el orden real de uso.
4. Resultados esperados y cómo verificarlos.
5. Problemas comunes con síntoma, causa comprobada y acción.
6. Referencias y contacto/diagnóstico, si aplica.

Omite secciones que no correspondan. Para cada procedimiento, usa pasos
numerados con una acción por paso. Las etiquetas de interfaz deben coincidir
literalmente con la aplicación; los comandos y rutas van en bloques de código.

## Capturas

- Captura la aplicación real solo cuando esté disponible; nunca simules una
  pantalla.
- Usa datos no sensibles. Marca los controles mencionados por el texto y añade
  texto alternativo descriptivo.
- Si no se puede capturar, marca el espacio como pendiente y explica el bloqueo.
- Guarda y nombra imágenes de forma coherente con la estructura del proyecto.

## Formatos HTML opcionales

Si el proyecto necesita manual interactivo, puede partir de `plantilla.html` y
`COMPONENTES.md`. Adapta el contenido y la identidad visual antes de usarla. La
fuente editable y el HTML empaquetado deben tener secciones equivalentes. Usa
`empaquetar_html.py` para incrustar recursos locales cuando se requiera un solo
archivo; no edites manualmente el archivo empaquetado.

## Verificación final

- [ ] Cada instrucción corresponde al comportamiento actual.
- [ ] Los mensajes y nombres de controles citados existen literalmente.
- [ ] Los enlaces y referencias apuntan a archivos existentes.
- [ ] Las capturas corresponden a la versión documentada y no contienen datos
      sensibles.
- [ ] No se incorporaron rutas, marcas, datos ni supuestos de otro proyecto.
- [ ] La documentación fue revisada en el formato final que recibirá la persona.
