---
name: nuevo-proyecto
description: Crea una subcarpeta nueva en C:\Source, su nodo inicial en el grafo de conocimiento y la deja lista para trabajar con el equipo (git, AGENTS.md, hooks). Úsalo cuando el usuario pida iniciar/crear un proyecto nuevo dentro de C:\Source.
---

1. Si el usuario no dio nombre y propósito del proyecto en una frase, pregúntalos
   antes de crear nada.
2. Crea `C:\Source\<nombre>\` si no existe.
3. Crea `C:\Source\.knowledge-graph\projects\<slug>.md` a partir de
   `_template.md`, con el propósito dado y `status: new` (regla de slug: ver
   agente `project-scout`).
4. Agrega la fila correspondiente a la tabla de
   `C:\Source\.knowledge-graph\graph.md`.
5. Invoca la skill `preparar-proyecto` sobre la carpeta nueva (git, AGENTS.md,
   CLAUDE.md, entorno de desarrollo, permisos). Si el proyecto es de modelado
   u optimización, sus reglas de oro parten de la skill `protocolo-matematico`.
6. Cierra recordando que las sesiones de trabajo se abren con la carpeta del
   proyecto como directorio de trabajo, no `C:\Source`.
