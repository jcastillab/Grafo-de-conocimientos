import tempfile
import unittest
from pathlib import Path

from tools.analizar_dependencias import build_registry


class BuildRegistryTests(unittest.TestCase):
    def test_ignora_entornos_y_cache(self):
        with tempfile.TemporaryDirectory() as temporal:
            root = Path(temporal)
            (root / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
            for ignored in (".venv", "__pycache__", "node_modules"):
                nested = root / ignored
                nested.mkdir()
                (nested / "third_party.py").write_text("VALUE = 2\n", encoding="utf-8")

            registry = build_registry(root)

        self.assertEqual(set(registry), {"app"})


if __name__ == "__main__":
    unittest.main()
