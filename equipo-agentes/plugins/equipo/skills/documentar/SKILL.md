---
name: documentar
description: Genera o actualiza documentación para personas del proyecto seleccionado con el agente documentador. Úsalo cuando se pida un manual, guía, README o actualizar documentación tras un cambio.
argument-hint: <proyecto> [usuario|admin|readme|actualizar]
---

Pedido: `$ARGUMENTS`

1. Identifica el proyecto y qué documento(s). Si no está claro para quién es
   (usuario final, administrador, desarrollador), pregúntalo: el rol define el
   manual.
2. Si el proyecto tiene interfaz y no tiene Playwright en su venv, avisa que
   las capturas lo necesitan (`preparar-proyecto`, paso 6) antes de lanzar.
3. Lanza el subagente `equipo:documentador` con: ruta del proyecto, documento(s),
   rol, y si es una actualización, qué cambió (diff o descripción).
   Manuales de roles distintos son independientes: lánzalos en paralelo.
4. Al volver, abre el HTML generado para que el usuario lo revise (navegador
   del panel) y resume lo que el documentador reportó, incluidos pendientes y
   comportamientos confusos de la app que haya encontrado.
