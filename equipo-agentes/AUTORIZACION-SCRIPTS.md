# Scripts y ejecutables para autorizar

Inventario de todo lo que el sistema de trabajo (plugin `equipo` y piloto
`optimizacion rutas`) crea o ejecuta, para pedir la excepción al antivirus /
política de seguridad. Estado probado el 2026-10-23 en este PC.

## Bloqueados hoy (necesitan autorización)

| # | Archivo (ruta completa) | Tipo | Qué hace | Cuándo corre | Lo ejecuta | Red / escribe | SHA-256 | Imprescindible |
|---|---|---|---|---|---|---|---|---|
| 1 | `C:\Source\equipo-agentes\plugins\equipo\hooks\verificar-tests.ps1` | PowerShell | Si hay `.py` cambiados sin commit, corre `pytest` del venv del proyecto; si falla, impide que Claude termine el turno. | Automático, al final de cada turno de Claude Code (hook Stop). | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File …` | No / un archivo marca en `%TEMP%\claude-equipo-tests-*.ok` | `07a0f52c1063ea5957aa41e4bde64354f4490dc634436d6fed3db9a7e8a6487c` | Sí: es el guardarraíl principal. |
| 2 | `C:\Source\equipo-agentes\plugins\equipo\hooks\formatear.ps1` | PowerShell | Formatea con `ruff` el `.py` que Claude acaba de editar. | Automático, tras cada edición (hook PostToolUse). | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File …` | No / reescribe solo ese `.py` | `e65101189b8dc1fceaa085a5002e2a5ea061937bdbab471eef2894c50ba13a64` | Recomendado. |
| 3 | `C:\Source\optimizacion rutas\venv\Scripts\ruff.exe` (ruff 0.17.2, PyPI) y su equivalente en cada venv | Ejecutable | Linter/formateador de Python. `python -m ruff` también falla con *Acceso denegado*. | Por el hook 2 y a mano. | El propio `.exe` | No / reescribe `.py` | `1e9625f0d34342e1ddde6eaa1410063bea9f1e8cd129de893df0718e4e10d762` | Recomendado (sin él, el hook 2 no hace nada). |

Síntoma observado: *"Acceso denegado a la ruta de acceso …"* incluso para
**leer** el `.ps1` (el ACL permite lectura y la ExecutionPolicy es
Bypass/Unrestricted): lo bloquea el antivirus/EDR. Probablemente afecte a
cualquier `.ps1` nuevo y a los `.exe` recién instalados por pip.

## Pendientes de instalar (pedir junto con lo anterior)

| # | Qué | Para qué | Descarga | Comando |
|---|---|---|---|---|
| 4 | Paquete `playwright` (PyPI) en el venv de cada proyecto con interfaz | Capturas anotadas de los manuales (`capturar.py`). | ~40 MB | `<venv>\Scripts\python.exe -m pip install playwright pillow` |
| 5 | **Navegador Chromium de Playwright** | Lo abre `capturar.py` en modo headless contra la app local. | ~150 MB a `%LOCALAPPDATA%\ms-playwright\` | `<venv>\Scripts\python.exe -m playwright install chromium` |

Al instalarlo, verificar que no queden bloqueados `chrome.exe` /
`chrome-headless-shell.exe` dentro de `%LOCALAPPDATA%\ms-playwright\` ni el
`node.exe` que trae el paquete `playwright` (`<venv>\Lib\site-packages\playwright\driver\`).

## Ya funcionan (para que consten en la solicitud)

| # | Archivo | Tipo | Qué hace | Cuándo corre | Red / escribe | SHA-256 |
|---|---|---|---|---|---|---|
| 6 | `C:\Source\equipo-agentes\plugins\equipo\skills\estilo-documentacion\capturar.py` | Python | Abre pantallas con Playwright, dibuja recuadros rosa numerados y guarda capturas. | `/documentar` | Solo localhost o archivos locales / `manual\img\*.webp` | `f3f3e69560f5d29c143f408bade202497a854200bd72a8f94d32fa237b2c7ede` |
| 7 | `C:\Source\equipo-agentes\plugins\equipo\skills\estilo-documentacion\empaquetar_html.py` | Python | Incrusta imágenes en el HTML del manual (un solo archivo). | `/documentar` | No / `manual\*.html` | `ad798d0f0315d7accc83a06252a6a28cf01c333a1c9f383a7bbdc28c64d84ea9` |
| 8 | `C:\Source\.knowledge-graph\tools\analizar_dependencias.py` (ya existía) | Python | Grafo de imports de un proyecto (solo lee con `ast`). | `/profundizar-proyecto` | No / `.knowledge-graph\deps\*.json` | `630aa6f224b2f006d7ff079fa2e6df604d8866df9ef53f6e69f7e75019e923fd` |
| 9 | `C:\Source\optimizacion rutas\scripts\evaluar_baseline.py` | Python | Compara la heurística de orden de paradas con el orden del archivo y el óptimo exacto. | A mano | No / opcional `--csv` | `1e9d320b7dfd9483b3b81b882043ee74b491bb9d91813b6a618a423f79f76900` |

Los `.py` dentro de `C:\Source` corren con el Python de cada venv. Los `.py`
en la carpeta temporal (`%TEMP%`) están bloqueados, pero el sistema no
los necesita.

Ejecutables ya permitidos que el sistema usa: `git.exe` 2.55, `python.exe`
de cada venv, `claude` CLI 2.1.309, `powershell.exe`.

## Después de autorizar

1. Renombrar `C:\Source\equipo-agentes\plugins\equipo\hooks\hooks.pendiente.json` → `hooks.json`.
2. Abrir una sesión nueva en un proyecto y comprobar con un test roto a
   propósito que el turno se bloquea (ver `README.md`, sección 2).
3. Si cambias un `.ps1`, su SHA-256 cambia: vuelve a calcularlo
   (`Get-FileHash <ruta>`) por si la excepción es por hash.
