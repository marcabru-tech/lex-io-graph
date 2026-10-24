"""ADR 007: jurisprudência não verificada nunca aparece sem selo (item D-1a)."""
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


class TestSeloComparacao(unittest.TestCase):
    def test_pagina_3_exibe_selo_para_registro_nao_verificado(self):
        from streamlit.testing.v1 import AppTest
        from lib.graph_builder import load_json

        juris = load_json("jurisprudencia.json")["jurisprudencia"]
        alvo = next((j for j in juris if j.get("estado_verificacao") != "verificado"), None)
        if alvo is None:
            self.skipTest("Nenhum registro não verificado em jurisprudencia.json")
        norma = alvo["normas_relacionadas"][0]
        outra = next(n["id"] for n in load_json("normas.json")["nodes"] if n["id"] != norma)

        pagina = next((RAIZ / "pages").glob("3_*Comparacao*.py"))
        at = AppTest.from_file(str(pagina), default_timeout=60).run()
        at.selectbox[0].set_value(norma)
        at.selectbox[1].set_value(outra)
        at.run()
        self.assertEqual(len(at.exception), 0)
        rotulos = [e.label for e in at.expander]
        com_numero = [r for r in rotulos if alvo["numero"] in r]
        self.assertTrue(com_numero, f"registro {alvo['numero']} não foi exibido")
        self.assertTrue(all(r.startswith("⚠ Em conferência") for r in com_numero))
        self.assertTrue(any("Não utilizar como precedente" in w.value for w in at.warning))


if __name__ == "__main__":
    unittest.main()
