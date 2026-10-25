"""A6-f: plurais de jurisdição, "Lei n.º" e campos nulos no tokenizador do IPII."""
import unittest

from lib.ipii.matcher import calcular_intersecao
from lib.ipii.tokenizer import _extrair_jurisdicoes, _numeros_de_lei, tokenizar_corpus, tokenizar_norma


def _jur(texto):
    return set(_extrair_jurisdicoes({"direito_comparado": texto}))


class TestPlurais(unittest.TestCase):
    def test_plurais_voltam_a_casar(self):
        casos = {
            "Inspirada nos modelos americanos e europeus": {"EUA", "UE"},
            "Como os códigos alemães": {"Alemanha"},
            "Como os juristas franceses": {"França"},
            "Como os civilistas italianos": {"Itália"},
            "Como os reguladores chineses": {"China"},
            "Nas encíclicas sociais": {"Vaticano"},
        }
        for texto, esperado in casos.items():
            self.assertEqual(_jur(texto), esperado, texto)

    def test_singular_continua(self):
        self.assertEqual(_jur("modelo americano e europeu"), {"EUA", "UE"})

    def test_negacao_vale_para_o_plural(self):
        self.assertEqual(_jur("Regras distintas dos modelos europeus"), set())

    def test_palavra_inteira_continua(self):
        self.assertEqual(_jur("europeusmente"), set())


class TestLeiNumero(unittest.TestCase):
    def test_formas_de_numero(self):
        for texto in ("Lei n.º 12.965/2014", "Lei nº 12.965/2014", "Lei n° 12965/2014",
                      "Lei no 12.965/2014", "Lei 12.965/2014", "Lei N.º 12.965/2014",
                      "Lei n. 12.965/2014", "lei n.° 12.965/2014"):
            self.assertEqual(_numeros_de_lei(texto), {"12965/2014"}, texto)

    def test_sem_lei_nao_extrai(self):
        self.assertEqual(_numeros_de_lei("Decreto n.º 12.975/2026"), set())

    def test_regulamenta_com_n_ponto_ordinal(self):
        lei = tokenizar_norma({"id": "mci", "tipo": "lei", "sigla": "Lei n.º 12.965/2014",
                               "ementa": "Marco Civil da Internet", "ano": 2014})
        dec = tokenizar_norma({"id": "dec", "tipo": "decreto", "sigla": "Decreto 1/2016",
                               "ementa": "Regulamenta a Lei n.º 12.965/2014", "ano": 2016})
        self.assertEqual(lei["numero_lei"], "12965/2014")
        self.assertEqual(dec["leis_citadas"], ["12965/2014"])
        self.assertEqual(calcular_intersecao(dec, lei)["tipo_sugerido"], "regulamenta")


class TestCamposNulos(unittest.TestCase):
    NULA = {"id": "x", "tipo": "lei", "ementa": None, "historia": None, "direito_comparado": None,
            "sigla": None, "temas": None, "autores": None, "latim": None, "artigos_chave": None,
            "orgao": None, "ano": None, "status": "vigente"}

    def test_tokenizar_com_campos_nulos(self):
        t = tokenizar_norma(self.NULA)
        self.assertEqual((t["temas"], t["artigos_chave"], t["orgao"]), ([], [], ""))
        self.assertEqual((t["jurisdicao"], t["leis_citadas"], t["ementa_tokens"]), ([], [], []))
        self.assertIsNone(t["numero_lei"])

    def test_tipos_inesperados_viram_vazio(self):
        t = tokenizar_norma({"id": "y", "ementa": ["lista"], "autores": [None, "texto", {"nome": None}],
                             "latim": {"a": 1}})
        self.assertEqual(t["ementa_tokens"], [])
        self.assertEqual(t["hermeneutica"]["autores"], [{"nome": "", "obra": ""}])
        self.assertEqual(t["hermeneutica"]["brocardos"], [])

    def test_par_com_norma_nula_nao_derruba_o_motor(self):
        tokens = tokenizar_corpus([self.NULA, {"id": "z", "tipo": "lei", "ementa": "Dados pessoais",
                                               "temas": ["dados_pessoais"], "ano": 2018}])
        r = calcular_intersecao(tokens["x"], tokens["z"])
        self.assertIn("temporal", r["dimensoes_sem_dado"])


if __name__ == "__main__":
    unittest.main()
