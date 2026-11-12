---
name: estilo-documentacion
description: Estilo y herramientas de la documentación para personas de C:\Source (manuales de usuario/administrador, README), copiado del manual de Conteo Rosas - metodología didáctica paso a paso, paleta Sunshine Bouquet, HTML interactivo y pantallazos con recuadro rosa y círculos numerados. Úsalo al escribir o revisar cualquier manual, guía o README de estos proyectos.
---

Todo en la carpeta de esta skill:

| Archivo | Para qué |
|---|---|
| `GUIA-ESTILO.md` | **La metodología.** Léela completa antes de escribir: roles, cabecera, secciones, cómo se escribe una tarea, capturas, problemas comunes, tono, checklist final. |
| `plantilla.html` | Punto de partida del HTML interactivo: CSS y JS del manual original (paleta, tipografías, modo oscuro, índice, checklists, buscador de errores, lightbox) con un esqueleto de secciones `{{…}}`. |
| `COMPONENTES.md` | Fragmentos HTML de cada componente (avisos, capturas, tablas, pasos, calculadora, trampas, anexo). |
| `img/logo_sunshine_bouquet.png` | Logo; cópialo a `manual/img/` del proyecto. |
| `capturar.py` | Capturas anotadas con Playwright desde `manual/capturas.json` (formato en su docstring). |
| `empaquetar_html.py` | Incrusta las imágenes en el HTML para que sea un solo archivo. `--prueba` se autoverifica. |

Flujo:

1. Lee `GUIA-ESTILO.md`. Si hay un manual anterior del proyecto, léelo
   también.
2. Copia `plantilla.html` → `manual/manual_<rol>.fuente.html` (la fuente que
   se edita, con imágenes por ruta) y el logo → `manual/img/`.
3. Capturas: escribe `manual/capturas.json` y corre, con el Python del venv
   del proyecto (necesita `playwright` + `python -m playwright install
   chromium`; Pillow para webp):
   `<venv>\Scripts\python.exe <esta carpeta>\capturar.py manual\capturas.json`
   Revisa cada imagen (ábrela) antes de usarla: marcas sobre lo correcto,
   nada sensible. `--solo nombre1,nombre2` para recapturar algunas.
4. Escribe `manual/MANUAL_<ROL>.md` y el HTML con las mismas secciones.
5. `<venv>\Scripts\python.exe <esta carpeta>\empaquetar_html.py manual\manual_<rol>.fuente.html -o manual\manual_<rol>.html`
   → el entregable de un solo archivo. Nunca edites el empaquetado: edita la
   fuente y vuelve a empaquetar.
6. Pasa la checklist final de la guía.
