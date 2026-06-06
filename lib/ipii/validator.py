# Copyright © 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado
# IPII (Interação Paramétrica Iterativa por Interoperabilidade) para Lex-IO-Graph / Lexiograph
# Todos os direitos reservados.
# Uso comercial, reprodução ou distribuição sem autorização escrita
# da Hubstry Deep Tech é expressamente proibido.
# Contato: globaldeeptechecosystem@hubstry.dev
# hubstry.dev/lex-io-graph
"""
Componente 3 — Validação contra arestas existentes.

Compara arestas sugeridas pelo engine IPII com arestas já existentes
no grafo. Mede precisão e cobertura. Identifica arestas novas
(descobertas) e arestas não detectadas (gap do engine).

Princípio de curadoria: o engine alerta, o curador decide.
Nenhuma aresta é adicionada automaticamente ao grafo.

Propriedade intelectual: Hubstry Deep Tech © 2026.
"""


def _par(source: str, target: str) -> tuple:
    """Par canônico ordenado alfabeticamente."""
    return tuple(sorted([source, target]))


def validar_arestas(sugeridas: list, existentes: list) -> dict:
    """
    Compara arestas sugeridas vs existentes.

    Returns:
        dict com métricas de precisão/cobertura e listas detalhadas.
    """

    # Indexar existentes por par canônico
    existentes_idx = {}
    for e in existentes:
        p = _par(e["source"], e["target"])
        existentes_idx[p] = e

    existentes_set = set(existentes_idx.keys())

    confirmadas = []
    novas = []

    for s in sugeridas:
        p = _par(s["source"], s["target"])
        if p in existentes_set:
            aresta_ex = existentes_idx[p]
            s_enriq = {
                **s,
                "tipo_existente": aresta_ex["tipo"],
                "match_tipo": s["tipo_sugerido"] == aresta_ex["tipo"],
            }
            confirmadas.append(s_enriq)
        else:
            novas.append(s)

    # Arestas existentes que o engine não detectou
    sugeridas_set = set(
        _par(s["source"], s["target"]) for s in sugeridas
    )
    faltando = [
        e for e in existentes
        if _par(e["source"], e["target"]) not in sugeridas_set
    ]

    total_sug = len(sugeridas)
    total_ex = len(existentes)

    return {
        "total_sugeridas": total_sug,
        "total_existentes": total_ex,
        "confirmadas": len(confirmadas),
        "novas": len(novas),
        "faltando": len(faltando),
        "precisao": round(len(confirmadas) / total_sug, 3) if total_sug else 0,
        "cobertura": round(len(confirmadas) / total_ex, 3) if total_ex else 0,
        "detalhe_confirmadas": confirmadas,
        "detalhe_novas": novas,
        "detalhe_faltando": faltando,
        "gap_engine": [
            {
                "par": f"{e['source']} ↔ {e['target']}",
                "tipo": e["tipo"],
                "descricao": e.get("descricao", "")[:120],
            }
            for e in faltando
        ],
    }


def filtrar_por_tier(novas: list, tier_max: int = 3) -> list:
    """Filtra novas arestas por tier (1 = mais forte)."""
    return [n for n in novas if n.get("tier", 5) <= tier_max]


def formatar_para_grafo(aresta_sugerida: dict, curador: str = "") -> dict:
    """
    Formata aresta sugerida para inserção no arestas.json.
    Chamado APENAS após aprovação manual do curador.
    """
    return {
        "source": aresta_sugerida["source"],
        "target": aresta_sugerida["target"],
        "tipo": aresta_sugerida["tipo_sugerido"],
        "descricao": (
            f"[IPII Engine — score {aresta_sugerida['score']} — "
            f"aprovado por {curador or 'curador'}] "
            f"Temas comuns: {', '.join(aresta_sugerida['temas_comuns'])}."
        ),
        "artigos": "",
        "ipii_score": aresta_sugerida["score"],
        "ipii_tier": aresta_sugerida.get("tier", 0),
        "ipii_curador": curador,
    }
