# Grafo de conocimientos

Genera desde cero una visualización HTML de las subcarpetas de primer nivel de
una carpeta base. Cada subcarpeta se trata como un proyecto; no se inspecciona ni
modifica su contenido. Por defecto no carga fichas, relaciones ni datos de
ninguna otra ubicación.

## Uso

Requiere Python 3.9 o posterior y no necesita dependencias externas.

```powershell
python tools/generar_grafo.py "<carpeta-base>"
```

El HTML se guarda como `grafo.html` dentro de la carpeta base. Para escoger otra
ubicación:

```powershell
python tools/generar_grafo.py "<carpeta-base>" --output "<ruta-salida>\grafo.html"
```

Sin argumento de carpeta, se escanea la carpeta padre del repositorio. El propio
repositorio del generador se excluye del grafo cuando está dentro de la carpeta
base.

```text
python tools/generar_grafo.py --help
```

## Metadatos opcionales (explícitos)

Solo si se pasan `--projects-dir` o `--deps-dir`, el generador lee fichas
Markdown o JSON de esas rutas. No usa automáticamente `projects/` ni `deps/`
del repositorio, pues podrían pertenecer a otra carpeta base. Sin metadatos, los
nodos usan el nombre original de cada carpeta, estado `new` y no tienen
relaciones. El generador no inventa relaciones.

Cuando se solicitan fichas, se asocian por nombre normalizado (ignora
mayúsculas, espacios, guiones y acentos). Si varias carpetas coinciden, se
conservan como nodos separados y se distinguen por su nombre original.

El escaneo es superficial intencionadamente: cada subcarpeta directa es un
nodo, no se deducen relaciones automáticamente ni se recorren subcarpetas
recursivamente.

## Desarrollo con agentes

Las instrucciones del repositorio están en `AGENTS.md`. El flujo de trabajo
portable para otros agentes está en
[`equipo-agentes/FLUJO-PORTABLE.md`](equipo-agentes/FLUJO-PORTABLE.md).
