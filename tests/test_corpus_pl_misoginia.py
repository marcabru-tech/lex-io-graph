"""Trava de regressão: história do PL 896/2023 (criminalização da misoginia).

Fonte: ficha da matéria no Senado Federal (PL 896/2023, autuado no Plenário do
Senado em 06/03/2023; mesmo número na Câmara). O trecho editorial sobre
islamismo e "tensão normativa civilizatória" foi retirado por decisão do
mantenedor: afirmação sem fonte e sem relação com a norma.
"""
import json
import unittest
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "data" / "normas.json"


def _historia():
    with open(CORPUS, encoding="utf-8") as f:
        nos = json.load(f)["nodes"]
    return next(n for n in nos if n.get("id") == "pl_misoginia")["historia"]


class TestHistoriaPlMisoginia(unittest.TestCase):
    def test_origem_no_senado(self):
        historia = _historia()
        self.assertIn("apresentado originalmente no Senado", historia)
        self.assertNotIn("proposto originalmente na Câmara", historia)

    def test_sem_trecho_editorial_retirado(self):
        historia = _historia()
        for termo in ("islamismo", "civilizatória"):
            self.assertNotIn(termo, historia)


if __name__ == "__main__":
    unittest.main()
