"""Genera una visualización autocontenida del grafo de conocimiento.

No depende de Claude ni de la herramienta Artifact: descubre las subcarpetas
de una carpeta base y las enriquece con projects/*.md y deps/*.json opcionales.
Escribe un único HTML que se abre en cualquier navegador, sin internet.

Uso:  python tools/generar_grafo.py [CARPETA_BASE] [--output grafo.html]
Por defecto escanea la carpeta padre del repositorio y escribe allí grafo.html.

Solo biblioteca estándar (no requiere PyYAML). El parser de frontmatter cubre
el formato de los nodos del grafo: escalares, listas inline [a, b] y listas
de objetos bajo `relationships:`.
"""

import argparse
import hashlib
import html
import json
import math
import random
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PROJECTS = RAIZ / "projects"
DEPS = RAIZ / "deps"


def _kv(texto):
    k, _, v = texto.partition(":")
    return k.strip(), v.strip().strip("\"'")


def parse_frontmatter(texto):
    lineas = texto.splitlines()
    if not lineas or lineas[0].strip() != "---":
        return {}, texto
    fin = lineas.index("---", 1)
    data, clave = {}, None
    for linea in lineas[1:fin]:
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        if linea.startswith("  - ") or linea.startswith("- "):
            if clave is None:
                continue
            k, v = _kv(linea.split("- ", 1)[1])
            data.setdefault(clave, []).append({k: v})
        elif linea.startswith("    ") and data.get(clave) and isinstance(data[clave][-1], dict):
            k, v = _kv(linea.strip())
            data[clave][-1][k] = v
        else:
            clave, _, v = linea.partition(":")
            clave, v = clave.strip(), v.strip()
            if v == "":
                data[clave] = []
            elif v.startswith("["):
                data[clave] = [x.strip().strip("\"'") for x in v.strip("[]").split(",") if x.strip()]
            else:
                data[clave] = v.strip("\"'")
    return data, "\n".join(lineas[fin + 1:])


def parse_secciones(cuerpo):
    secciones = {}
    for bloque in re.split(r"^## ", cuerpo, flags=re.M)[1:]:
        titulo, _, texto = bloque.partition("\n")
        secciones[titulo.strip()] = texto.strip()
    return secciones


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", texto.lower())


def cargar_proyectos(raiz, carpeta_projects):
    """Descubre subcarpetas de primer nivel y enriquece las que tengan ficha."""
    fichas = {}
    for md in sorted(carpeta_projects.glob("*.md")):
        if md.stem.startswith("_"):
            continue
        fm, cuerpo = parse_frontmatter(md.read_text(encoding="utf-8"))
        clave = normalizar(md.stem)
        fichas[clave] = (md.stem, fm, cuerpo)
        if fm.get("name"):
            fichas.setdefault(normalizar(fm["name"]), (md.stem, fm, cuerpo))

    proyectos = {}
    for carpeta in sorted(raiz.iterdir(), key=lambda p: p.name.casefold()):
        if not carpeta.is_dir() or carpeta.name.startswith(".") or carpeta.resolve() == RAIZ.resolve():
            continue
        ficha = fichas.get(normalizar(carpeta.name))
        pid, fm, cuerpo = ficha if ficha else (carpeta.name, {}, "")
        conflicto_id = pid in proyectos
        if conflicto_id:
            pid = carpeta.name
            sufijo = 2
            while pid in proyectos:
                pid = f"{carpeta.name} ({sufijo})"
                sufijo += 1
        proyectos[pid] = {
            "id": pid,
            "name": carpeta.name if conflicto_id else fm.get("name", carpeta.name),
            "status": fm.get("status", "new"),
            "stack": fm.get("stack", []) if isinstance(fm.get("stack"), list) else [],
            "tags": fm.get("tags", []) if isinstance(fm.get("tags"), list) else [],
            "secciones": parse_secciones(cuerpo),
            "relationships": [r for r in fm.get("relationships", []) if isinstance(r, dict)],
        }
    return proyectos


def resolver(ref, proyectos):
    """Acepta el slug del archivo o el nombre del frontmatter (sin distinguir mayúsculas)."""
    for pid, p in proyectos.items():
        if ref and ref.lower() in (pid.lower(), p["name"].lower()):
            return pid
    return None


def construir_aristas(proyectos):
    aristas, vistas, avisos = [], set(), set()
    for pid, p in proyectos.items():
        for r in p["relationships"]:
            destino = resolver(r.get("project"), proyectos)
            if destino is None:
                aviso = (pid, r.get("project"))
                if aviso not in avisos:
                    print(f"aviso: {pid} referencia '{r.get('project')}' que no tiene nodo", file=sys.stderr)
                    avisos.add(aviso)
                continue
            clave = (frozenset((pid, destino)), r.get("tipo", ""))
            if clave in vistas:
                continue
            vistas.add(clave)
            aristas.append({
                "from": pid, "to": destino,
                "tipo": r.get("tipo", ""), "evidencia": r.get("evidencia", ""),
            })
    return aristas


def layout_circular(ids, w=800, h=600):
    n = len(ids)
    cx, cy, r = w / 2, h / 2, min(w, h) * 0.36
    return {i: [cx + r * math.cos(2 * math.pi * k / n - math.pi / 2),
                cy + r * math.sin(2 * math.pi * k / n - math.pi / 2)]
            for k, i in enumerate(ids)}


def layout_fuerzas(ids, aristas, w=1000, h=700, iters=120):
    """Fruchterman-Reingold simple; determinista con semilla fija."""
    if not ids:
        return {}
    rnd = random.Random(1)
    pos = {i: [rnd.random() * w, rnd.random() * h] for i in ids}
    k = math.sqrt(w * h / len(ids))
    temp = w / 10
    for _ in range(iters):
        disp = {i: [0.0, 0.0] for i in ids}
        for a in ids:
            for b in ids:
                if a == b:
                    continue
                dx = pos[a][0] - pos[b][0]
                dy = pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 0.01
                f = k * k / d
                disp[a][0] += dx / d * f
                disp[a][1] += dy / d * f
        for e in aristas:
            a, b = e["from"], e["to"]
            dx = pos[a][0] - pos[b][0]
            dy = pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 0.01
            f = d * d / k
            disp[a][0] -= dx / d * f
            disp[a][1] -= dy / d * f
            disp[b][0] += dx / d * f
            disp[b][1] += dy / d * f
        for i in ids:
            dx, dy = disp[i]
            d = math.hypot(dx, dy) or 0.01
            step = min(d, temp)
            pos[i][0] = min(w - 20, max(20, pos[i][0] + dx / d * step))
            pos[i][1] = min(h - 20, max(20, pos[i][1] + dy / d * step))
        temp *= 0.95
    return pos


def cargar_internos(proyectos, carpeta_deps):
    internos, hashes = {}, {}
    for pid in proyectos:
        archivo = carpeta_deps / f"{pid}.json"
        if not archivo.exists():
            continue
        d = json.loads(archivo.read_text(encoding="utf-8"))
        # Se compara solo el contenido (módulos y aristas), no package_root, que cambia por carpeta.
        canon = json.dumps({"m": d.get("modules", []), "e": d.get("edges", [])}, sort_keys=True)
        hashes[pid] = hashlib.sha256(canon.encode("utf-8")).hexdigest()
        mods = d.get("modules", [])
        ids = [m["id"] for m in mods]
        aristas = [e for e in d.get("edges", []) if e["from"] in ids and e["to"] in ids]
        grado = {i: 0 for i in ids}
        for e in aristas:
            grado[e["from"]] += 1
            grado[e["to"]] += 1
        pos = layout_fuerzas(ids, aristas)
        internos[pid] = {
            "modules": [{**m, "x": pos[m["id"]][0], "y": pos[m["id"]][1], "grado": grado[m["id"]]}
                        for m in mods],
            "edges": aristas,
        }
    # Proyectos con el mismo JSON de dependencias (mismo código).
    for pid in internos:
        iguales = [o for o in internos if o != pid and hashes[o] == hashes[pid]]
        internos[pid]["compartido_con"] = iguales
    return internos


def main():
    parser = argparse.ArgumentParser(
        description="Genera un grafo a partir de las subcarpetas de una carpeta base."
    )
    parser.add_argument(
        "root", nargs="?", type=Path, default=RAIZ.parent,
        help=f"carpeta base que contiene los proyectos (predeterminada: {RAIZ.parent})",
    )
    parser.add_argument("--output", type=Path, help="archivo HTML de salida (predeterminado: <root>/grafo.html)")
    parser.add_argument("--projects-dir", type=Path, default=PROJECTS,
                        help="carpeta con fichas Markdown opcionales")
    parser.add_argument("--deps-dir", type=Path, default=DEPS,
                        help="carpeta con JSON de dependencias opcionales")
    args = parser.parse_args()
    raiz = args.root.resolve()
    if not raiz.is_dir():
        parser.error(f"no existe la carpeta base: {raiz}")
    salida = (args.output or raiz / "grafo.html").resolve()
    proyectos = cargar_proyectos(raiz, args.projects_dir.resolve())
    if not proyectos:
        sys.exit(f"No se encontraron subcarpetas de proyecto en {raiz}")
    aristas = construir_aristas(proyectos)
    ids = list(proyectos)
    pos = layout_circular(ids)
    nodos = []
    for pid in ids:
        p = proyectos[pid]
        x, y = pos[pid]
        nodos.append({
            "id": pid, "name": p["name"], "status": p["status"],
            "stack": p["stack"], "tags": p["tags"],
            "secciones": p["secciones"], "x": x, "y": y,
        })
    datos = {
        "nodos": nodos,
        "aristas": aristas,
        "internos": cargar_internos(proyectos, args.deps_dir.resolve()),
        "generado": "generado por tools/generar_grafo.py",
    }
    payload = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    salida.parent.mkdir(parents=True, exist_ok=True)
    titulo = html.escape(str(raiz))
    documento = PLANTILLA.replace("__TITLE__", titulo).replace("__DATA__", payload)
    salida.write_text(documento, encoding="utf-8")
    print(f"OK: {salida} ({len(nodos)} proyectos, {len(aristas)} relaciones, "
          f"{len(datos['internos'])} con vista interna)")


PLANTILLA = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grafo de conocimiento</title>
<style>
:root{--bg:#fbf8f4;--fg:#222;--muted:#777;--line:#ccc;--panel:#fff;--accent:#e0457b;
--active:#2e8b57;--empty:#999;--entrega:#d68910;--new:#3b7dd8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1b1b1f;--fg:#eee;--muted:#aaa;--line:#555;--panel:#26262c}}
:root[data-theme="dark"]{--bg:#1b1b1f;--fg:#eee;--muted:#aaa;--line:#555;--panel:#26262c}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif}
header{padding:12px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
h1{font-size:18px;margin:0 8px 0 0}
button{font:inherit;padding:4px 10px;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:6px;cursor:pointer}
main{display:flex;gap:16px;padding:0 16px 16px;flex-wrap:wrap}
#mapa{flex:1 1 560px;min-width:0;background:var(--panel);border-radius:8px;border:1px solid var(--line)}
svg{width:100%;height:auto;display:block}
#panel{flex:0 1 340px;background:var(--panel);border-radius:8px;border:1px solid var(--line);padding:12px 14px;min-height:200px}
#panel h2{font-size:16px;margin:0 0 6px}
#panel pre{white-space:pre-wrap;font:inherit;margin:4px 0 10px}
.tag{display:inline-block;font-size:12px;padding:1px 7px;border-radius:10px;border:1px solid var(--line);margin:2px 2px 0 0}
.nota{color:var(--muted);font-size:12px}
.nodo{cursor:pointer}
.lbl{font-size:12px;fill:var(--fg)}
.etq{font-size:10px;fill:var(--muted)}
.arista{stroke:var(--line);stroke-width:1.4;fill:none}
.arista.fuerte{stroke:var(--accent);stroke-width:2}
</style>
</head>
<body>
<header>
  <h1>Grafo de conocimiento — __TITLE__</h1>
  <button id="btn-over">Overview</button>
  <span id="titulo-int" class="nota"></span>
</header>
<main>
  <div id="mapa"></div>
  <div id="panel"><p class="nota">Haz clic en un proyecto o módulo para ver su detalle.</p></div>
</main>
<script>
const DATA = __DATA__;
const COLORES = {active:"var(--active)", empty:"var(--empty)", entrega:"var(--entrega)", new:"var(--new)"};
const PALETA = ["#e0457b","#2e8b57","#3b7dd8","#d68910","#8e44ad","#16a085","#c0392b","#7f8c8d","#2c3e50","#f39c12"];
const NS = "http://www.w3.org/2000/svg";
const mapa = document.getElementById("mapa");
const panel = document.getElementById("panel");
const titulo = document.getElementById("titulo-int");

function el(tag, attrs, parent){
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function txt(tag, texto, parent, cls){
  const e = document.createElement(tag);
  e.textContent = texto;
  if (cls) e.className = cls;
  if (parent) parent.appendChild(e);
  return e;
}
function svgRoot(){
  mapa.textContent = "";
  return el("svg", {viewBox: "0 0 800 600"}, mapa);
}
function marcador(svg){
  const defs = el("defs", {}, svg);
  const m = el("marker", {id:"flecha", viewBox:"0 0 10 10", refX:"18", refY:"5", markerWidth:"6", markerHeight:"6", orient:"auto-start-reverse"}, defs);
  el("path", {d:"M0,0 L10,5 L0,10 z", fill:"var(--line)"}, m);
}

function mostrarOverview(){
  titulo.textContent = "";
  const svg = svgRoot();
  marcador(svg);
  const pos = {};
  DATA.nodos.forEach(n => pos[n.id] = n);
  DATA.aristas.forEach(a => {
    const f = pos[a.from], t = pos[a.to];
    const l = el("line", {x1:f.x, y1:f.y, x2:t.x, y2:t.y, class:"arista", "marker-end":"url(#flecha)"}, svg);
    txt("title", a.tipo + ": " + a.evidencia, l);
    el("text", {x:(f.x+t.x)/2, y:(f.y+t.y)/2 - 4, "text-anchor":"middle", class:"etq"}, svg).textContent = a.tipo;
  });
  DATA.nodos.forEach(n => {
    const g = el("g", {class:"nodo", transform:`translate(${n.x},${n.y})`}, svg);
    el("circle", {r:34, fill: COLORES[n.status] || "var(--new)", "fill-opacity":"0.25", stroke: COLORES[n.status] || "var(--new)", "stroke-width":"2"}, g);
    if (DATA.internos[n.id]) {
      el("circle", {r:40, fill:"none", stroke:"var(--accent)", "stroke-dasharray":"4 3"}, g);
    }
    el("text", {y:50, "text-anchor":"middle", class:"lbl"}, g).textContent = n.name;
    el("text", {y:5, "text-anchor":"middle", class:"etq"}, g).textContent = n.status;
    g.addEventListener("click", () => mostrarNodo(n));
  });
  panel.textContent = "";
  txt("p", "Haz clic en un proyecto para ver su detalle. Los que tienen borde punteado tienen vista interna de dependencias.", panel, "nota");
}

function mostrarNodo(n){
  panel.textContent = "";
  txt("h2", n.name, panel);
  txt("div", "Estado: " + n.status, panel, "nota");
  n.stack.forEach(s => txt("span", s, panel, "tag"));
  const rel = DATA.aristas.filter(a => a.from === n.id || a.to === n.id);
  for (const titulo_sec of ["Propósito", "Puntos de entrada", "Docs propios", "Notas"]) {
    if (n.secciones[titulo_sec]) {
      txt("h3", titulo_sec, panel).style.fontSize = "14px";
      txt("pre", n.secciones[titulo_sec], panel);
    }
  }
  if (rel.length) {
    txt("h3", "Relaciones", panel).style.fontSize = "14px";
    rel.forEach(a => txt("div", `${a.from} → ${a.to} (${a.tipo})`, panel, "nota"));
  }
  if (DATA.internos[n.id]) {
    const b = txt("button", "Ver dependencias internas", panel);
    b.style.marginTop = "10px";
    b.addEventListener("click", () => mostrarInterno(n.id));
  }
}

function mostrarInterno(pid){
  const d = DATA.internos[pid];
  const nodo = DATA.nodos.find(n => n.id === pid);
  titulo.textContent = "Dependencias internas: " + (nodo ? nodo.name : pid);
  const svg = svgRoot();
  const subs = [...new Set(d.modules.map(m => m.subpaquete))];
  const color = s => PALETA[subs.indexOf(s) % PALETA.length];
  const pos = {};
  d.modules.forEach(m => pos[m.id] = m);
  d.edges.forEach(e => {
    const f = pos[e.from], t = pos[e.to];
    el("line", {x1:f.x*0.8+80, y1:f.y*0.8+60, x2:t.x*0.8+80, y2:t.y*0.8+60, class:"arista"}, svg);
  });
  d.modules.forEach(m => {
    const r = 4 + 2 * Math.sqrt(m.grado);
    const c = el("circle", {cx:m.x*0.8+80, cy:m.y*0.8+60, r:r, fill: color(m.subpaquete), "fill-opacity":"0.8", class:"nodo",
      stroke: m.shim ? "var(--fg)" : "none", "stroke-dasharray": m.shim ? "3 2" : "none"}, svg);
    txt("title", `${m.id} (${m.path})`, c);
    c.addEventListener("click", () => mostrarModulo(pid, m));
  });
  panel.textContent = "";
  const b = txt("button", "← volver al overview", panel);
  b.addEventListener("click", mostrarOverview);
  b.style.marginBottom = "10px";
  if (d.compartido_con.length) {
    const nombres = d.compartido_con.map(id => (DATA.nodos.find(n => n.id === id) || {name:id}).name);
    txt("p", "Nota: este proyecto tiene el mismo código de dependencias que " + nombres.join(", ") + ". Es una copia, no un proyecto independiente.", panel, "nota");
  }
  txt("p", `${d.modules.length} módulos, ${d.edges.length} imports. Tamaño = conexiones; color = subpaquete. Haz clic en un módulo.`, panel, "nota");
}

function mostrarModulo(pid, m){
  const d = DATA.internos[pid];
  panel.textContent = "";
  txt("h2", m.id, panel);
  txt("div", "Ruta: " + m.path, panel, "nota");
  txt("div", "Líneas: " + m.loc + " · subpaquete: " + m.subpaquete, panel, "nota");
  if (m.shim) txt("p", "Shim: " + (m.nota || "reexporta otro módulo."), panel, "nota");
  const sale = d.edges.filter(e => e.from === m.id).map(e => e.to);
  const entra = d.edges.filter(e => e.to === m.id).map(e => e.from);
  txt("h3", "Importa (" + sale.length + ")", panel).style.fontSize = "14px";
  txt("pre", sale.join("\n") || "—", panel);
  txt("h3", "Lo importan (" + entra.length + ")", panel).style.fontSize = "14px";
  txt("pre", entra.join("\n") || "—", panel);
}

document.getElementById("btn-over").addEventListener("click", mostrarOverview);
mostrarOverview();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
