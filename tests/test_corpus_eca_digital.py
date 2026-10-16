"""Trava de regressão: vigência do ECA Digital (Lei 15.211/2025).

Fontes: Lei 15.211/2025, arts. 41 (vetado) e 41-A; MP 1.319/2025, art. 1º;
Lei 15.352/2026, arts. 19 e 20 — textos no Planalto.
Não há dispositivo que preveja "180 dias para adequação" das plataformas.
"""
import json
import unittest
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "data" / "normas.json"


def _historia_eca_digital():
    with open(CORPUS, encoding="utf-8") as f:
        nos = json.load(f)["nodes"]
    return next(n for n in nos if n.get("id") == "eca_digital")["historia"]


class TestHistoriaEcaDigital(unittest.TestCase):
    def test_nao_reintroduz_prazo_de_180_dias(self):
        self.assertNotIn("180 dias", _historia_eca_digital())

    def test_registra_art_41a_e_data_de_vigencia(self):
        historia = _historia_eca_digital()
        self.assertIn("41-A", historia)
        self.assertIn("17/03/2026", historia)


if __name__ == "__main__":
    unittest.main()
