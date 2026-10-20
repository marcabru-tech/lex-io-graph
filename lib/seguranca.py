"""
Validação de dados externos antes de entrarem em HTML.

O radar grava em data/radar_legislativo.json texto vindo das APIs do Senado,
da Câmara e do LexML. A página do radar insere esse texto em HTML com
unsafe_allow_html=True; por isso o texto é escapado e o link só é exibido se
apontar para uma das fontes oficiais.

Dado externo não é exibido via Markdown: escapar a sintaxe com barra
invertida não desliga o autolink do GFM (www.x.com, a@x.com) e deixa a barra
visível. Os blocos são montados em HTML por lib/radar_cartao.py.
"""

import re
from urllib.parse import urlsplit

# Domínios das fontes do radar (lib/radar.py). Aceita o domínio exato e
# qualquer subdomínio: www25.senado.leg.br, www.camara.leg.br, www.lexml.gov.br.
DOMINIOS_PERMITIDOS = ("senado.leg.br", "camara.leg.br", "lexml.gov.br")

_CARACTERES_HOST = set("abcdefghijklmnopqrstuvwxyz0123456789.-")


def _host_permitido(host: str) -> bool:
    return any(host == d or host.endswith("." + d) for d in DOMINIOS_PERMITIDOS)


def url_segura(url) -> str | None:
    """Devolve a URL se for https para uma fonte oficial; senão, None.

    Recusa também o que o navegador e o urllib interpretam de forma diferente:
    barra invertida, espaço e caracteres de controle, credenciais antes do
    host (https://x@host) e host com caracteres fora de [a-z0-9.-].
    """
    if not isinstance(url, str) or not url:
        return None
    if "\\" in url or any(ord(c) <= 32 or ord(c) == 127 for c in url):
        return None
    try:
        partes = urlsplit(url)
        partes.port  # porta inválida levanta ValueError
    except ValueError:
        return None
    if partes.scheme != "https":
        return None
    if partes.username is not None or partes.password is not None:
        return None
    host = partes.hostname or ""
    if not host or not set(host) <= _CARACTERES_HOST:
        return None
    if not _host_permitido(host):
        return None
    return url


# Execução do workflow que gravou o snapshot (updater.montar_proveniencia).
# [0-9] e não \d: em str, \d aceita dígitos de qualquer escrita Unicode.
# fullmatch e não $: $ aceita uma quebra de linha no fim.
_EXECUCAO = re.compile(r"https://github\.com/marcabru-tech/lex-io-graph/actions/runs/[0-9]+")


def url_execucao_segura(url) -> str | None:
    """Devolve a URL se for exatamente uma execução do Actions deste repositório."""
    if not isinstance(url, str) or not _EXECUCAO.fullmatch(url):
        return None
    try:
        partes = urlsplit(url)
    except ValueError:
        return None
    if (partes.scheme, partes.netloc) != ("https", "github.com") or partes.query or partes.fragment:
        return None
    return url


# Sequências de espaço, tabulação e quebra de linha. Não inclui o espaço não
# separável (U+00A0): ele não forma linha em branco no Markdown e, em HTML,
# não é colapsado, então trocá-lo mudaria o visual.
_ESPACOS = re.compile(r"[ \t\n\r\f\v]+")


def normalizar_espacos(texto) -> str:
    """Uma linha só: impede a linha em branco que encerra um bloco HTML no Markdown."""
    return _ESPACOS.sub(" ", str(texto)).strip(" ")
