"""A3: chave_proposicao sem anos impossíveis por concatenação."""
import json
import unittest
from pathlib import Path

from lib.taxonomia import chave_proposicao, indice_corpus

RAIZ = Path(__file__).resolve().parent.parent


class TestAnos(unittest.TestCase):
    def test_quatro_digitos(self):
        self.assertEqual(chave_proposicao("PL 2.780/2024"), ["PL 2780/2024"])
        self.assertEqual(chave_proposicao("PL 10/1998"), ["PL 10/1998"])

    def test_dois_digitos_com_pivo(self):
        # pivo 26 = ano de 2026
        self.assertEqual(chave_proposicao("PL 10/98", pivo=26), ["PL 10/1998"])
        self.assertEqual(chave_proposicao("PL 2.338/23", pivo=26), ["PL 2338/2023"])
        self.assertEqual(chave_proposicao("PL 5/26", pivo=26), ["PL 5/2026"])
        self.assertEqual(chave_proposicao("PL 5/27", pivo=26), ["PL 5/1927"])
        self.assertEqual(chave_proposicao("PL 5/00", pivo=26), ["PL 5/2000"])

    def test_ano_invalido_nao_gera_chave(self):
        for texto in ("PL 123/205", "PL 1/20265", "PL 1/9", "PL 1/"):
            self.assertEqual(chave_proposicao(texto, pivo=26), [], texto)

    def test_nunca_produz_ano_com_mais_de_quatro_digitos(self):
        for texto in ("PL 123/205", "PL 1/20265", "PL 10/98", "PL 1/2026"):
            for chave in chave_proposicao(texto, pivo=26):
                self.assertEqual(len(chave.split("/")[1]), 4, chave)

    def test_normalizacoes_preservadas(self):
        self.assertEqual(chave_proposicao("MP 1.317/2025"), ["MPV 1317/2025"])
        self.assertEqual(chave_proposicao("PL nº 002.338/2023"), ["PL 2338/2023"])
        self.assertEqual(chave_proposicao("PL 896 / 2023"), ["PL 896/2023"])
        self.assertEqual(chave_proposicao("PL 896/2023 (aprovado Senado — aguarda Câmara)"), ["PL 896/2023"])

    def test_texto_ambiguo_com_varias_proposicoes(self):
        self.assertEqual(chave_proposicao("PL 2338/2023 e PL 10/98 e PL 3/205", pivo=26),
                         ["PL 2338/2023", "PL 10/1998"])

    def test_vazio(self):
        self.assertEqual(chave_proposicao(""), [])
        self.assertEqual(chave_proposicao(None), [])


class TestSemRegressaoNoCorpus(unittest.TestCase):
    def test_indice_do_corpus_so_tem_anos_de_quatro_digitos(self):
        normas = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
        for chave in indice_corpus(normas):
            self.assertRegex(chave, r"^[A-Z]+ \d+/\d{4}$")


if __name__ == "__main__":
    unittest.main()
