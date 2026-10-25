"""Travas de segurança do Radar Legislativo.

O cartão, os termos monitorados e a legenda de proveniência entram na página
como blocos HTML com unsafe_allow_html=True. Estes testes garantem que texto
vindo das APIs não vira tag ativa nem Markdown (nem autolink do GFM), que o
link "ver fonte" só aponta para as fontes oficiais, por https, e que o link da
proveniência só aponta para uma execução do Actions deste repositório.
"""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest import mock

from lib.radar_cartao import html_cartao, html_proveniencia, html_termos_monitorados
from lib.seguranca import normalizar_espacos, url_execucao_segura, url_segura

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
  <div class="radar-sigla">PL 2338/2023<span class="novidade-badge">NOVO</span> <a href="{URL_SENADO}" target="_blank" rel="noopener noreferrer" style="color:#1abc9c;font-size:10px;">↗ ver fonte</a></div>
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


class _Texto(HTMLParser):
    def __init__(self):
        super().__init__()
        self.partes: list[str] = []

    def handle_data(self, data):
        self.partes.append(data)


def _texto_exibido(html: str) -> str:
    p = _Texto()
    p.feed(html)
    p.close()
    return "".join(p.partes)


# Endereços que o autolink do GFM transformaria em link se o texto fosse
# Markdown; num bloco HTML ficam inertes. Mais a tentativa de fechar o bloco.
HOSTIS = (
    "www.attacker.example/path",
    "contato@attacker.example",
    "https://attacker.example/path",
    "[x](https://attacker.example) <a href=https://attacker.example>y</a>",
    "fim\n\n<img src=x onerror=alert(1)>",
)


class _BlocoHtmlInerte:
    """Requisitos comuns aos blocos que saem do Markdown para HTML."""

    def assertBlocoInerte(self, html: str, links_esperados: list[str]):
        self.assertTrue(html.startswith("<div"), "bloco HTML precisa começar com <div>")
        self.assertNotIn("\n", html)
        tags = _tags(html)
        self.assertLessEqual({t for t, _ in tags}, {"div", "strong", "a"})
        self.assertEqual([a.get("href") for t, a in tags if t == "a"], links_esperados)
        for tag, attrs in tags:
            for nome in attrs:
                self.assertFalse(nome.startswith("on"), f"{tag}: atributo {nome}")


class TestTermosMonitorados(_BlocoHtmlInerte, unittest.TestCase):
    def test_termos_hostis_ficam_texto(self):
        html = html_termos_monitorados(list(HOSTIS))
        self.assertBlocoInerte(html, [])
        exibido = _texto_exibido(html)
        for termo in HOSTIS:
            self.assertIn(normalizar_espacos(termo), exibido)
        self.assertNotIn("\\", exibido)

    def test_rotulo_em_negrito(self):
        self.assertEqual(html_termos_monitorados(["dados pessoais", "LGPD"]),
                         "<div><strong>Termos monitorados:</strong> dados pessoais, LGPD</div>")

    def test_aspas_nao_viram_entidade(self):
        self.assertIn("d'água \"x\"", html_termos_monitorados(["d'água \"x\""]))

    def test_termos_reais_aparecem_iguais(self):
        termos = [t for d in _ler_radar().get("temas", {}).values()
                  for t in d.get("termos_monitorados", [])]
        self.assertTrue(termos)
        html = html_termos_monitorados(termos)
        self.assertBlocoInerte(html, [])
        self.assertEqual(_texto_exibido(html),
                         "Termos monitorados: " + ", ".join(normalizar_espacos(t) for t in termos))


class TestProveniencia(_BlocoHtmlInerte, unittest.TestCase):
    VALIDA = TestUrlExecucaoSegura.VALIDA

    def test_executor_e_hash_hostis_ficam_texto(self):
        for hostil in HOSTIS:
            with self.subTest(hostil=hostil):
                html = html_proveniencia(hostil, self.VALIDA, hostil)
                self.assertBlocoInerte(html, [self.VALIDA])
                self.assertIn(normalizar_espacos(hostil), _texto_exibido(html))

    def test_url_de_execucao_invalida_nao_vira_link(self):
        for url in HOSTIS + ("javascript:alert(1)", None):
            with self.subTest(url=url):
                html = html_proveniencia("github-actions", url, "288f6bf724d75bc6")
                self.assertBlocoInerte(html, [])
                self.assertNotIn("ver execução", html)

    def test_texto_igual_a_legenda_anterior(self):
        html = html_proveniencia("github-actions", self.VALIDA, "288f6bf724d75bc626f4")
        self.assertBlocoInerte(html, [self.VALIDA])
        self.assertEqual(_texto_exibido(html), "Proveniência do snapshot: coletado por github-actions "
                                               "(ver execução) · sha256 288f6bf724d7…")

    def test_sem_url_e_sem_hash(self):
        html = html_proveniencia("local", None, None)
        self.assertBlocoInerte(html, [])
        self.assertEqual(_texto_exibido(html), "Proveniência do snapshot: coletado por local")


if __name__ == "__main__":
    unittest.main()
