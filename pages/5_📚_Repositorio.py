import streamlit as st
from pathlib import Path
from lib.constants import APP_NAME, APP_SUBTITLE, APP_VERSION
from lib.repositorio import AUTORES, BROCARDOS, TRADICOES_JURIDICAS, MAGNIFICA_HUMANITAS
from lib.multisemiose import CITACOES, OBRAS_ARTE, GLOSSARIO
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
    .autor-nome  { color: #d4a853; font-size:16px; font-weight:bold; font-family:monospace; }
    .autor-datas { color: #706a60; font-size:12px; font-family:monospace; margin-left:8px; }
    .autor-obra  { color: #3dc8e6; font-size:12px; font-family:monospace; margin:6px 0; }
    .autor-corrente { color: #9b59b6; font-size:11px; font-family:monospace; }
    .autor-contrib  { color: #e8e4dc; font-size:13px; line-height:1.6; margin:8px 0; }
    .autor-brasil   { color: #8a8478; font-size:11px; line-height:1.5; }
    .latim-original { color: #d4a853; font-size:15px; font-style:italic; font-family:monospace; }
    .latim-lit { color: #706a60; font-size:12px; margin:4px 0; }
    .latim-jur { color: #e8e4dc; font-size:13px; line-height:1.6; margin:6px 0; }
    .latim-ctx { color: #8a8478; font-size:11px; }
    .latim-br  { color: #3dc8e6; font-size:11px; margin-top:4px; }
    .trad-card {
        background: rgba(61,200,230,0.05);
        border: 1px solid rgba(61,200,230,0.2);
        border-radius: 8px; padding: 16px; margin-bottom: 12px;
    }
    .trad-nome   { color: #3dc8e6; font-size:15px; font-weight:bold; font-family:monospace; }
    .trad-paises { color: #706a60; font-size:11px; font-family:monospace; margin:4px 0; }
    .cit-card {
        background: rgba(155,89,182,0.06);
        border: 1px solid rgba(155,89,182,0.25);
        border-radius: 8px; padding: 16px; margin-bottom: 14px;
    }
    .cit-autor { color: #9b59b6; font-size:15px; font-weight:bold; font-family:monospace; }
    .cit-obra  { color: #706a60; font-size:12px; font-family:monospace; margin:4px 0; }
    .cit-orig  { color: #d4a853; font-size:13px; font-style:italic; line-height:1.6; margin:8px 0; }
    .cit-trad  { color: #e8e4dc; font-size:13px; line-height:1.6; margin:4px 0; }
    .cit-jur   { color: #8a8478; font-size:12px; line-height:1.6; margin-top:8px; }
    .cit-uso   { color: #3dc8e6; font-size:11px; margin-top:6px; }
    .gloss-termo { color: #d4a853; font-size:15px; font-weight:bold; font-family:monospace; }
    .gloss-latim { color: #9b59b6; font-size:11px; font-style:italic; margin:4px 0; }
    .gloss-def   { color: #e8e4dc; font-size:13px; line-height:1.7; margin:8px 0; }
    .gloss-corr  { color: #706a60; font-size:11px; }
    .gloss-ex    { color: #3dc8e6; font-size:11px; margin-top:6px; }
    .section-divider {
        border: none; border-top: 1px solid rgba(212,168,83,0.2);
        margin: 32px 0 24px 0;
    }
    .bakhtin-footer {
        font-family: monospace; font-size: 11px; color: #454040;
        text-align: center; padding: 16px 0; line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📚 Repositório de Conhecimento")
st.markdown(
    f'<div class="app-subtitle">{APP_NAME} · {APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)
st.markdown(
    "Inventário pancrônico de autores, brocardos latinos, tradições jurídicas, "
    "citações literárias, obras de arte e glossário. "
    "Fundamento metodológico: dialogismo e polifonia bakhtinianos "
    "(Bakhtin, 1895–1975)."
)

secao = st.radio(
    "Seção",
    [
        "⚖️ Inventário Doutrinário",
        "📜 Latim Jurídico",
        "🌐 Direito Comparado Glocal",
        "📖 Literatura e Arte",
        "🔤 Glossário Jurídico",
        "📋 Magnifica Humanitas"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# =============================================================
# SEÇÃO 1 — Inventário doutrinário
# =============================================================
if secao == "⚖️ Inventário Doutrinário":
    st.markdown("## Inventário Doutrinário")
    st.markdown(
        "Metodologia pancrônica — o arco histórico completo acessível simultaneamente. "
        "Bakhtin (1895–1975): o ordenamento jurídico como sistema polifônico — "
        "Kelsen, Bobbio, Canaris, Gadamer e Dworkin como vozes coexistentes, não sequenciais."
    )
    correntes = sorted(set(a["corrente"] for a in AUTORES.values()))
    corrente_sel = st.selectbox("Filtrar por corrente hermenêutica", ["Todas"] + correntes)
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
  <div class="autor-brasil">🇧🇷 {autor['relevancia_brasil']}</div>
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 2 — Latim jurídico
# =============================================================
elif secao == "📜 Latim Jurídico":
    st.markdown("## Latim Jurídico")
    st.markdown(
        "O direito romano não é passado — é substrato vivo do ordenamento. "
        "Corpus Iuris Civilis de Justiniano (533 d.C.) como fonte primária. "
        "Ulpiano (170–228 d.C.): *Iuris praecepta sunt haec: honeste vivere, "
        "alterum non laedere, suum cuique tribuere.*"
    )
    busca = st.text_input("Buscar brocardo", placeholder="ex: lex, habeas, pacta...")
    for b in BROCARDOS:
        if busca and busca.lower() not in b['original'].lower() \
                and busca.lower() not in b['traducao_juridica'].lower():
            continue
        with st.expander(f"*{b['original']}*"):
            st.markdown(f"**Tradução literal:** {b['traducao_literal']}")
            st.markdown(f"**Tradução jurídica:** {b['traducao_juridica']}")
            st.markdown(f"<div class='latim-ctx'>📜 {b['contexto_romano']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='latim-br'>🇧🇷 {b['uso_brasil']}</div>", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 3 — Direito comparado glocal
# =============================================================
elif secao == "🌐 Direito Comparado Glocal":
    st.markdown("## Direito Comparado Glocal (global + local, Robertson, 1990s)")
    st.markdown(
        "O direito brasileiro em diálogo com tradições jurídicas mundiais. "
        "Metodologia: localizar a norma brasileira, identificar sua inspiração glocal, "
        "mapear convergências e divergências, extrair o vetor estratégico."
    )
    for key, trad in TRADICOES_JURIDICAS.items():
        st.markdown(f"""
<div class="trad-card">
  <div class="trad-nome">{trad['nome']}</div>
  <div class="trad-paises">Países: {', '.join(trad['paises'])}</div>
  <div class="autor-contrib" style="margin-top:8px;">{trad['caracteristicas']}</div>
  <div class="latim-br" style="margin-top:6px;">🇧🇷 {trad['brasil']}</div>
  <div class="latim-ctx" style="margin-top:4px;">📚 {trad['codigos_referencia']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### Comparações normativas glocais")
    comparacoes = [
        {
            "titulo": "Proteção de dados pessoais",
            "normas": [
                ("🇧🇷 Brasil", "LGPD — Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018)", "Inspirada no GDPR. ANPD como autoridade supervisora. Efeito territorial com exceções."),
                ("🇪🇺 União Europeia", "GDPR — General Data Protection Regulation (2016)", "Efeito extraterritorial — empresas brasileiras com usuários europeus estão sujeitas. Multas de até 4% do faturamento global."),
                ("🇺🇸 Califórnia/EUA", "CCPA — California Consumer Privacy Act (2018)", "Direito à não venda de dados pessoais. Abordagem setorial americana — sem lei federal equivalente ao GDPR."),
            ]
        },
        {
            "titulo": "Regulação de plataformas digitais",
            "normas": [
                ("🇧🇷 Brasil", "Marco Civil art. 19 + Decretos 12.975 e 12.976/2026", "Art. 19 parcialmente inconstitucional (STF Tema 987). Regime em transição — 24+ PDLs da oposição."),
                ("🇪🇺 União Europeia", "DSA — Digital Services Act (2022)", "Deveres proativos para plataformas de grande porte. Notice-and-takedown sem ordem judicial."),
                ("🇺🇸 EUA", "Section 230 — Communications Decency Act (1996)", "Imunidade ampla — sob pressão similar ao art. 19 brasileiro."),
            ]
        },
        {
            "titulo": "Regulação de IA (Inteligência Artificial)",
            "normas": [
                ("🇧🇷 Brasil", "PL 2.338/2023 — Marco Legal da IA (em tramitação)", "Abordagem por risco. Inspirado no EU AI Act. Mais avançado da América Latina."),
                ("🇪🇺 União Europeia", "EU AI Act (2024)", "Primeiro marco regulatório de IA do mundo. Proibições absolutas para IA de alto risco. Transparência algorítmica obrigatória."),
                ("🇨🇳 China", "Regulamento de IA Generativa (2023)", "Controle centralizado — alinhamento com valores socialistas. Registro obrigatório de modelos de IA."),
                ("🕊️ Vaticano", "Magnifica Humanitas — Leão XIV (25/05/2026)", "Dignidade humana como limite intransponível. IA deve ser 'desarmada' de lógicas de dominação."),
            ]
        },
        {
            "titulo": "Codificação civil — arco histórico pancrônico",
            "normas": [
                ("🇧🇷 Brasil", "CC/1916 → CC/2002 → Reforma 2025 (PL 4/2025)", "CC/2002 absorveu o Código Comercial de 1850. Reforma 2025 cria Livro VI — Direito Civil Digital."),
                ("🇩🇪 Alemanha", "BGB (1896) + HGB (1897) — separados e vigentes", "Modelo oposto ao Brasil: civil e comercial separados até hoje."),
                ("🇮🇹 Itália", "Codice Civile (1942)", "Unificou civil e comercial — mesmo caminho do Brasil, 60 anos antes."),
                ("🇫🇷 França", "Code Civil (1804) — Código Napoleônico", "Manteve separação com o Code de Commerce (1807)."),
            ]
        }
    ]
    for comp in comparacoes:
        with st.expander(f"🌐 {comp['titulo']}"):
            for pais, norma, desc in comp['normas']:
                st.markdown(f"**{pais}** — {norma}")
                st.markdown(f"<div class='autor-brasil'>{desc}</div>", unsafe_allow_html=True)
                st.markdown("---")

# =============================================================
# SEÇÃO 4 — Literatura e Arte
# =============================================================
elif secao == "📖 Literatura e Arte":
    st.markdown("## Literatura e Arte")
    st.markdown(
        "A literatura universal como instrumento de fundamentação jurídica — "
        "tradição dos grandes doutrinadores e da jurisprudência brasileira. "
        "Rui Barbosa citava Shakespeare no plenário. "
        "Pontes de Miranda citava Goethe. "
        "O STF tem Dostoiévski e Kafka em votos sobre devido processo legal."
    )

    aba_lit, aba_arte = st.tabs(["📚 Citações Literárias", "🖼️ Obras de Arte"])

    with aba_lit:
        normas_filter = st.multiselect(
            "Filtrar por norma relacionada",
            options=["cf88", "lgpd", "marco_civil", "eca", "eca_digital",
                     "pl_ia", "pl_cc_digital", "stf_tema987"],
            default=[],
            format_func=lambda x: {
                "cf88": "CF/88", "lgpd": "LGPD", "marco_civil": "Marco Civil",
                "eca": "ECA", "eca_digital": "ECA Digital", "pl_ia": "PL IA",
                "pl_cc_digital": "PL CC Digital", "stf_tema987": "STF Tema 987"
            }.get(x, x)
        )
        for cit in CITACOES:
            if normas_filter and not any(n in cit['normas_relacionadas'] for n in normas_filter):
                continue
            st.markdown(f"""
<div class="cit-card">
  <span class="cit-autor">{cit['autor']}</span>
  <span class="autor-datas"> {cit['datas']}</span><br>
  <div class="cit-obra">📖 {cit['obra']}</div>
  <div class="cit-orig">"{cit['citacao_original']}"</div>
  <div class="cit-trad">→ {cit['traducao']}</div>
  <div class="cit-jur">⚖️ {cit['contexto_juridico']}</div>
  <div class="cit-uso">🇧🇷 {cit['uso_jurisprudencia']}</div>
</div>""", unsafe_allow_html=True)

    with aba_arte:
        st.markdown(
            "*Obras em domínio público. A análise multissemiótica dispensa a reprodução da imagem.*"
        )
        for i in range(0, len(OBRAS_ARTE), 2):
            cols = st.columns(2)
            for j, obra in enumerate(OBRAS_ARTE[i:i+2]):
                with cols[j]:
                    st.markdown(f"""
<div style="margin-bottom:16px;">
  <strong style="color:#e8e4dc;">{obra['titulo']}</strong><br>
  <span style="color:#9b59b6;font-size:12px;font-family:monospace;">{obra['autor']} ({obra['datas_autor']})</span><br>
  <span style="color:#706a60;font-size:11px;font-style:italic;">{obra['tecnica']} · {obra['ano']} · {obra['localizacao']}</span>
</div>""", unsafe_allow_html=True)
                    with st.expander("Conexão jurídica"):
                        st.markdown(obra['descricao'])
                        st.markdown(obra['conexao_juridica'])

# =============================================================
# SEÇÃO 5 — Glossário
# =============================================================
elif secao == "🔤 Glossário Jurídico":
    st.markdown("## Glossário Jurídico")
    st.markdown(
        "Termos técnicos com etimologia, definição rigorosa, corrente hermenêutica "
        "e exemplo na jurisprudência brasileira. "
        "O glossário como camada semiótica do atlas — "
        "cada termo é um nó de significação no campo normativo."
    )
    busca_g = st.text_input("Buscar termo", placeholder="ex: antinomia, hermenêutica, glocal...")
    for g in GLOSSARIO:
        if busca_g and busca_g.lower() not in g['termo'].lower() \
                and busca_g.lower() not in g['definicao'].lower():
            continue
        with st.expander(g['termo']):
            st.markdown(f"""
<div class="gloss-latim">{g['latim']}</div>
<div class="gloss-def">{g['definicao']}</div>
<div class="gloss-corr">Corrente: {g['corrente']}</div>
<div class="gloss-ex">🇧🇷 {g['exemplo_brasil']}</div>
""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 6 — Magnifica Humanitas
# =============================================================
elif secao == "📋 Magnifica Humanitas":
    st.markdown("## Encíclica *Magnifica Humanitas* — Papa Leão XIV (2026)")
    st.markdown(
        f"**{MAGNIFICA_HUMANITAS['autor']}** · "
        f"{MAGNIFICA_HUMANITAS['data']} · "
        f"{MAGNIFICA_HUMANITAS['local']}"
    )
    st.markdown(f"**Tema central:** {MAGNIFICA_HUMANITAS['tema_central']}")
    with st.expander("Tese principal"):
        tese = MAGNIFICA_HUMANITAS['tese_principal']
        st.markdown(f"*{tese}*")
    with st.expander("Capítulos"):
        for cap in MAGNIFICA_HUMANITAS['capitulos']:
            st.markdown(f"- {cap}")
    with st.expander("Continuidade histórica pancrônica"):
        st.markdown(MAGNIFICA_HUMANITAS['continuidade_historica'])
    with st.expander("Convergência histórica — semana de 21–27 maio/2026"):
        st.markdown(MAGNIFICA_HUMANITAS['convergencia_maio_2026'])
    with st.expander("Presença da Anthropic no lançamento"):
        st.markdown(MAGNIFICA_HUMANITAS['presenca_anthropic'])
    with st.expander("Impacto no ordenamento jurídico brasileiro"):
        for item in MAGNIFICA_HUMANITAS['impacto_brasil']:
            st.markdown(f"- {item}")

# ---- Rodapé editorial Bakhtin ----
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="bakhtin-footer">
Fundamento metodológico: dialogismo e polifonia bakhtinianos — Mikhail Bakhtin (1895–1975)<br>
O ordenamento jurídico brasileiro como sistema polifônico: múltiplas vozes coexistindo em tensão produtiva<br>
sem fusão em voz única autoritária — legislador, juiz, doutrinador, literato, artista, estrategista<br>
<em>Lex-IO-Graph · Lexiograph | Hubstry Deep Tech · Rio de Janeiro · 2026</em>
</div>
""", unsafe_allow_html=True)

render_footer()
