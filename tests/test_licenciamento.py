"""Travas do licenciamento por componente (item C8, decisão D7 de 24/10/2026)."""
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EMAIL = "globaldeeptechecosystem@hubstry.dev"
ARQUIVOS_IPII = [
    "lib/ipii/__init__.py", "lib/ipii/matcher.py", "lib/ipii/tokenizer.py",
    "lib/ipii/validator.py", "ipii_engine.py", "pages/9_🔬_IPII_Engine.py",
]


class TestLicenciamento(unittest.TestCase):
    def test_licenca_do_ipii(self):
        txt = (RAIZ / "lib" / "ipii" / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(txt.startswith("PolyForm Noncommercial License 1.0.0"))
        self.assertIn(EMAIL, txt)
        self.assertIn("polyformproject.org/licenses/noncommercial/1.0.0", txt)

    def test_apache_da_raiz_intacta(self):
        txt = (RAIZ / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Apache License", txt)
        self.assertNotIn("PolyForm", txt, "o texto da Apache não deve ser modificado; a exceção fica no NOTICE")

    def test_notice_declara_a_excecao(self):
        txt = (RAIZ / "NOTICE").read_text(encoding="utf-8")
        for termo in ("Apache License 2.0", "PolyForm Noncommercial License 1.0.0", "lib/ipii/", "ipii_engine.py", EMAIL):
            self.assertIn(termo, txt)

    def test_cabecalhos_do_ipii(self):
        for rel in ARQUIVOS_IPII:
            with self.subTest(arquivo=rel):
                cabecalho = "".join((RAIZ / rel).read_text(encoding="utf-8").splitlines(True)[:8])
                self.assertIn("PolyForm Noncommercial 1.0.0", cabecalho)
                self.assertNotIn("Todos os direitos reservados", cabecalho)

    def test_politica_de_seguranca(self):
        self.assertIn(EMAIL, (RAIZ / "SECURITY.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
