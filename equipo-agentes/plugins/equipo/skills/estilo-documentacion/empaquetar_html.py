"""Incrusta en base64 las imágenes locales de un manual HTML -> un solo archivo.

Uso:
    python empaquetar_html.py manual\\manual_usuario.html [-o salida.html]
    python empaquetar_html.py --prueba     # autoverificación

Reemplaza `src="ruta"` y `url(ruta)` que apunten a archivos locales existentes
(relativos al HTML). Deja intactas las URLs http(s) y los data: ya incrustados.
"""

import argparse
import base64
import re
import sys
import tempfile
from pathlib import Path

MIME = {
    ".png": "image/png",
    ".webp": "image/webp",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".gif": "image/gif",
}
PATRON = re.compile(r"""(src=["']|url\(["']?)([^"')]+?)(["')])""")


def empaquetar(html: str, carpeta: Path) -> tuple[str, list[str]]:
    faltan = []

    def reemplazar(m: re.Match) -> str:
        ruta = m.group(2)
        if ruta.startswith(("http:", "https:", "data:", "#", "//")):
            return m.group(0)
        archivo = (carpeta / ruta).resolve()
        mime = MIME.get(archivo.suffix.lower())
        if not mime or not archivo.is_file():
            if mime:
                faltan.append(ruta)
            return m.group(0)
        datos = base64.b64encode(archivo.read_bytes()).decode("ascii")
        return f"{m.group(1)}data:{mime};base64,{datos}{m.group(3)}"

    return PATRON.sub(reemplazar, html), faltan


def _prueba() -> None:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "img").mkdir()
        (d / "img" / "a.png").write_bytes(b"\x89PNG")
        html = '<img src="img/a.png"><i style="background:url(img/a.png)"></i><img src="https://x/y.png"><img src="img/no.png">'
        out, faltan = empaquetar(html, d)
        assert out.count("data:image/png;base64,iVBORw==") == 2, out
        assert "https://x/y.png" in out
        assert faltan == ["img/no.png"], faltan
    print("prueba ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("html", type=Path, nargs="?")
    ap.add_argument("-o", "--salida", type=Path)
    ap.add_argument("--prueba", action="store_true")
    args = ap.parse_args()
    if args.prueba:
        _prueba()
        return 0
    if not args.html:
        ap.error("falta el HTML")
    html = args.html.read_text(encoding="utf-8")
    out, faltan = empaquetar(html, args.html.resolve().parent)
    destino = args.salida or args.html
    destino.write_text(out, encoding="utf-8")
    print(f"ok  {destino} ({len(out) / 1e6:.1f} MB)")
    for f in faltan:
        print(f"AVISO imagen no encontrada: {f}", file=sys.stderr)
    return 1 if faltan else 0


if __name__ == "__main__":
    sys.exit(main())
