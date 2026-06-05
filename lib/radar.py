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
    "dados": ["proteção dados pessoais", "LGPD", "privacidade digital"],
    "menores": ["criança adolescente digital", "ECA digital", "proteção menores internet"],
    "plataformas": ["responsabilidade plataformas", "moderação conteúdo", "redes sociais"],
    "trabalho_digital": ["riscos psicossociais trabalho", "NR-1", "teletrabalho algoritmo"],
}

# ---- Senado Federal ----
def buscar_senado(termo: str, max_resultados: int = 10) -> list[dict]:
    """
    Busca PLs no Senado Federal Dados Abertos.
    Endpoint: legis.senado.leg.br/dadosabertos/materia/pesquisa/lista
    """
    url = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista"
    params = {
        "palavrasChave": termo,
        "siglaTipo": "PL,PLP,PEC,MPV",
        "qtdRegistros": max_resultados,
    }
    headers = {"Accept": "application/json"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        materias = (
            data.get("PesquisaBasicaMateria", {})
                .get("Materias", {})
                .get("Materia", [])
        )
        if isinstance(materias, dict):
            materias = [materias]

        resultados = []
        for m in materias:
            ident = m.get("IdentificacaoMateria", {})
            dados = m.get("DadosBasicosMateria", {})
            sit = (
                m.get("SituacaoAtual", {})
                 .get("Autuacoes", {})
                 .get("Autuacao", {})
            )
            if isinstance(sit, list):
                sit = sit[0] if sit else {}
            situacao = sit.get("Situacao", {}).get("DescricaoSituacao", "")

            resultados.append({
                "fonte": "Senado Federal",
                "id": str(ident.get("CodigoMateria", "")),
                "sigla": (
                    ident.get("SiglaSubtipoMateria", "") + " " +
                    str(ident.get("NumeroMateria", "")) + "/" +
                    str(ident.get("AnoMateria", ""))
                ).strip(),
                "ementa": dados.get("EmentaMateria", "")[:300],
                "ano": str(ident.get("AnoMateria", "")),
                "status": situacao or "Em tramitação",
                "url": (
                    "https://www25.senado.leg.br/web/atividade/materias/-/materia/" +
                    str(ident.get("CodigoMateria", ""))
                ),
                "termo_busca": termo,
                "data_deteccao": datetime.now().isoformat(),
            })

        return resultados

    except requests.exceptions.Timeout:
        print(f"  [Senado] Timeout para '{termo}'")
        return []
    except Exception as e:
        print(f"  [Senado] Erro para '{termo}': {e}")
        return []


# ---- Câmara dos Deputados ----
def buscar_camara(termo: str, max_resultados: int = 10) -> list[dict]:
    """
    Busca proposições na Câmara dos Deputados Dados Abertos.
    Endpoint: dadosabertos.camara.leg.br/api/v2/proposicoes
    """
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    params = {
        "keywords": termo,
        "siglaTipo": "PL,PLP,PEC,MPV",
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
                "ementa": p.get("ementa", "")[:300],
                "ano": str(p.get("ano", "")),
                "status": p.get("statusProposicao", {}).get("descricaoSituacao", "Em tramitação"),
                "url": p.get("uri", ""),
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
