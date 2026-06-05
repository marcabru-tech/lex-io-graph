import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import json

from lib.graph_builder import build_compliance_graph, get_intersections
from lib.constants import THEMES, NODE_TYPE_LABELS

st.set_page_config(page_title="Grafo Normativo - Lexiograph Compliance Map", layout="wide", page_icon="📊")

st.markdown("""
<style>
    [data-testid="stSidebar"] { min-width: 320px; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("# Grafo Normativo")
st.markdown("Visualização interativa das conexões entre normas do ordenamento jurídico digital brasileiro.")

# ---- Filtros ----
st.sidebar.markdown("## Filtros")

st.sidebar.markdown("**Temas regulatórios**")
theme_options = list(THEMES.keys())
theme_labels = {k: THEMES[k] for k in theme_options}

selected_themes = []
for key in theme_options:
    if st.sidebar.checkbox(theme_labels[key], value=True, key="theme_" + key):
        selected_themes.append(key)

st.sidebar.markdown("---")

st.sidebar.markdown("**Tipos de norma**")
type_options = list(NODE_TYPE_LABELS.keys())
type_labels = {k: NODE_TYPE_LABELS[k] for k in type_options}

selected_types = []
for key in type_options:
    if st.sidebar.checkbox(type_labels[key], value=True, key="type_" + key):
        selected_types.append(key)

st.sidebar.markdown("---")
st.sidebar.markdown("**Legenda do grafo**")
st.sidebar.markdown("• Nós maiores = normas fundamentais")
st.sidebar.markdown("• Linhas sólidas = hierarquia normativa")
st.sidebar.markdown("• Linhas tracejadas = interseção temática")
st.sidebar.markdown("• Passe o mouse sobre nós e linhas para ver detalhes")
st.sidebar.markdown("• Arraste nós para reorganizar")
st.sidebar.markdown("• Use os botões de navegação no canto inferior esquerdo do grafo")

if not selected_themes:
    st.warning("Nenhum tema selecionado. Marque pelo menos um tema na barra lateral.")
    st.stop()

if not selected_types:
    st.warning("Nenhum tipo de norma selecionado. Marque pelo menos um tipo na barra lateral.")
    st.stop()

G = build_compliance_graph(
    themes=selected_themes,
    norm_types=selected_types,
)

if len(G.nodes) == 0:
    st.warning("Nenhuma norma encontrada com os filtros selecionados.")
    st.stop()

undirected_G = G.to_undirected()
num_componentes = nx.number_connected_components(undirected_G)

col1, col2, col3 = st.columns(3)
col1.metric("Nós visíveis", len(G.nodes))
col2.metric("Conexões visíveis", len(G.edges))
col3.metric("Componentes conectados", num_componentes)

# ---- Grafo Pyvis ----
GRAFO_ALTURA = 900

net = Network(
    height=str(GRAFO_ALTURA) + "px",
    width="100%",
    directed=True,
    bgcolor="#08070e",
    font_color="#e8e4dc",
    notebook=False,
    cdn_resources="remote",
)

physics_options = {
    "physics": {
        "forceAtlas2Based": {
            "gravitationalConstant": -200,
            "centralGravity": 0.008,
            "springLength": 350,
            "springConstant": 0.02,
            "damping": 0.5,
            "avoidOverlap": 0.8
        },
        "solver": "forceAtlas2Based",
        "stabilization": {
            "enabled": True,
            "iterations": 400,
            "updateInterval": 25
        },
        "maxVelocity": 20,
        "minVelocity": 0.5
    },
    "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "font": {
            "size": 18,
            "face": "monospace",
            "color": "#e8e4dc",
            "strokeWidth": 3,
            "strokeColor": "#08070e"
        },
        "shadow": True,
        "margin": 12
    },
    "edges": {
        "smooth": {
            "type": "continuous",
            "roundness": 0.5
        },
        "arrows": {
            "to": {
                "enabled": True,
                "scaleFactor": 1.0
            }
        },
        "font": {
            "size": 14,
            "face": "monospace",
            "color": "#b8b2a6",
            "align": "middle",
            "strokeWidth": 4,
            "strokeColor": "#08070e"
        },
        "shadow": False
    },
    "interaction": {
        "hover": True,
        "navigationButtons": True,
        "keyboard": True,
        "zoomView": True,
        "dragView": True,
        "tooltipDelay": 200
    }
}

net.set_options(json.dumps(physics_options))

EDGE_TYPE_SHORT = {
    "hierarquia": "HIERARQUIA",
    "intersecao": "INTERSEÇÃO",
    "antinomia": "ANTINOMIA",
    "complementaridade": "COMPLEMENTAR",
    "regulamenta": "REGULAMENTA",
    "interpreta": "INTERPRETA",
}

# ---- Adicionar nós ----
for node_id in G.nodes:
    d = G.nodes[node_id]
    node_type = d.get("tipo", "")
    if node_type == "constituicao":
        node_size = 50
    elif node_type == "lei":
        node_size = 35
    elif node_type == "jurisprudencia":
        node_size = 25
    elif node_type == "orgao":
        node_size = 28
    else:
        node_size = 30

    art = d.get("artigos_chave", [])
    art_str = ""
    if art:
        art_str = "<br><b>Artigos:</b> " + " | ".join(art)

    tip = (
        "<div style='max-width:400px; font-family: monospace; font-size: 13px; line-height: 1.6;'>"
        + "<b style='font-size:15px;'>" + d.get("nome", "") + "</b><br><br>"
        + "<i>" + d.get("ementa", "") + "</i><br><br>"
        + "<b>Tipo:</b> " + d.get("tipo_label", "") + "<br>"
        + "<b>Status:</b> " + d.get("status", "") + "<br>"
        + "<b>Órgão:</b> " + d.get("orgao", "") + "<br>"
        + "<b>Ano:</b> " + str(d.get("ano", ""))
        + art_str
        + "</div>"
    )

    net.add_node(
        node_id,
        label=d.get("label", node_id),
        title=tip,
        color={
            "background": d.get("color", "#888888"),
            "border": d.get("color", "#888888"),
        },
        size=node_size,
        shape="dot",
    )

# ---- Adicionar arestas ----
for u, v, d in G.edges(data=True):
    edge_tipo = d.get("tipo", "")
    edge_label = EDGE_TYPE_SHORT.get(edge_tipo, edge_tipo.upper())

    tip = (
        "<div style='max-width:450px; font-family: monospace; font-size: 13px; line-height: 1.6;'>"
        + "<b style='font-size:14px;'>" + d.get("tipo_label", "") + "</b><br><br>"
        + d.get("descricao", "") + "<br><br>"
        + "<b>Artigos cruzados:</b> " + d.get("artigos", "")
        + "</div>"
    )

    is_dashed = edge_tipo in ("intersecao", "antinomia", "complementaridade")

    net.add_edge(
        u, v,
        title=tip,
        color={
            "color": d.get("color", "#888888"),
            "highlight": "#ffffff",
            "hover": "#ffffff",
        },
        label=edge_label,
        width=2 if edge_tipo == "hierarquia" else 1.5,
        dashes=is_dashed,
        font={
            "size": 14,
            "strokeWidth": 4,
            "strokeColor": "#08070e",
            "color": "#b8b2a6",
            "align": "middle",
        },
        smooth={
            "type": "continuous",
            "roundness": 0.5,
        },
    )

# ---- Salvar e injetar CSS nos botões de navegação ----
tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
net.save_graph(tmp.name)

with open(tmp.name, "r", encoding="utf-8") as f:
    html_content = f.read()

nav_css = """
<style>
    .vis-navigation {
        position: absolute !important;
        bottom: 16px !important;
        left: 16px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 2px !important;
    }
    .vis-navigation .vis-button {
        background: rgba(15, 14, 24, 0.92) !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(212, 168, 83, 0.4) !important;
        border-radius: 6px !important;
        width: 32px !important;
        height: 32px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        padding: 0 !important;
        margin: 1px !important;
    }
    .vis-navigation .vis-button:hover {
        background: rgba(212, 168, 83, 0.2) !important;
        border-color: #d4a853 !important;
        transform: scale(1.08) !important;
    }
    .vis-navigation .vis-button:after,
    .vis-navigation .vis-button .vis-up,
    .vis-navigation .vis-button .vis-down,
    .vis-navigation .vis-button .vis-left,
    .vis-navigation .vis-button .vis-right,
    .vis-navigation .vis-button .vis-zoomIn,
    .vis-navigation .vis-button .vis-zoomOut,
    .vis-navigation .vis-button .vis-zoomExtends {
        color: #d4a853 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        opacity: 1 !important;
    }
    .vis-navigation .vis-button:hover:after,
    .vis-navigation .vis-button:hover .vis-up,
    .vis-navigation .vis-button:hover .vis-down,
    .vis-navigation .vis-button:hover .vis-left,
    .vis-navigation .vis-button:hover .vis-right,
    .vis-navigation .vis-button:hover .vis-zoomIn,
    .vis-navigation .vis-button:hover .vis-zoomOut,
    .vis-navigation .vis-button:hover .vis-zoomExtends {
        color: #ffffff !important;
    }
    .vis-navigation .vis-button.vis-up:after { content: "▲" !important; }
    .vis-navigation .vis-button.vis-down:after { content: "▼" !important; }
    .vis-navigation .vis-button.vis-left:after { content: "◀" !important; }
    .vis-navigation .vis-button.vis-right:after { content: "▶" !important; }
    .vis-navigation .vis-button.vis-zoomIn:after { content: "+" !important; font-size: 20px !important; }
    .vis-navigation .vis-button.vis-zoomOut:after { content: "−" !important; font-size: 20px !important; }
    .vis-navigation .vis-button.vis-zoomExtends:after { content: "⌂" !important; font-size: 16px !important; }
    .vis-navigation > div {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 2px !important;
    }
</style>
"""

tooltip_fix = """<script>
document.addEventListener('DOMContentLoaded', function() {
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.className && typeof node.className === 'string' && node.className.indexOf('vis-tooltip') !== -1) {
                    var raw = node.innerHTML;
                    if (raw && raw.indexOf('&lt;') !== -1) {
                        node.innerHTML = raw
                            .replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&')
                            .replace(/&#x27;/g,"'").replace(/&quot;/g,'"');
                    }
                }
            });
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
});
</script>"""
html_content = html_content.replace("</head>", nav_css + tooltip_fix + "</head>")

components.html(html_content, height=GRAFO_ALTURA + 20, scrolling=False)

st.markdown("---")
st.markdown("### Explorar norma")

node_options = {nid: G.nodes[nid].get("nome", nid) for nid in G.nodes}

selected_node = st.selectbox(
    "Selecione uma norma para ver detalhes e conexões",
    options=list(node_options.keys()),
    format_func=lambda x: node_options[x],
)

if selected_node:
    nd = G.nodes[selected_node]

    col_info, col_conex = st.columns([1, 1])

    with col_info:
        st.markdown("#### " + nd.get("nome", ""))
        st.markdown("**Sigla:** " + nd.get("label", ""))
        st.markdown("**Tipo:** " + nd.get("tipo_label", ""))
        st.markdown("**Status:** " + nd.get("status", ""))
        st.markdown("**Órgão:** " + nd.get("orgao", ""))
        st.markdown("**Ementa:** " + nd.get("ementa", ""))
        art = nd.get("artigos_chave", [])
        if art:
            st.markdown("**Artigos-chave:** " + " | ".join(art))

    with col_conex:
        ix = get_intersections(G, selected_node)
        if ix:
            st.markdown("#### Conexões (" + str(len(ix)) + ")")
            for inter in ix:
                st.markdown(
                    "- **" + inter["tipo_relacao"] + "** com `" + inter["outro_no"] + "`"
                )
                st.markdown("  " + inter["descricao"])
                st.markdown("  *" + inter["artigos"] + "*")
        else:
            st.markdown("Nenhuma conexão encontrada com os filtros atuais.")
