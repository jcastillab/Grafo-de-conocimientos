---
name: protocolo-matematico
description: Checklist compartida de rigor numérico/estadístico (baseline, anti-leakage, métrica única, reproducibilidad, tests numéricos, trazabilidad) para proyectos de modelado, ML/DL, forecasting u optimización. Referencia para auditar o para redactar el AGENTS.md de un proyecto matemático.
---

# Protocolo de rigor matemático

Checklist compartida para proyectos de modelado estadístico/ML/DL u
optimización numérica bajo `C:\Source`. Generaliza lo que `markov_v3` ya
probó en la práctica (ver `markov_v3/AGENTS.md` como ejemplo vivo completo)
en una lista de verificación reutilizable para cualquier proyecto nuevo del
mismo tipo.

Esta checklist es para **auditoría externa** (lo que usa el subagente
`rigor-numerico-scout`), no reemplaza el `AGENTS.md` propio de cada
proyecto. Cada proyecto matemático sigue necesitando su propio `AGENTS.md`
con sus reglas concretas (métricas exactas, estructura de carpetas, comandos
de pipeline, etc.).

## Cuándo aplica

Proyectos cuyo núcleo es modelado estadístico, machine learning / deep
learning, forecasting, u optimización numérica (programación lineal,
simulación, etc.). No aplica a proyectos de visión por computador puro,
ingestión/ETL de datos, o front-end — aunque un proyecto mixto (p.ej. CV +
un módulo de forecasting) puede aplicar la checklist solo a ese módulo.

## Checklist

1. **Baseline obligatorio y documentado.** Todo modelo nuevo se compara
   contra un baseline simple explícito antes de aceptarse. Gana por métrica
   en igualdad de condiciones de evaluación, no por complejidad.
2. **Anti-data-leakage verificable.** Si hay dimensión temporal o causal,
   todo feature usado para predecir en el origen `t0` tiene timestamp
   `<= t0`. Debe existir una forma explícita de verificarlo (test automático
   o un backtest causal tipo rolling-origin), no solo una convención de
   código.
3. **Métrica principal única y justificada por escrito.** Se elige y
   documenta antes de comparar modelos entre sí, no se decide ad-hoc por
   experimento ni se cambia a mitad de camino sin justificar por qué.
4. **Reproducibilidad.** Semillas fijas donde haya aleatoriedad, entorno
   declarado (requirements/pyproject/lockfile), y todos los parámetros de
   configuración centralizados en un único archivo (nunca hardcodeados
   dentro del código).
5. **Tests de validación numérica.** Al menos smoke tests que corran el
   pipeline de punta a punta y validen invariantes del dominio (rangos,
   no-negatividad, consistencia de shapes/dimensiones) — no basta con tests
   unitarios de funciones sueltas.
6. **Trazabilidad de corridas.** Los outputs de una corrida son
   reproducibles o idempotentes, y están claramente separados de los inputs
   crudos (los datos de entrada no se editan a mano).

## Optimización combinatoria (ruteo, TSP/VRP, asignación, scheduling)

Traducción de la checklist para proyectos cuyo núcleo es un optimizador y no
un predictor:

1. **Baseline** = (a) la solución trivial u operativa actual (p. ej. el orden
   de paradas tal cual viene en el archivo fuente) y (b) el **óptimo exacto**
   en instancias pequeñas (fuerza bruta / Held-Karp / MILP) donde sea
   tratable. Una heurística se acepta midiendo cuánto mejora a (a) y cuánto
   se aleja de (b).
2. **"Leakage"** = que el optimizador no lea información que en producción no
   existe al planear (p. ej. el orden real ejecutado, tiempos reales). Un
   test lo hace explícito si esas columnas existen en los insumos.
3. **Métrica** = el objetivo (distancia, tiempo, costo) + **gap %** contra el
   óptimo o la mejor cota conocida: `gap = (heurística − óptimo) / óptimo`.
   Documentar qué aproxima (p. ej. haversine ≠ distancia por carretera).
4. **Reproducibilidad** = determinismo o semilla fija en metaheurísticas;
   límites de tiempo del solver declarados en config.
5. **Tests** = factibilidad (permutación válida, restricciones cumplidas),
   heurística ≤ baseline trivial, heurística ≥ óptimo exacto en instancias
   chicas, y un smoke E2E sobre los datos reales.
6. **Trazabilidad** = igual que arriba.

## Cómo se usa

- Auditoría: skill `revisar-rigor-matematico` → subagente
  `rigor-numerico-scout` (que precarga esta skill).
- Proyecto nuevo o sin reglas escritas: usa esta checklist como base de las
  "reglas de oro" de su `AGENTS.md` (skill `preparar-proyecto`).
