"""Travas de segurança do Radar Legislativo.

O cartão do radar entra na página com unsafe_allow_html=True. Estes testes
garantem que texto vindo das APIs não vira tag ativa nem Markdown, que o link
"ver fonte" só aponta para as fontes oficiais, por https, e que o link da
proveniência só aponta para uma execução do Actions deste repositório.
"""
import html as html_mod
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest import mock

from lib.radar_cartao import html_cartao
from lib.seguranca import (normalizar_espacos, texto_markdown_seguro,
                           url_execucao_segura, url_segura)

RAIZ = Path(__file__).resolve().parent.parent

URL_SENADO = "https://www25.senado.leg.br/web/atividade/materias/-/materia/172783"
URL_CAMARA = "https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=2647780"


class _Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags: list[tuple[str, dict]] = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def _tags(html: str) -> list[tuple[str, dict]]:
    p = _Tags()
    p.feed(html)
    p.close()
    return p.tags


def _sem_tag_ativa(caso: unittest.TestCase, html: str) -> None:
    tags = _tags(html)
    caso.assertLessEqual({t for t, _ in tags}, {"div", "span", "a"})
    for tag, attrs in tags:
        for nome in attrs:
            caso.assertFalse(nome.startswith("on"), f"{tag}: atributo {nome}")


def _ler_radar() -> dict:
    return json.loads((RAIZ / "data" / "radar_legislativo.json").read_text(encoding="utf-8"))


class TestUrlSegura(unittest.TestCase):
    def test_aceita_urls_reais_do_radar(self):
        self.assertEqual(url_segura(URL_SENADO), URL_SENADO)
        self.assertEqual(url_segura(URL_CAMARA), URL_CAMARA)

    def test_aceita_dominio_exato_e_lexml(self):
        self.assertIsNotNone(url_segura("https://camara.leg.br/"))
        self.assertIsNotNone(url_segura("https://www.lexml.gov.br/urn/urn:lex:br:federal:lei:2018-08-14;13709"))

    def test_rejeita(self):
        casos = (
            "javascript:alert(1)",
            "JavaScript:alert(1)",
            "http://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=1",
            "https://camara.leg.br.evil.com/proposicoesWeb",
            "https://evil.com/?x=senado.leg.br",
            "https://evilcamara.leg.br/",
            "https://www.camara.leg.br@evil.com/",
            "https://evil.com@www.camara.leg.br/",
            "https://evil.com\\@www.camara.leg.br/",
            " https://www.camara.leg.br/",
            "https://www.camara.leg.br/\njavascript:alert(1)",
            "https://www.camara.leg.br:99999/",
            "//www.camara.leg.br/",
            "data:text/html,<script>alert(1)</script>",
            "",
            None,
            123,
        )
        for url in casos:
            with self.subTest(url=url):
                self.assertIsNone(url_segura(url))


class TestCartaoRadar(unittest.TestCase):
    def test_texto_externo_nao_vira_tag(self):
        item = {
            "sigla": "<script>alert(1)</script>",
            "fonte": "<b>Senado</b>",
            "ementa": "<img src=x onerror=alert(1)>",
            "status": "<iframe src=//evil.com>",
            "data_deteccao": "<svg onload=",
            "url": URL_SENADO,
        }
        html = html_cartao(item, no_corpus={"sigla": "<i>LGPD</i>"})
        _sem_tag_ativa(self, html)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("JÁ NO GRAFO · &lt;i&gt;LGPD&lt;/i&gt;", html)
        self.assertNotIn("<script", html)
        self.assertNotIn("<img", html)

    def test_link_fora_da_lista_nao_aparece(self):
        for url in ("javascript:alert(1)", "https://evil.com/?x=senado.leg.br", ""):
            with self.subTest(url=url):
                html = html_cartao({"sigla": "PL 1/2026", "url": url})
                self.assertNotIn("<a ", html)
                self.assertNotIn("ver fonte", html)

    def test_aspas_na_url_nao_saem_do_href(self):
        # Se a aspa fechasse o href, o parser devolveria só o trecho anterior a
        # ela e a igualdade com a URL inteira falharia; onmouseover viraria
        # atributo. Os dois asserts finais cobrem exatamente isso.
        url = URL_CAMARA + '&x="onmouseover=alert(1)'
        html = html_cartao({"sigla": "PL 1/2026", "url": url})
        self.assertIn("&quot;onmouseover", html)
        links = [a for t, a in _tags(html) if t == "a"]
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["href"], url)
        self.assertNotIn("onmouseover", links[0])

    def test_html_igual_ao_da_pagina_para_item_comum(self):
        item = {
            "sigla": "PL 2338/2023",
            "fonte": "Senado Federal",
            "ementa": "Dispõe sobre o uso da Inteligência Artificial.",
            "status": "Em tramitação",
            "data_deteccao": "2026-10-19T09:00:00",
            "url": URL_SENADO,
        }
        esperado = f"""
<div class="radar-card">
  <div class="radar-sigla">PL 2338/2023<span class="novidade-badge">NOVO</span> <a href="{URL_SENADO}" target="_blank" style="color:#1abc9c;font-size:10px;">↗ ver fonte</a></div>
  <div class="radar-fonte">Senado Federal · Detectado: 2026-10-19</div>
  <div class="radar-ementa">Dispõe sobre o uso da Inteligência Artificial.</div>
  <div class="radar-status">Status: Em tramitação</div>
</div>"""
        self.assertEqual(html_cartao(item, novidade=True), esperado)


CAMPOS_TEXTO = ("sigla", "fonte", "ementa", "status", "data_deteccao")


class TestCartaoSemFugaParaMarkdown(unittest.TestCase):
    """st.markdown encerra o bloco HTML na primeira linha em branco."""

    def test_ementa_com_linha_em_branco_fica_numa_linha(self):
        item = {
            "sigla": "PL\n\n1/2026",
            "fonte": "Senado\t\tFederal",
            "ementa": "texto\n\n[clique](https://evil.com) ![x](https://evil.com/a.png)",
            "status": " \r\n\r\n Em tramitação \n",
            "data_deteccao": "\n\n2026-10-19T09:00:00",
            "url": URL_SENADO,
        }
        html = html_cartao(item, no_corpus={"sigla": "LGPD\r\n\r\n"})
        self.assertIsNone(re.search(r"\n[ \t]*\n", html), "cartão com linha em branco")
        self.assertIn('<div class="radar-ementa">texto [clique](https://evil.com) '
                      '![x](https://evil.com/a.png)</div>', html)
        self.assertIn('<div class="radar-sigla">PL 1/2026<', html)
        self.assertIn("Senado Federal · Detectado: 2026-10-19</div>", html)
        self.assertIn("Status: Em tramitação</div>", html)
        self.assertIn("JÁ NO GRAFO · LGPD</span>", html)
        _sem_tag_ativa(self, html)
        self.assertNotIn("img", {t for t, _ in _tags(html)})

    def test_itens_reais_geram_o_mesmo_html_de_antes(self):
        radar = _ler_radar()
        itens = [(i, False) for d in radar.get("temas", {}).values()
                 for f in ("senado", "camara", "lexml") for i in d.get(f, [])]
        itens += [(n, True) for n in radar.get("novidades_detectadas", [])]
        self.assertTrue(itens, "radar sem itens")
        for item, novidade in itens:
            depois = html_cartao(item, novidade=novidade)
            # "Antes" = o mesmo cartão sem a normalização de espaços.
            with mock.patch("lib.radar_cartao.normalizar_espacos", str):
                antes = html_cartao(item, novidade=novidade)
            ja_normalizado = all(normalizar_espacos(item.get(c) or "") == str(item.get(c) or "")
                                 for c in CAMPOS_TEXTO)
            with self.subTest(id=item.get("id")):
                if ja_normalizado:
                    self.assertEqual(depois, antes)
                else:
                    # Texto real com quebra de linha: só o espaçamento muda.
                    self.assertEqual(depois.split(), antes.split())


class TestUrlExecucaoSegura(unittest.TestCase):
    VALIDA = "https://github.com/marcabru-tech/lex-io-graph/actions/runs/39302278851"

    def test_aceita_formato_exato(self):
        self.assertEqual(url_execucao_segura(self.VALIDA), self.VALIDA)

    def test_aceita_a_do_snapshot_atual(self):
        url = (_ler_radar().get("proveniencia") or {}).get("execucao_url")
        if url is None:
            self.skipTest("snapshot sem execucao_url")
        self.assertEqual(url_execucao_segura(url), url)

    def test_rejeita(self):
        casos = (
            "https://github.com/outro-dono/lex-io-graph/actions/runs/1",
            "https://github.com/marcabru-tech/outro-repo/actions/runs/1",
            "javascript:alert(1)",
            "https://github.com.evil.com/marcabru-tech/lex-io-graph/actions/runs/1",
            "https://evil.com/https://github.com/marcabru-tech/lex-io-graph/actions/runs/1",
            self.VALIDA + "?x=1",
            self.VALIDA + "#x",
            self.VALIDA + "/jobs/2",
            self.VALIDA + "\n",
            "http://github.com/marcabru-tech/lex-io-graph/actions/runs/1",
            "https://github.com/marcabru-tech/lex-io-graph/actions/runs/",
            "https://github.com/marcabru-tech/lex-io-graph/actions/runs/\u0661\u0662",
            "https://user@github.com/marcabru-tech/lex-io-graph/actions/runs/1",
            "",
            None,
            1,
        )
        for url in casos:
            with self.subTest(url=url):
                self.assertIsNone(url_execucao_segura(url))


def _como_exibido(md: str) -> str:
    """O que o Markdown mostra: sem as barras de escape e com entidades decodificadas."""
    return html_mod.unescape(re.sub(r"\\([!-/:-@\[-`{-~])", r"\1", md))


class TestTextoMarkdownSeguro(unittest.TestCase):
    def test_link_e_tag_viram_texto(self):
        t = texto_markdown_seguro("[link](https://evil.com) <b>x</b>")
        self.assertEqual(t, r"\[link\]\(https://evil\.com\) &lt;b&gt;x&lt;/b&gt;")
        self.assertIsNone(re.search(r"(?<!\\)[\[\]()<>]", t))
        self.assertEqual(_como_exibido(t), "[link](https://evil.com) <b>x</b>")

    def test_todos_os_especiais_sao_escapados(self):
        especiais = "\\`*_{}[]()#+-.!|~$"
        self.assertEqual(texto_markdown_seguro(especiais), "".join("\\" + c for c in especiais))

    def test_espacos_normalizados(self):
        self.assertEqual(texto_markdown_seguro("  dados\n\n\tpessoais  "), "dados pessoais")

    def test_aspa_simples_nao_vira_entidade(self):
        self.assertEqual(texto_markdown_seguro("d'água"), "d'água")

    def test_termos_reais_aparecem_iguais(self):
        termos = [t for d in _ler_radar().get("temas", {}).values()
                  for t in d.get("termos_monitorados", [])]
        self.assertTrue(termos)
        for termo in termos:
            with self.subTest(termo=termo):
                self.assertEqual(_como_exibido(texto_markdown_seguro(termo)), normalizar_espacos(termo))


if __name__ == "__main__":
    unittest.main()
