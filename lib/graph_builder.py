"""
Construtor de grafos para o Lexiograph Compliance Map.

Gera o grafo NetworkX a partir dos dados JSON e fornece
funções de análise, filtragem e exportação.
"""

import json
from pathlib import Path
from typing import Optional

import networkx as nx

from lib.constants import (
    EDGE_COLORS,
    EDGE_TYPE_LABELS,
    NODE_COLORS,
    NODE_TYPE_LABELS,
)

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(filename: str) -> dict:
    """Carrega arquivo JSON do diretório data/."""
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def build_compliance_graph(
    themes: Optional[list[str]] = None,
    norm_types: Optional[list[str]] = None,
) -> nx.DiGraph:
    """
    Constrói o grafo de compliance a partir dos dados JSON.

    Args:
        themes: lista de temas para filtrar (ex: ["dados_pessoais", "menores"]).
                Se None, inclui todos.
        norm_types: lista de tipos de nó para filtrar (ex: ["lei", "constituicao"]).
                    Se None, inclui todos.

    Returns:
        nx.DiGraph com nós e arestas filtrados.
    """
    raw_nodes = load_json("normas.json")["nodes"]
    raw_edges = load_json("arestas.json")["edges"]

    # Filtrar nós por tema e tipo
    filtered_nodes = []
    for node in raw_nodes:
        if themes and not any(t in node.get("temas", []) for t in themes):
            continue
        if norm_types and node.get("tipo") not in norm_types:
            continue
        filtered_nodes.append(node)

    node_ids = {n["id"] for n in filtered_nodes}

    # Filtrar arestas: ambas pontas devem estar nos nós filtrados
    filtered_edges = [
        e for e in raw_edges
        if e["source"] in node_ids and e["target"] in node_ids
    ]

    # Construir grafo
    G = nx.DiGraph()

    for node in filtered_nodes:
        G.add_node(
            node["id"],
            label=node["sigla"],
            nome=node["nome"],
            tipo=node["tipo"],
            tipo_label=NODE_TYPE_LABELS.get(node["tipo"], node["tipo"]),
            ementa=node.get("ementa", ""),
            status=node.get("status", ""),
            artigos_chave=node.get("artigos_chave", []),
            temas=node.get("temas", []),
            orgao=node.get("orgao", ""),
            ano=node.get("ano", ""),
            color=NODE_COLORS.get(node["tipo"], "#888888"),
        )

    for edge in filtered_edges:
        G.add_edge(
            edge["source"],
            edge["target"],
            tipo=edge["tipo"],
            tipo_label=EDGE_TYPE_LABELS.get(edge["tipo"], edge["tipo"]),
            descricao=edge.get("descricao", ""),
            artigos=edge.get("artigos", ""),
            color=EDGE_COLORS.get(edge["tipo"], "#888888"),
        )

    return G


def get_node_centrality(G: nx.DiGraph) -> dict:
    """Retorna betweenness centrality de cada nó."""
    return nx.betweenness_centrality(G)


def get_intersections(G: nx.DiGraph, node_id: str) -> list[dict]:
    """Retorna todas as interseções (arestas) de um nó específico."""
    intersections = []
    for source, target, data in G.edges(data=True):
        if source == node_id or target == node_id:
            other = target if source == node_id else source
            intersections.append({
                "outro_no": G.nodes[other].get("label", other),
                "outro_nome": G.nodes[other].get("nome", other),
                "tipo_relacao": data.get("tipo_label", ""),
                "descricao": data.get("descricao", ""),
                "artigos": data.get("artigos", ""),
            })
    return intersections


def build_compliance_matrix() -> list[dict]:
    """
    Constrói a matriz de compliance: empresas × normas.
    Retorna lista de dicts para renderização em tabela.
    """
    from lib.constants import EMPRESAS_MODELO

    raw_nodes = load_json("normas.json")["nodes"]
    leis = [n for n in raw_nodes if n["tipo"] in ("lei", "constituicao", "norma_regulamentar")]

    matrix = []
    for empresa in EMPRESAS_MODELO:
        row = {"empresa": empresa["nome"], "setor": empresa["setor"], "risco": empresa["risco_base"]}
        for lei in leis:
            # Lógica simplificada de risco baseada em temas
            empresa_temas = _temas_por_setor(empresa["setor"])
            intersecao = set(empresa_temas) & set(lei.get("temas", []))
            if len(intersecao) >= 2:
                row[lei["sigla"]] = "alto"
            elif len(intersecao) == 1:
                row[lei["sigla"]] = "medio"
            elif lei["tipo"] == "constituicao":
                row[lei["sigla"]] = "aplicavel"
            else:
                row[lei["sigla"]] = "baixo"
        matrix.append(row)

    return matrix


def _temas_por_setor(setor: str) -> list[str]:
    """Mapeia setor da empresa para temas regulatórios aplicáveis."""
    mapa = {
        "Tecnologia": ["dados_pessoais", "internet", "ia", "trabalho"],
        "Serviços de TI": ["dados_pessoais", "internet", "ia", "trabalho"],
        "Educação": ["dados_pessoais", "menores", "internet", "ia"],
        "Financeiro": ["dados_pessoais", "internet", "ia", "trabalho"],
        "Marketing": ["dados_pessoais", "internet"],
    }
    return mapa.get(setor, ["dados_pessoais"])


def export_graph_json(G: nx.DiGraph) -> str:
    """Exporta o grafo como JSON serializável."""
    data = {
        "nodes": [
            {
                "id": n,
                **{k: v for k, v in G.nodes[n].items()}
            }
            for n in G.nodes
        ],
        "edges": [
            {
                "source": u,
                "target": v,
                **{k: v for k, v in G.edges[u, v].items()}
            }
            for u, v in G.edges
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)
