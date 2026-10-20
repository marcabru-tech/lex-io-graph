"""
Validação de dados externos antes de entrarem em HTML.

O radar grava em data/radar_legislativo.json texto vindo das APIs do Senado,
da Câmara e do LexML. A página do radar insere esse texto em HTML com
unsafe_allow_html=True; por isso o texto é escapado e o link só é exibido se
apontar para uma das fontes oficiais.
"""

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
