---
name: preparar-proyecto
description: Prepara el proyecto indicado según su tecnología, convenciones locales y herramientas de agente solicitadas. Úsalo cuando se pida preparar u onboardear un proyecto.
argument-hint: <carpeta del proyecto>
---

Proyecto: `$ARGUMENTS`. Si no se indicó una ruta inequívoca, pregunta.

1. **Diagnóstico.** Inspecciona la carpeta elegida: control de versiones,
   instrucciones, documentación, archivos de dependencias, pruebas y estructura
   real. No consultes inventarios externos.
2. **Plan.** Muestra qué existe, qué propones crear y por qué. Confirma antes de
   escribir, instalar paquetes, inicializar Git o cambiar configuración.
3. **Convenciones.** Usa solo plantillas que correspondan a la tecnología y al
   agente solicitados. Adapta cada una a los hechos verificados; si no existe
   una plantilla adecuada, crea instrucciones neutrales o pregunta.
4. **Control de versiones.** Si se solicita inicializar Git, revisa antes los
   archivos que se incluirían y prepara un `.gitignore` apropiado al contenido
   comprobado. Nunca incluyas secretos, datos privados o artefactos voluminosos
   por defecto.
5. **Instrucciones locales.** Si se solicitan, crea o actualiza el archivo de
   instrucciones que use el agente elegido. No añadas archivos de integración
   para otras plataformas salvo petición explícita.
6. **Dependencias y permisos.** Propón solo dependencias requeridas por el
   proyecto. Explica origen, tamaño y efectos; espera confirmación antes de
   instalarlas o habilitar hooks.
7. **Validación.** Ejecuta las comprobaciones propias del proyecto. Si no hay
   pruebas o comandos verificables, dilo; no inventes una suite ni la declares
   aprobada.
8. **Grafo opcional.** Solo si se solicita, actualiza el grafo de la carpeta
   base explícitamente elegida, sin incorporar metadatos de otras ubicaciones.
9. **Versionado.** Revisa el diff y crea commits únicamente si se pidió o está
   autorizado por las instrucciones vigentes. Manténlos pequeños y enfocados.

Termina con lo realizado, validaciones ejecutadas y decisiones pendientes.
