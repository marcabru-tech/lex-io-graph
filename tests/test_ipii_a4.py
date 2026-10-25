"""A4: regras determinísticas do IPII, uma por etapa, com os pares reais medidos."""
import json
import unittest
from pathlib import Path

from lib.ipii.matcher import _sugerir_tipo
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



def _tok(ontologia, **extra):
    return {"ontologia": ontologia, **extra}


ZERO = {"temas": 0.0, "hierarquia": 0.0, "hermeneutica": 0.0, "comparado": 0.0, "temporal": 0.0, "ementa": 0.0}


class TestEtapa2Interpreta(unittest.TestCase):
    def test_jurisprudencia_e_constituicao_e_interpreta_nos_dois_sentidos(self):
        self.assertEqual(_sugerir_tipo(ZERO, _tok("jurisprudencia"), _tok("constituicao"), set()), "interpreta")
        self.assertEqual(_sugerir_tipo(ZERO, _tok("constituicao"), _tok("jurisprudencia"), set()), "interpreta")

    def test_hierarquia_preservada_para_os_demais_pares_com_constituicao(self):
        for outro in ("lei", "decreto", "documento_internacional", "pl", "orgao"):
            self.assertEqual(_sugerir_tipo(ZERO, _tok("constituicao"), _tok(outro), set()), "hierarquia", outro)

    def test_interpreta_preservada_para_lei_e_decreto(self):
        for outro in ("lei", "decreto", "norma_regulamentar"):
            self.assertEqual(_sugerir_tipo(ZERO, _tok("jurisprudencia"), _tok(outro), set()), "interpreta", outro)

    def test_jurisprudencia_com_outros_tipos_nao_vira_interpreta(self):
        for outro in ("pl", "documento_internacional", "orgao", "jurisprudencia"):
            self.assertNotEqual(_sugerir_tipo(ZERO, _tok("jurisprudencia"), _tok(outro), set()), "interpreta", outro)


if __name__ == "__main__":
    unittest.main()
