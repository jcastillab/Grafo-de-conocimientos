import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.generar_grafo import cargar_internos, cargar_proyectos


class CargarProyectosTests(unittest.TestCase):
    def test_cli_predeterminado_genera_solo_desde_la_carpeta_base(self):
        with tempfile.TemporaryDirectory() as temporal:
            base = Path(temporal)
            raiz = base / "proyectos"
            raiz.mkdir()
            (raiz / "alpha").mkdir()
            (raiz / "beta").mkdir()
            salida = base / "grafo.html"
            script = Path(__file__).resolve().parents[1] / "tools" / "generar_grafo.py"

            resultado = subprocess.run(
                [sys.executable, str(script), str(raiz), "--output", str(salida)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertEqual(resultado.stderr, "")
            self.assertIn("2 proyectos, 0 relaciones, 0 con vista interna", resultado.stdout)
            self.assertTrue(salida.is_file())

    def test_no_carga_fichas_si_no_se_piden_expresamente(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal) / "proyectos"
            raiz.mkdir()
            (raiz / "proyecto-local").mkdir()

            proyectos = cargar_proyectos(raiz)

        proyecto = proyectos["proyecto-local"]
        self.assertEqual(proyecto["name"], "proyecto-local")
        self.assertEqual(proyecto["status"], "new")
        self.assertEqual(proyecto["relationships"], [])

    def test_no_carga_dependencias_si_no_se_indican(self):
        proyectos = {"proyecto-local": {}}

        self.assertEqual(cargar_internos(proyectos), {})

    def test_conserva_carpetas_cuyos_nombres_normalizados_colisionan(self):
        with tempfile.TemporaryDirectory() as temporal:
            base = Path(temporal)
            raiz = base / "proyectos"
            fichas = base / "fichas"
            raiz.mkdir()
            fichas.mkdir()
            (raiz / "mi-proyecto").mkdir()
            (raiz / "miproyecto").mkdir()
            (fichas / "mi-proyecto.md").write_text(
                "---\nname: mi-proyecto\nstatus: active\n---\n\n## Propósito\nFicha\n",
                encoding="utf-8",
            )

            proyectos = cargar_proyectos(raiz, fichas)

        self.assertEqual(len(proyectos), 2)
        self.assertEqual(set(proyectos), {"mi-proyecto", "miproyecto"})
        self.assertEqual({p["name"] for p in proyectos.values()}, {"mi-proyecto", "miproyecto"})
        self.assertTrue(all(p["status"] == "active" for p in proyectos.values()))


if __name__ == "__main__":
    unittest.main()
