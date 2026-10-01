"""
Conjuntos computados a partir do corpus.

Cada vetor tematico (lib.constants.THEMES) define um conjunto:
    A = { x in normas | A in temas(x) }
As operacoes (intersecao, diferenca) sao calculadas sobre normas.json, de
modo que novos vetores e novas normas entram na pagina sem edicao manual.

Distincao epistemologica mantida na pagina: conjuntos CLASSIFICAM (a que
campo uma norma pertence); o grafo RELACIONA (de onde a norma retira
validade, o que regulamenta, quem a interpreta). Pertencer ao mesmo conjunto
nao implica aresta, e uma aresta nao implica pertencer ao mesmo conjunto.
"""

from itertools import combinations

import plotly.graph_objects as go

from lib.constants import THEMES
from lib.graph_builder import load_json


def carregar():
    normas = load_json("normas.json")["nodes"]
    arestas = load_json("arestas.json")["edges"]
    return normas, arestas


def conjuntos(normas: list[dict]) -> dict[str, set[str]]:
    """tema -> conjunto de ids. Inclui apenas temas declarados em THEMES."""
    out = {t: set() for t in THEMES}
    for n in normas:
        for t in n.get("temas") or []:
            if t in out:
                out[t].add(n["id"])
    return out


def matriz_intersecoes(cj: dict[str, set[str]]):
    temas = list(cj)
    return temas, [[len(cj[a] & cj[b]) for b in temas] for a in temas]


def lacunas(cj: dict[str, set[str]]) -> list[tuple[str, str]]:
    """Pares de vetores com intersecao vazia no corpus atual."""
    return [(a, b) for a, b in combinations(cj, 2) if cj[a] and cj[b] and not (cj[a] & cj[b])]


def relacoes_no_par(a: set[str], b: set[str], arestas: list[dict]) -> list[dict]:
    """Arestas que ligam um elemento de A a um de B (em qualquer sentido)."""
    return [e for e in arestas
            if (e["source"] in a and e["target"] in b) or (e["source"] in b and e["target"] in a)]


def pares_em_frases(cj: dict[str, set[str]], nome) -> tuple[list[str], list[str]]:
    """
    A matriz em linguagem simples. Devolve (frases dos pares com interseção,
    ordenadas da maior para a menor; nomes dos pares disjuntos).
    `nome` converte id de norma em rótulo legível.
    """
    com, sem = [], []
    for a, b in combinations(cj, 2):
        if not (cj[a] and cj[b]):
            continue
        comum = cj[a] & cj[b]
        if comum:
            rot = ", ".join(sorted(nome(i) for i in comum))
            n = len(comum)
            com.append((n, f"**{THEMES[a]}** e **{THEMES[b]}** compartilham "
                           f"{n} norma{'s' if n > 1 else ''}: {rot}."))
        else:
            sem.append(f"{THEMES[a]} × {THEMES[b]}")
    return [f for _, f in sorted(com, key=lambda x: -x[0])], sem


def figura_matriz(cj: dict[str, set[str]]) -> go.Figure:
    """
    Triangulo inferior: |A ∩ B| = |B ∩ A|, entao a metade superior repetiria
    os mesmos numeros. A diagonal e a cardinalidade de cada conjunto.
    """
    temas, m = matriz_intersecoes(cj)
    m = [[v if j <= i else None for j, v in enumerate(linha)] for i, linha in enumerate(m)]
    rot = [THEMES[t] for t in temas]
    fig = go.Figure(go.Heatmap(
        z=m, x=rot, y=rot, hoverongaps=False,
        text=[["" if v is None else v for v in linha] for linha in m],
        colorscale=[[0, "#14171f"], [0.15, "#3a2f1a"], [1, "#d4a853"]],
        texttemplate="%{text}", textfont=dict(family="DM Mono, monospace", size=12),
        hovertemplate="<b>%{y}</b> ∩ <b>%{x}</b><br>%{z} norma(s)<extra></extra>",
        showscale=False, xgap=2, ygap=2,
    ))
    fig.update_layout(
        height=520, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono, monospace", color="#e8e4dc", size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(side="bottom", tickangle=-35, showgrid=False),
        yaxis=dict(autorange="reversed", showgrid=False),
    )
    return fig
