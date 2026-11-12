---
name: profundizar-proyecto
description: Genera (o refresca) el grafo de dependencias reales de código (imports internos entre módulos) de los proyectos Python de C:\Source, como caché en .knowledge-graph/deps/. Úsalo antes de ver-grafo cuando el usuario quiera "profundizar" en un proyecto, ver sus módulos internos, o cuando el código de un proyecto cambió y el grafo interno quedó desactualizado.
---

Genera los datos que `ver-grafo` usa para el drill-down de "ver dentro de un
proyecto". No dibuja nada — solo produce/actualiza los JSON en
`.knowledge-graph/deps/<slug>.json`. Al terminar, invoca `ver-grafo` para que
reconstruya el Artifact con los datos nuevos.

## Herramienta

`C:\Source\.knowledge-graph\tools\analizar_dependencias.py` — script stdlib
(solo usa `ast`, no ejecuta nada de los proyectos). Uso:

```
<python> analizar_dependencias.py <raiz_paquete> [--package-name NOMBRE]
    [--strip-prefix PREFIJO ...] [--shim-dir DIR ...] --out <salida.json>
```

**Importante:** usa el `<python>` del propio `.venv`/`venv` de cada proyecto
(no un Python global del sistema) — en este entorno el intérprete global ha
dado `PermissionError` al leer ciertos `.py` (probablemente bloqueado por el
antivirus), mientras que el venv de cada proyecto lee sin problema. El
script en sí no necesita ninguna dependencia del proyecto instalada (solo
usa `ast`), así que cualquier Python del propio proyecto sirve igual de
bien aunque no tenga paquetes instalados.

## Proyectos en el alcance (fijo por ahora, ver notas si se agrega uno)

| Proyecto | Comando |
|---|---|
| markov_v3 | `markov_v3/.venv/Scripts/python.exe analizar_dependencias.py "markov_v3/src" --strip-prefix src --out ".knowledge-graph/deps/markov_v3.json"` |
| conteo-rosas-portable-2026-10-08 | `conteo-rosas-portable-2026-10-08/.venv/Scripts/python.exe analizar_dependencias.py "conteo-rosas-portable-2026-10-08/src/conteo_rosas" --package-name conteo_rosas --shim-dir "conteo-rosas-portable-2026-10-08/src/modeling" --shim-dir "conteo-rosas-portable-2026-10-08/src/models" --out ".knowledge-graph/deps/conteo-rosas-portable-2026-10-08.json"` |
| Vision-artificial | `conteo-rosas-portable-2026-10-08/.venv/Scripts/python.exe analizar_dependencias.py "Vision-artificial/src/conteo_rosas" --package-name conteo_rosas --shim-dir "Vision-artificial/src/modeling" --shim-dir "Vision-artificial/src/models" --out ".knowledge-graph/deps/vision-artificial.json"` (Vision-artificial no tiene venv propio; reusa el de conteo-rosas-portable porque es el mismo código) |
| optimizacion rutas | `"optimizacion rutas/venv/Scripts/python.exe" analizar_dependencias.py "optimizacion rutas/app" --package-name app --out ".knowledge-graph/deps/optimizacion-rutas.json"` |

Todos los comandos corren con cwd en `C:\Source` y rutas relativas a ahí.

Fuera de alcance (no generar su grafo interno salvo que el usuario lo pida
explícitamente): `Vision Artificial` (carpeta vacía, sin código) y
`entrega_almer_20260826-2041` (artefacto de entrega congelado, no un
proyecto en desarrollo activo).

## Cuándo regenerar

Si el JSON en `.knowledge-graph/deps/<slug>.json` ya existe y es más
reciente que el `updated` del nodo del proyecto en
`.knowledge-graph/projects/<slug>.md`, no hace falta recalcular — está al
día. Si no existe, o el nodo se actualizó después (lo que suele pasar justo
después de que `actualizar-grafo` tocó ese proyecto), vuelve a correr el
comando correspondiente.

## Pasos

1. Para cada proyecto en alcance que necesite regenerarse (ver arriba),
   corre su comando.
2. Si algún proyecto nuevo entra al alcance (otro paquete Python real
   apareció en `C:\Source`), agrega su fila a la tabla de este archivo con
   el comando correcto (detectando su `--package-name` por el nombre del
   paquete y revisando si tiene imports estilo `src.X` que necesiten
   `--strip-prefix`) en vez de improvisarlo cada vez.
3. Al terminar de regenerar lo que haga falta, invoca la skill `ver-grafo`
   para que reconstruya el Artifact con los JSON actualizados.
4. Confirma en una línea qué proyectos se regeneraron (o que todo estaba al
   día).
