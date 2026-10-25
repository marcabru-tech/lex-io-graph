"""Curadoria com fontes primárias (25/10/2026): cronologia do casamento, 27 PDLs, encíclica, Decreto 12.976."""
import ast
import json
import unittest
from pathlib import Path

from lib.conformidade import ENQUADRAMENTO_DECRETO_12976_IA
from lib.repositorio import MAGNIFICA_HUMANITAS, TRADICOES_JURIDICAS

RAIZ = Path(__file__).resolve().parent.parent


def _strings_python(caminho: str) -> list:
    """Valores efetivos das strings do módulo, lidos por AST.

    A AST já junta a concatenação implícita ("a " "b" -> "a b"), então o teste
    vê o texto exibido, sem depender de regex sobre o código-fonte.
    """
    arvore = ast.parse((RAIZ / caminho).read_text(encoding="utf-8"))
    return [n.value for n in ast.walk(arvore) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _strings_json(valor) -> list:
    if isinstance(valor, str):
        return [valor]
    if isinstance(valor, dict):
        return [s for v in valor.values() for s in _strings_json(v)]
    if isinstance(valor, list):
        return [s for v in valor for s in _strings_json(v)]
    return []


NORMAS = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))
STRINGS = {
    "lib/inteligencia.py": _strings_python("lib/inteligencia.py"),
    "lib/repositorio.py": _strings_python("lib/repositorio.py"),
    "data/normas.json": _strings_json(NORMAS),
}


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
        total = 0
        for caminho, strings in STRINGS.items():
            for texto in strings:
                if "27 PDLs" not in texto:
                    continue
                total += 1
                with self.subTest(arquivo=caminho, trecho=texto[:60]):
                    # Toda menção cita o levantamento; o título da Tensão 3 traz a data.
                    self.assertTrue("Radar do Lexiograph" in texto or "(base da Câmara, 15/08/2026)" in texto)
        # Strings com "27 PDLs": inteligencia.py 2 (título da Tensão 3 e convergência),
        # repositorio.py 1, normas.json 5. A análise da Tensão 3 diz "contou 27" (ver abaixo).
        self.assertEqual(total, 8)

    def test_sem_enumeracao_de_partidos(self):
        textos = STRINGS["lib/inteligencia.py"]
        self.assertFalse(any("Republicanos" in t for t in textos))
        self.assertTrue(any("contagem do levantamento, não total oficial da Câmara" in t for t in textos))


class TestEnciclica(unittest.TestCase):
    def test_fonte_oficial_igual_a_do_corpus(self):
        no = next((n for n in NORMAS["nodes"] if n["id"] == "magnifica_humanitas"), None)
        self.assertIsNotNone(no, "Nó 'magnifica_humanitas' não encontrado em normas.json")
        url = no["fonte_oficial_url"]
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
