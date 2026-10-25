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
        self.assertEqual(r["precisao_tipo"], round(r["acertos_tipo"] / len(r["detalhe_confirmadas"]), 3))



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



class TestEtapa3RegulamentaComEvidencia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lib.ipii.tokenizer import tokenizar_corpus
        normas = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
        cls.tok = tokenizar_corpus(normas)

    def _tipo(self, a, b):
        return _sugerir_tipo(ZERO, self.tok[a], self.tok[b], set())

    def test_controles_positivos_com_a_lei_citada(self):
        # Decreto 13.118 "Regulamenta a Lei 15.506/2026"; Decreto 12.975 cita a Lei 12.965/2014
        self.assertEqual(self._tipo("lei_15506_2026", "decreto_13118_2026"), "regulamenta")
        self.assertEqual(self._tipo("decreto_12975_2026", "marco_civil"), "regulamenta")

    def test_casos_sem_evidencia_nao_viram_regulamenta(self):
        self.assertNotEqual(self._tipo("lei_15504_2026", "decreto_13118_2026"), "regulamenta")
        self.assertNotEqual(self._tipo("eca_digital", "decreto_12975_2026"), "regulamenta")

    def test_numero_de_outra_lei_no_decreto_nao_basta(self):
        decreto = {"ontologia": "decreto", "leis_citadas": ["12965/2014"]}
        lei = {"ontologia": "lei", "numero_lei": "15504/2026"}
        self.assertNotEqual(_sugerir_tipo(ZERO, decreto, lei, set()), "regulamenta")
        lei_certa = {"ontologia": "lei", "numero_lei": "12965/2014"}
        self.assertEqual(_sugerir_tipo(ZERO, decreto, lei_certa, set()), "regulamenta")

    def test_extracao_de_numero_de_lei(self):
        from lib.ipii.tokenizer import _numeros_de_lei
        self.assertEqual(_numeros_de_lei("altera a Lei nº 12.965/2014 e a Lei 8.069/1990"),
                         {"12965/2014", "8069/1990"})
        self.assertEqual(_numeros_de_lei("Decreto 12.975/2026"), set())



class TestEtapa4Jurisdicao(unittest.TestCase):
    def _jur(self, texto):
        from lib.ipii.tokenizer import _extrair_jurisdicoes
        return set(_extrair_jurisdicoes({"direito_comparado": texto}))

    def test_positivos(self):
        self.assertIn("UE", self._jur("Inspirada no GDPR (União Europeia, 2016)."))
        self.assertIn("UE", self._jur("O DSA (Digital Services Act) de 2022."))
        self.assertIn("EUA", self._jur("Análoga à Section 230 dos Estados Unidos."))

    def test_sigla_eua(self):
        self.assertIn("EUA", self._jur("Executive Order on AI — EUA (2023)."))
        self.assertNotIn("EUA", self._jur("Uma eutanásia e a teuar não são siglas."))

    def test_negacao_explicita_nao_conta(self):
        self.assertNotIn("UE", self._jur("A Suíça negocia acordos próprios, distintos dos da União Europeia."))
        self.assertNotIn("EUA", self._jur("Modelo diferente do adotado nos Estados Unidos."))

    def test_negacao_vale_so_na_mesma_oracao(self):
        texto = "Acordos distintos dos da Suíça. A União Europeia adota o GDPR."
        self.assertIn("UE", self._jur(texto))

    def test_uma_ocorrencia_valida_basta(self):
        texto = "Regras distintas da União Europeia em tarifas; inspirada no GDPR em dados."
        self.assertIn("UE", self._jur(texto))

    def test_dsa_dentro_de_outra_palavra_nao_casa(self):
        # sigla dentro de palavra (erro de digitação ou composição) não é a jurisdição
        self.assertNotIn("UE", self._jur("A responsabilidsade civil e a pradsa local."))

    def test_caso_real_efta(self):
        from lib.ipii.tokenizer import tokenizar_corpus
        normas = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
        tok = tokenizar_corpus([n for n in normas if n["id"] == "acordo_mercosul_efta"])
        self.assertNotIn("UE", tok["acordo_mercosul_efta"]["jurisdicao"])



def _token(id_, ano, temas=("dados_pessoais",), ontologia="lei"):
    return {"id": id_, "ontologia": ontologia, "temas": list(temas),
            "hermeneutica": {"autores": [], "brocardos": [], "correntes": []},
            "temporal": {"ano": ano, "status": "vigente", "em_vigor": True},
            "jurisdicao": [], "ementa_tokens": ["dados"], "numero_lei": None, "leis_citadas": []}


class TestEtapa5AnoDesconhecido(unittest.TestCase):
    def test_ano_ausente_tira_a_dimensao_e_redistribui_os_pesos(self):
        from lib.ipii.matcher import PESOS, calcular_intersecao
        r = calcular_intersecao(_token("a", None), _token("b", 2020))
        self.assertIsNone(r["scores_parciais"]["temporal"])
        self.assertEqual(r["dimensoes_sem_dado"], ["temporal"])
        # (0,30·1 + 0,15·0,3 + 0 + 0 + 0,15·1) / 0,90, com os PESOS de 25/10/2026.
        self.assertAlmostEqual(r["score"], 0.55, places=3)
        self.assertNotIn("temporal", [k for k in PESOS if r["scores_parciais"][k] is not None])

    def test_ano_ausente_nao_e_tratado_como_cem_anos(self):
        from lib.ipii.matcher import calcular_intersecao
        sem_ano = calcular_intersecao(_token("a", None), _token("b", 2020))["score"]
        cem_anos = calcular_intersecao(_token("a", 1900), _token("b", 2020))["score"]
        self.assertGreater(sem_ano, cem_anos)

    def test_com_os_dois_anos_nada_muda(self):
        from lib.ipii.matcher import PESOS, calcular_intersecao
        r = calcular_intersecao(_token("a", 2019), _token("b", 2020))
        self.assertEqual(r["dimensoes_sem_dado"], [])
        self.assertAlmostEqual(r["score"], 0.595, places=3)
        self.assertEqual(set(r["scores_parciais"]), set(PESOS))

    def test_sem_nenhuma_dimensao_utilizavel_nao_inventa_pontuacao(self):
        from unittest import mock
        import lib.ipii.matcher as m
        with mock.patch.dict(m.PESOS, {"temas": 0, "hierarquia": 0, "hermeneutica": 0,
                                       "comparado": 0, "temporal": 1.0, "ementa": 0}, clear=True):
            r = m.calcular_intersecao(_token("a", None), _token("b", None))
        self.assertEqual(r["score"], 0.0)
        self.assertEqual(r["classificacao"], "irrelevante")

    def test_campos_ano_orgao_sigla_intactos(self):
        normas = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
        sem_ano = {n["id"] for n in normas if not n.get("ano")}
        self.assertEqual(sem_ano, {"stf_adimc", "stj_resp", "stj_resp_plat"})


if __name__ == "__main__":
    unittest.main()
