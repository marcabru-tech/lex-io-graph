import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import json

from lib.curadoria import render_principio_curadoria
from lib.conformidade import (
    render_disclaimer,
    render_questionario,
    gerar_radar,
    render_radar,
    gerar_relatorio_html,
    render_botao_limpar,
    render_disclaimer_rodape,
)
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

st.markdown("""<style>
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
</style>""", unsafe_allow_html=True)

st.markdown("# Lex-IO-Graph")
st.markdown(
    f'<div class="app-subtitle">{APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)

# ── Data loading ──
from pathlib import Path
DATA_DIR = Path("data")

@st.cache_data
def carregar_dados():
    with open(DATA_DIR / "normas.json", encoding="utf-8") as f:
        normas = json.load(f)["nodes"]
    with open(DATA_DIR / "arestas.json", encoding="utf-8") as f:
        arestas = json.load(f)["edges"]
    return normas, arestas

normas, arestas = carregar_dados()

# ═══════════════════════════════════════════════════════
# SEÇÃO 1 — GRAFO NORMATIVO
# ═══════════════════════════════════════════════════════

st.markdown("## 🕸️ Grafo Normativo Interativo")

with st.expander("📐 Por que grafo? — estatuto epistemológico"):
    st.markdown("""
O grafo tem estatuto epistemológico próprio, e a razão não é ilustrativa. Na forma
discursiva, a arquitetura de relações precisa ser reconstruída pelo leitor ao longo da
sucessão de enunciados; no grafo, ela é o próprio objeto — modelada explicitamente e,
portanto, percorrível, verificável e computável. O ganho não é dispensar a
interpretação, mas torná-la rastreável; e não é expressivo — todo grafo se reduz
formalmente a relações binárias —, mas inferencial: centralidade, ciclos, caminhos,
componentes e dependências são consequências obtidas por operação sobre a topologia,
sem que cada uma exija a reconstrução discursiva de uma cadeia argumentativa
distribuída.

Não se trata de intuição sem precedente: Charles Sanders Peirce construiu, nos Grafos
Existenciais, uma lógica diagramática dotada de regras próprias de inferência; Gilles
Deleuze e Félix Guattari pensaram o rizoma como forma de conexão sem centro organizador
único. Minha hipótese é mais específica: o grafo oferece a mediação formal entre a
descrição da complexidade — no sentido de Edgar Morin e das teorias dos sistemas
complexos — e sua operacionalização em sistemas de decisão.

É o que sustento no Lex-IO-Graph, onde o campo normativo, feito de remissões,
vigências, revogações parciais, competências, exceções e antinomias, é irredutível à
subsunção linear porque é **derrotável**: exceções não se acrescentam simplesmente à
cadeia; elas reconfiguram a topologia de aplicabilidade, prevalência e efeito.

Não por acaso, automações como as do n8n, orquestradores como o Apache Airflow e os
grafos computacionais do aprendizado profundo convergem para formas relacionais: não
porque a máquina leia grafos melhor do que texto, mas porque, para ser executável, o
texto precisa tornar explícitas relações que nele permanecem distribuídas e implícitas
— e essa estrutura tem forma de grafo.
""")

    st.markdown("---")
    st.caption("""
**Nota bibliográfica.** Sobre os Grafos Existenciais, ver PEIRCE, Charles S. *Logic of
the Future: Writings on Existential Graphs*. Ed. Ahti-Veikko Pietarinen. Berlin/Boston:
Mouton De Gruyter, 2019–2025, 3 v. em 5 t.; cf. PEIRCE, Charles S. *Collected Papers of
Charles Sanders Peirce*. Ed. Charles Hartshorne e Paul Weiss. Cambridge, MA: Harvard
University Press, 1933, v. 4. Sobre a dimensão inferencial do raciocínio diagramático e
a distinção entre dedução corolarial e teoremática, ver PEIRCE, Charles S. *The New
Elements of Mathematics*. Ed. Carolyn Eisele. The Hague: Mouton, 1976, v. 4; ROBERTS,
Don D. *The Existential Graphs of Charles S. Peirce*. The Hague: Mouton, 1973; SHIN,
Sun-Joo. *The Iconic Logic of Peirce's Graphs*. Cambridge, MA: MIT Press, 2002.
""")
st.markdown(
    "Mapa das normas do corpus e suas interseções calculadas pelo IPII Engine. "
    "Visualização interativa — arraste, zoom, passe o mouse para detalhes."
)

# ---- Sidebar ----
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
st.sidebar.markdown("**Legenda do grafo**")
st.sidebar.markdown("""
• Nós maiores = normas fundamentais\n
• CF/88 ancorada no topo\n
• Linhas sólidas = subordinação\n
• Linhas tracejadas = coordenação\n
• Passe o mouse sobre nós e arestas para detalhes\n
""")

_grafo_ok = bool(selected_themes and selected_types)
if not _grafo_ok:
    st.warning("Marque pelo menos um tema e um tipo de norma na barra lateral.")

if _grafo_ok:
    G = build_compliance_graph(themes=selected_themes, norm_types=selected_types)
    if len(G.nodes) == 0:
        st.warning("Nenhuma norma encontrada com os filtros selecionados.")
        _grafo_ok = False

if _grafo_ok:
    undirected_G = G.to_undirected()
    num_componentes = nx.number_connected_components(undirected_G)

    col1, col2, col3 = st.columns(3)
    col1.metric("Nós visíveis", len(G.nodes))
    col2.metric("Conexões visíveis", len(G.edges))
    col3.metric("Componentes conectados", num_componentes)

    col_b, col_m = st.columns([3, 1])
    with col_b:
        busca_texto = st.text_input(
            "Buscar norma",
            placeholder="ex: LGPD, Marco Civil, menores, IA...",
            label_visibility="collapsed"
        )
    with col_m:
        modo_viz = st.radio("Modo", ["🕸️ Grafo", "📋 Lista"],
                            horizontal=True, label_visibility="collapsed")

    nos_destacados = set()
    if busca_texto:
        for nid in G.nodes:
            nd = G.nodes[nid]
            texto = (nd.get("nome","") + " " + nd.get("label","") + " " +
                     nd.get("ementa","") + " " + " ".join(nd.get("temas",[]))).lower()
            if busca_texto.lower() in texto:
                nos_destacados.add(nid)
        if nos_destacados:
            st.success(f"{len(nos_destacados)} norma(s) encontrada(s) para '{busca_texto}'")
        else:
            st.warning(f"Nenhuma norma encontrada para '{busca_texto}'")

    if modo_viz == "📋 Lista":
        st.markdown("### Normas visíveis")
        for nid in sorted(G.nodes, key=lambda x: G.nodes[x].get("label",x)):
            nd = G.nodes[nid]
            destaque = nid in nos_destacados and bool(busca_texto)
            border_color = "#d4a853" if destaque else "rgba(255,255,255,0.08)"
            conexoes = len(list(G.edges(nid)))
            st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid {border_color};
    border-radius:6px;padding:12px 16px;margin-bottom:8px;">
    <span style="color:#d4a853;font-family:monospace;font-weight:bold;">{nd.get("label",nid)}</span>
    <span style="color:#706a60;font-size:11px;margin-left:8px;">
    {nd.get("tipo_label","")} · {nd.get("status","")} · {conexoes} conexão(ões)</span><br>
    <span style="color:#8a8478;font-size:12px;">{nd.get("ementa","")}</span>
    </div>""", unsafe_allow_html=True)

    if modo_viz == "🕸️ Grafo":
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
        LEVEL_Y = {0: -600, 1: -300, 2: -100, 3: 150, 4: 400}

        for node_id in G.nodes:
            d = G.nodes[node_id]
            node_type = d.get("tipo", "")
            size_map = {
                "constituicao": 55, "lei": 35, "jurisprudencia": 25,
                "orgao": 28, "decreto": 30, "norma_regulamentar": 30,
                "pl": 22, "documento_internacional": 28,
            }
            node_size = size_map.get(node_type, 28)
            shape = NODE_SHAPES.get(node_type, "dot")
            level = HIERARCHY_LEVELS.get(node_type, 3)
            y_pos = LEVEL_Y.get(level, 0)
            art = d.get("artigos_chave", [])
            art_txt = ""
            if art:
                art_txt = "\nArtigos: " + " | ".join(art[:4])
                if len(art) > 4:
                    art_txt += " ..."
            tip = (
                d.get("nome", "") + "\n"
                + "-" * 36 + "\n"
                + d.get("ementa", "") + "\n"
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
                color={"background": d.get("color", "#888888"), "border": d.get("color", "#888888")},
                size=node_size,
                shape=shape,
                y=y_pos,
                physics=True,
            )

        for u, v, d in G.edges(data=True):
            edge_tipo = d.get("tipo", "")
            edge_label = EDGE_TYPE_SHORT.get(edge_tipo, edge_tipo.upper())
            tip = (
                d.get("tipo_label", "") + "\n"
                + "-" * 36 + "\n"
                + d.get("descricao", "") + "\n"
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
                max-width: 400px !important; min-width: 180px !important;
                white-space: pre-wrap !important; word-break: break-word !important;
                font-family: monospace !important; font-size: 12px !important;
                line-height: 1.65 !important; padding: 10px 14px !important;
                background: rgba(10,9,18,0.97) !important;
                border: 1px solid rgba(212,168,83,0.5) !important;
                border-radius: 6px !important; color: #e8e4dc !important;
                box-shadow: 0 4px 24px rgba(0,0,0,0.7) !important;
                pointer-events: none !important;
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
        aba_factual, aba_doutrina, aba_conexoes = st.tabs([
            "📋 Factual", "📚 Doutrinário", "🔗 Conexões"
        ])
        with aba_factual:
            col_info, col_art = st.columns([1, 1])
            with col_info:
                st.markdown("#### " + nd.get("nome", ""))
                st.markdown("**Sigla:** " + nd.get("label", ""))
                st.markdown("**Tipo:** " + nd.get("tipo_label", ""))
                st.markdown("**Status:** " + nd.get("status", ""))
                st.markdown("**Órgão:** " + nd.get("orgao", ""))
                st.markdown("**Ano:** " + str(nd.get("ano", "")))
                st.markdown("**Ementa:** " + nd.get("ementa", ""))
            with col_art:
                art = nd.get("artigos_chave", [])
                if art:
                    st.markdown("**Artigos-chave:**")
                    for a in art:
                        st.markdown(f"- {a}")
                historia = nd.get("historia", "")
                if historia:
                    st.markdown("**Contexto histórico:**")
                    st.markdown(historia)
        with aba_doutrina:
            autores = nd.get("autores", [])
            latim = nd.get("latim", [])
            dir_comp = nd.get("direito_comparado", "")
            if autores:
                st.markdown("#### Autores e referências doutrinárias")
                for a in autores:
                    with st.expander(f"{a['nome']} ({a['datas']})"):
                        st.markdown(f"**Obra:** {a['obra']}")
                        st.markdown(f"**Contribuição:** {a['contribuicao']}")
            if latim:
                st.markdown("#### Latim jurídico")
                for l in latim:
                    with st.expander(f"*{l['original']}*"):
                        st.markdown(f"**Tradução literal:** {l['traducao_literal']}")
                        st.markdown(f"**Tradução jurídica:** {l['traducao_juridica']}")
                        st.markdown(f"**Contexto romano:** {l['contexto_romano']}")
            if dir_comp:
                st.markdown("#### Direito comparado glocal")
                st.markdown(dir_comp)
            if not autores and not latim and not dir_comp:
                st.info("Conteúdo doutrinário em elaboração para esta norma.")
        with aba_conexoes:
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

    # ═══════════════════════════════════════════════════════
# SEÇÃO 2 — QUADRO DE CONFORMIDADE
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## ⚖️ Quadro de Conformidade")
st.markdown(
    "Descubra quais normas se aplicam ao seu negócio, "
    "onde estão os riscos e o que fazer agora."
)

render_disclaimer()

render_principio_curadoria()

perfil, submitted = render_questionario()

if submitted:
    radar = gerar_radar(perfil, normas, arestas)
    st.session_state["radar_gerado"] = radar
    st.session_state["radar_perfil"] = perfil

if "radar_gerado" in st.session_state:
    render_radar(st.session_state["radar_gerado"])

    col_dl, col_clr = st.columns(2)
    with col_dl:
        html_rel = gerar_relatorio_html(
            st.session_state["radar_gerado"],
            st.session_state["radar_perfil"],
        )
        st.download_button(
            label="📄 Baixar Relatório (HTML)",
            data=html_rel,
            file_name="lexiograph-conformidade.html",
            mime="text/html",
            use_container_width=True,
        )
        st.caption("Abra no browser e use Ctrl+P → Salvar como PDF")
    with col_clr:
        render_botao_limpar()

    render_disclaimer_rodape()

render_footer()
