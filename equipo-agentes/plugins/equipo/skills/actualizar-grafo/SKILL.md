---
name: actualizar-grafo
description: Revisa las subcarpetas de C:\Source contra el grafo de conocimiento (.knowledge-graph) y crea/actualiza los nodos que falten o estén desactualizados. Úsalo cuando el usuario pida "actualizar el grafo", o cuando detectes de paso una carpeta nueva sin documentar.
---

1. Lista las subcarpetas de primer nivel de `C:\Source`.
2. Lee la tabla índice de `C:\Source\.knowledge-graph\graph.md` para ver qué
   proyectos ya tienen nodo en `.knowledge-graph/projects/`.
3. Para cada subcarpeta sin nodo correspondiente, o cuyo nodo luzca
   claramente desactualizado, lanza el subagente `equipo:project-scout` (Agent tool)
   con el path de esa subcarpeta. Si hay varias pendientes y son
   independientes, lánzalos en paralelo.
4. No toques nodos que ya están al día — no reescribas por reescribir.
5. Si creaste o actualizaste al menos un nodo (paso 3), invoca la skill
   `ver-grafo` para refrescar el Artifact visual con los datos nuevos — ella
   ya se encarga de actualizar el mismo link guardado en
   `.knowledge-graph/.artifact-url` en vez de crear uno nuevo. Si no hubo
   cambios, no hace falta regenerarlo.
6. Al terminar, confirma en una sola línea qué nodos se crearon o
   actualizaron (o que todo estaba al día), y si refrescaste el Artifact.
