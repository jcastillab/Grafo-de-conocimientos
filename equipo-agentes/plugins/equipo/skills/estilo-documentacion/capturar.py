"""Capturas anotadas para manuales a partir de una especificación local.

Lee una especificación JSON (por convención `manual/capturas.json`), abre cada
pantalla con Playwright, dibuja un recuadro rosa y un círculo numerado sobre
cada elemento marcado y guarda la imagen (webp si hay Pillow, si no png).

Uso:
    <venv>\\Scripts\\python.exe capturar.py manual\\capturas.json [--solo nombre1,nombre2]

Especificación:
{
  "base_url": "http://127.0.0.1:8000",          # opcional; o "archivo" por captura
  "viewport": {"width": 1600, "height": 1000},   # opcional
  "salida": "img",                               # relativa al JSON
  "capturas": [
    {
      "nombre": "organizar-paso1",
      "url": "/conteo/organizar",                # o "archivo": "../data/mapa.html"
      "pasos": [                                 # opcional, en orden
        {"click": "text=Nueva organización"},
        {"llenar": ["#ruta", "D:\\\\videos"]},
        {"esperar": "text=Listar videos"},
        {"pausa_ms": 500}
      ],
      "recorte": "main .card",                   # opcional: solo esa zona (+ margen)
      "pagina_completa": false,
      "marcas": [{"selector": "text=Elegir carpeta", "n": 1}]
    }
  ]
}
Los selectores son de Playwright (CSS, `text=...`, `role=button[name="..."]`).
"""

import argparse
import json
import sys
from pathlib import Path

ROSA = "#d23b8c"
MARGEN_RECORTE = 28  # px alrededor del recorte para que entren los círculos

# Recuadro con halo suave + círculo numerado con anillo blanco, como el manual original.
JS_MARCAR = """
(marcas) => {
  document.querySelectorAll('[data-marca-manual]').forEach(e => e.remove());
  const faltan = [];
  for (const m of marcas) {
    const el = m.el;
    if (!el) { faltan.push(m.n); continue; }
    const r = el.getBoundingClientRect();
    const x = r.left + window.scrollX, y = r.top + window.scrollY;
    const caja = document.createElement('div');
    caja.setAttribute('data-marca-manual', '');
    Object.assign(caja.style, {
      position: 'absolute', left: (x - 6) + 'px', top: (y - 6) + 'px',
      width: (r.width + 12) + 'px', height: (r.height + 12) + 'px',
      border: '4px solid ROSA', borderRadius: '10px',
      boxShadow: '0 0 0 5px rgba(210,59,140,.22)', zIndex: 2147483646,
      pointerEvents: 'none', boxSizing: 'border-box'
    });
    const num = document.createElement('div');
    num.setAttribute('data-marca-manual', '');
    num.textContent = String(m.n);
    Object.assign(num.style, {
      position: 'absolute', left: (x - 24) + 'px', top: (y - 24) + 'px',
      width: '40px', height: '40px', borderRadius: '50%', background: 'ROSA',
      color: '#fff', font: '700 22px/40px "Segoe UI", system-ui, sans-serif',
      textAlign: 'center', boxShadow: '0 0 0 4px #fff, 0 2px 6px rgba(0,0,0,.25)',
      zIndex: 2147483647, pointerEvents: 'none'
    });
    document.body.append(caja, num);
  }
  return faltan;
}
""".replace("ROSA", ROSA)


def _url(cap, base_url, carpeta_spec):
    if "archivo" in cap:
        return (carpeta_spec / cap["archivo"]).resolve().as_uri()
    return base_url.rstrip("/") + "/" + cap.get("url", "").lstrip("/")


def _pasos(page, pasos):
    for p in pasos:
        if "click" in p:
            page.locator(p["click"]).first.click()
        elif "llenar" in p:
            sel, valor = p["llenar"]
            page.locator(sel).first.fill(valor)
        elif "esperar" in p:
            page.locator(p["esperar"]).first.wait_for()
        elif "pausa_ms" in p:
            page.wait_for_timeout(p["pausa_ms"])
        else:
            raise ValueError(f"Paso desconocido: {p}")


def _guardar(png: bytes, destino_sin_ext: Path) -> Path:
    try:
        from io import BytesIO

        from PIL import Image
    except ImportError:
        destino = destino_sin_ext.with_suffix(".png")
        destino.write_bytes(png)
        return destino
    destino = destino_sin_ext.with_suffix(".webp")
    Image.open(BytesIO(png)).save(destino, "WEBP", quality=86, method=6)
    return destino


def capturar(spec_path: Path, solo: set[str] | None = None) -> list[str]:
    from playwright.sync_api import sync_playwright

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    carpeta = spec_path.parent
    salida = carpeta / spec.get("salida", "img")
    salida.mkdir(parents=True, exist_ok=True)
    viewport = spec.get("viewport", {"width": 1600, "height": 1000})
    problemas = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport=viewport, device_scale_factor=1)
        for cap in spec["capturas"]:
            if solo and cap["nombre"] not in solo:
                continue
            page.goto(_url(cap, spec.get("base_url", ""), carpeta), wait_until="networkidle")
            _pasos(page, cap.get("pasos", []))
            marcas = []
            for m in cap.get("marcas", []):
                loc = page.locator(m["selector"]).first
                handle = loc.element_handle(timeout=5000) if loc.count() else None
                marcas.append({"n": m["n"], "el": handle})
            faltan = page.evaluate(JS_MARCAR, marcas)
            if faltan:
                problemas.append(f"{cap['nombre']}: no se encontró el elemento de la(s) marca(s) {faltan}")
            if cap.get("recorte"):
                caja = page.locator(cap["recorte"]).first.bounding_box()
                if caja is None:
                    problemas.append(f"{cap['nombre']}: recorte '{cap['recorte']}' no visible")
                    continue
                clip = {
                    "x": max(0, caja["x"] - MARGEN_RECORTE),
                    "y": max(0, caja["y"] - MARGEN_RECORTE),
                    "width": caja["width"] + 2 * MARGEN_RECORTE,
                    "height": caja["height"] + 2 * MARGEN_RECORTE,
                }
                png = page.screenshot(clip=clip, full_page=True)
            else:
                png = page.screenshot(full_page=cap.get("pagina_completa", False))
            destino = _guardar(png, salida / cap["nombre"])
            print(f"ok  {destino.relative_to(carpeta)}")
        browser.close()
    return problemas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("spec", type=Path)
    ap.add_argument("--solo", help="nombres de captura separados por coma")
    args = ap.parse_args()
    solo = set(args.solo.split(",")) if args.solo else None
    problemas = capturar(args.spec.resolve(), solo)
    for p in problemas:
        print(f"AVISO {p}", file=sys.stderr)
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
