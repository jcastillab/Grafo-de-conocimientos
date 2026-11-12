# Instrucciones para agentes

- Responde en español, salvo que el usuario pida otro idioma.
- Antes de cambiar código, revisa el estado de Git y las instrucciones de las
  carpetas afectadas. Conserva cambios previos que no sean tuyos.
- Para tareas de desarrollo, sigue [`equipo-agentes/FLUJO-PORTABLE.md`](equipo-agentes/FLUJO-PORTABLE.md).
- Mantén cada commit pequeño, enfocado y con mensaje claro. No mezcles tareas
  independientes; verifica que solo incluyes tus propios cambios.
- Este repositorio no requiere dependencias externas para generar el grafo.
  Comprobaciones básicas: `python tools/generar_grafo.py --help` y
  `python -m py_compile tools/generar_grafo.py tools/analizar_dependencias.py`.
  Consulta `README.md` para generar una visualización.
