---
name: markov_v3
path: C:\Source\markov_v3
stack: [python-3.12, pandas, parquet, streamlit, pytest]
tags: [forecasting, agricultura, ml]
status: active
created: 2026-10-08
updated: 2026-11-05
relationships:
  - project: conteo-rosas-portable-2026-10-08
    tipo: origen-investigacion-inversa
    evidencia: docs/MODELOS_PRONOSTICO.md de conteo-rosas indica que el pronóstico se transfirió desde este proyecto.
  - project: conteo-rosas-portable-2026-10-08
    tipo: plantilla-de-evolucion
    evidencia: su paquete src/conteo_rosas/pronostico/ ya quitó M3 (commit fedba57), usa solo RF/RF_HORIZON/GLM_NB/BAYES_NB y reentrena en cada corrida (rolling_training).
---

## Propósito

Pronóstico de corte comercial de rosas Freedom (fincas ALMER, LA PRADERA,
SANTA HELENA). Pipeline reproducible por fases + proyección operacional
semanal idempotente + dashboard unificado de evaluación histórica y
pronóstico futuro.

## Puntos de entrada

- `scripts/run_historical.py` — pipeline histórico completo (fases 0-8)
- `scripts/train_models_cmd.py` — entrena y congela modelos (4 familias)
- `scripts/run_operational.py` — proyecta la semana siguiente (idempotente, `ONLY_NEXT_ISO_WEEK`)
- `scripts/validate_run.py` — valida corrida e integridad
- `scripts/run_pipeline.py` — todo de una vez
- `python -m streamlit run src/dashboard_streamlit.py` — dashboard
- `python -m pytest tests -q` — tests

## Modelos operacionales

RF, RF_HORIZON, GLM_NB, BAYES_NB — bundles en `outputs/models/bundles`.
M3, Dirichlet-M3, P32 y Semi-Markov se retiraron el 2026-11-05 (código en `legacy/`);
el modelo de referencia es `RF_OPT_FENO`.

## Reglas de oro propias del proyecto

Cero leakage (features con timestamp ≤ t0), parámetros solo en
`config/pipeline.yaml`, Excel solo como entrada RAW/auditoría (interno en
Parquet), métrica principal WAPE (nunca MAPE).

## Git y entorno

Git inicializado el 2026-11-05 (rama `main`, commit inicial `chore: incorporar proyecto...`).
Solo se versionan código, config, docs, tests y xlsx de `data/raw` < 5 MB; `data/vision`,
`recepcion`, zips y `outputs/` quedan fuera. El `.venv` usa Python 3.14 aunque AGENTS.md
dice 3.12. Auditoría completa del 2026-11-05 pendiente de corrección (Fase 2).

## Docs propios

`README.md`, `AGENTS.md`, `docs/GUIA_DATOS_ENTRADA.md` — fuente de verdad
detallada. Este nodo es solo un resumen, no la reemplaza.
