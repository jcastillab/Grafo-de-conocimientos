---
name: revisar-rigor-matematico
description: Revisa el rigor numérico/estadístico de un proyecto matemático de C:\Source contra el protocolo compartido (skill protocolo-matematico). Úsalo cuando el usuario pida auditar o revisar rigor, data leakage, baseline, métricas o reproducibilidad de un proyecto de modelado estadístico/ML/DL u optimización numérica.
---

1. Identifica el proyecto objetivo (si no es obvio por el contexto,
   pregúntale al usuario cuál subcarpeta de `C:\Source` revisar).
2. Lanza el subagente `equipo:rigor-numerico-scout` (Agent tool) con el path de ese
   proyecto.
3. Presenta su reporte al usuario tal cual (cumple/no cumple/no aplica por
   punto de checklist + veredicto), sin reinterpretarlo ni suavizarlo.
4. Si el usuario pide corregir algo de lo encontrado, es trabajo aparte —
   esta skill solo diagnostica, no corrige.

Termina con el veredicto de una línea que dio el subagente.
