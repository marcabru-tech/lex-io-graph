"""Curadoria com fontes primárias (25/10/2026): cronologia do casamento, 27 PDLs, encíclica, Decreto 12.976."""
import json
import re
import unittest
from pathlib import Path

from lib.conformidade import ENQUADRAMENTO_DECRETO_12976_IA
from lib.repositorio import MAGNIFICA_HUMANITAS, TRADICOES_JURIDICAS

RAIZ = Path(__file__).resolve().parent.parent
TEXTOS = {p: (RAIZ / p).read_text(encoding="utf-8")
          for p in ("lib/inteligencia.py", "lib/repositorio.py", "data/normas.json")}


class TestCasamento(unittest.TestCase):
    def test_cronologia_dos_atos_oficiais(self):
        t = TRADICOES_JURIDICAS["canonico"]["brasil"]
        self.assertNotIn("1916", t)
        self.assertNotIn("via Portugal", t)
        for trecho in ("Decreto de 3 de novembro de 1827", "Decreto nº 181/1890", "24 de maio de 1890",
                       "Constituição de 1934 (art. 146)"):
            self.assertIn(trecho, t)


class TestPdls(unittest.TestCase):
    def test_toda_mencao_aos_27_pdls_cita_o_levantamento(self):
        for caminho, texto in TEXTOS.items():
            plano = " ".join(re.sub(r'"\s*\n\s*"', "", texto).split())
            for m in re.finditer(r"27 PDLs", plano):
                trecho = plano[m.start():m.start() + 200]
                with self.subTest(arquivo=caminho, trecho=trecho[:60]):
                    self.assertTrue("Radar do Lexiograph" in trecho or "(base da Câmara, 15/08/2026)" in trecho)

    def test_sem_enumeracao_de_partidos(self):
        self.assertNotIn("Republicanos", TEXTOS["lib/inteligencia.py"])
        self.assertIn("contagem do levantamento, não total oficial da Câmara",
                      " ".join(re.sub(r'"\s*\n\s*"', "", TEXTOS["lib/inteligencia.py"]).split()))


class TestEnciclica(unittest.TestCase):
    def test_fonte_oficial_igual_a_do_corpus(self):
        nos = json.loads(TEXTOS["data/normas.json"])["nodes"]
        url = next(n for n in nos if n["id"] == "magnifica_humanitas")["fonte_oficial_url"]
        self.assertEqual(MAGNIFICA_HUMANITAS["fonte_oficial_url"], url)
        self.assertTrue(url.startswith("https://www.vatican.va/"))


class TestAvisoDecreto(unittest.TestCase):
    def test_arts_9_e_10_conforme_a_redacao_oficial(self):
        t = ENQUADRAMENTO_DECRETO_12976_IA
        for trecho in ("art. 9º veda aos provedores de aplicações de internet", "imagem ou o som da vítima",
                       "art. 10 exige", "salvaguardas técnicas e procedimentais",
                       "conforme a regulamentação da autoridade competente", "não atrai, por si só"):
            self.assertIn(trecho, t)


if __name__ == "__main__":
    unittest.main()
