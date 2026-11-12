---
name: revisar-rigor-matematico
description: Revisa el rigor numérico/estadístico del proyecto indicado contra el protocolo compartido. Úsalo cuando la persona usuaria pida auditar leakage, baseline, métricas o reproducibilidad de modelos u optimizadores.
---

1. Identifica el proyecto objetivo (si no es obvio por el contexto,
   pregunta qué carpeta o módulo revisar).
2. Lanza el subagente `equipo:rigor-numerico-scout` (Agent tool) con el path de ese
   proyecto.
3. Presenta su reporte al usuario tal cual (cumple/no cumple/no aplica por
   punto de checklist + veredicto), sin reinterpretarlo ni suavizarlo.
4. Si el usuario pide corregir algo de lo encontrado, es trabajo aparte —
   esta skill solo diagnostica, no corrige.

Termina con el veredicto de una línea que dio el subagente.
