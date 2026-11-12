# Equipo de agentes — método portable e integración Claude Code

Este directorio separa el método general de las integraciones de plataforma.
Las instrucciones describen procedimientos; no contienen inventarios ni
supuestos sobre las carpetas de un usuario.

## Método portable

Lee [`FLUJO-PORTABLE.md`](FLUJO-PORTABLE.md) para aplicar el ciclo de trabajo
desde cualquier agente. En este repositorio, `../AGENTS.md` es el punto de
entrada para herramientas que reconocen ese formato. En otra herramienta,
indícale que lea ambos documentos y siga la plantilla de solicitud del flujo.

Los perfiles y skills bajo `plugins/equipo/` son guías procedimentales. Úsalos
solo cuando la tarea lo requiera y basa cualquier dato factual en el proyecto
seleccionado por la persona usuaria.

## Integración opcional: Claude Code

`plugins/equipo/` conserva los formatos propios de Claude Code: agentes, skills,
comandos y hooks. Esos mecanismos son opcionales; el método portable no depende
de que estén disponibles.

Para instalar el plugin en Claude Code:

Sustituye el marcador por la ruta local real de este directorio.

```powershell
claude plugin marketplace add <ruta-al-repositorio>\equipo-agentes
claude plugin install equipo@equipo-agentes
```

Reinicia Claude Code y comprueba que la interfaz muestre los agentes del plugin.

Los hooks vienen desactivados en `plugins/equipo/hooks/hooks.pendiente.json`.
Antes de activarlos, revisa qué ejecutan, confirma que están permitidos en el
entorno y sigue las instrucciones de esa configuración.

## Perfiles disponibles

| Perfil | Función procedimental |
|---|---|
| `escritor-tests` | Convierte criterios de aceptación en pruebas. |
| `documentador` | Documenta el comportamiento verificado del proyecto seleccionado. |
| `rigor-numerico-scout` | Audita modelos y optimizadores según evidencia del proyecto. |
| `project-scout` | Documenta una carpeta seleccionada sin importar datos externos. |
| `backend-fastapi`, `frontend-angular` | Implementan componentes según contratos y convenciones locales. |
| `auditor-seguridad` | Revisa riesgos de seguridad con evidencia. |

Los nombres son identificadores de la integración; cuando una plataforma no
permita registrar esos perfiles, el agente puede leer el archivo Markdown
correspondiente y seguirlo como una instrucción de rol.
