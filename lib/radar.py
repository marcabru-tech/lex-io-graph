"""
lib/radar.py — Radar Legislativo do Lex-IO-Graph.

Consulta APIs públicas brasileiras e retorna dados normalizados.
Não escreve arquivos — apenas coleta e normaliza.

Fontes:
  - Senado Federal Dados Abertos (legis.senado.leg.br)
  - Câmara dos Deputados Dados Abertos (dadosabertos.camara.leg.br)
  - LexML (lexml.gov.br) — output Atom/XML

Arquitetura: este módulo é chamado pelo updater.py (GitHub Action)
e pela página 8_Radar_Legislativo.py (exibição no app).
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

TIMEOUT = 30

# ---- Temas monitorados ----
TEMAS_RADAR = {
    "ia": ["inteligência artificial", "IA generativa", "algoritmo decisão"],
    "dados": ["dados pessoais", "LGPD", "privacidade"],
    "menores": ["criança adolescente digital", "ECA digital", "proteção menores internet"],
    "plataformas": ["plataformas digitais", "redes sociais", "moderação de conteúdo"],
    "trabalho_digital": ["trabalho por aplicativo", "plataformas de trabalho", "riscos psicossociais"],
    "infraestrutura_digital": ["datacenter", "computação em nuvem"],
    "mercados_digitais": ["mercados digitais", "concorrência digital"],
    "minerais_criticos": ["minerais críticos", "terras raras"],
    "soberania_digital": ["soberania digital", "soberania tecnológica"],
    # Acordos submetidos ao Congresso costumam chegar como PDL com a ementa
    # "Aprova o texto do Acordo..."; a promulgacao (decreto) sai no DOU e nao
    # e coberta por Senado/Camara.
    "acordos_internacionais": ["aprova o texto do acordo", "Mercosul"],
}

# ---- Senado Federal ----
# Desde a modernizacao do portal de dados abertos (2025), o endpoint
# materia/pesquisa/lista ignora palavrasChave e qtdRegistros e devolve a lista
# de materias do ano em formato plano (Codigo, Sigla, Numero, Ano, Ementa,
# Autor, Data). Por isso: uma unica requisicao por execucao (cache) e filtro
# por palavra-chave feito aqui, sobre a ementa. Verificado em 01/10/2026.
SIGLAS_SENADO = {"PL", "PLP", "PEC", "MPV", "PDL"}
_SENADO_CACHE: Optional[list] = None
_STOP = {"de", "da", "do", "das", "dos", "e", "a", "o", "em", "na", "no", "para"}


def _normalizar(txt: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", txt or "").encode("ascii", "ignore").decode()
    return t.lower()


def _casa_termo(termo: str, ementa: str) -> bool:
    """Todas as palavras significativas do termo aparecem na ementa."""
    import re
    e = _normalizar(ementa)
    palavras = [w for w in re.split(r"\s+", _normalizar(termo)) if w and w not in _STOP]
    # palavra inteira (evita "nr" casar com "inr..." e "1" com qualquer numero)
    return bool(palavras) and all(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", e)
                                  for w in palavras)


def _lista_senado() -> list:
    global _SENADO_CACHE
    if _SENADO_CACHE is not None:
        return _SENADO_CACHE
    url = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista"
    resp = requests.get(url, params={"palavrasChave": "lei"},
                        headers={"Accept": "application/json"}, timeout=TIMEOUT)
    resp.raise_for_status()
    materias = (resp.json().get("PesquisaBasicaMateria", {})
                .get("Materias", {}).get("Materia", []))
    if isinstance(materias, dict):
        materias = [materias]
    _SENADO_CACHE = materias
    return materias


def buscar_senado(termo: str, max_resultados: int = 10) -> list[dict]:
    """
    Busca proposicoes no Senado Federal Dados Abertos (filtro local por termo).
    Endpoint: legis.senado.leg.br/dadosabertos/materia/pesquisa/lista
    """
    try:
        materias = _lista_senado()
    except requests.exceptions.Timeout:
        print(f"  [Senado] Timeout para '{termo}'")
        return []
    except Exception as e:
        print(f"  [Senado] Erro para '{termo}': {e}")
        return []

    resultados = []
    for m in materias:
        codigo = str(m.get("Codigo") or "").strip()
        sigla = (m.get("Sigla") or "").strip()
        # Item sem codigo nao e materia; tipo fora da lista nao interessa ao radar.
        if not codigo or sigla not in SIGLAS_SENADO:
            continue
        ementa = m.get("Ementa") or ""
        if not _casa_termo(termo, ementa):
            continue
        numero = str(m.get("Numero") or "").lstrip("0") or "0"
        ano = str(m.get("Ano") or "")
        resultados.append({
            "fonte": "Senado Federal",
            "id": codigo,
            "sigla": m.get("DescricaoIdentificacao") or f"{sigla} {numero}/{ano}",
            "ementa": ementa,
            "ano": ano,
            "status": f"Apresentada em {m['Data']}" if m.get("Data") else "Em tramitação",
            "autor": m.get("Autor", ""),
            "url": "https://www25.senado.leg.br/web/atividade/materias/-/materia/" + codigo,
            "termo_busca": termo,
            "data_deteccao": datetime.now().isoformat(),
        })
        if len(resultados) >= max_resultados:
            break
    return resultados


# ---- Câmara dos Deputados ----
def buscar_camara(termo: str, max_resultados: int = 10) -> list[dict]:
    """
    Busca proposições na Câmara dos Deputados Dados Abertos.
    Endpoint: dadosabertos.camara.leg.br/api/v2/proposicoes
    """
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    params = {
        "keywords": termo,
        "siglaTipo": "PL,PLP,PEC,MPV,PDL",
        "itens": max_resultados,
        "ordem": "DESC",
        "ordenarPor": "id",
    }
    headers = {"Accept": "application/json"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        proposicoes = data.get("dados", [])
        resultados = []

        for p in proposicoes:
            resultados.append({
                "fonte": "Câmara dos Deputados",
                "id": str(p.get("id", "")),
                "sigla": (
                    p.get("siglaTipo", "") + " " +
                    str(p.get("numero", "")) + "/" +
                    str(p.get("ano", ""))
                ).strip(),
                "ementa": p.get("ementa", ""),
                "ano": str(p.get("ano", "")),
                "status": p.get("statusProposicao", {}).get("descricaoSituacao", "Em tramitação"),
                "url": "https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=" + str(p.get("id", "")),
                "termo_busca": termo,
                "data_deteccao": datetime.now().isoformat(),
            })

        return resultados

    except requests.exceptions.Timeout:
        print(f"  [Câmara] Timeout para '{termo}'")
        return []
    except Exception as e:
        print(f"  [Câmara] Erro para '{termo}': {e}")
        return []


# ---- LexML ----
def buscar_lexml(termo: str, max_resultados: int = 10) -> list[dict]:
    """
    Busca normas no LexML.
    Endpoint: lexml.gov.br/busca/search — output Atom XML
    Namespace Atom: http://www.w3.org/2005/Atom
    """
    # DESATIVADO (ago/2026): o LexML passou a exigir verificacao anti-bot
    # com JavaScript. Responde 200 com pagina de intersticio em HTML, nao
    # com Atom XML. Sem caminho de acesso oficial, Senado e Camara cobrem
    # o radar. Reativar quando houver API documentada ou chave de acesso.
    return []
    url = "https://www.lexml.gov.br/busca/search"
    params = {
        "q": termo,
        "start": 1,
        "rows": max_resultados,
    }

    try:
        resp = requests.get(url, params=params, timeout=TIMEOUT)
        resp.raise_for_status()

        # Parse Atom XML
        NS = {
            "atom": "http://www.w3.org/2005/Atom",
            "lexml": "http://www.lexml.gov.br/oai/oaidc",
        }

        root = ET.fromstring(resp.content)
        entries = root.findall("atom:entry", NS)

        resultados = []
        for entry in entries[:max_resultados]:
            titulo = entry.findtext("atom:title", namespaces=NS) or ""
            link_el = entry.find("atom:link[@rel='alternate']", NS)
            link = link_el.get("href", "") if link_el is not None else ""
            summary = entry.findtext("atom:summary", namespaces=NS) or ""

            resultados.append({
                "fonte": "LexML",
                "id": link,
                "sigla": titulo[:100],
                "ementa": summary[:300],
                "ano": "",
                "status": "Vigente",
                "url": link,
                "termo_busca": termo,
                "data_deteccao": datetime.now().isoformat(),
            })

        return resultados

    except ET.ParseError as e:
        print(f"  [LexML] Parse XML erro para '{termo}': {e}")
        return []
    except requests.exceptions.Timeout:
        print(f"  [LexML] Timeout para '{termo}'")
        return []
    except Exception as e:
        print(f"  [LexML] Erro para '{termo}': {e}")
        return []


# ---- Radar completo ----
def coletar_radar(
    temas: Optional[list[str]] = None,
    max_por_fonte: int = 5
) -> dict:
    """
    Coleta dados de todas as fontes para os temas selecionados.
    Retorna dict normalizado pronto para salvar como radar_legislativo.json.
    """
    if temas is None:
        temas = list(TEMAS_RADAR.keys())

    resultados = {
        "ultima_atualizacao": datetime.now().isoformat(),
        "temas": {},
    }

    for tema in temas:
        if tema not in TEMAS_RADAR:
            continue

        termos = TEMAS_RADAR[tema]
        resultados["temas"][tema] = {
            "termos_monitorados": termos,
            "senado": [],
            "camara": [],
            "lexml": [],
        }

        for termo in termos[:2]:  # Máximo 2 termos por tema para evitar rate limit
            print(f"  [{tema}] Senado: '{termo}'")
            resultados["temas"][tema]["senado"] += buscar_senado(termo, max_por_fonte)

            print(f"  [{tema}] Câmara: '{termo}'")
            resultados["temas"][tema]["camara"] += buscar_camara(termo, max_por_fonte)

            print(f"  [{tema}] LexML: '{termo}'")
            resultados["temas"][tema]["lexml"] += buscar_lexml(termo, max_por_fonte)

        # Deduplicar por ID dentro de cada fonte
        for fonte in ["senado", "camara", "lexml"]:
            vistos = set()
            dedup = []
            for item in resultados["temas"][tema][fonte]:
                if item["id"] not in vistos:
                    vistos.add(item["id"])
                    dedup.append(item)
            resultados["temas"][tema][fonte] = dedup

    return resultados
