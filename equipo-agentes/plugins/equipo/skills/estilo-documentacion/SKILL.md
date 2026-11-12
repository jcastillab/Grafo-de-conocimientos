---
name: estilo-documentacion
description: Método y herramientas para crear o revisar documentación basada en el contenido y las convenciones del proyecto seleccionado.
---

Todo en la carpeta de esta skill:

| Archivo | Para qué |
|---|---|
| `GUIA-ESTILO.md` | **La metodología.** Léela antes de escribir; define principios, estructura sugerida, capturas y verificación final. |
| `plantilla.html` | Punto de partida opcional para HTML interactivo, con índice, checklists, buscador y esqueleto de secciones. Adapta su identidad visual al proyecto seleccionado. |
| `COMPONENTES.md` | Fragmentos HTML de cada componente (avisos, capturas, tablas, pasos, calculadora, trampas, anexo). |
| `capturar.py` | Capturas anotadas con Playwright desde `manual/capturas.json` (formato en su docstring). |
| `empaquetar_html.py` | Incrusta las imágenes en el HTML para que sea un solo archivo. `--prueba` se autoverifica. |

Flujo:

1. Lee `GUIA-ESTILO.md`. Si hay un manual anterior del proyecto, léelo
   también.
2. Si el proyecto no tiene una plantilla propia, acuerda una ruta para la fuente
   HTML y adapta colores, marca e imágenes a recursos autorizados del proyecto
   actual. No copies activos de otros proyectos.
3. Capturas: son opcionales. Si la persona las pide y el entorno dispone de
   Python y Playwright, guarda la especificación en la carpeta acordada y
   ejecuta `python <ruta-a-capturar.py> <especificación.json>`. No instales
   dependencias sin autorización. Si la herramienta no está disponible, informa
   la limitación y no inventes capturas.
4. Escribe los formatos solicitados en las rutas acordadas y mantenlos con las
   mismas secciones.
5. Si se pide un HTML autónomo, usa `empaquetar_html.py` con las rutas acordadas.
   Nunca edites el empaquetado: edita la fuente y vuelve a generarlo.
6. Pasa la checklist final de la guía.
