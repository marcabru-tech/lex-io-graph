import streamlit as st
from lib.constants import APP_NAME, APP_SUBTITLE, APP_VERSION
from lib.repositorio import AUTORES, BROCARDOS, TRADICOES_JURIDICAS
from lib.footer import render_footer

st.set_page_config(
    page_title=f"{APP_NAME} — Repositório de Conhecimento",
    layout="wide",
    page_icon="📚"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { min-width: 280px; }
    .block-container { padding-top: 2rem; }
    .app-subtitle {
        font-family: monospace; font-size: 11px; color: #706a60;
        letter-spacing: 0.06em; line-height: 1.6;
        margin-top: -8px; margin-bottom: 16px; max-width: 800px;
    }
    .autor-card {
        background: rgba(212,168,83,0.06);
        border: 1px solid rgba(212,168,83,0.2);
        border-radius: 8px; padding: 16px; margin-bottom: 12px;
    }
    .autor-nome { color: #d4a853; font-size: 16px; font-weight: bold; font-family: monospace; }
    .autor-datas { color: #706a60; font-size: 12px; font-family: monospace; margin-left: 8px; }
    .autor-obra { color: #3dc8e6; font-size: 12px; font-family: monospace; margin: 6px 0; }
    .autor-corrente { color: #9b59b6; font-size: 11px; font-family: monospace; }
    .autor-contrib { color: #e8e4dc; font-size: 13px; line-height: 1.6; margin: 8px 0; }
    .autor-brasil { color: #8a8478; font-size: 11px; line-height: 1.5; }
    .latim-original { color: #d4a853; font-size: 15px; font-style: italic; font-family: monospace; }
    .latim-lit { color: #706a60; font-size: 12px; margin: 4px 0; }
    .latim-jur { color: #e8e4dc; font-size: 13px; line-height: 1.6; margin: 6px 0; }
    .latim-ctx { color: #8a8478; font-size: 11px; }
    .latim-br  { color: #3dc8e6; font-size: 11px; margin-top: 4px; }
    .trad-card {
        background: rgba(61,200,230,0.05);
        border: 1px solid rgba(61,200,230,0.2);
        border-radius: 8px; padding: 16px; margin-bottom: 12px;
    }
    .trad-nome { color: #3dc8e6; font-size: 15px; font-weight: bold; font-family: monospace; }
    .trad-paises { color: #706a60; font-size: 11px; font-family: monospace; margin: 4px 0; }
    .section-divider {
        border: none; border-top: 1px solid rgba(212,168,83,0.2);
        margin: 32px 0 24px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"# 📚 Repositório de Conhecimento")
st.markdown(
    f'<div class="app-subtitle">{APP_NAME} · {APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)
st.markdown(
    "Inventário pancrônico de autores, brocardos latinos e tradições jurídicas "
    "que fundamentam o ordenamento jurídico digital brasileiro."
)

# ---- Navegação interna ----
secao = st.radio(
    "Seção",
    ["Inventário Doutrinário", "Latim Jurídico", "Direito Comparado Glocal"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# =============================================================
# SEÇÃO 1 — Inventário doutrinário
# =============================================================
if secao == "Inventário Doutrinário":
    st.markdown("## Inventário Doutrinário")
    st.markdown(
        "Autores que fundamentam o sistema de inteligência jurídico-estratégica do Lex-IO-Graph. "
        "Metodologia pancrônica — o arco histórico completo acessível simultaneamente, "
        "sem hierarquia temporal. Dialogismo e polifonia bakhtinianos "
        "(Bakhtin, 1895–1975) como método epistemológico."
    )

    # Filtro por corrente
    correntes = sorted(set(a["corrente"] for a in AUTORES.values()))
    corrente_sel = st.selectbox(
        "Filtrar por corrente hermenêutica",
        ["Todas"] + correntes
    )

    for key, autor in AUTORES.items():
        if corrente_sel != "Todas" and autor["corrente"] != corrente_sel:
            continue

        st.markdown(f"""
<div class="autor-card">
  <span class="autor-nome">{autor['nome']}</span>
  <span class="autor-datas">{autor['datas']} · {autor['nacionalidade']}</span><br>
  <div class="autor-obra">📖 {autor['obra_principal']}</div>
  <div class="autor-corrente">⚖ {autor['corrente']}</div>
  <div class="autor-contrib">{autor['contribuicao']}</div>
  <div class="autor-brasil">🇧🇷 Relevância no Brasil: {autor['relevancia_brasil']}</div>
</div>
""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 2 — Latim jurídico
# =============================================================
elif secao == "Latim Jurídico":
    st.markdown("## Latim Jurídico")
    st.markdown(
        "Brocardos do direito romano com tradução literal, tradução jurídica, "
        "contexto histórico e uso atual na jurisprudência brasileira. "
        "O direito romano não é passado — é substrato vivo do ordenamento. "
        "Corpus Iuris Civilis de Justiniano (533 d.C.) como fonte primária."
    )

    busca = st.text_input("Buscar brocardo", placeholder="ex: lex, habeas, pacta...")

    for b in BROCARDOS:
        if busca and busca.lower() not in b['original'].lower() and busca.lower() not in b['traducao_juridica'].lower():
            continue

        with st.expander(f"*{b['original']}*"):
            st.markdown(f"""
<div class="latim-lit">Tradução literal: {b['traducao_literal']}</div>
<div class="latim-jur">{b['traducao_juridica']}</div>
<div class="latim-ctx">📜 Contexto romano: {b['contexto_romano']}</div>
<div class="latim-br">🇧🇷 Uso no Brasil: {b['uso_brasil']}</div>
""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 3 — Direito comparado glocal
# =============================================================
elif secao == "Direito Comparado Glocal":
    st.markdown("## Direito Comparado Glocal")
    st.markdown(
        "Glocal (global + local, Robertson, 1990s) — o direito brasileiro em diálogo "
        "com tradições jurídicas mundiais. Metodologia: "
        "identificar a norma brasileira, localizar sua inspiração glocal, "
        "mapear convergências e divergências, extrair o vetor estratégico."
    )

    for key, trad in TRADICOES_JURIDICAS.items():
        st.markdown(f"""
<div class="trad-card">
  <div class="trad-nome">{trad['nome']}</div>
  <div class="trad-paises">Países: {', '.join(trad['paises'])}</div>
  <div class="autor-contrib" style="margin-top:8px;">{trad['caracteristicas']}</div>
  <div class="latim-br" style="margin-top:6px;">🇧🇷 Brasil: {trad['brasil']}</div>
  <div class="latim-ctx" style="margin-top:4px;">📚 Referências: {trad['codigos_referencia']}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### Comparações normativas glocais")

    comparacoes = [
        {
            "titulo": "Proteção de dados pessoais",
            "normas": [
                ("🇧🇷 Brasil", "LGPD — Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018)", "Inspirada no GDPR. Efeito territorial. ANPD como autoridade supervisora."),
                ("🇪🇺 União Europeia", "GDPR — General Data Protection Regulation (2016)", "Efeito extraterritorial — empresas brasileiras com usuários europeus estão sujeitas. Multas de até 4% do faturamento global."),
                ("🇺🇸 Califórnia/EUA", "CCPA — California Consumer Privacy Act (2018)", "Direito à não venda de dados pessoais. Abordagem setorial americana — sem lei federal equivalente ao GDPR."),
            ]
        },
        {
            "titulo": "Responsabilidade de plataformas digitais",
            "normas": [
                ("🇧🇷 Brasil", "Marco Civil da Internet art. 19 (Lei 12.965/2014) + Decretos 12.975 e 12.976/2026", "Art. 19 declarado parcialmente inconstitucional (STF Tema 987, 2025). Regime em transição — 24+ PDLs da oposição."),
                ("🇪🇺 União Europeia", "DSA — Digital Services Act (2022)", "Deveres proativos para plataformas de grande porte. Notice-and-takedown sem ordem judicial. Modelo que o Brasil está convergindo."),
                ("🇺🇸 EUA", "Section 230 — Communications Decency Act (1996)", "Imunidade ampla das plataformas por conteúdo de terceiros — sob pressão similar ao art. 19 brasileiro."),
            ]
        },
        {
            "titulo": "Codificação civil — arco histórico pancrônico",
            "normas": [
                ("🇧🇷 Brasil", "CC/1916 → CC/2002 → Reforma 2025 (PL 4/2025)", "CC/1916 influenciado pelo BGB alemão. CC/2002 absorveu o Código Comercial de 1850 (Lei 556 — Brasil Império). Reforma 2025 resgata Pontes de Miranda e cria Livro VI — Direito Civil Digital."),
                ("🇩🇪 Alemanha", "BGB — Bürgerliches Gesetzbuch (1896) + HGB — Handelsgesetzbuch (1897)", "Código Civil e Código Comercial separados e vigentes — modelo oposto ao Brasil que unificou em 2002."),
                ("🇮🇹 Itália", "Codice Civile (1942)", "Unificou civil e comercial — mesmo caminho do Brasil, mas 60 anos antes."),
                ("🇫🇷 França", "Code Civil (1804 — Código Napoleônico)", "Manteve separação com o Code de Commerce (1807, inspiração do Código Comercial brasileiro de 1850)."),
            ]
        }
    ]

    for comp in comparacoes:
        with st.expander(f"🌐 {comp['titulo']}"):
            for pais, norma, desc in comp['normas']:
                st.markdown(f"**{pais}** — {norma}")
                st.markdown(f"<div class='autor-brasil'>{desc}</div>", unsafe_allow_html=True)
                st.markdown("---")

render_footer()
