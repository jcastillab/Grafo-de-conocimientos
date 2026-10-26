---
name: conteo-rosas-portable-2026-10-08
path: C:\Source\conteo-rosas-portable-2026-10-08
stack: [python-3.12, ultralytics, opencv, supervision, pandas, numpy, polars, openpyxl, xlrd]
tags: [vision-artificial, conteo-rosas, pronostico, series-de-tiempo, markov, portable]
status: active
created: 2026-10-13
updated: 2026-10-15
relationships:
  - project: markov_v3
    tipo: origen-investigacion
    evidencia: docs/MODELOS_PRONOSTICO.md (l. 20 y 135) indica que el desarrollo histórico del pronóstico proviene de markov_v3 y fue transferido a este repositorio; docs/historico/GUIA_USO_pre_refactor.md y configs/pronostico.yaml replican su criterio de conteo.
  - project: Vision-artificial
    tipo: mismo-proyecto-copia-portable
    evidencia: README.md y GUIA_USO.md son byte-por-byte idénticos a los de Vision-artificial (diff vacío). Este repo no tiene remoto git (solo commit local "Versionado inicial del proyecto conteo-rosas"), nombre con fecha y empaquetado portable (.venv, Dockerfile, requirements.lock.txt), mientras Vision-artificial es el repo canónico conectado a Azure DevOps.
---

## Propósito

Proyecto Python 0.2.0 (`pyproject.toml`, paquete `conteo-rosas`) que cuenta rosas
en video mediante visión artificial (detección y tracking con Ultralytics/BoT-SORT),
compara los conteos contra cortes reales semanales y genera un pronóstico semanal
de cosecha. Ver `README.md` para la descripción completa y `docs/ARQUITECTURA.md`
para el diseño por capas.

## Puntos de entrada

- Lanzadores `.bat` en la raíz (Windows, usan `.venv`): `flujo_semanal.bat`,
  `procesar_lote.bat`, `preparar.bat`, `organizar.bat`, `qc.bat`, `comparar.bat`,
  `pronostico.bat`, `validar_pronostico.bat`, `empaquetar.bat`, `pruebas.bat`.
- CLI: `cli.py` (invocado por `cli.bat`).
- Paquete: `src/conteo_rosas/` (subpaquetes `ingesta`, `deteccion`, `agregacion`,
  `comparacion`, `pronostico`, `entrenamiento`, `proyeccion`, `interfaces/gui`, etc.).
- Configuración: `config.yaml` raíz y `configs/` (`botsort_rosas.yaml`,
  `comparacion.yaml`, `entrenamiento.yaml`, `fenologia.yaml`, `pronostico.yaml`,
  `modelos_pronostico_activos.json`). Rutas locales en `CAMBIAR_RUTAS.txt`.
- Tests: `tests/` (CI en `.github/workflows/tests.yml`).

## Docs propios

- `README.md` — visión general, instalación y uso (fuente principal).
- `GUIA_USO.md` — guía operativa.
- `CHANGELOG.md` — historial de versiones.
- `docs/ARQUITECTURA.md` — arquitectura del paquete.
- `docs/MANUAL_USUARIO.md`, `docs/GUIA_TECNICA.md`, `docs/DESARROLLO.md`.
- `docs/COMPARACION.md` — metodología de comparación conteo vs. corte real.
- `docs/MODELOS_PRONOSTICO.md` — modelos de pronóstico (documento extenso).
- `docs/HANDOFF.md`, `docs/portar_a_nuevo_pc.md` — traspaso y puesta en otro equipo.
- `docs/historico/` — documentación previa a la refactorización (no vigente).

## Notas

- Datos grandes en `data/` (videos/resultados de visión, parquets de pronóstico,
  bundles de modelos, pesos `.pt`). No se leen en la exploración; el listado de
  archivos excede 100k entradas, por lo que conviene buscar con patrones acotados.
- Carpeta "portable": incluye `.venv` propio con Python de Windows; `Dockerfile`
  y `requirements.lock.txt` también presentes.
- Requisitos de instalación (GPU, torch cu128, Python 3.12) están en `requirements.txt`.
- Relación con `markov_v3` inferida de menciones explícitas en la documentación
  (no de imports ni rutas compartidas en código).
