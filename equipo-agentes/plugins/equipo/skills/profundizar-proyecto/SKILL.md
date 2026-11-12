---
name: profundizar-proyecto
description: Calcula dependencias entre módulos Python de una carpeta de paquete indicada por la persona usuaria. Úsalo cuando pida explorar imports internos de un proyecto.
---

Esta skill analiza un paquete explícito. No mantiene una lista fija de proyectos
ni selecciona rutas por conocimiento previo.

1. Solicita o determina la carpeta raíz del paquete que se analizará. Si hay
   varias candidatas, pregunta cuál usar.
2. Comprueba que la carpeta existe y acuerda la ruta de salida del JSON. No
   sobrescribas datos existentes sin autorización.
3. Ejecuta `tools/analizar_dependencias.py` con el Python disponible y la ruta
   del paquete:

   ```text
   python tools/analizar_dependencias.py <raiz-paquete> --out <salida.json>
   ```

   Si el paquete requiere opciones, usa únicamente las que se deduzcan de su
   estructura actual y confirma el comando antes de ejecutarlo si cambia el
   alcance. Opciones disponibles: `--package-name`, `--strip-prefix` y
   `--shim-dir`.
4. El analizador lee código con `ast`; no ejecuta el proyecto analizado.
5. Informa la carpeta analizada, la salida y cualquier limitación. Para mostrar
   esos datos dentro de un grafo, pasa explícitamente la carpeta del JSON con
   `--deps-dir` al generador.
