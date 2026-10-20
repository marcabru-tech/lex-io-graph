"""Travas de regressão das correções editoriais da auditoria de 19/10/2026.

Impedem o retorno de atribuições jurisprudenciais sem fonte e de erros
factuais corrigidos em lib/, pages/ e app.py. Leitura de texto puro.
"""
import re
import unittest
from pathlib import Path

from lib.multisemiose import CITACOES

RAIZ = Path(__file__).resolve().parent.parent

ARQUIVOS = (
    list((RAIZ / "lib").glob("*.py"))
    + list((RAIZ / "pages").glob("*.py"))
    + [RAIZ / "app.py"]
)

PROIBIDAS = (
    "CIDH art. 3º",
    "Convenção Interamericana de Direitos Humanos",
    "CC/2025",
    "segundo ano do reinado",
    "Voto descoberto e censitário",
    "absorveu o Código Comercial",
    "absorveu a parte terrestre",
    "PL 2.253/2024",
    "cria Livro VI",
    "Guerra Institucional Tripartite",
    "Resgate da doutrina de Pontes de Miranda",
    "Modelo oposto ao Brasil",
)

ATRIBUICAO_JURISPRUDENCIAL = re.compile(
    r"Min\.|Rui Barbosa|citad[oa]s? em votos|citad[oa] por|mais citada|STJ e STF utilizam|votos do ST[FJ]",
    re.IGNORECASE,
)


class TestEdicaoEditorial(unittest.TestCase):
    def test_atribuicao_jurisprudencial_casa_abreviatura_de_ministro(self):
        # r"Min\." exige o ponto literal: casa a abreviatura, não a palavra.
        self.assertIsNotNone(ATRIBUICAO_JURISPRUDENCIAL.search("voto do Min. Fux"))
        self.assertIsNone(ATRIBUICAO_JURISPRUDENCIAL.search("Ministério da Fazenda"))

    def test_frases_corrigidas_nao_retornam(self):
        for arquivo in ARQUIVOS:
            texto = arquivo.read_text(encoding="utf-8")
            for frase in PROIBIDAS:
                self.assertNotIn(frase, texto, f"{arquivo.name}: {frase}")

    def test_comparacao_alemanha_com_unificacao_parcial_no_brasil(self):
        pagina = next((RAIZ / "pages").glob("5_*.py"), None)
        self.assertIsNotNone(pagina, "página 5 (Repositório) não encontrada em pages/")
        self.assertIn(
            "O BGB e o HGB permanecem como códigos distintos; no Brasil, "
            "o CC/2002 promoveu unificação parcial do direito privado.",
            pagina.read_text(encoding="utf-8"),
        )

    def test_citacoes_sem_atribuicao_jurisprudencial_sem_fonte(self):
        for cit in CITACOES:
            if cit["id"] in ("tiradentes_mandado", "graciliano_relatorios"):
                continue
            self.assertIsNone(
                ATRIBUICAO_JURISPRUDENCIAL.search(cit["uso_jurisprudencia"]),
                cit["id"],
            )

    def test_batatas_atribuida_a_quincas_borba(self):
        cit = next((c for c in CITACOES if c["id"] == "machado_memorias"), None)
        self.assertIsNotNone(cit, "citação 'machado_memorias' ausente de CITACOES")
        self.assertIn("Quincas Borba", cit["obra"])
        self.assertNotIn("Memórias Póstumas", cit["obra"])
        self.assertIn("ao vencedor, as batatas", cit["citacao_original"])

    def test_pena_pessoal_na_convencao_americana_art_5(self):
        cit = next((c for c in CITACOES if c["id"] == "tiradentes_mandado"), None)
        self.assertIsNotNone(cit, "citação 'tiradentes_mandado' ausente de CITACOES")
        self.assertIn("Convenção Americana sobre Direitos Humanos (art. 5º, item 3)",
                      cit["uso_jurisprudencia"])


if __name__ == "__main__":
    unittest.main()
