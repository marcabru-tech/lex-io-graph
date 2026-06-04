"""
Lex Quantum — Compliance Map
Dashboard interativo de grafos para o ordenamento jurídico digital brasileiro.

Executar:
    streamlit run app.py

Deploy:
    Streamlit Community Cloud → conectar ao repositório GitHub
"""

import streamlit as st

st.set_page_config(
    page_title="Lex Quantum — Compliance Map",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- CSS customizado ----
st.markdown("""
<style>
    /* Tipografia e cores do Lexiograph */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=DM+Mono:wght@300;400&display=swap');

    :root {
        --lex: #d4a853;
        --io: #3dc8e6;
        --graph: #c44b4b;
    }

    .stApp {
        font-family: 'DM Mono', monospace;
    }

    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
    }

    .stMetric > div {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 8px;
        padding: 16px;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #0a0a12;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    /* Pilhas semânticas */
    .pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-family: 'DM Mono', monospace;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .pill--lex { background: rgba(212,168,83,0.15); color: #d4a853; border: 1px solid rgba(212,168,83,0.3); }
    .pill--io { background: rgba(61,200,230,0.15); color: #3dc8e6; border: 1px solid rgba(61,200,230,0.3); }
    .pill--graph { background: rgba(196,75,75,0.15); color: #c44b4b; border: 1px solid rgba(196,75,75,0.3); }
</style>
""", unsafe_allow_html=True)

# ---- Hero ----
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        "<h1 style='text-align:center; font-size: 2.8rem; letter-spacing: 0.04em; "
        "background: linear-gradient(135deg, #c44b4b, #d4a853, #3dc8e6); "
        "-webkit-background-clip: text; background-clip: text; color: transparent;'>"
        "Lex Quantum</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-family: DM Mono, monospace; font-size: 14px; "
        "color: #706a60; letter-spacing: 0.15em; text-transform: uppercase;'>"
        "Compliance Map — Ordenamento Jurídico Digital Brasileiro</p>",
        unsafe_allow_html=True,
    )

st.divider()

# ---- Métricas rápidas ----
from lib.graph_builder import build_compliance_graph, load_json

G = build_compliance_graph()
raw_edges = load_json("arestas.json")["edges"]
raw_juris = load_json("jurisprudencia.json")["jurisprudencia"]

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Normas mapeadas", len(G.nodes))
col_b.metric("Conexões normativas", len(raw_edges))
col_c.metric("Jurisprudência vinculada", len(raw_juris))
col_d.metric("Temas regulatórios", 6)

st.divider()

# ---- Apresentação ----
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
    elif tipo == "lei":
        pill_class = "pill--io"
    elif tipo == "jurisprudencia":
        pill_class = "pill--graph"
    else:
        pill_class = "pill--io"

    artigos = " · ".join(node.get("artigos_chave", []))
    artigos_html = f"<br><span style='font-size:12px; color:#706a60;'>{artigos}</span>" if artigos else ""

    st.markdown(
        f"<div style='padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);'>"
        f"<span class='pill {pill_class}'>{node['sigla']}</span> "
        f"<strong>{node['nome']}</strong>"
        f"<br><span style='font-size:13px; color:#b8b2a6;'>{node['ementa']}</span>"
        f"{artigos_html}"
        f"</div>",
        unsafe_allow_html=True,
    )

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
