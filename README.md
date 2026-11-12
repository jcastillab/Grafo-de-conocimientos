# Grafo de conocimientos

Genera una visualización HTML de las subcarpetas de primer nivel de una carpeta
base. Cada subcarpeta se trata como un proyecto; no se inspecciona ni modifica su
contenido. Las fichas Markdown y los JSON de dependencias son opcionales y
aportan descripciones, relaciones y vistas internas.

## Uso

Requiere Python 3.9 o posterior y no necesita dependencias externas.

```powershell
python tools/generar_grafo.py "D:\proyectos\IDEA"
```

El HTML se guarda como `grafo.html` dentro de la carpeta base. Para escoger otra
ubicación:

```powershell
python tools/generar_grafo.py "D:\proyectos\IDEA" --output "D:\temp\grafo.html"
```

Sin argumento de carpeta, se escanea la carpeta padre del repositorio. El propio
repositorio del generador se excluye del grafo cuando está dentro de la carpeta
base.

```text
python tools/generar_grafo.py --help
```

## Fichas y relaciones opcionales

Las fichas en `projects/*.md` se asocian a una carpeta por su nombre (ignorando
mayúsculas, espacios, guiones y acentos). Si no hay ficha, el nombre de la
carpeta se usa como nombre del nodo y su estado es `new`. Las relaciones se
declaran en el frontmatter `relationships` de las fichas. Los JSON bajo `deps/`
se usan para mostrar dependencias internas; ambos directorios pueden cambiarse
con `--projects-dir` y `--deps-dir`.

El escaneo es superficial intencionadamente: cada subcarpeta directa es un
nodo, no se deducen relaciones automáticamente ni se recorren subcarpetas
recursivamente.
