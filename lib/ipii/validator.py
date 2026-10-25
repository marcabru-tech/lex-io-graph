# Copyright © 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado
# IPII (Interação Paramétrica Iterativa por Interoperabilidade) para Lex-IO-Graph / Lexiograph
# Licença: PolyForm Noncommercial 1.0.0 (ver lib/ipii/LICENSE).
# Estudo e pesquisa liberados; uso comercial somente com autorização
# prévia e por escrito do titular.
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


LIMITE_RESUMO = 120


def resumir(texto, limite: int = LIMITE_RESUMO) -> str:
    """Resumo legível: corta em palavra inteira e indica a continuação com "…".

    O texto integral é guardado à parte (campo descricao_completa) para que a
    interface permita lê-lo inteiro.
    """
    texto = " ".join(str(texto or "").split())
    if len(texto) <= limite:
        return texto
    corte = texto[:limite].rsplit(" ", 1)[0] or texto[:limite]
    return corte.rstrip(" ,;:.—-") + "…"


def _par(source: str, target: str) -> tuple:
    """Par canônico ordenado alfabeticamente."""
    return tuple(sorted([source, target]))


def validar_arestas(sugeridas: list, existentes: list, excluidas: frozenset = frozenset()) -> dict:
    """
    Compara arestas sugeridas vs existentes.

    `excluidas` são ids de normas fora do IPII (matcher.STATUS_EXCLUIDOS_DO_IPII).
    Aresta existente com uma delas não pode ser sugerida por regra, não por
    limite do engine: sai de total_existentes, faltando e gap_engine, para não
    rebaixar a cobertura nem aparecer como "não detectada", e é listada em
    fora_do_ipii.

    Returns:
        dict com métricas de precisão/cobertura e listas detalhadas.
    """

    fora_do_ipii = [e for e in existentes if {e["source"], e["target"]} & excluidas]
    existentes = [e for e in existentes if not {e["source"], e["target"]} & excluidas]

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
        # Entre as confirmadas (par certo), quantas têm também o tipo certo.
        "acertos_tipo": sum(1 for c in confirmadas if c["match_tipo"]),
        "precisao_tipo": (round(sum(1 for c in confirmadas if c["match_tipo"]) / len(confirmadas), 3)
                          if confirmadas else 0),
        "detalhe_confirmadas": confirmadas,
        "detalhe_novas": novas,
        "detalhe_faltando": faltando,
        "gap_engine": [
            {
                "par": f"{e['source']} ↔ {e['target']}",
                "tipo": e["tipo"],
                "descricao": resumir(e.get("descricao")),
                "descricao_completa": e.get("descricao") or "",
            }
            for e in faltando
        ],
        "fora_do_ipii": [
            {
                "par": f"{e['source']} ↔ {e['target']}",
                "tipo": e["tipo"],
                "descricao": resumir(e.get("descricao")),
                "descricao_completa": e.get("descricao") or "",
            }
            for e in fora_do_ipii
        ],
    }


def filtrar_por_tier(novas: list, tier_max: int = 3) -> list:
    """Filtra novas arestas por tier (1 = mais forte). Tier 0 ("irrelevante")
    ou ausente/inválido nunca passa (A6-c)."""
    return [n for n in novas
            if type(n.get("tier")) is int and 1 <= n["tier"] <= tier_max]


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
