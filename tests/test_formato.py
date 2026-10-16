"""Testes de lib.formato. Uso: python -m unittest discover tests"""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.formato import (  # noqa: E402
    ANO_NAO_CONFIRMADO,
    ano_exibicao,
    cartao_norma_html,
    link_fonte_oficial,
    quantidade,
    resumo_verificacao,
)


def reg(estado):
    """Registro mínimo: resumo_verificacao só lê estado_verificacao."""
    return {"id": "x", "estado_verificacao": estado}


class TestQuantidade(unittest.TestCase):
    def test_zero_fica_no_plural(self):
        self.assertEqual(quantidade(0, "verificado", "verificados"), "0 verificados")

    def test_um_fica_no_singular(self):
        self.assertEqual(quantidade(1, "verificado", "verificados"), "1 verificado")

    def test_dois_ou_mais_ficam_no_plural(self):
        self.assertEqual(quantidade(2, "pendente", "pendentes"), "2 pendentes")
        self.assertEqual(quantidade(17, "pendente", "pendentes"), "17 pendentes")


class TestResumoVerificacao(unittest.TestCase):
    def test_corpus_vazio(self):
        self.assertEqual(
            resumo_verificacao([]),
            "0 verificados · 0 pendentes · 0 contestados",
        )

    def test_distribuicao_em_plural(self):
        registros = [reg("pendente")] * 3 + [reg("contestado")] * 2
        self.assertEqual(
            resumo_verificacao(registros),
            "0 verificados · 3 pendentes · 2 contestados",
        )

    def test_distribuicao_hipotetica_com_dois_contestados(self):
        registros = [reg("pendente")] * 3 + [reg("contestado")]
        self.assertEqual(
            resumo_verificacao(registros),
            "0 verificados · 3 pendentes · 1 contestado",
        )

    def test_um_de_cada_fica_no_singular(self):
        registros = [reg("verificado"), reg("pendente"), reg("contestado")]
        self.assertEqual(
            resumo_verificacao(registros),
            "1 verificado · 1 pendente · 1 contestado",
        )

    def test_sem_estado_nao_aparece_quando_zero(self):
        self.assertNotIn("sem estado", resumo_verificacao([reg("pendente")]))

    def test_sem_estado_aparece_quando_houver(self):
        registros = [reg("verificado"), reg(None), {"id": "y"}]
        self.assertEqual(
            resumo_verificacao(registros),
            "1 verificado · 0 pendentes · 0 contestados · 2 sem estado",
        )

    def test_estado_invalido_conta_como_sem_estado(self):
        self.assertIn("1 sem estado", resumo_verificacao([reg("verificadoo")]))


class TestLinkFonteOficial(unittest.TestCase):
    URL = "https://www.planalto.gov.br/ccivil_03/leis/l8069.htm"

    def test_com_url_rende_link(self):
        trecho = link_fonte_oficial(self.URL)
        self.assertIn(f'href="{self.URL}"', trecho)
        self.assertIn("Fonte oficial", trecho)
        self.assertIn('rel="noopener noreferrer"', trecho)

    def test_sem_url_nao_rende_nada(self):
        self.assertEqual(link_fonte_oficial(None), "")
        self.assertEqual(link_fonte_oficial(""), "")

    def test_esquema_nao_http_nao_rende(self):
        self.assertEqual(link_fonte_oficial("javascript:alert(1)"), "")
        self.assertEqual(link_fonte_oficial("ftp://exemplo.gov.br/ato.pdf"), "")

    def test_url_e_escapada(self):
        trecho = link_fonte_oficial('https://exemplo.gov.br/a"b')
        self.assertNotIn('a"b', trecho)
        self.assertIn("&quot;", trecho)

    def test_corpus_real_rende_link_onde_ha_fonte_e_nada_onde_e_null(self):
        caminho = Path(__file__).resolve().parent.parent / "data" / "normas.json"
        with open(caminho, encoding="utf-8") as f:
            nos = json.load(f)["nodes"]
        com_link = [n for n in nos if link_fonte_oficial(n.get("fonte_oficial_url"))]
        sem_link = [n for n in nos if not link_fonte_oficial(n.get("fonte_oficial_url"))]
        self.assertEqual(len(com_link), 27)
        self.assertEqual({n["id"] for n in sem_link}, {"stj_resp", "stj_resp_plat"})


class TestAnoExibicao(unittest.TestCase):
    def test_ano_presente(self):
        self.assertEqual(ano_exibicao(2014), "2014")
        self.assertEqual(ano_exibicao("1988"), "1988")

    def test_ano_nulo_ou_vazio(self):
        self.assertEqual(ano_exibicao(None), ANO_NAO_CONFIRMADO)
        self.assertEqual(ano_exibicao(""), ANO_NAO_CONFIRMADO)

    def test_nunca_exibe_none(self):
        self.assertNotIn("None", ano_exibicao(None))

    def test_corpus_real_sem_ano_so_jurisprudencia_nao_conferida(self):
        caminho = Path(__file__).resolve().parent.parent / "data" / "normas.json"
        with open(caminho, encoding="utf-8") as f:
            nos = json.load(f)["nodes"]
        sem_ano = {n["id"] for n in nos if n.get("ano") in (None, "")}
        # ADR 008: ano de jurisprudência não é inferido sem data de julgamento
        # conferida em fonte oficial (ADI 5527 contestada; dois REsp pendentes).
        self.assertEqual(sem_ano, {"stf_adimc", "stj_resp", "stj_resp_plat"})


class TestCartaoNormaHtml(unittest.TestCase):
    MALICIOSO = {
        "id": "x",
        "tipo": "lei",
        "sigla": '<script>alert("sigla")</script>',
        "nome": "<img src=x onerror=alert(1)>",
        "ementa": "texto com <b>tag</b> & e-comercial",
        "artigos_chave": ["<i>Art. 1º</i>"],
        "fonte_oficial_url": None,
    }

    def test_campos_do_corpus_sao_escapados(self):
        h = cartao_norma_html(self.MALICIOSO)
        self.assertNotIn("<script>", h)
        self.assertNotIn("<img", h)
        self.assertNotIn("<b>", h)
        self.assertNotIn("<i>", h)
        self.assertIn("&lt;script&gt;", h)
        self.assertIn("&amp;", h)

    def test_html_estrutural_permanece(self):
        h = cartao_norma_html(self.MALICIOSO)
        for marca in ('<div class="norma-item">', '<span class="pill ',
                      "<strong>", '<div class="norma-ementa">', "</div>"):
            self.assertIn(marca, h)

    def test_pilula_por_tipo(self):
        self.assertIn("pill--lex", cartao_norma_html({"tipo": "constituicao"}))
        self.assertIn("pill--graph", cartao_norma_html({"tipo": "jurisprudencia"}))
        self.assertIn("pill--io", cartao_norma_html({"tipo": "lei"}))

    def test_campos_ausentes_nao_quebram_nem_exibem_none(self):
        h = cartao_norma_html({"tipo": "lei"})
        self.assertNotIn("None", h)

    def test_link_entra_quando_ha_fonte(self):
        no = dict(self.MALICIOSO, fonte_oficial_url="https://www.planalto.gov.br/x.htm")
        self.assertIn("Fonte oficial", cartao_norma_html(no))
        self.assertNotIn("Fonte oficial", cartao_norma_html(self.MALICIOSO))


class TestResumoComCorpusReal(unittest.TestCase):
    def test_legenda_que_a_home_exibe_hoje(self):
        caminho = Path(__file__).resolve().parent.parent / "data" / "jurisprudencia.json"
        with open(caminho, encoding="utf-8") as f:
            registros = json.load(f)["jurisprudencia"]
        self.assertEqual(
            resumo_verificacao(registros),
            "0 verificados · 3 pendentes · 1 contestado",
        )


if __name__ == "__main__":
    unittest.main()
