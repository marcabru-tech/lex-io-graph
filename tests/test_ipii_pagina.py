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


class TestTierEValoresMalformados(unittest.TestCase):
    def test_tier_invalido_nao_quebra_o_filtro(self):
        from lib.ipii_pagina import filtrar_por_tier, tier_valido
        for ruim in ("x", None, [1], {"a": 1}, 0, 9, True, 2.7):
            self.assertIn(tier_valido(ruim), range(1, 6), ruim)
        novas = [{"tier": "x"}, {"tier": 1}, {"tier": [2]}, "não é objeto", {"tier": 3}]
        self.assertEqual(len(filtrar_por_tier(novas, 5)), 4)
        self.assertEqual(len(filtrar_por_tier(novas, 1)), 1)
        self.assertEqual(filtrar_por_tier("não é lista", 5), [])

    def test_tipo_lista_ou_dict_nao_quebra(self):
        from lib.ipii_pagina import rotulo_tipo
        self.assertEqual(rotulo_tipo("regulamenta"), "Regulamentação")
        self.assertEqual(rotulo_tipo(["x"]), "['x']")
        self.assertEqual(rotulo_tipo(None, "Não especificado"), "Não especificado")
        html = html_aresta_nova({"tipo_sugerido": {"a": 1}, "tier": [1]})
        self.assertIn("TIER 5", html)


class TestPaginaComRelatorioMalformado(unittest.TestCase):
    """Caminho da página: o relatório vem com tier, tipo e entradas malformados."""

    def test_todas_as_secoes_renderizam_sem_excecao(self):
        import shutil
        import streamlit as st
        from streamlit.testing.v1 import AppTest
        raiz = Path(__file__).resolve().parent.parent
        rel = raiz / "data" / "ipii_resultado.json"
        copia = Path(tempfile.mkdtemp()) / "ipii_resultado.json"
        shutil.copy(rel, copia)
        try:
            dados = json.loads(rel.read_text(encoding="utf-8"))
            dados["detalhe_novas"] = [{"source": MALICIOSO, "target": "b", "tier": "x", "score": 1,
                                       "classificacao": "fraca", "tipo_sugerido": ["lista"]},
                                      {"tier": {"a": 1}}, "texto solto"]
            dados["detalhe_confirmadas"] = [{"source": "a", "tipo_existente": {"b": 2}}, 7]
            dados["gap_engine"] = [{"par": "a ↔ b", "tipo": ["x"]}, None]
            dados["fora_do_ipii"] = [{"par": "c ↔ d", "tipo": {"y": 1}}]
            dados["precisao"] = "quebrado"
            rel.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
            st.cache_data.clear()
            at = AppTest.from_file(str(raiz / "pages" / "9_🔬_IPII_Engine.py"), default_timeout=60)
            at.run()
            for opcao in at.radio[0].options:
                at.radio[0].set_value(opcao).run()
                if at.selectbox:
                    for tier in at.selectbox[0].options:
                        at.selectbox[0].set_value(tier).run()
                        self.assertEqual(len(at.exception), 0, (opcao, tier))
                self.assertEqual(len(at.exception), 0, opcao)
        finally:
            shutil.copy(copia, rel)
            st.cache_data.clear()
