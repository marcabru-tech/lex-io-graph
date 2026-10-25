"""A5: a contagem declarada no ADR 007 acompanha data/jurisprudencia.json."""
import json
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ADR = (RAIZ / "docs" / "adr" / "007-estados-de-verificacao-jurisprudencia.md").read_text(encoding="utf-8")
REGISTROS = json.loads((RAIZ / "data" / "jurisprudencia.json").read_text(encoding="utf-8"))["jurisprudencia"]


class TestContagemDoAdr007(unittest.TestCase):
    def test_contagem_atual_bate_com_o_corpus(self):
        m = re.search(r"Contagem atual: (\d+) registros", ADR)
        self.assertIsNotNone(m, "o ADR 007 deve declarar a contagem atual")
        self.assertEqual(int(m.group(1)), len(REGISTROS))

    def test_ids_e_estados_declarados_batem_com_o_corpus(self):
        bloco = ADR.split("## Atualização")[-1]
        # Par a par: cada id com o próprio estado entre parênteses (A6-g).
        declarados = dict(re.findall(r"`(\w+)`\s*\(`(\w+)`\)", " ".join(bloco.split())))
        self.assertEqual(declarados, {r["id"]: r["estado_verificacao"] for r in REGISTROS})
        self.assertFalse(any(r["estado_verificacao"] == "verificado" for r in REGISTROS))
        self.assertIn("nenhum", bloco)

    def test_decisao_historica_preservada(self):
        self.assertIn("guarda cinco registros", ADR)  # contexto da data da decisão
        self.assertIn("a decisão acima não muda", ADR)


if __name__ == "__main__":
    unittest.main()
