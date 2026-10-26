---
name: equipo-agentes
path: C:\Source\equipo-agentes
stack: [claude-code-plugin, markdown, powershell, python, playwright]
tags: [tooling, agentes, documentacion, protocolo]
status: active
created: 2026-10-23
updated: 2026-10-23
relationships: []
---

## Propósito

Plugin de Claude Code `equipo` (marketplace local `equipo-agentes`) con todo
lo compartido entre proyectos de `C:\Source`: el método de desarrollo
(`/desarrollar`), la incorporación de proyectos (`/preparar-proyecto`), la
documentación estilo manual de Conteo Rosas (`/documentar` + agente
`documentador` + skill `estilo-documentacion`), el rigor numérico
(`protocolo-matematico`, `rigor-numerico-scout`) y las skills del grafo.
Reemplaza a `C:\Source\.claude\agents|skills`, que no se ven desde proyectos
con git propio ni desde worktrees.

## Puntos de entrada

- Instalación: `claude plugin marketplace add C:\Source\equipo-agentes` +
  `claude plugin install equipo@equipo-agentes` (nivel usuario; se lee directo
  de la carpeta).
- `plugins/equipo/skills/*/SKILL.md`, `plugins/equipo/agents/*.md`.
- `plugins/equipo/hooks/` — Stop (pytest) y PostToolUse (ruff), desactivados
  en `hooks.pendiente.json` hasta autorizar los `.ps1`.
- `plugins/equipo/skills/estilo-documentacion/capturar.py`,
  `empaquetar_html.py`.

## Docs propios

- `README.md` (instalar, activar hooks, compartir).

## Notas

- El antivirus corporativo bloquea leer/ejecutar `.ps1` nuevos y `.exe`
  recién instalados (p. ej. `ruff.exe`); los `.py` dentro de `C:\Source` sí
  corren.
- Los agentes del plugin se invocan como `equipo:<nombre>`.
