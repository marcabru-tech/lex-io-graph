"""
Página 1 — Grafo Normativo Interativo

Visualização force-directed do ordenamento jurídico digital brasileiro
com filtros por tema e hierarquia normativa.
"""

import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
from pathlib import Path

from lib.graph_builder import build_compliance_graph, get_intersections
from lib.constants import THEMES, NODE_TYPE_LABELS

st.set_page_config(page_title="Grafo Normativo — Lex Quantum", layout="wide", page_icon="📊")

st.markdown("# 📊 Grafo Normativo")
st.markdown("Visualização interativa das conexões entre normas do ordenamento jurídico digital brasileiro.")

# ---- Filtros ----
st.sidebar.markdown("## Filtros")

selected_themes = st.sidebar.multiselect(
    "Filtrar por tema",
    options=list(THEMES.keys()),
    format_func=lambda x: THEMES[x],
    default=list(THEMES.keys()),
)

selected_types = st.sidebar.multiselect(
    "Filtrar por tipo de norma",
    options=list(NODE_TYPE_LABELS.keys()),
    format_func=lambda x: NODE_TYPE_LABELS[x],
    default=list(NODE_TYPE_LABELS.keys()),
)

# ---- Construir grafo filtrado ----
G = build_compliance_graph(
    themes=selected_themes if selected_themes else None,
    norm_types=selected_types if selected_types else None,
)

if len(G.nodes) == 0:
    st.warning("Nenhuma norma encontrada com os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ---- Métricas do grafo filtrado ----
col1, col2, col3 = st.columns(3)
col1.metric("Nós visíveis", len(G.nodes))
col2.metric("Conexões visíveis", len(G.edges))
col3.metric("Componentes conectados", len(list(nx.connected_components(nx.Graph(G)))))

# ---- Gerar visualização Pyvis ----
net = Network(
    height="700px",
    width="100%",
    directed=True,
    bgcolor="#08070e",
    font_color="#e8e4dc",
    notebook=False,
    cdn_resources="remote",
)

# Configuração física
net.set_options("""
{
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -80,
      "centralGravity": 0.015,
      "springLength": 200,
      "springConstant": 0.04,
      "damping": 0.4
    },
    "solver": "forceAtlas2Based",
    "stabilization": {
      "enabled": true,
      "iterations": 200
    }
  },
  "nodes": {
    "borderWidth": 2,
    "borderWidthSelected": 3,
    "font": {
      "size": 14,
      "face": "DM Mono, monospace",
      "color": "#e8e4dc"
    },
    "shadow": true
  },
  "edges": {
    "smooth": {
      "type": "cubicBezier",
      "forceDirection": "none",
      "roundness": 0.4
    },
    "arrows": {
      "to": {
        "enabled": true,
        "scaleFactor": 0.8
      }
    },
    "font": {
      "size": 10,
      "face": "DM Mono, monospace",
      "color": "#706a60",
      "align": "middle"
    },
    "shadow": false
  },
  "interaction": {
    "hover": true,
    "navigationButtons": true,
    "keyboard": true
  }
}
""")

# Adicionar nós
for node_id in G.nodes:
    data = G.nodes[node_id]
    size = 30 if data.get("tipo") == "constituicao" else 22 if data.get("tipo") == "lei" else 18
    net.add_node(
        node_id,
        label=data.get("label", node_id),
        title=f"<b>{data.get('nome', '')}</b><br><br>"
              f"<i>{data.get('ementa', '')}</i><br><br>"
              f"<b>Tipo:</b> {data.get('tipo_label', '')}<br>"
              f"<b>Status:</b> {data.get('status', '')}<br>"
              f"<b>Órgão:</b> {data.get('orgao', '')}<br>"
              f"<b>Ano:</b> {data.get('ano', '')}",
        color=data.get("color", "#888888"),
        size=size,
        shape="dot",
    )

# Adicionar arestas
for u, v, data in G.edges(data=True):
    net.add_edge(
        u, v,
        title=f"<b>{data.get('tipo_label', '')}</b><br><br>"
              f"{data.get('descricao', '')}<br><br>"
              f"<b>Artigos:</b> {data.get('artigos', '')}",
        color={"color": data.get("color", "#888888"), "highlight": "#ffffff"},
        label=data.get("tipo", ""),
        width=2 if data.get("tipo") == "hierarquia" else 1,
        dashes=True if data.get("tipo") in ("intersecao", "antinomia") else False,
    )

# Renderizar
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
    net.save_graph(f.name)
    html_path = f.name

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=720, scrolling=False)

# ---- Detalhe do nó selecionado ----
st.markdown("---")
st.markdown("### Explorar norma")

node_options = {
    node_id: G.nodes[node_id].get("nome", node_id)
    for node_id in G.nodes
}

selected_node = st.selectbox(
    "Selecione uma norma para ver detalhes e conexões",
    options=list(node_options.keys()),
    format_func=lambda x: node_options[x],
)

if selected_node:
    node_data = G.nodes[selected_node]
    st.markdown(f"#### {node_data.get('nome', '')}")
    st.markdown(f"**Sigla:** {node_data.get('label', '')}")
    st.markdown(f"**Tipo:** {node_data.get('tipo_label', '')}")
    st.markdown(f"**Status:** {node_data.get('status', '')}")
    st.markdown(f"**Órgão:** {node_data.get('orgao', '')}")
    st.markdown(f"**Ementa:** {node_data.get('ementa', '')}")

    artigos = node_data.get("artigos_chave", [])
    if artigos:
        st.markdown("**Artigos-chave:** " + " · ".join(artigos))

    intersections = get_intersections(G, selected_node)
    if intersections:
        st.markdown(f"#### Conexões ({len(intersections)})")
        for inter in intersections:
            st.markdown(
                f"- **{inter['tipo_relacao']}** com `{inter['outro_no']}` — "
                f"{inter['descricao'][:150]}...  "
                f"*{inter['artigos']}*"
            )
