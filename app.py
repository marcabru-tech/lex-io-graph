import streamlit as st
from lib.graph_builder import build_compliance_graph, load_json

st.set_page_config(
    page_title="Lexiograph Compliance Map",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { font-family: monospace; }
    .pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .pill--lex { background: rgba(212,168,83,0.15); color: #d4a853; border: 1px solid rgba(212,168,83,0.3); }
    .pill--io { background: rgba(61,200,230,0.15); color: #3dc8e6; border: 1px solid rgba(61,200,230,0.3); }
    .pill--graph { background: rgba(196,75,75,0.15); color: #c44b4b; border: 1px solid rgba(196,75,75,0.3); }
    .norma-item {
        padding: 16px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .norma-item:last-child { border-bottom: none; }
    .norma-ementa {
        font-size: 13px;
        color: #b8b2a6;
        line-height: 1.7;
        margin-top: 4px;
    }
    .norma-artigos {
        font-size: 11px;
        color: #706a60;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        "<h1 style='text-align:center; font-size: 2.8rem; letter-spacing: 0.04em; "
        "background: linear-gradient(135deg, #c44b4b, #d4a853, #3dc8e6); "
        "-webkit-background-clip: text; background-clip: text; color: transparent;'>"
        "Lexiograph</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-size: 14px; color: #706a60; letter-spacing: 0.15em; text-transform: uppercase;'>"
        "Compliance Map — Ordenamento Jurídico Digital Brasileiro</p>",
        unsafe_allow_html=True,
    )

st.divider()

G = build_compliance_graph()
raw_edges = load_json("arestas.json")["edges"]
raw_juris = load_json("jurisprudencia.json")["jurisprudencia"]

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Normas mapeadas", len(G.nodes))
col_b.metric("Conexões normativas", len(raw_edges))
col_c.metric("Jurisprudência vinculada", len(raw_juris))
col_d.metric("Temas regulatórios", 6)

st.divider()

st.markdown("""
### Sobre este mapa

Este dashboard interativo mapeia as **conexões, hierarquias e interseções** do ordenamento
jurídico digital brasileiro — da Constituição Federal às normas regulamentares, passando
por legislação ordinária, projetos de lei e jurisprudência dos tribunais superiores.

**Foco de aplicação:** empresas que contratam desenvolvedores júnior e precisam mitigar
riscos regulatórios em suas entregas técnicas.
""")

st.markdown("#### Normas mapeadas")

normas_data = load_json("normas.json")["nodes"]

for node in normas_data:
    tipo = node["tipo"]
    if tipo == "constituicao":
        pill_class = "pill--lex"
    elif tipo == "jurisprudencia":
        pill_class = "pill--graph"
    else:
        pill_class = "pill--io"

    ementa_completa = node["ementa"]
    artigos = node.get("artigos_chave", [])
    artigos_str = " | ".join(artigos) if artigos else ""

    item_html = '<div class="norma-item">'
    item_html += '<span class="pill ' + pill_class + '">' + node["sigla"] + '</span> '
    item_html += '<strong>' + node["nome"] + '</strong>'
    item_html += '<div class="norma-ementa">' + ementa_completa + '</div>'
    if artigos_str:
        item_html += '<div class="norma-artigos">' + artigos_str + '</div>'
    item_html += '</div>'

    st.markdown(item_html, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
#### Como navegar

| Página | O que você encontra |
|--------|-------------------|
| **Grafo Normativo** | Visualização interativa do mapa de conexões entre normas |
| **Matriz de Compliance** | Tabela cruzada: empresas × normas com nível de risco |
| **Comparação Normativa** | Análise lado a lado de pares de normas |
| **Radar de Riscos** | Mapa de calor das exposições de dev júnior |

> *Gramática semiótica dos sistemas digitais — Lexiograph, 2025*
""")