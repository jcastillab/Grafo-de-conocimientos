# Grafo de conocimiento — C:\Source

Índice de los proyectos en `C:\Source`. Cada fila enlaza al nodo completo en
`.knowledge-graph/projects/<slug>.md` (frontmatter YAML + resumen). Lee el
nodo del proyecto que te interese antes de explorar su carpeta desde cero.

Mantenimiento: ver `CLAUDE.md` raíz y la skill `actualizar-grafo`. No se pide
aparte — es parte del trabajo normal cuando aparece o cambia un proyecto.

| Proyecto | Estado | Stack | Nodo |
|---|---|---|---|
| markov_v3 | active | python-3.12, pandas, streamlit | [projects/markov_v3.md](projects/markov_v3.md) |
| optimizacion rutas | active | python, fastapi, pandas, pulp, folium | [projects/optimizacion-rutas.md](projects/optimizacion-rutas.md) |
| conteo-rosas-portable-2026-10-08 | active | python-3.12, ultralytics, opencv, pandas | [projects/conteo-rosas-portable-2026-10-08.md](projects/conteo-rosas-portable-2026-10-08.md) |
| entrega_almer_20260826-2041 | entrega | python, fastapi, ultralytics | [projects/entrega-almer-20260826-2041.md](projects/entrega-almer-20260826-2041.md) |
| Vision-artificial | active | python-3.12, ultralytics, opencv, pandas | [projects/vision-artificial.md](projects/vision-artificial.md) |
| equipo-agentes | active | claude-code-plugin, powershell, python | [projects/equipo-agentes.md](projects/equipo-agentes.md) |

## Relaciones entre proyectos

conteo-rosas-portable-2026-10-08 -> markov_v3: origen-investigacion (el pronóstico se desarrolló en markov_v3 y se transfirió; documentado en docs/MODELOS_PRONOSTICO.md)
conteo-rosas-portable-2026-10-08 <-> Vision-artificial: mismo-proyecto-copia-portable (README.md y GUIA_USO.md idénticos; Vision-artificial es el repo canónico con remoto Azure DevOps, conteo-rosas-portable-2026-10-08 es un export portable sin remoto)

Cuando un proyecto dependa de otro (comparta datos,
código, modelos, etc.), anótalo en el campo `relationships` del frontmatter
de ambos nodos y aquí como una línea `A -> B: por qué`.

## Agregar un proyecto nuevo

No lo hagas a mano salvo caso simple: usa la skill `nuevo-proyecto` (plugin `equipo`), o el
subagente `equipo:project-scout` si la carpeta ya existe y solo falta documentarla.
Plantilla de nodo en `.knowledge-graph/projects/_template.md`.
