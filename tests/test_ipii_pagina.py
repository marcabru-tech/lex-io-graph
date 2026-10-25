"""Página do IPII: escape do HTML e falha legível sem o corpus (revisão da A4)."""
import json
import tempfile
import unittest
from pathlib import Path

from lib.ipii.tokenizer import _padrao_termo
from lib.ipii_pagina import html_aresta_confirmada, html_aresta_nova, ler_total_normas, pct

MALICIOSO = '<script>alert(1)</script>'


class TestEscape(unittest.TestCase):
    def test_aresta_nova_escapa_todos_os_campos(self):
        html = html_aresta_nova({"source": MALICIOSO, "target": "<b>x</b>", "score": "<i>1</i>",
                                 "classificacao": "<u>forte</u>", "tipo_sugerido": "<img src=x>",
                                 "temas_comuns": [MALICIOSO], "jurisdicoes_comuns": ["<svg onload=1>"],
                                 "tier": 1})
        for bruto in (MALICIOSO, "<b>x</b>", "<i>1</i>", "<U>FORTE</U>", "<img src=x>", "<svg onload=1>"):
            self.assertNotIn(bruto, html)
        self.assertIn("&lt;script&gt;", html)

    def test_aresta_confirmada_escapa_todos_os_campos(self):
        html = html_aresta_confirmada({"source": MALICIOSO, "target": "x", "score": MALICIOSO,
                                       "tipo_sugerido": MALICIOSO, "tipo_existente": "<b>y</b>",
                                       "match_tipo": False})
        self.assertNotIn(MALICIOSO, html)
        self.assertNotIn("<b>y</b>", html)

    def test_valores_malformados_nao_quebram(self):
        html = html_aresta_nova({"temas_comuns": "não é lista", "tier": "x"})
        self.assertIn("tier-card", html)
        self.assertEqual(pct(None), "—")
        self.assertEqual(pct("abc"), "—")
        self.assertEqual(pct(0.429), "43%")


class TestCorpusAusenteOuInvalido(unittest.TestCase):
    def test_arquivo_ausente(self):
        n, erro = ler_total_normas(Path(tempfile.gettempdir()) / "nao_existe_normas.json")
        self.assertIsNone(n)
        self.assertIn("não encontrado", erro)

    def test_json_invalido(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            f.write("{ quebrado")
        n, erro = ler_total_normas(Path(f.name))
        self.assertIsNone(n)
        self.assertIn("inválido", erro)

    def test_sem_lista_de_normas(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump({"outra": 1}, f)
        self.assertIsNone(ler_total_normas(Path(f.name))[0])

    def test_corpus_real(self):
        raiz = Path(__file__).resolve().parent.parent
        n, erro = ler_total_normas(raiz / "data" / "normas.json")
        self.assertIsNone(erro)
        self.assertGreater(n, 0)


class TestCacheDoPadrao(unittest.TestCase):
    def test_padrao_compilado_uma_vez_por_termo(self):
        self.assertIs(_padrao_termo("gdpr"), _padrao_termo("gdpr"))


if __name__ == "__main__":
    unittest.main()
