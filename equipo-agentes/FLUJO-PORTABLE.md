# Flujo de desarrollo portable para agentes

Este documento es el método común del equipo. No requiere Claude Code, nombres
de comandos, agentes, skills, hooks ni APIs particulares. Si la herramienta
tiene esas funciones, puede usarlas; si no, el agente actual realiza los pasos
secuencialmente y declara qué revisiones no pudo independizar.

## Cuándo se considera terminado

La tarea está terminada cuando se verificaron sus criterios de aceptación, se
ejecutaron las pruebas o comprobaciones relevantes, se revisó el diff, se
actualizó la documentación afectada y los cambios propios quedaron en commits
pequeños. Informa resultados con evidencia; no afirmes que se ejecutó algo que
no se ejecutó.

## Pasos

1. **Entender el contexto.** Lee las instrucciones aplicables (`AGENTS.md` y
   equivalentes), la documentación relevante y el estado de Git. No sobrescribas
   ni incluyas cambios preexistentes ajenos. Si el objetivo no está claro,
   pregunta antes de hacer cambios.
2. **Explorar.** Ubica el código, las pruebas existentes y patrones cercanos.
   Usa búsqueda o exploración delegada si está disponible; de lo contrario,
   explora directamente.
3. **Planificar.** Resume objetivo, archivos probables y criterios de aceptación
   comprobables. Para cambios grandes o ambiguos, valida el plan con el usuario
   antes de editar.
   Para tareas con varios commits, trabaja en una rama de tarea si no estás ya
   en una; no cambies de rama con modificaciones sin guardar.
4. **Probar primero cuando corresponda.** Añade o ajusta pruebas que expresen el
   comportamiento esperado y verifica que detectan el problema. Si no hay un
   marco de pruebas, usa la comprobación automatizada más cercana y explica la
   limitación.
5. **Implementar de forma acotada.** Cambia lo mínimo necesario. No amplíes el
   alcance ni refactorices áreas no relacionadas. Ejecuta pruebas específicas y
   luego las comprobaciones pertinentes del proyecto.
6. **Revisar.** Inspecciona el diff completo buscando errores, regresiones,
   secretos, cambios accidentales y documentación desactualizada. Si hay otro
   agente disponible, pídele una revisión independiente con el diff y los
   criterios; si no, haz una auto-revisión explícita y no la presentes como
   independiente.
7. **Corregir y verificar.** Atiende hallazgos confirmados y vuelve a ejecutar
   las comprobaciones afectadas. Comunica cualquier hallazgo que decidas dejar
   pendiente y por qué.
8. **Documentar y versionar.** Actualiza la documentación necesaria. Revisa
   `git diff` y `git status`; crea commits pequeños, enfocados y con mensajes
   claros. Separa cambios independientes en commits diferentes y no incluyas
   archivos ajenos. Usa mensajes breves y descriptivos, por ejemplo
   `docs: añade flujo portable de agentes`. No hagas push, merge ni publiques
   cambios salvo petición.
9. **Cerrar.** Resume qué cambió, commits creados, comprobaciones ejecutadas y
   pendientes o limitaciones.

## Uso de los roles disponibles

Los perfiles de `plugins/equipo/agents/` son guías de especialidad, no requieren
que la plataforma registre agentes con esos nombres. Un agente puede leer el
perfil pertinente y adoptar ese rol para una revisión acotada. Los archivos de
`plugins/equipo/skills/` contienen procedimientos y referencias reutilizables;
consulta solo los relevantes. Omite la cabecera de metadatos si tu herramienta
no la reconoce.

Si la plataforma permite delegar, asigna tareas independientes con archivos y
criterios claros, y evita dos escritores sobre los mismos archivos. Si no
permite delegar, realiza los pasos en una sola sesión y señala esa limitación.

## Plantilla de solicitud para otro agente

> Sigue `equipo-agentes/FLUJO-PORTABLE.md` y las instrucciones `AGENTS.md` del
> proyecto. Tarea: **[describir objetivo]**. Criterios de aceptación:
> **[lista verificable]**. Conserva cambios ajenos, ejecuta las comprobaciones
> pertinentes, revisa el diff y guarda mis cambios en commits pequeños y
> separados por tema. No hagas push ni merge.
