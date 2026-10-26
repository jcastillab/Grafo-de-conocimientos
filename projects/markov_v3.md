---
name: markov_v3
path: C:\Source\markov_v3
stack: [python-3.12, pandas, parquet, streamlit, pytest]
tags: [forecasting, agricultura, ml]
status: active
created: 2026-10-08
updated: 2026-10-08
relationships:
  - project: conteo-rosas-portable-2026-10-08
    tipo: origen-investigacion-inversa
    evidencia: docs/MODELOS_PRONOSTICO.md de conteo-rosas indica que el pronóstico se transfirió desde este proyecto.
---

## Propósito

Pronóstico de corte comercial de rosas Freedom (fincas ALMER, LA PRADERA,
SANTA HELENA). Pipeline reproducible por fases + proyección operacional
semanal idempotente + dashboard unificado de evaluación histórica y
pronóstico futuro.

## Puntos de entrada

- `scripts/run_historical.py` — pipeline histórico completo (fases 0-8)
- `scripts/train_models_cmd.py` — entrena y congela modelos (mejor por familia)
- `scripts/run_operational.py` — proyecta la semana siguiente (idempotente, `ONLY_NEXT_ISO_WEEK`)
- `scripts/validate_run.py` — valida corrida e integridad
- `scripts/run_pipeline.py` — todo de una vez
- `python -m streamlit run src/dashboard_streamlit.py` — dashboard
- `python -m pytest tests -q` — tests

## Modelos operacionales

M3 (baseline obligatorio), RF, RF_HORIZON, GLM_NB, BAYES_NB, BAYES_DIRICHLET
— bundles en `outputs/models/bundles`.

## Reglas de oro propias del proyecto

Cero leakage (features con timestamp ≤ t0), parámetros solo en
`config/pipeline.yaml`, Excel solo como entrada RAW/auditoría (interno en
Parquet), métrica principal WAPE (nunca MAPE).

## Docs propios

`README.md`, `AGENTS.md`, `docs/GUIA_DATOS_ENTRADA.md` — fuente de verdad
detallada. Este nodo es solo un resumen, no la reemplaza.
