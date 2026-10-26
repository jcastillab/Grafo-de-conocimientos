---
name: Vision-artificial
path: C:\Source\Vision-artificial
stack: [python-3.12, ultralytics, opencv, pandas, numpy, openpyxl, xlrd]
tags: [vision-artificial, conteo-rosas, pronostico, cosecha]
status: active
created: 2026-10-14
updated: 2026-10-15
relationships:
  - project: conteo-rosas-portable-2026-10-08
    tipo: mismo-proyecto-copia-portable
    evidencia: README.md y GUIA_USO.md son byte-por-byte idénticos entre ambas carpetas (diff vacío); misma estructura src/conteo_rosas y paquete "conteo-rosas". Vision-artificial tiene remoto git `origin` apuntando a Azure DevOps (SunshineBouquetCompany/Zeus - IntegrationHub/Vision-artificial) y un único commit "Versión nueva del proyecto de conteo de rosas"; conteo-rosas-portable-2026-10-08 no tiene remoto y su único commit es "Versionado inicial del proyecto conteo-rosas", consistente con ser un export portable (nombre con fecha, incluye `.venv`/Dockerfile según su nodo) de este mismo proyecto.
---

## Propósito

"Sunshine — Conteo de rosas": cuenta rosas en video por visión artificial
(detección y tracking), compara los conteos contra cortes reales semanales
(Excel multifinca + QA) y genera un pronóstico de cosecha para la semana ISO
siguiente. Es el repositorio canónico (conectado a Azure DevOps) del mismo
proyecto que `conteo-rosas-portable-2026-10-08` distribuye como paquete
portable.

## Puntos de entrada

- Lanzadores `.bat` en la raíz: `preparar.bat`, `comparar.bat`, `pronostico.bat`,
  `flujo_semanal.bat`, `organizar.bat`, `procesar_lote.bat`, `validar_pronostico.bat`,
  `empaquetar.bat`, `pruebas.bat`, `cli.bat`.
- CLI: `cli.py`.
- Paquete: `src/conteo_rosas/` (`dominio`, `ingesta`, `deteccion`, `agregacion`,
  `comparacion`, `pronostico`, `entrenamiento`, `proyeccion`, `distribucion`,
  `validacion`, `cli/`, `interfaces/gui/`).
- Configuración: `config.yaml` raíz y `configs/` (`comparacion.yaml`,
  `pronostico.yaml`, `entrenamiento.yaml`, `fenologia.yaml`, `botsort_rosas.yaml`,
  `modelos_pronostico_activos.json`). Rutas locales en `CAMBIAR_RUTAS.txt`.
- Tests: `tests/` (`conteo_rosas/`, `integration/`).
- Scripts auxiliares en `scripts/` (entrenamiento, auditoría, empaquetado, GUI).

## Docs propios

- `README.md` — visión general, instalación y uso (fuente principal).
- `GUIA_USO.md` — guía operativa semanal.
- `docs/TECNICO.md` — arquitectura y contratos técnicos.
- `docs/MANUAL_USUARIO.md`, `docs/NEGOCIO_Y_OPERACION.md`,
  `docs/MODELOS_Y_ENTRENAMIENTO.md`.
- `docs/historico/` — material histórico, no vigente.

## Notas

- Repo git con remoto Azure DevOps (`Vision-artificial`); un único commit
  "Versión nueva del proyecto de conteo de rosas".
- No tiene `pyproject.toml` en la raíz pese a que el README lo menciona
  (`requires-python = ">=3.12,<3.13"`, paquete `conteo-rosas` v0.2.0); verificar
  si falta el archivo o está excluido de git antes de instalar con `pip install -e .`.
- Relación con `conteo-rosas-portable-2026-10-08` confirmada por contenido
  textual idéntico (README/GUIA_USO) y estructura, no asumida solo por el nombre.
