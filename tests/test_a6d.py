"""A6-d: escape no Grafo, risco "referência", regex de proposição e chave desconhecida no relatório."""
import json
import re
import unittest
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from unittest import mock

import lib.conformidade as conf
from lib.grafo_cartao import html_cartao_norma
from lib.taxonomia import chave_proposicao

RAIZ = Path(__file__).resolve().parent.parent
MALICIOSO = '<script>alert(1)</script><img src=x onerror=alert(1)>'


class _Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, [n for n, _ in attrs]))


def _tags(html):
    p = _Tags()
    p.feed(html)
    return p.tags


class TestCartaoGrafo(unittest.TestCase):
    def test_texto_dos_dados_e_escapado(self):
        nd = {"label": MALICIOSO, "tipo_label": MALICIOSO, "status": MALICIOSO, "ementa": MALICIOSO}
        html = html_cartao_norma(MALICIOSO, nd, 3, True)
        self.assertNotIn("<script", html)
        self.assertNotIn("<img", html)
        self.assertLessEqual({t for t, _ in _tags(html)}, {"div", "span", "br"})
        self.assertFalse(any(a.startswith("on") for _, attrs in _tags(html) for a in attrs))
        self.assertIn("&lt;script&gt;", html)

    def test_normas_reais_exibem_o_mesmo_texto(self):
        for nd in json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]:
            html = html_cartao_norma(nd["id"], nd, 0, False)
            texto = unescape(re.sub(r"<[^>]+>", "", html))
            with self.subTest(id=nd["id"]):
                self.assertIn(nd.get("label", nd["id"]), texto)
                self.assertIn(nd.get("ementa", ""), texto)


class TestRiscoReferencia(unittest.TestCase):
    NORMAS = [
        {"id": "lei_a", "tipo": "lei", "status": "vigente"},
        {"id": "lei_b", "tipo": "lei", "status": "vigente"},
        {"id": "tratado", "tipo": "tratado", "status": "instrumento_externo"},
        {"id": "estranho", "tipo": "lei", "status": "status_inventado"},
        {"id": "etica", "tipo": "documento", "status": "referencia_etica"},
        {"id": "stf", "tipo": "jurisprudencia", "status": "em_conferencia"},
        {"id": "pl", "tipo": "pl", "status": "tramitacao"},
    ]

    def _radar(self, arestas):
        with mock.patch.object(conf, "_score_norma", return_value=0.5), \
             mock.patch.object(conf, "_tags_norma", return_value=set()):
            return conf.gerar_radar({}, self.NORMAS, arestas)

    def _risco(self, a, b, tipo="antinomia"):
        return self._radar([{"source": a, "target": b, "tipo": tipo}])["arestas"][0]["risco"]

    def test_antinomia_com_externo_ou_desconhecido_vira_referencia(self):
        for outro in ("tratado", "estranho", "etica"):
            for tipo in ("antinomia", "intersecao", "complementaridade"):
                self.assertEqual(self._risco("lei_a", outro, tipo), "referencia", (outro, tipo))
                self.assertEqual(self._risco(outro, "lei_a", tipo), "referencia", (outro, tipo))

    def test_vigentes_seguem_a_regra_anterior(self):
        self.assertEqual(self._risco("lei_a", "lei_b", "antinomia"), "alto")
        self.assertEqual(self._risco("lei_a", "lei_b", "intersecao"), "medio")
        self.assertEqual(self._risco("lei_a", "lei_b", "complementaridade"), "baixo")
        self.assertEqual(self._risco("lei_a", "pl"), "prospectivo")

    def test_em_conferencia_prevalece(self):
        self.assertEqual(self._risco("stf", "tratado"), "em_conferencia")

    def test_referencia_fora_da_priorizacao(self):
        r = self._radar([{"source": "lei_a", "target": "tratado", "tipo": "antinomia"},
                         {"source": "lei_a", "target": "lei_b", "tipo": "complementaridade"}])
        self.assertEqual([a["risco"] for a in r["arestas"]], ["baixo", "referencia"])
        vigentes = [a["risco"] for a in r["arestas"] if a["risco"] in ("alto", "medio", "baixo")]
        self.assertEqual(vigentes[0], "baixo")  # "Maior interseção entre vigentes" ignora a referência
        self.assertIn("referencia", conf.RISCO_ROTULO)
        self.assertIn("referencia", conf.RISCO_ICO)


class TestRelatorioChaveDesconhecida(unittest.TestCase):
    def test_chave_fora_do_questionario_nao_quebra(self):
        perfil = {"setor": conf.PERGUNTAS["setor"]["opcoes"][0], "<b>extra</b>": "valor"}
        radar = conf.gerar_radar(perfil, json.loads((RAIZ / "data" / "normas.json").read_text(
            encoding="utf-8"))["nodes"], [])
        html = conf.gerar_relatorio_html(radar, perfil)
        self.assertIn("&lt;b&gt;extra&lt;/b&gt;", html)
        self.assertIn(conf.PERGUNTAS["setor"]["label"], html)


class TestRegexProposicao(unittest.TestCase):
    def test_casos(self):
        casos = {
            "PL 2338/2023": ["PL 2338/2023"],
            "PL nº 2.338/2023": ["PL 2338/2023"],
            "MP 1.317/2025, de": ["MPV 1317/2025"],
            "Ver PL 2338/2023.": ["PL 2338/2023"],
            "PL ./2024": [],
            "PL 2338/2023abc": [],
            "PLP 74/2026 e PL 278/2026": ["PLP 74/2026", "PL 278/2026"],
        }
        for texto, esperado in casos.items():
            self.assertEqual(chave_proposicao(texto, pivo=26), esperado, texto)


if __name__ == "__main__":
    unittest.main()
