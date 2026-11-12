---
name: ver-grafo
description: Genera o muestra una visualización HTML de los proyectos contenidos en una carpeta base indicada por la persona usuaria.
---

1. Obtén la ruta de la carpeta base de la petición o del contexto actual. Si es
   ambigua, pregunta antes de escanear.
2. Genera el HTML con `tools/generar_grafo.py <carpeta-base>`. El modo normal
   descubre carpetas desde cero y no carga inventarios, fichas ni dependencias
   de otros orígenes.
3. Solo pasa `--projects-dir` o `--deps-dir` si la persona pidió usar esos
   metadatos y confirmó que corresponden a la misma carpeta base.
4. No inventes relaciones. Una vista sin relaciones es válida si no se
   proporcionaron relaciones verificadas.
5. Abre o presenta el archivo HTML resultante si la plataforma lo permite; si
   no, devuelve su ruta completa y cómo abrirlo.
6. Resume el número de carpetas incluidas y la ubicación del archivo. No
   reportes referencias a ubicaciones no consultadas.
