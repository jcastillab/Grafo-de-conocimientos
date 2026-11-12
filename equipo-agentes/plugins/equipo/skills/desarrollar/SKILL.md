---
name: desarrollar
description: Lleva una tarea de desarrollo de punta a punta: explorar, planificar, probar, implementar, revisar, documentar y versionar. Úsalo cuando la persona usuaria pida construir, corregir o mejorar un proyecto.
argument-hint: <tarea a desarrollar>
---

# Protocolo de trabajo

Un cambio está **terminado** solo cuando: los criterios de aceptación tienen
tests, la suite completa está verde, pasó revisión independiente, la
documentación visible está al día y quedó en un commit. Muestra evidencia
(salida de pytest, archivo:línea), nunca solo "funciona".

Reglas:
- **Una tarea = un commit revisable.** Si el plan pasa de ~400 líneas de diff
  o mezcla temas, pártelo y haz un ciclo por parte.
- **Rama por tarea** (`feat/…`, `fix/…`, `refactor/…`) salvo cambios
  triviales; nunca trabajes directo en `main` algo de más de un commit.
- **Paralelizar**: dos tareas sin archivos en común van en sesiones separadas
  en worktree; nunca dos escritores sobre los mismos archivos.
- **Commits semánticos** (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`,
  `chore:`), en español, el porqué en el cuerpo.
- La sesión se abre con la carpeta del proyecto como directorio de trabajo (si
  no, sus hooks y su `AGENTS.md` no se cargan).
- Los hooks del plugin corren pytest al terminar cada turno con `.py`
  cambiados y formatean con ruff al editar. Si el hook bloquea, arregla la
  causa; nunca lo esquives.

# Pasos

Tarea: `$ARGUMENTS`

0. **Contexto.** Lee las instrucciones y documentación que existan dentro del
   proyecto seleccionado. No consultes nodos ni inventarios de otras carpetas.
   Si el proyecto no tiene git o instrucciones locales, propone
   `preparar-proyecto` primero. Comprueba
   `git status`: si hay cambios ajenos sin commitear, pregunta antes de
   seguir. Crea la rama de la tarea.
1. **Explorar** (solo si el área no es conocida): subagente `Explore`
   enfocado en los archivos que la tarea toca, funciones reutilizables y
   tests existentes.
2. **Plan.** Redacta: objetivo, archivos a tocar, qué se reutiliza y
   **criterios de aceptación verificables** (cada uno se puede convertir en
   un test o en un comando con salida esperada). Para cambios numéricos,
   incluye baseline y métrica según la skill `protocolo-matematico`.
   Pide aprobación al usuario antes de seguir (plan mode si la tarea es
   grande). Si el backlog trae ítems independientes, propón sesiones
   paralelas para ellos.
3. **Tests primero.** Subagente `equipo:escritor-tests` con la ruta del proyecto, la
   tarea y los criterios. No sigas hasta que reporte los tests fallando por
   la razón esperada.
4. **Implementar** en la sesión principal hasta que los tests nuevos y la
   suite completa pasen. No edites los tests para que pasen; si un test está
   mal, explica por qué y corrígelo como cambio aparte y visible.
5. **Revisión en paralelo** (un solo mensaje, varios agentes):
   - skill `code-review` sobre el diff de la rama;
   - subagente `equipo:rigor-numerico-scout` si se tocó lógica numérica, de
     modelado u optimización (pásale el módulo cambiado, no todo el proyecto);
   - subagente `equipo:documentador` si cambió algo que ve una persona: pantallas,
     comandos, mensajes de error, archivos de salida, configuración.
6. **Corregir** los hallazgos confirmados. Lo que decidas no corregir, dilo
   con el motivo. Vuelve a correr la suite.
7. **Commit** con la skill `commit:commit`. Actualiza el nodo del grafo si
   cambió el propósito, stack o puntos de entrada del proyecto.

Cierra con: qué cambió, evidencia (tests, revisión), qué quedó fuera.
