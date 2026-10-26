"""Extrae un grafo de dependencias (imports internos) de un paquete Python.

Uso:
    python analizar_dependencias.py <package_root> [--package-name NOMBRE]
        [--strip-prefix PREFIJO ...] [--shim-dir DIR ...] [--out salida.json]

- <package_root>: carpeta raíz del paquete a analizar (ej. src/conteo_rosas).
- --package-name: prefijo usado en imports absolutos que se refieren a este
  mismo paquete (ej. "conteo_rosas" para que "from conteo_rosas.x import y"
  se resuelva contra el registro de módulos, cuyos ids son relativos a
  <package_root>, es decir "x", no "conteo_rosas.x").
- --strip-prefix: prefijos adicionales a probar al resolver un import
  absoluto que no matchea directamente (ej. "src" para el patrón dual de
  markov_v3: "import canonical" / "import src.canonical" deben colapsar al
  mismo nodo "canonical").
- --shim-dir: carpetas hermanas de <package_root> (rutas absolutas) que se
  agregan como nodos "shim" (sin resolver sus aristas) porque hacen
  manipulación dinámica de sys.modules en vez de imports estáticos.

Solo usa ast.parse (no ejecuta nada, no requiere el venv del proyecto ni sus
dependencias instaladas). Los imports a librerías externas/stdlib se
ignoran: el grafo es solo de módulos dentro del propio paquete.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path


def module_id_for(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = list(rel.parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else "__root__"


def package_of(module_id: str, is_package: bool) -> str:
    if is_package:
        return module_id
    parts = module_id.split(".")
    return ".".join(parts[:-1])


def build_registry(root: Path) -> dict[str, dict]:
    registry: dict[str, dict] = {}
    for py_file in root.rglob("*.py"):
        mid = module_id_for(py_file, root)
        is_pkg = py_file.name == "__init__.py"
        try:
            loc = len(py_file.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            loc = 0
        parts_for_top = mid.split(".")
        top = parts_for_top[0] if (mid != "__root__" and len(parts_for_top) > 1) else "_root"
        registry[mid] = {
            "id": mid,
            "path": str(py_file.relative_to(root)).replace("\\", "/"),
            "subpaquete": top,
            "loc": loc,
            "shim": False,
            "is_package": is_pkg,
            "file": py_file,
        }
    return registry


def resolve_absolute(name: str, registry: dict, package_name: str | None, strip_prefixes: list[str]) -> str | None:
    candidates = [name]
    if package_name and name == package_name:
        candidates.append("__root__")
    if package_name and name.startswith(package_name + "."):
        candidates.append(name[len(package_name) + 1 :])
    for prefix in strip_prefixes:
        if name == prefix:
            candidates.append("__root__")
        if name.startswith(prefix + "."):
            candidates.append(name[len(prefix) + 1 :])
    # probar también recortando progresivamente el final (import de un
    # submódulo específico de un paquete ya registrado como __init__)
    expanded = []
    for cand in candidates:
        expanded.append(cand)
        parts = cand.split(".")
        for i in range(len(parts) - 1, 0, -1):
            expanded.append(".".join(parts[:i]))
    for cand in expanded:
        if cand in registry:
            return cand
    return None


def resolve_relative(module: str | None, level: int, importing_id: str, importing_is_pkg: bool, registry: dict) -> str | None:
    base_parts = importing_id.split(".") if importing_id != "__root__" else []
    if not importing_is_pkg:
        base_parts = base_parts[:-1]
    # level=1 -> paquete actual; level=2 -> un nivel arriba; etc.
    up = level - 1
    if up > 0:
        base_parts = base_parts[: len(base_parts) - up] if up <= len(base_parts) else []
    if module:
        base_parts = base_parts + module.split(".")
    candidate = ".".join(base_parts) if base_parts else "__root__"
    if candidate in registry:
        return candidate
    parts = candidate.split(".")
    for i in range(len(parts) - 1, 0, -1):
        cand = ".".join(parts[:i])
        if cand in registry:
            return cand
    return None


def extract_edges(registry: dict, package_name: str | None, strip_prefixes: list[str]) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for mid, info in registry.items():
        try:
            source = info["file"].read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(info["file"]))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    target = resolve_absolute(alias.name, registry, package_name, strip_prefixes)
                    if target and target != mid:
                        edges.add((mid, target))
            elif isinstance(node, ast.ImportFrom):
                if node.level and node.level > 0:
                    target = resolve_relative(node.module, node.level, mid, info["is_package"], registry)
                else:
                    target = resolve_absolute(node.module or "", registry, package_name, strip_prefixes)
                if target and target != mid:
                    edges.add((mid, target))
    return edges


def collect_shims(shim_dirs: list[Path]) -> list[dict]:
    shims = []
    for d in shim_dirs:
        if not d.is_dir():
            continue
        init = d / "__init__.py"
        note = ""
        if init.is_file():
            try:
                text = init.read_text(encoding="utf-8", errors="replace")
                if "sys.modules" in text:
                    note = "reescribe sys.modules dinámicamente"
            except OSError:
                pass
        shims.append({
            "id": d.name,
            "path": d.name,
            "subpaquete": "_shim",
            "loc": 0,
            "shim": True,
            "nota": note or "no resuelto estáticamente",
        })
    return shims


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("package_root", type=Path)
    parser.add_argument("--package-name", default=None)
    parser.add_argument("--strip-prefix", action="append", default=[])
    parser.add_argument("--shim-dir", action="append", default=[], type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    root = args.package_root.resolve()
    if not root.is_dir():
        print(f"No existe el directorio: {root}", file=sys.stderr)
        sys.exit(1)

    registry = build_registry(root)
    edges = extract_edges(registry, args.package_name, args.strip_prefix)
    shims = collect_shims(args.shim_dir)

    modules = [
        {k: v for k, v in info.items() if k not in ("file", "is_package")}
        for info in registry.values()
    ] + shims

    result = {
        "package_root": str(root),
        "modules": modules,
        "edges": [{"from": a, "to": b} for a, b in sorted(edges)],
    }

    out = args.out
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Escrito {out} ({len(modules)} módulos, {len(result['edges'])} aristas)")
    else:
        print(text)


if __name__ == "__main__":
    main()
