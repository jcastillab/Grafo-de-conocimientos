---
name: preparar-proyecto
description: Incorpora un proyecto de C:\Source al sistema de trabajo del equipo - git, .gitignore, AGENTS.md + CLAUDE.md, dependencias de desarrollo (ruff, playwright), permisos base y commit inicial. Úsalo cuando un proyecto no tenga git o AGENTS.md, o cuando el usuario pida "preparar" / "onboardear" un proyecto.
argument-hint: <carpeta del proyecto>
---

Plantillas en la carpeta `templates/` de esta skill. Proyecto: `$ARGUMENTS`
(si no se indicó, pregúntalo).

1. **Diagnóstico.** Revisa qué hay: `.git`, `AGENTS.md`, `CLAUDE.md`,
   `README.md`, `.gitignore`, venv (`venv`/`.venv`) y su Python,
   `requirements*.txt`/`pyproject.toml`, `tests/`, `.claude/settings*.json`.
   Lee el nodo del grafo del proyecto. Muestra al usuario en una tabla qué
   existe y qué vas a crear; no sobrescribas nada sin mostrarlo primero.
2. **`.gitignore`.** Parte de `templates/gitignore-python`. Pregunta qué
   carpetas de datos son insumos crudos o salidas generadas (por defecto no se
   versionan datos de negocio) y agrégalas. Si ya existe, solo añade lo que
   falte.
3. **git.** Si no hay repo: `git init -b main`. Revisa `git status` antes del
   primer commit: que no entren venvs, datos, binarios grandes (>5 MB) ni
   secretos (`.env`, claves, tokens). Si ves algo dudoso, pregunta.
4. **`AGENTS.md`.** Desde `templates/AGENTS.md`, redactado con lo que
   encontraste en el código (no inventes): reglas de oro (si es matemático,
   desde la skill `protocolo-matematico`), qué es realmente el núcleo,
   estructura, comandos reales probados, cómo validar. Muéstraselo al usuario
   y ajusta antes de escribirlo. Si ya existe, propón solo lo que falte.
5. **`CLAUDE.md`.** Si no existe, cópialo de `templates/CLAUDE.md` (una línea,
   `@AGENTS.md`). Si existe, verifica que contenga `@AGENTS.md`; sin esa línea
   el `AGENTS.md` se ignora porque `C:\Source\CLAUDE.md` está más arriba.
6. **Dependencias de desarrollo.** `requirements-dev.txt` desde la plantilla
   (ruff; playwright solo si el proyecto tiene interfaz que documentar).
   Instálalas en el venv del proyecto con su propio Python. Playwright además
   necesita `python -m playwright install chromium` (descarga ~150 MB: pide
   confirmación).
7. **Permisos base.** `.claude/settings.json` desde `templates/settings.json`
   (se versiona; lo personal sigue en `settings.local.json`). Si ya existe,
   mezcla las reglas sin borrar las del usuario.
8. **Tests.** Corre la suite con el venv. Si no hay `tests/` o falla, repórtalo
   (no lo arregles aquí: es la primera tarea para `/desarrollar`).
9. **Commit inicial** (`chore: incorporar proyecto al sistema de trabajo`).
10. **Grafo.** Actualiza el nodo del proyecto (git, AGENTS.md, notas) vía
    `project-scout` o editándolo si el cambio es menor.

Cierra con la tabla de lo hecho y la lista de deuda encontrada (posibles
primeras tareas para `/desarrollar`).
