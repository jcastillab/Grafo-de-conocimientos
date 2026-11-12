import tempfile
import unittest
from pathlib import Path

from tools.generar_grafo import cargar_proyectos


class CargarProyectosTests(unittest.TestCase):
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
