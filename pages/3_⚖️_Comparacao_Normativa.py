"""
Página 3 — Comparação e Contraste Normativo

Análise lado a lado de pares de normas com interseções.
"""

import streamlit as st

from lib.graph_builder import build_compliance_graph, load_json
from lib.constants import EDGE_TYPE_LABELS, THEMES
from lib.footer import render_footer

st.set_page_config(page_title="Comparação Normativa — Lex Quantum", layout="wide", page_icon="⚖️")

st.markdown("# ⚖️ Comparação e Contraste Normativo")
st.markdown("Análise lado a lado de pares de normas com interseções identificadas no grafo.")

# ---- Carregar dados ----
G = build_compliance_graph()
raw_nodes = load_json("normas.json")["nodes"]
raw_edges = load_json("arestas.json")["edges"]
raw_juris = load_json("jurisprudencia.json")["jurisprudencia"]

# ---- Selecionar par ----
st.markdown("### Selecionar par de normas")

node_options = {n["id"]: f"{n['sigla']} — {n['nome']}" for n in raw_nodes}

col1, col2 = st.columns(2)
with col1:
    norma_a = st.selectbox("Norma A", options=list(node_options.keys()), format_func=lambda x: node_options[x], index=1)
with col2:
    norma_b = st.selectbox("Norma B", options=list(node_options.keys()), format_func=lambda x: node_options[x], index=4)

# ---- Buscar aresta entre as duas normas ----
edge_data = None
for u, v, data in G.edges(data=True):
    if (u == norma_a and v == norma_b) or (u == norma_b and v == norma_a):
        edge_data = data
        break

# ---- Exibir comparação ----
if norma_a == norma_b:
    st.warning("Selecione duas normas diferentes para comparar.")
    st.stop()

data_a = raw_nodes[[i for i, n in enumerate(raw_nodes) if n["id"] == norma_a][0]]
data_b = raw_nodes[[i for i, n in enumerate(raw_nodes) if n["id"] == norma_b][0]]

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"#### {data_a['sigla']}")
    st.markdown(f"**Nome completo:** {data_a['nome']}")
    st.markdown(f"**Tipo:** {data_a['tipo']}")
    st.markdown(f"**Status:** {data_a['status']}")
    st.markdown(f"**Órgão:** {data_a['orgao']}")
    st.markdown(f"**Ano:** {data_a['ano']}")
    st.markdown(f"**Ementa:** {data_a['ementa']}")
    if data_a.get("artigos_chave"):
        st.markdown("**Artigos-chave:** " + " · ".join(data_a["artigos_chave"]))

with col_b:
    st.markdown(f"#### {data_b['sigla']}")
    st.markdown(f"**Nome completo:** {data_b['nome']}")
    st.markdown(f"**Tipo:** {data_b['tipo']}")
    st.markdown(f"**Status:** {data_b['status']}")
    st.markdown(f"**Órgão:** {data_b['orgao']}")
    st.markdown(f"**Ano:** {data_b['ano']}")
    st.markdown(f"**Ementa:** {data_b['ementa']}")
    if data_b.get("artigos_chave"):
        st.markdown("**Artigos-chave:** " + " · ".join(data_b["artigos_chave"]))

# ---- Conexão ----
st.markdown("---")
if edge_data:
    st.markdown(f"### Conexão: {edge_data.get('tipo_label', edge_data.get('tipo', ''))}")
    st.markdown(f"**Tipo:** `{edge_data.get('tipo', '')}`")
    st.markdown(f"**Descrição:** {edge_data.get('descricao', '')}")
    st.markdown(f"**Artigos cruzados:** {edge_data.get('artigos', '')}")
else:
    st.info("Não há conexão direta documentada entre estas duas normas no grafo.")

# ---- Jurisprudência vinculada ----
st.markdown("---")
st.markdown("### Jurisprudência vinculada")

juris_relativa = [
    j for j in raw_juris
    if norma_a in j.get("normas_relacionadas", []) or norma_b in j.get("normas_relacionadas", [])
]

if juris_relativa:
    for j in juris_relativa:
        with st.expander(f"**{j['tribunal']} — {j['numero']}** ({j['ano']})"):
            st.markdown(f"**Tema:** {j['tema']}")
            st.markdown(f"**Resumo:** {j['resumo']}")
            st.markdown(f"**Impacto para dev júnior:** {j['impacto_dev_junior']}")
else:
    st.markdown("Nenhuma jurisprudência diretamente vinculada a este par de normas no banco atual.")

# ---- Pares sugeridos ----
st.markdown("---")
st.markdown("### Pares de alto contraste sugeridos")

sugestoes = [
    ("lgpd", "eca_digital", "LGPD vs. ECA Digital — dados de menores"),
    ("lgpd", "pl_ia", "LGPD vs. PL 2.338 — decisões automatizadas"),
    ("lgpd", "nr1", "LGPD vs. NR-1 — monitoramento de empregados"),
    ("marco_civil", "lgpd", "Marco Civil vs. LGPD — guarda de dados e bases legais"),
    ("eca_digital", "pl_ia", "ECA Digital vs. PL 2.338 — IA atingindo menores"),
    ("cf88", "lgpd", "Constituição vs. LGPD — fundamentação constitucional"),
]

for id_a, id_b, titulo in sugestoes:
    st.markdown(f"- **{titulo}** — `{node_options.get(id_a, id_a)}` × `{node_options.get(id_b, id_b)}`")

render_footer()
