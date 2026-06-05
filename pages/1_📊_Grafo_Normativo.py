import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import json

from lib.graph_builder import build_compliance_graph, get_intersections
from lib.constants import (
    APP_NAME, APP_SUBTITLE, APP_VERSION,
    THEMES, NODE_TYPE_LABELS, NODE_SHAPES, HIERARCHY_LEVELS
)
from lib.footer import render_footer

st.set_page_config(
    page_title=f"{APP_NAME} — Grafo Normativo",
    layout="wide",
    page_icon="📊"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { min-width: 320px; }
    .block-container { padding-top: 2rem; }
    .app-subtitle {
        font-family: monospace;
        font-size: 11px;
        color: #706a60;
        letter-spacing: 0.06em;
        line-height: 1.6;
        margin-top: -8px;
        margin-bottom: 16px;
        max-width: 800px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# Grafo Normativo")
st.markdown(
    f'<div class="app-subtitle">{APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)
st.markdown("Visualização interativa das conexões entre normas do ordenamento jurídico digital brasileiro.")

# ---- Filtros ----
st.sidebar.markdown(f"## {APP_NAME}")
st.sidebar.markdown(
    f'<div style="font-size:10px;color:#706a60;font-family:monospace;'
    f'line-height:1.5;margin-bottom:12px;">{APP_SUBTITLE}</div>',
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
st.sidebar.markdown("## Filtros")

DEFAULT_THEMES = {"dados_pessoais", "internet"}
st.sidebar.markdown("**Temas regulatórios**")
theme_options = list(THEMES.keys())

selected_themes = []
for key in theme_options:
    checked = key in DEFAULT_THEMES
    if st.sidebar.checkbox(THEMES[key], value=checked, key="theme_" + key):
        selected_themes.append(key)

st.sidebar.markdown("---")

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
• Nós maiores = normas fundamentais\n
• CF/88 ancorada no topo — hierarquia espacial corresponde à hierarquia normativa\n
• Linhas sólidas = relações de subordinação\n
• Linhas tracejadas = relações de coordenação\n
• Passe o mouse sobre nós e arestas para detalhes\n
• Arraste nós para reorganizar\n
""")

st.sidebar.markdown("---")

# ---- Semântica das cores ----
st.sidebar.markdown("**Semântica das cores**")
st.sidebar.markdown("""
<style>
.cor-item { display:flex; align-items:flex-start; gap:8px;
  padding: 4px 0; font-size:11px; line-height:1.5; }
.cor-box { width:14px; height:14px; border-radius:3px;
  flex-shrink:0; margin-top:2px; }
.cor-label { color:#e8e4dc; font-weight:bold; }
.cor-desc  { color:#8a8478; font-size:10px; }
</style>

<div class="cor-item">
  <div class="cor-box" style="background:#d4a853;"></div>
  <div><span class="cor-label">Dourado</span>
  <span class="cor-desc"> — CF/88, norma fundamental. Sol, razão, intelecto (Kelsen)</span></div>
</div>
<div class="cor-item">
  <div class="cor-box" style="background:#3dc8e6;"></div>
  <div><span class="cor-label">Ciano</span>
  <span class="cor-desc"> — Leis vigentes. Água, fluxo, movimento normativo</span></div>
</div>
<div class="cor-item">
  <div class="cor-box" style="background:#e67e22;"></div>
  <div><span class="cor-label">Laranja</span>
  <span class="cor-desc"> — Normas regulamentares e decretos. Calor, concretização</span></div>
</div>
<div class="cor-item">
  <div class="cor-box" style="background:#c44b4b;"></div>
  <div><span class="cor-label">Vermelho</span>
  <span class="cor-desc"> — Jurisprudência, tensão, antinomia. Sangue, conflito (Bobbio)</span></div>
</div>
<div class="cor-item">
  <div class="cor-box" style="background:#9b59b6;"></div>
  <div><span class="cor-label">Roxo</span>
  <span class="cor-desc"> — Órgãos institucionais. Sabedoria, autoridade</span></div>
</div>
<div class="cor-item">
  <div class="cor-box" style="background:#1abc9c;"></div>
  <div><span class="cor-label">Verde-esmeralda</span>
  <span class="cor-desc"> — Decretos executivos. Ação, implementação</span></div>
</div>
<div class="cor-item">
  <div class="cor-box" style="background:#8b8b8b;"></div>
  <div><span class="cor-label">Cinza</span>
  <span class="cor-desc"> — PLs em tramitação. Indefinição, vetor prospectivo</span></div>
</div>
<div class="cor-item">
  <div class="cor-box" style="background:#c8a96e;"></div>
  <div><span class="cor-label">Ocre</span>
  <span class="cor-desc"> — Documentos internacionais. Tradição, civilização</span></div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# ---- Legenda das formas ----
st.sidebar.markdown("**Semântica das formas**")
st.sidebar.markdown("""
<div style="font-size:11px; line-height:2; color:#8a8478;">
● Círculo — norma positiva vigente<br>
◆ Diamante — jurisprudência (precisão, corte)<br>
■ Quadrado — órgão / instituição (solidez)<br>
▲ Triângulo — PL / vetor prospectivo<br>
⬡ Hexágono — documento internacional
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# ---- Legenda doutrinária das relações ----
st.sidebar.markdown("**Tipos de relação jurídica**")
st.sidebar.markdown("""
<style>
.rel-item { padding: 5px 0 8px 0; font-size:11px; line-height:1.6;
  border-bottom:1px solid rgba(255,255,255,0.05); }
.rel-item:last-child { border-bottom:none; }
.rel-line { display:inline-block; width:18px; height:2px;
  vertical-align:middle; margin-right:6px; border-radius:1px; }
.rel-solid-gold   { background:#d4a853; }
.rel-solid-orange { background:#e67e22; }
.rel-solid-purple { background:#9b59b6; }
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
  <span class="rel-ref">(Kelsen, 1881–1973)</span>
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
    do dispositivo. STF (Supremo Tribunal Federal) = vinculante;
    STJ (Superior Tribunal de Justiça) = persuasivo.</span>
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
  <span class="rel-ref">(Canaris, 1937–2021)</span>
  <span class="rel-desc">Normas que se reforçam mutuamente,
    formando sistema coerente.</span>
</div>
<div class="rel-item">
  <span class="rel-line rel-dash-red"></span>
  <span class="rel-label">Antinomia</span>
  <span class="rel-ref">(Bobbio, 1909–2004)</span>
  <span class="rel-desc">Conflito normativo real — aplicação simultânea
    gera insegurança jurídica. Resolve-se por <em>lex superior</em>,
    <em>lex posterior</em> ou <em>lex specialis</em>.</span>
</div>
""", unsafe_allow_html=True)

if not selected_themes:
    st.warning("Nenhum tema selecionado. Marque pelo menos um tema na barra lateral.")
    st.stop()
if not selected_types:
    st.warning("Nenhum tipo de norma selecionado. Marque pelo menos um tipo na barra lateral.")
    st.stop()

G = build_compliance_graph(themes=selected_themes, norm_types=selected_types)

if len(G.nodes) == 0:
    st.warning("Nenhuma norma encontrada com os filtros selecionados.")
    st.stop()

undirected_G = G.to_undirected()
num_componentes = nx.number_connected_components(undirected_G)

col1, col2, col3 = st.columns(3)
col1.metric("Nós visíveis", len(G.nodes))
col2.metric("Conexões visíveis", len(G.edges))
col3.metric("Componentes conectados", num_componentes)

# ---- Grafo PyVis com hierarquia espacial ----
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
    "hierarquia":        "HIERARQUIA",
    "intersecao":        "INTERSEÇÃO",
    "antinomia":         "ANTINOMIA",
    "complementaridade": "COMPLEMENTAR",
    "regulamenta":       "REGULAMENTA",
    "interpreta":        "INTERPRETA",
}

# Calcular posição Y baseada na hierarquia normativa
# CF/88 no topo — y menor = mais alto no vis.js (coordenadas invertidas)
LEVEL_Y = {0: -600, 1: -300, 2: -100, 3: 150, 4: 400}

for node_id in G.nodes:
    d = G.nodes[node_id]
    node_type = d.get("tipo", "")

    # Tamanho por tipo
    size_map = {
        "constituicao": 55, "lei": 35, "jurisprudencia": 25,
        "orgao": 28, "decreto": 30, "norma_regulamentar": 30,
        "pl": 22, "documento_internacional": 28,
    }
    node_size = size_map.get(node_type, 28)

    # Forma geométrica
    shape = NODE_SHAPES.get(node_type, "dot")

    # Posição Y hierárquica
    level = HIERARCHY_LEVELS.get(node_type, 3)
    y_pos = LEVEL_Y.get(level, 0)

    # Tooltip texto puro
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
            "border":     d.get("color", "#888888"),
        },
        size=node_size,
        shape=shape,
        y=y_pos,
        physics=True,
    )

for u, v, d in G.edges(data=True):
    edge_tipo  = d.get("tipo", "")
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
        color={"color": d.get("color", "#888888"),
               "highlight": "#ffffff", "hover": "#ffffff"},
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
        font-family: monospace !important;
        font-size: 12px !important;
        line-height: 1.65 !important;
        padding: 10px 14px !important;
        background: rgba(10,9,18,0.97) !important;
        border: 1px solid rgba(212,168,83,0.5) !important;
        border-radius: 6px !important;
        color: #e8e4dc !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.7) !important;
        pointer-events: none !important;
    }
    .vis-navigation { position:absolute !important; bottom:16px !important; left:16px !important; }
    .vis-navigation .vis-button {
        background: rgba(15,14,24,0.92) !important;
        border: 1px solid rgba(212,168,83,0.4) !important;
        border-radius: 6px !important;
        width: 32px !important; height: 32px !important;
        display:flex !important; align-items:center !important;
        justify-content:center !important; cursor:pointer !important;
        transition: all 0.2s ease !important;
    }
    .vis-navigation .vis-button:hover {
        background: rgba(212,168,83,0.2) !important;
        border-color: #d4a853 !important;
        transform: scale(1.08) !important;
    }
    .vis-navigation .vis-button.vis-up:after    { content:"▲" !important; color:#d4a853 !important; font-size:14px !important; font-weight:bold !important; }
    .vis-navigation .vis-button.vis-down:after  { content:"▼" !important; color:#d4a853 !important; font-size:14px !important; font-weight:bold !important; }
    .vis-navigation .vis-button.vis-left:after  { content:"◀" !important; color:#d4a853 !important; font-size:14px !important; font-weight:bold !important; }
    .vis-navigation .vis-button.vis-right:after { content:"▶" !important; color:#d4a853 !important; font-size:14px !important; font-weight:bold !important; }
    .vis-navigation .vis-button.vis-zoomIn:after     { content:"+" !important; color:#d4a853 !important; font-size:18px !important; font-weight:bold !important; }
    .vis-navigation .vis-button.vis-zoomOut:after    { content:"−" !important; color:#d4a853 !important; font-size:18px !important; font-weight:bold !important; }
    .vis-navigation .vis-button.vis-zoomExtends:after{ content:"⌖" !important; color:#d4a853 !important; font-size:14px !important; font-weight:bold !important; }
    .vis-navigation .vis-button:hover:after { color:#ffffff !important; }
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
                    "- **" + inter["tipo_relacao"] + "** com `"
                    + inter["outro_no"] + "`"
                )
                st.markdown("  " + inter["descricao"])
                st.markdown("  *" + inter["artigos"] + "*")
        else:
            st.markdown("Nenhuma conexão encontrada com os filtros atuais.")

render_footer()
