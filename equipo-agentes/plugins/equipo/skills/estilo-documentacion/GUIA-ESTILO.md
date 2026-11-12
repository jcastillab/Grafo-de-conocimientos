# Guía de estilo de documentación — C:\Source

Destilada del manual de Conteo Rosas
(`conteo-rosas-portable-2026-10-08/manual/`: `MANUAL_USUARIO.md`,
`manual_usuario.html`, `MANUAL_ADMINISTRADOR.md`). Ese manual es el ejemplo
vivo: ante la duda, ábrelo y hazlo igual.

La idea central: **una persona que no sabe de informática hace su trabajo
leyendo esto, sin preguntar a nadie.** Didáctico, desmenuzado, con la pantalla
delante.

---

## 1. Un manual por rol

- Cada rol tiene su manual: `MANUAL_USUARIO.md` (quien opera día a día),
  `MANUAL_ADMINISTRADOR.md` (quien instala, configura, mantiene). Solo crea
  otro rol si de verdad existe (p. ej. "analista que lee el Excel").
- Proyecto sin interfaz: el "usuario" es quien corre los scripts y usa las
  salidas (Excel, mapas, reportes). Se documenta igual: comandos en lugar de
  botones, salidas en lugar de pantallas (y captura de la salida si es visual:
  mapa HTML, dashboard, Excel).
- El README del repo es para quien llega al código: qué es en 3 líneas, cómo
  arrancar, enlaces a los manuales y al `AGENTS.md`. Mismo tono, más corto.

## 2. Cabecera fija (en este orden)

```markdown
<img src="img/logo_sunshine_bouquet.png" alt="Sunshine Bouquet" width="240">

# Manual de <rol> — <Proyecto>

> **Para quién es:** <rol y qué hace, en una frase>. No hace falta saber de informática.
> **Qué NO cubre:** <tareas de otro rol> — está en `manual/MANUAL_<OTRO>.md`.
> Hay una versión interactiva con checklists y buscador de errores en `manual/manual_<rol>.html` (ábrela con doble clic).
>
> Última revisión: <aaaa-mm-dd>.
```

## 3. Estructura de secciones

Numeradas desde 0, en este orden (omite las que no apliquen, no inventes
relleno):

| # | Sección | Qué lleva |
|---|---|---|
| 0 | **¿Qué es esto?** | Qué hace en **3 puntos numerados**, en lenguaje de la operación (no técnico). Dónde funciona. Qué entrega. Luego **"Tu trabajo en N pasos"** (una línea `A → B → C`) y **"Palabras que vas a ver"** (glosario: término → significado cotidiano con ejemplo). |
| 1 | **Antes de empezar** | Checklist `- [ ]` de lo que hay que tener a mano. Tip si algo sorprende (p. ej. "no necesitas clave"). |
| 2 | **Arrancar** | Cómo abrirlo, cuánto tarda, qué ves cuando está listo, cómo apagarlo bien. |
| 3 | **Los menús / las partes** | Tabla *Menú → Para qué sirve*, con enlaces a la sección de cada tarea. Captura del menú. |
| 4… | **Una sección por tarea** | En el orden en que se hacen en la realidad. |
| n-2 | **Problemas comunes** | Tabla *Ves esto… → Qué pasa → Qué hacer* (ver §6). |
| n-1 | **Cuándo llamar al administrador** | Lista de situaciones concretas + "copia el mensaje exacto o haz captura (`Win + Shift + S`)". |

Manual de administrador, además: **"Tu papel"** (sección 0), requisitos del
PC, instalación paso a paso, configuración, **"Trampas silenciosas (no dan
error)"** (lista numerada de cosas que fallan sin avisar) y **"Anexo
técnico"** (variables de entorno, comandos, API, estructura de carpetas,
historial de cambios).

## 4. Cómo se escribe una tarea

1. Pasos numerados, **uno por acción**. Si un asistente tiene pasos propios,
   nómbralos igual que la app ("Paso 1 — Carpeta origen").
2. Nombres de la interfaz **en negrita y exactos**, como aparecen en pantalla:
   **Organizar → Nueva organización**, **Lanzar corrida**. Rutas de menú con
   `→`.
3. Lo que la app dice, *en cursiva y literal entre comillas*: *"Ingesta OK:
   N video(s)…"*. Sácalo del código (grep), no lo parafrasees.
4. Cierra la tarea con **✅ Listo cuando** + la señal visible de éxito.
5. Avisos en bloque citado, máximo uno o dos por tarea:
   - `> 💡 **Tip:**` atajo o aclaración útil.
   - `> ⚠️ **Cuidado:**` lo que hace perder trabajo o da resultados malos.
   - `❌ **NO**` para prohibiciones en checklists de entrega.
6. Valores esperados con **números concretos** en tabla (*Característica → Lo
   esperado*), nunca "un valor adecuado".
7. Botones de una pantalla: tabla *Botón → Qué hace*. Hojas de un Excel: tabla
   *Hoja → Qué contiene*. Casos que dependen de una elección: tabla *Si
   eliges… → Qué pasa*.
8. "Cómo leer los números": qué significa cada columna importante, qué valor
   es bueno/malo (umbrales), que **vacío no es cero**.
9. Rutas y comandos en bloque de código, una por bloque.

## 5. Capturas de pantalla

- **Una captura por paso con interacción.** Pantalla completa para orientarse
  la primera vez; recorte de la zona relevante después.
- Cada punto de interés lleva **recuadro rosa + círculo numerado** (lo dibuja
  `capturar.py`). Numera en el orden en que la persona lo usa. Marca solo lo
  que el texto menciona: 1 a 6 marcas por captura.
- El pie de figura nombra cada número: *"**1** **Elegir carpeta** o **2**
  pega la ruta, y **3** **Listar videos**."* En HTML: `<b class="n">1</b>`.
- `alt` describe la pantalla ("Paso 1 del asistente: carpeta origen").
- Datos de la captura: realistas pero no sensibles (nada de claves, cédulas,
  datos personales).
- Nombres de archivo: `img/<seccion>-<paso>.webp`. La especificación vive en
  `manual/capturas.json` para poder regenerarlas cuando cambie la interfaz.
- Si no puedes capturar (la app no levanta), deja `<!-- CAPTURA PENDIENTE:
  descripción y marcas -->` y repórtalo. Nunca una pantalla inventada.

## 6. Problemas comunes

- Fuente: los mensajes reales del código (`raise`, `HTTPException(detail=…)`,
  validaciones del frontend, `st.error`, mensajes de scripts). Grep y cópialos
  literales; usa `…` para las partes variables.
- Columnas: **Ves esto…** (mensaje o síntoma) · **Qué pasa** (causa en
  palabras simples) · **Qué hacer** (acción concreta; si es del admin:
  "**Avisa al administrador**" + qué decirle).
- Agrupa por área (Arranque, Cargar, Procesar…). En el HTML van en
  `window.ERR` (`[área, mensaje, causa, qué hacer]`) para el buscador.

## 7. Tono

- Tú, frases cortas, voz activa. Una idea por frase.
- Metáforas cotidianas para lo técnico ("la ventana negra es el motor: no la
  cierres").
- Toda sigla o término raro se explica la primera vez o va al glosario.
- Cuánto tarda, cuánto ocupa, qué pasa si se corta la luz: lo que la persona
  se va a preguntar, respóndelo antes.
- Honestidad: lo que está "en construcción" se dice; lo que no se debe tocar,
  se dice por qué.
- **Nada inventado.** Cada botón, mensaje, ruta y número debe existir en el
  código o verse en la app.

## 8. Dos formatos sincronizados

- `manual/MANUAL_<ROL>.md`: fuente legible en el repo, con las imágenes
  enlazadas (`img/…`).
- `manual/manual_<rol>.fuente.html`: la fuente del HTML, construida desde
  `plantilla.html` (misma estética que Conteo Rosas), con imágenes por ruta.
- `manual/manual_<rol>.html`: el entregable, generado con `empaquetar_html.py`
  desde la fuente; un solo archivo que se abre con doble clic. Nunca se edita
  a mano. Mismas secciones y contenido
  que el MD; el HTML convierte:
  - checklists → `.checklist` con progreso guardado en el navegador;
  - tareas largas → `.steps` con "Hecho" por paso;
  - Problemas comunes → buscador (`window.ERR`);
  - cálculos que la persona haría a mano (espacio en disco, tiempos) →
    calculadora `.tool`;
  - recorrido → `.flow` con enlaces a cada sección.
- `data-ns` del `.shell`: un identificador único por manual (p. ej.
  `rutas-usuario`) para que las checklists no se mezclen entre manuales.

## 9. Checklist final (antes de entregar)

- [ ] Cabecera completa con fecha de revisión de hoy.
- [ ] Cada número de cada captura aparece en su pie de figura, y viceversa.
- [ ] Cada mensaje citado existe literal en el código (grep).
- [ ] Cada botón/menú citado existe en el frontend o se ve en la captura.
- [ ] MD y HTML tienen las mismas secciones con la misma numeración.
- [ ] Todos los enlaces del índice y del `.flow` llevan a una sección que existe.
- [ ] HTML empaquetado (sin rutas `img/` sueltas) y abre con doble clic.
- [ ] Nada sensible en capturas ni ejemplos.
