"""Travas do Lote B da auditoria de prontidão (24/10/2026).

Garantem que as correções técnicas não regridam: dependências fixadas,
barreira de testes antes do deploy, configuração de produção do Streamlit,
caminhos absolutos e resumo legível das descrições do IPII.
"""
import re
import tomllib
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


class TestDependencias(unittest.TestCase):
    def test_requirements_tudo_fixado(self):
        linhas = [l.split("#")[0].strip() for l in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines()]
        pacotes = [l for l in linhas if l]
        self.assertGreater(len(pacotes), 5)
        soltos = [p for p in pacotes if "==" not in p]
        self.assertEqual(soltos, [], f"Dependências sem versão exata: {soltos}")

    def test_versoes_da_auditoria(self):
        txt = (RAIZ / "requirements.txt").read_text(encoding="utf-8")
        self.assertRegex(txt, r"(?m)^streamlit==1\.66\.1$")
        self.assertRegex(txt, r"(?m)^pillow==13\.0\.0$")

    def test_python_fixado(self):
        self.assertEqual((RAIZ / ".python-version").read_text().strip(), "3.12")


class TestBarreiraDeDeploy(unittest.TestCase):
    def test_testes_antes_do_build_sem_paralelismo(self):
        txt = (RAIZ / "cloudbuild.yaml").read_text(encoding="utf-8")
        ids = re.findall(r"(?m)^  - id: (\w+)", txt)
        self.assertEqual(ids, ["Testes", "Buildpack", "Pull", "Push", "Deploy"])
        self.assertNotRegex(txt, r"(?m)^\s+waitFor:", "waitFor permitiria rodar o build em paralelo aos testes")
        self.assertIn("unittest discover tests", txt)
        self.assertIn("smoke_test.py", txt)


class TestConfiguracaoStreamlit(unittest.TestCase):
    def test_producao(self):
        cfg = tomllib.loads((RAIZ / ".streamlit" / "config.toml").read_text(encoding="utf-8"))
        self.assertEqual(cfg["client"]["showErrorDetails"], "none")
        self.assertIs(cfg["browser"]["gatherUsageStats"], False)


class TestCaminhos(unittest.TestCase):
    def test_paginas_nao_abrem_data_por_caminho_relativo(self):
        for pagina in (RAIZ / "pages").glob("*.py"):
            with self.subTest(pagina=pagina.name):
                self.assertNotIn('open("data/', pagina.read_text(encoding="utf-8"))

    def test_grafo_apaga_o_temporario(self):
        src = next((RAIZ / "pages").glob("1_*Grafo*.py")).read_text(encoding="utf-8")
        self.assertIn("os.unlink(tmp.name)", src)


class TestResumoIPII(unittest.TestCase):
    def setUp(self):
        from lib.ipii.validator import resumir, validar_arestas
        self.resumir, self.validar = resumir, validar_arestas

    def test_curto_fica_igual(self):
        self.assertEqual(self.resumir("Texto curto."), "Texto curto.")
        self.assertEqual(self.resumir(None), "")

    def test_corta_em_palavra_inteira(self):
        texto = "Convergência normativa entre " * 10
        r = self.resumir(texto)
        self.assertLessEqual(len(r), 121)
        self.assertTrue(r.endswith("…"))
        self.assertTrue(texto.startswith(r[:-1]))
        self.assertIn(texto[len(r) - 1], " ", "o corte deve cair entre palavras")

    def test_relatorio_guarda_o_texto_integral(self):
        longa = "Descrição longa da relação curada " * 8
        existentes = [{"source": "a", "target": "b", "tipo": "hierarquia", "descricao": longa}]
        rel = self.validar([], existentes)
        item = rel["gap_engine"][0]
        self.assertEqual(item["descricao_completa"], longa)
        self.assertTrue(item["descricao"].endswith("…"))


if __name__ == "__main__":
    unittest.main()
