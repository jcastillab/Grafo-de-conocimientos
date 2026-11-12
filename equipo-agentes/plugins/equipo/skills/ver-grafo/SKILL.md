---
name: ver-grafo
description: Genera una visualización interactiva (Artifact) del grafo de conocimiento de C:\Source, con nodos por proyecto y flechas por relación. Úsalo cuando el usuario pida "ver el grafo", "muéstrame el grafo visualmente/gráficamente", o un diagrama de las relaciones entre proyectos.
---

1. Lee `C:\Source\.knowledge-graph\graph.md` para la lista de proyectos.
2. Lee el frontmatter y el cuerpo de cada `C:\Source\.knowledge-graph\projects\<slug>.md`:
   - `name`, `status`, `stack`, `tags`.
   - `relationships`: lista de `{project, tipo, evidencia}` — cada una es
     una arista `este-proyecto -> project`, etiquetada con `tipo`.
   - Del cuerpo: Propósito, Puntos de entrada, Docs propios, Notas (para el
     panel de detalle; resume si son largos, no los copies completos).
2b. Para cada proyecto, revisa si existe
    `C:\Source\.knowledge-graph\deps\<slug>.json` (lo genera la skill
    `profundizar-proyecto`). Si no existe para ningún proyecto, sigue solo
    con la vista de overview (pasos normales). Si existe para al menos uno,
    cárgalo (es JSON: `{modules:[{id,path,subpaquete,loc,shim}],
    edges:[{from,to}]}`) para construir también su vista interna (paso 4).
    No generes tú los JSON aquí — si están desactualizados o faltan y el
    usuario pidió profundidad, dile que corra `profundizar-proyecto` primero
    (o invócala tú si el pedido del usuario claramente lo requiere).
3. Antes de construir el artifact, sigue el flujo obligatorio de la
   herramienta Artifact: `quickstart` con `intent: "other"` (es un
   diagrama/visualización, no un documento ni una presentación), y carga
   `artifact-design` (y `artifact-diagramming` si aplica a cómo vas a
   dibujar el grafo).
4. Construye un único HTML con dos vistas conmutables por JS (sin recargar
   la página):
   - **Overview** (SVG inline, posiciones fijas — solo 6 nodos, no hace
     falta layout de fuerzas): un nodo por proyecto, diferenciado por
     `status` (active / empty / entrega / new); una flecha por cada
     relación, con su `tipo` como etiqueta. Click en un nodo → panel con
     Propósito, Puntos de entrada, Docs propios y Notas.
   - **Interna** (solo para proyectos con JSON de dependencias cargado):
     si el proyecto tiene decenas de módulos, el posicionamiento manual no
     alcanza — usa D3.js (`d3-force` para el layout + `d3-zoom` para
     pan/zoom), cargado como UMD desde cdnjs (único CDN de scripts que
     permite el CSP del Artifact), versión exacta con al menos 2 semanas de
     antigüedad. En el nodo del proyecto en el overview, si tiene datos
     internos, agrega una indicación de que es "clickeable para profundizar"
     (ej. icono o borde distinto) y un segundo click (o un botón explícito)
     lo lleva a su vista interna:
     - Color = `subpaquete` (comunidad), tamaño = grado (in+out degree) —
       replica el grafo de referencia que dio el usuario: hubs grandes,
       periferia chica.
     - Nodo con `shim: true` se dibuja distinto (borde punteado) con su
       `nota` visible.
     - Click en un módulo → panel con su `path`, `loc`, y qué módulos
       importa / lo importan (derivado de `edges`).
     - Botón "← volver" regresa al overview.
     - Si dos proyectos comparten el mismo JSON de dependencias en
       contenido (ej. Vision-artificial y conteo-rosas-portable-2026-10-08,
       que son el mismo código), muestra una nota visible en la vista
       interna de ambos indicándolo, en vez de duplicar la explicación como
       si fueran independientes.
   - Sin llamadas a servicios externos: todos los datos van embebidos en el
     HTML en el momento de publicar (un Artifact no puede leer el disco del
     usuario).
5. Revisa si existe `C:\Source\.knowledge-graph\.artifact-url`:
   - Si existe y tiene una URL, pásala como `url` en `Artifact.publish` para
     actualizar ese mismo artifact (primero léelo con `action: "read"` como
     exige la herramienta antes de publicar sobre una URL conocida).
   - Si no existe, publica sin `url` (crea uno nuevo) y guarda la URL
     devuelta en ese archivo (créalo).
6. Responde con el link del artifact en una línea.
