# AGENTS.md - <proyecto>

<Una o dos frases: qué hace el proyecto, para quién y qué entrega.>

## Reglas de oro

<!-- 4 a 8 reglas que un agente NO puede romper. Concretas y verificables.
     Proyecto matemático: parte de la skill protocolo-matematico (baseline,
     leakage, métrica, config única). Ejemplos de markov_v3/AGENTS.md:
     "M3 es el baseline obligatorio", "Todo parámetro vive en config/pipeline.yaml". -->

1. **<regla>.** <por qué / cómo se verifica>
2. **Todo parámetro vive en `<archivo de config>`**, nunca hardcodeado.
3. **Los insumos crudos (`<carpeta>`) no se editan a mano**; todo lo derivado se regenera.

## Qué es realmente el núcleo

<!-- Lo que un agente malinterpretaría leyendo solo el stack. Ej.: "el
     optimizador es una heurística TSP determinística, no LP aunque pulp esté
     en requirements". Métrica principal y qué aproxima. -->

## Estructura

```text
<carpeta>/   <qué hay>
tests/       pytest
manual/      manuales para personas (skill estilo-documentacion)
```

## Entorno y comandos

```powershell
# Entorno: <venv|.venv> (Python <versión>)
.\<venv>\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt

# Tests (también los corre el hook al terminar cada turno):
.\<venv>\Scripts\python.exe -m pytest -q

# <Pipeline / app / scripts principales>:
.\<venv>\Scripts\python.exe <script>
```

## Cómo validar un cambio

<!-- Qué comando o salida demuestra que el sistema sigue bien además de pytest:
     un smoke E2E, una corrida de validación, un mapa que se regenera. -->

## Cómo se trabaja aquí

Con el plugin `equipo`: `/desarrollar <tarea>` (tests primero, revisión,
commit), `/documentar` para manuales, `/revisar-rigor-matematico` para
auditar. Commits semánticos en español.
