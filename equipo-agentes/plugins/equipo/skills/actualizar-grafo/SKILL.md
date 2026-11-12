---
name: actualizar-grafo
description: Descubre y actualiza un grafo de conocimientos desde la carpeta base que indique la persona usuaria. Úsalo cuando pida generar, regenerar o actualizar el grafo.
---

1. Determina la carpeta base a partir de la petición o del contexto actual. Si
   no se puede identificar con certeza, pregunta; no asumas una ruta conocida.
2. Lista únicamente las subcarpetas directas de esa carpeta. Excluye la propia
   herramienta del grafo y archivos/carpetas de salida. No recorras subcarpetas
   de forma recursiva salvo que se solicite.
3. Para una vista básica, ejecuta el generador de este repositorio con la ruta
   explícita de la carpeta base. No leas fichas, índices ni cachés de otro
   origen; el generador debe comenzar sin metadatos implícitos.
4. Solo si la persona solicita enriquecer la vista, inspecciona proyectos
   dentro de la carpeta base y crea relaciones a partir de evidencia verificable
   allí. No infieras relaciones por nombres parecidos.
5. Si se solicita guardar fichas o datos auxiliares, acuerda primero su
   ubicación y pasa esa ruta explícitamente al generador.
6. Informa la ruta del HTML generado, cuántos nodos contiene y cualquier
   limitación real. No menciones referencias a carpetas que no se hayan
   solicitado ni encontrado en la carpeta base.
