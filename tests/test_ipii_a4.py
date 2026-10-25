"""A4: regras determinísticas do IPII, uma por etapa, com os pares reais medidos."""
import json
import unittest
from pathlib import Path

from lib.ipii.validator import validar_arestas

RAIZ = Path(__file__).resolve().parent.parent


class TestPrecisaoDeTipo(unittest.TestCase):
    def test_precisao_de_tipo_relatada(self):
        sug = [{"source": "a", "target": "b", "tipo_sugerido": "intersecao"},
               {"source": "c", "target": "d", "tipo_sugerido": "regulamenta"},
               {"source": "e", "target": "f", "tipo_sugerido": "intersecao"}]
        ex = [{"source": "a", "target": "b", "tipo": "intersecao"},
              {"source": "d", "target": "c", "tipo": "complementaridade"}]
        r = validar_arestas(sug, ex)
        self.assertEqual((r["confirmadas"], r["acertos_tipo"], r["precisao_tipo"]), (2, 1, 0.5))

    def test_sem_confirmadas_nao_divide_por_zero(self):
        self.assertEqual(validar_arestas([], [])["precisao_tipo"], 0)

    def test_resultado_versionado_tem_a_metrica(self):
        r = json.loads((RAIZ / "data" / "ipii_resultado.json").read_text(encoding="utf-8"))
        self.assertIn("precisao_tipo", r)
        self.assertEqual(r["acertos_tipo"], sum(1 for c in r["detalhe_confirmadas"] if c["match_tipo"]))


if __name__ == "__main__":
    unittest.main()
