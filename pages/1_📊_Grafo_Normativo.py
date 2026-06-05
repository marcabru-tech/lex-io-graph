import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import json

from lib.graph_builder import build_compliance_graph, get_intersections
from lib.constants import THEMES, NODE_TYPE_LABELS
from lib.footer import render_footer

st.set_page_config(
    page_title="Grafo Normativo - Lexiograph Compliance Map",
    layout="wide",
    page_icon="📊"
)

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

# Temas — apenas dois pré-selecionados por padrão
DEFAULT_THEMES = {"dados_pessoais", "internet"}
st.sidebar.markdown("**Temas regulatórios**")
theme_options = list(THEMES.keys())

selected_themes = []
for key in theme_options:
    checked = key in DEFAULT_THEMES
    if st.sidebar.checkbox(THEMES[key], value=checked, key="theme_" + key):
        selected_themes.append(key)

st.sidebar.markdown("---")

# Tipos — PLs, decretos e órgãos desmarcados por padrão
DEFAULT_TYPES = {"constituicao", "lei", "jurisprudencia", "norma_regulamentar"}
st.sidebar.markdown("**Tipos de norma**")
type_options = list(NODE_TYPE_LABELS.keys())

selected_types = []
for key in type_options:
    checked = key in DEFAULT_TYPES
    if st.sidebar.checkbox(NODE_TYPE_LABELS[key], value=checked, key="type_" + key):
        selected_types.append(key)

st.sidebar.markdown("---")

# ---- Legenda visual ----
st.sidebar.markdown("**Legenda do grafo**")
st.sidebar.markdown("""
• Nós maiores = normas fundamentais  
• Linhas sólidas = relações de subordinação  
• Linhas tracejadas = relações de coordenação  
• Passe o mouse sobre nós e arestas para ver detalhes  
• Arraste nós para reorganizar  
""")

st.sidebar.markdown("---")

# ---- Legenda doutrinária das relações ----
st.sidebar.markdown("**Tipos de relação jurídica**")
st.sidebar.markdown("""
<style>
.rel-item { padding: 5px 0 8px 0; font-size: 11px; line-height: 1.6;
  border-bottom: 1px solid rgba(255,255,255,0.05); }
.rel-item:last-child { border-bottom: none; }
.rel-line { display:inline-block; width:18px; height:2px;
  vertical-align:middle; margin-right:6px; border-radius:1px; }
.rel-solid-gold  { background:#d4a853; }
.rel-solid-orange{ background:#e67e22; }
.rel-solid-purple{ background:#9b59b6; }
.rel-dash-cyan {
  background-image:repeating-linear-gradient(
    90deg,#3dc8e6 0,#3dc8e6 5px,transparent 5px,transparent 9px); }
.rel-dash-green {
  background-image:repeating-linear-gradient(
    90deg,#2ecc71 0,#2ecc71 5px,transparent 5px,transparent 9px); }
.rel-dash-red {
  background-image:repeating-linear-gradient(
    90deg,#c44b4b 0,#c44b4b 5px,transparent 5px,transparent 9px); }
.rel-label { font-weight:bold; color:#e8e4dc; font-size:11px; }
.rel-ref   { color:#d4a853; font-size:10px; font-style:italic; margin-left:4px; }
.rel-desc  { color:#8a8478; font-size:10px; display:block;
  margin-top:2px; padding-left:24px; line-height:1.5; }
.rel-group { font-size:9px; color:#706a60; letter-spacing:0.12em;
  text-transform:uppercase; margin:8px 0 4px 0; }
</style>

<div class="rel-group">Subordinação normativa</div>

<div class="rel-item">
  <span class="rel-line rel-solid-gold"></span>
  <span class="rel-label">Hierarquia</span>
  <span class="rel-ref">(Kelsen)</span>
  <span class="rel-desc">Norma superior confere validade à inferior.
    Conflito: <em>lex superior derogat inferiori</em>.</span>
</div>

<div class="rel-item">
  <span class="rel-line rel-solid-orange"></span>
  <span class="rel-label">Regulamenta</span>
  <span class="rel-desc">Norma posterior detalha operacionalmente
    a anterior sem alterar hierarquia.</span>
</div>

<div class="rel-item">
  <span class="rel-line rel-solid-purple"></span>
  <span class="rel-label">Interpreta</span>
  <span class="rel-desc">Decisão judicial fixa o sentido autêntico
    do dispositivo. STF = vinculante; STJ = persuasivo.</span>
</div>

<div class="rel-group" style="margin-top:10px;">Coordenação normativa</div>

<div class="rel-item">
  <span class="rel-line rel-dash-cyan"></span>
  <span class="rel-label">Interseção</span>
  <span class="rel-desc">Duas normas regulam o mesmo fato por ângulos
    distintos. Aplicação simultânea possível.</span>
</div>

<div class="rel-item">
  <span class="rel-line rel-dash-green"></span>
  <span class="rel-label">Complementaridade</span>
  <span class="rel-ref">(Canaris)</span>
  <span class="rel-desc">Normas que se reforçam mutuamente,
    formando sistema coerente.</span>
</div>

<div class="rel-item">
  <span class="rel-line rel-dash-red"></span>
  <span class="rel-label">Antinomia</span>
  <span class="rel-ref">(Bobbio)</span>
  <span class="rel-desc">Conflito normativo real — aplicação
    simultânea gera insegurança jurídica. Resolve-se por
    <em>lex superior</em>, <em>lex posterior</em>
    ou <em>lex specialis</em>.</span>
</div>
""", unsafe_allow_html=True)

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
        "stabilization": {"enabled": True, "iterations": 400, "updateInterval": 25},
        "maxVelocity": 20,
        "minVelocity": 0.5
    },
    "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "font": {"size": 18, "face": "monospace", "color": "#e8e4dc",
                 "strokeWidth": 3, "strokeColor": "#08070e"},
        "shadow": True,
        "margin": 12
    },
    "edges": {
        "smooth": {"type": "continuous", "roundness": 0.5},
        "arrows": {"to": {"enabled": True, "scaleFactor": 1.0}},
        "font": {"size": 14, "face": "monospace", "color": "#b8b2a6",
                 "align": "middle", "strokeWidth": 4, "strokeColor": "#08070e"},
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
    art_txt = ""
    if art:
        art_txt = "\nArtigos: " + " | ".join(art[:4])
        if len(art) > 4:
            art_txt += " ..."

    tip = (
        d.get("nome", "") + "\n"
        + "-" * 36 + "\n"
        + d.get("ementa", "")[:300] + "\n"
        + "-" * 36 + "\n"
        + "Tipo:   " + d.get("tipo_label", "") + "\n"
        + "Status: " + d.get("status", "") + "\n"
        + "Orgao:  " + d.get("orgao", "") + "\n"
        + "Ano:    " + str(d.get("ano", ""))
        + art_txt
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

for u, v, d in G.edges(data=True):
    edge_tipo = d.get("tipo", "")
    edge_label = EDGE_TYPE_SHORT.get(edge_tipo, edge_tipo.upper())

    tip = (
        d.get("tipo_label", "") + "\n"
        + "-" * 36 + "\n"
        + d.get("descricao", "")[:280] + "\n"
        + "-" * 36 + "\n"
        + "Artigos: " + d.get("artigos", "")
    )

    is_dashed = edge_tipo in ("intersecao", "antinomia", "complementaridade")

    net.add_edge(
        u, v,
        title=tip,
        color={"color": d.get("color", "#888888"), "highlight": "#ffffff", "hover": "#ffffff"},
        label=edge_label,
        width=2 if edge_tipo == "hierarquia" else 1.5,
        dashes=is_dashed,
        font={"size": 14, "strokeWidth": 4, "strokeColor": "#08070e",
              "color": "#b8b2a6", "align": "middle"},
        smooth={"type": "continuous", "roundness": 0.5},
    )

tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
net.save_graph(tmp.name)

with open(tmp.name, "r", encoding="utf-8") as f:
    html_content = f.read()

injected_css = """
<style>
    .vis-tooltip {
        max-width: 400px !important;
        min-width: 180px !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
        line-height: 1.65 !important;
        padding: 10px 14px !important;
        background: rgba(10, 9, 18, 0.97) !important;
        border: 1px solid rgba(212,168,83,0.5) !important;
        border-radius: 6px !important;
        color: #e8e4dc !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.7) !important;
        pointer-events: none !important;
    }
    .vis-navigation .vis-button {
        background: rgba(15,14,24,0.92) !important;
        border: 1px solid rgba(212,168,83,0.4) !important;
        border-radius: 6px !important;
    }
    .vis-navigation .vis-button:hover {
        background: rgba(212,168,83,0.2) !important;
        border-color: #d4a853 !important;
    }
</style>
"""

html_content = html_content.replace("</head>", injected_css + "</head>")
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

render_footer()
