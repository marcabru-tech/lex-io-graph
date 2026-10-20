"""Travas de segurança do Radar Legislativo.

O cartão do radar entra na página com unsafe_allow_html=True. Estes testes
garantem que texto vindo das APIs não vira tag ativa e que o link "ver fonte"
só aponta para as fontes oficiais, por https.
"""
import unittest
from html.parser import HTMLParser

from lib.radar_cartao import html_cartao
from lib.seguranca import url_segura

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
        tags = _tags(html)
        self.assertLessEqual({t for t, _ in tags}, {"div", "span", "a"})
        for tag, attrs in tags:
            for nome in attrs:
                self.assertFalse(nome.startswith("on"), f"{tag}: atributo {nome}")
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
        url = URL_CAMARA + '&x="onmouseover=alert(1)'
        html = html_cartao({"sigla": "PL 1/2026", "url": url})
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


if __name__ == "__main__":
    unittest.main()
