---
name: optimizacion rutas
path: C:\Source\optimizacion rutas
stack: [python, fastapi, sqlalchemy, sqlite, angular, pandas, highspy, folium]
tags: [etl, optimizacion, rutas, logistica]
status: active
created: 2026-10-08
updated: 2026-10-26
relationships: []
---

## Propósito

Sistema de optimización y reconciliación de rutas de reparto/visita a fincas
(Sunshine). Combina un pipeline ETL que normaliza datos de fincas y paradas
(Excel/KML) con servicios de cálculo de distancia, orden de paradas y
recorrido, y expone (o expondrá) una API con FastAPI. También genera mapas
interactivos (folium) y reportes de reconciliación.

Reglas y comandos del proyecto en su `AGENTS.md` (importado por `CLAUDE.md`).
Repo git propio desde 2026-10-23 (sin `datos/`, `data/` ni Excel/KML).

## Stack

- Python (venv local en `venv/`)
- FastAPI + uvicorn (API, aún con `app/api` mínimo/placeholder)
- pydantic / pydantic-settings (`app/core/config.py`)
- pandas + openpyxl (procesamiento de datos Excel)
- folium (generación de mapas HTML)
- pulp (optimización, programación lineal)
- pytest (tests en `tests/`)

## Estructura

- `app/` — paquete principal:
  - `api/` — endpoints (esqueleto, solo `__init__.py` por ahora)
  - `core/config.py` — configuración de la app
  - `etl/` — `build_tables.py`, `export_csv.py`, `load_master.py`,
    `normalize.py`, `reconcile_report.py`
  - `services/` — `distancia.py`, `orden_paradas.py`, `recorrido.py`
  - `repository/`, `schemas/` — esqueletos, aún vacíos
- `scripts/` — puntos de entrada ejecutables: `run_etl.py`, `build_map.py`,
  `mapa_rutas.py`, `cruce_fincas.py`
- `data/` — salidas generadas: `processed/`, `mapa_rutas.html`,
  `reporte_reconciliacion.md`
- `datos/` — insumos crudos: Excel de fincas/rutas/paradas, KML de fincas,
  diccionario de fincas, mapas de ejemplo
- `tests/` — `test_distancia.py`, `test_orden_paradas.py`,
  `test_recorrido.py`
- `requirements.txt` — dependencias (ver Stack)
- `.claude/` — settings locales de Claude Code para este proyecto
- `venv/` — entorno virtual Python (no versionar/explorar)

## Puntos de entrada

- `scripts/run_etl.py` — corre el pipeline ETL (normalización, construcción
  de tablas, reconciliación)
- `scripts/build_map.py` / `scripts/mapa_rutas.py` — generan los mapas HTML
  en `data/`
- `scripts/cruce_fincas.py` — cruce de datos de fincas/rutas
- API FastAPI en `app/` (routing aún no implementado en `app/api`)

## Docs propios

- `AGENTS.md` — reglas de oro (heurística TSP, baseline, config única), núcleo, comandos, cómo validar.

## Notas

- El optimizador real es vecino más cercano + 2-opt sobre haversine; `pulp`
  está en requirements pero no se usa.
- Primer ciclo `/desarrollar` (2026-10-23): baseline + gap (óptimo exacto
  Held-Karp para rutas de hasta 12 paradas), fusionado en `main`;
  `scripts/evaluar_baseline.py`.
- FESTIVO (2026-10-23): el alias de rutas ya no se aplica a FDS (FUNZA y
  FUNZA, MSOQUERA separadas); las FDS con mismas paradas en la fuente se
  reportan en la reconciliación y no se suman dos veces en el baseline.
- App web (2026-10-26, rama feat/app-web, sin fusionar): backend FastAPI + SQLite con roles y auditoría, frontend Angular en frontend/, simulador de rutas nuevas (heurística + MILP), manuales en manual/. Contrato en docs/CONTRATO_API.md. Límites de los datos (cobertura 35,8 %, red actual con un bus por tarifa, personas repetidas) en AGENTS.md.
