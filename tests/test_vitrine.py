"""Vitrine (index.html), README e artigos: números e afirmações travados (PR de conteúdo 1b).

Os números da página institucional vêm do corpus; se o corpus mudar e a página
não, a CI quebra (critério 5 da auditoria de prontidão).
"""
import json
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _corpus():
    normas = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
    arestas = json.loads((RAIZ / "data" / "arestas.json").read_text(encoding="utf-8"))["edges"]
    paginas = len(list((RAIZ / "pages").glob("*.py")))
    return len(normas), len(arestas), paginas


class TestNumeros(unittest.TestCase):
    def setUp(self):
        self.n_normas, self.n_arestas, self.n_paginas = _corpus()
        self.index = (RAIZ / "index.html").read_text(encoding="utf-8")

    def _todos(self, padrao, texto):
        achados = [int(x) for x in re.findall(padrao, texto)]
        self.assertTrue(achados, f"padrão não encontrado: {padrao}")
        return achados

    def test_index_normas(self):
        for padrao in (r"(\d+) normas mapeadas", r"corpus (\d+) normas", r"sobre as (\d+) normas do corpus", r"(\d+) normas, \d+ arestas mapeadas"):
            for n in self._todos(padrao, self.index):
                self.assertEqual(n, self.n_normas, padrao)

    def test_index_arestas(self):
        for padrao in (r"(\d+) arestas tipadas", r"corpus \d+ normas · (\d+) arestas", r"\d+ normas, (\d+) arestas mapeadas"):
            for n in self._todos(padrao, self.index):
                self.assertEqual(n, self.n_arestas, padrao)

    def test_paginas_do_app(self):
        for n in self._todos(r"(\d+) páginas de inteligência", self.index):
            self.assertEqual(n, self.n_paginas)
        linhas = re.findall(r"<td>(\d+)</td>\s*<td style=\"color: var\(--(?:lex|io)\);\">", self.index)
        self.assertTrue(linhas, "padrão da tabela do app não encontrado em index.html")
        self.assertEqual(sorted(map(int, linhas))[-1], self.n_paginas, "a tabela do app deve listar todas as páginas")

    def test_readme(self):
        readme = (RAIZ / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"{self.n_paginas} páginas · {self.n_normas} nós no corpus · {self.n_arestas} conexões", readme)


class TestAfirmacoes(unittest.TestCase):
    PROIBIDAS = ("o único atlas", "único produto", "risco regulatório zero", "O risco regulatório é zero",
                 "LGPD compliant", "Zero dados coletados", "(consentimento existe) AND (base legal válida)", "tratamento pode ser realizado",
                 "inaliável", "ARTIGO 1 DE 3", "onmicrosoft.com", "7 princípios")

    def test_index_sem_afirmacoes_retiradas(self):
        index = (RAIZ / "index.html").read_text(encoding="utf-8")
        for frase in self.PROIBIDAS:
            with self.subTest(frase=frase):
                self.assertNotIn(frase, index)

    def test_index_tem_aviso_de_triagem_e_privacidade(self):
        index = (RAIZ / "index.html").read_text(encoding="utf-8")
        self.assertIn("não é certificação de conformidade", index)
        self.assertIn('id="privacidade"', index)
        self.assertIn("30 dias", index)
        self.assertIn("configuração técnica atual", index, "os 30 dias não podem soar como conclusão jurídica")
        self.assertIn("Responsável pelo tratamento", index)
        self.assertIn("art. 18", index)

    def test_artigos_sem_erros_corrigidos(self):
        textos = "\n".join(p.read_text(encoding="utf-8") for p in (RAIZ / "artigos").glob("*.html"))
        for frase in ("por 8 a 2", "Decreto 38/1935", "positivia", "7 Princípios", "São Bernardo, três",
                      "9 páginas de inteligência", "DE 3", "onmicrosoft.com"):
            with self.subTest(frase=frase):
                self.assertNotIn(frase, textos)


if __name__ == "__main__":
    unittest.main()
