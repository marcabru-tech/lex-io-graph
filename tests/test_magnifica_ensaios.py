"""PR 7b: mesmos critérios editoriais da PR 7 nos ensaios e no Repositório."""
import ast
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVOS = [RAIZ / "lib" / "inteligencia.py", RAIZ / "lib" / "repositorio.py",
            RAIZ / "pages" / "5_📚_Repositorio.py", RAIZ / "data" / "normas.json"]


def _literal(caminho: Path, nome: str):
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    for no in arvore.body:
        if isinstance(no, ast.Assign) and any(getattr(t, "id", None) == nome for t in no.targets):
            return ast.literal_eval(no.value)
    raise KeyError(nome)


class TestSemAfirmacoesSemFonte(unittest.TestCase):
    def test_sem_presenca_nao_confirmada_nem_local_divergente(self):
        for arq in ARQUIVOS:
            texto = arq.read_text(encoding="utf-8")
            self.assertNotIn("Chris Olah", texto, arq.name)  # volta só com fonte primária conferida
            self.assertNotIn("Sala Nova do Sínodo", texto, arq.name)

    def test_sem_citacao_literal_nao_conferida(self):
        for arq in ARQUIVOS:
            self.assertNotIn("A IA precisa ser desarmada", arq.read_text(encoding="utf-8"), arq.name)

    def test_sem_causalidade_nem_superlativo(self):
        for arq in ARQUIVOS:
            texto = arq.read_text(encoding="utf-8")
            for proibido in ("com impacto no PL 2.338", "Momento civilizatório singular",
                             "convergiram no mesmo campo normativo"):
                self.assertNotIn(proibido, texto, (arq.name, proibido))


class TestRepositorio(unittest.TestCase):
    MH = _literal(RAIZ / "lib" / "repositorio.py", "MAGNIFICA_HUMANITAS")

    def test_natureza_explicita(self):
        self.assertIn("sem força jurídica", self.MH["natureza"])

    def test_tese_e_capitulos_como_sintese(self):
        self.assertTrue(self.MH["tese_principal"].startswith("Síntese do Lexiograph, não citação literal"))
        for cap in self.MH["capitulos"]:
            self.assertTrue(cap.startswith("Tema (síntese):"), cap)

    def test_convergencia_sem_causalidade(self):
        self.assertIn("sem relação causal demonstrada", self.MH["convergencia_maio_2026"])
        self.assertNotIn("presenca_anthropic", self.MH)
        self.assertIn("convergencias_brasil", self.MH)

    def test_pagina_usa_as_chaves_existentes(self):
        pagina = (RAIZ / "pages" / "5_📚_Repositorio.py").read_text(encoding="utf-8")
        for chave in ("presenca_anthropic", "impacto_brasil"):
            self.assertNotIn(f"['{chave}']", pagina)
        for chave in ("natureza", "convergencias_brasil", "tese_principal"):
            self.assertIn(f"['{chave}']", pagina)


class TestInteligencia(unittest.TestCase):
    def test_caso_marca_a_leitura_e_a_natureza(self):
        casos = _literal(RAIZ / "lib" / "inteligencia.py", "CASOS_ESTRATEGICOS")
        caso = next(c for c in casos if c["id"] == "magnifica_humanitas_vaticano")
        self.assertTrue(caso["sintese"].startswith("Na leitura deste ensaio"))
        self.assertIn("sem força jurídica", caso["sintese"])
        self.assertIn("Santa Sé tem status de Estado observador", caso["prospectiva"]["36_meses"])

    def test_dado_do_censo_com_o_denominador_do_ibge(self):
        casos = _literal(RAIZ / "lib" / "inteligencia.py", "CASOS_ESTRATEGICOS")
        caso = next(c for c in casos if c["id"] == "magnifica_humanitas_vaticano")
        self.assertIn("56,7% das pessoas com 10 anos ou mais se declararam católicas", caso["sintese"])
        self.assertNotIn("57% da população", caso["sintese"])


if __name__ == "__main__":
    unittest.main()
