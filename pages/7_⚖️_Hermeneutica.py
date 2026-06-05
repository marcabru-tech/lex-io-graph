import streamlit as st
from lib.constants import APP_NAME, APP_SUBTITLE, APP_VERSION
from lib.hermeneutica import (
    CORRENTES_HERMENEUTICAS, FONTES_DIREITO, ARCO_CC, BRASIL_IMPERIO
)
from lib.footer import render_footer

st.set_page_config(
    page_title=f"{APP_NAME} — Hermenêutica e Fontes do Direito",
    layout="wide",
    page_icon="⚖️"
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
    .herm-card {
        background: rgba(212,168,83,0.05);
        border: 1px solid rgba(212,168,83,0.2);
        border-radius: 8px; padding: 16px; margin-bottom: 14px;
    }
    .herm-nome   { color: #d4a853; font-size:15px; font-weight:bold; font-family:monospace; }
    .herm-autor  { color: #9b59b6; font-size:12px; font-family:monospace; margin: 4px 0; }
    .herm-obra   { color: #3dc8e6; font-size:11px; font-style:italic; margin: 4px 0; }
    .herm-princ  { color: #e8e4dc; font-size:13px; line-height:1.7; margin: 8px 0; }
    .herm-critica{ color: #706a60; font-size:11px; line-height:1.6; margin-top: 6px; }
    .herm-brasil { color: #3dc8e6; font-size:11px; line-height:1.6; margin-top: 6px; }
    .herm-tensao { color: #c44b4b; font-size:10px; font-family:monospace; margin-top: 6px; }
    .fonte-card {
        background: rgba(61,200,230,0.04);
        border-left: 3px solid;
        padding: 12px 16px; margin-bottom: 10px; border-radius: 0 6px 6px 0;
    }
    .fonte-nome  { font-size:14px; font-weight:bold; font-family:monospace; }
    .fonte-desc  { color: #b8b2a6; font-size:12px; line-height:1.7; margin: 6px 0; }
    .fonte-ex    { color: #3dc8e6; font-size:11px; }
    .fonte-latim { color: #d4a853; font-size:10px; font-style:italic; margin-top:4px; }
    .cc-card {
        background: rgba(30,173,156,0.05);
        border: 1px solid rgba(30,173,156,0.2);
        border-radius: 8px; padding: 14px; margin-bottom: 12px;
    }
    .cc-ano    { color: #1abc9c; font-size:18px; font-weight:bold; font-family:monospace; }
    .cc-nome   { color: #e8e4dc; font-size:14px; font-weight:bold; margin-left: 10px; }
    .cc-ctx    { color: #706a60; font-size:11px; font-style:italic; margin: 4px 0; }
    .cc-char   { color: #b8b2a6; font-size:12px; line-height:1.7; margin: 8px 0; }
    .cc-inf    { color: #9b59b6; font-size:11px; }
    .imp-card {
        background: rgba(212,168,83,0.04);
        border: 1px solid rgba(212,168,83,0.15);
        border-radius: 8px; padding: 14px; margin-bottom: 12px;
    }
    .imp-ano     { color: #d4a853; font-size:16px; font-weight:bold; font-family:monospace; }
    .imp-nome    { color: #e8e4dc; font-size:13px; font-weight:bold; margin-left:8px; }
    .imp-dest    { color: #3dc8e6; font-size:11px; font-style:italic; margin: 4px 0; }
    .imp-desc    { color: #b8b2a6; font-size:12px; line-height:1.7; margin: 8px 0; }
    .section-divider {
        border: none; border-top: 1px solid rgba(212,168,83,0.2);
        margin: 32px 0 24px 0;
    }
    .lexiograph-value {
        background: rgba(212,168,83,0.08);
        border: 1px solid rgba(212,168,83,0.3);
        border-radius: 8px; padding: 20px; margin: 20px 0;
        font-family: monospace; font-size: 12px; color: #b8b2a6; line-height: 1.9;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚖️ Hermenêutica e Fontes do Direito")
st.markdown(
    f'<div class="app-subtitle">{APP_NAME} · {APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)
st.markdown(
    "A camada hermenêutica como pano de fundo permanente do ordenamento — "
    "é ela que explica por que as tensões do grafo existem. "
    "Sem hermenêutica, o mapa normativo é estático; com ela, é vivo."
)

secao = st.radio(
    "Seção",
    [
        "🔍 Correntes Hermenêuticas",
        "📐 Fontes do Direito",
        "📜 Arco Histórico do Código Civil",
        "👑 Brasil Império",
        "✨ O Valor Epistemológico do Lex-IO-Graph"
    ],
    horizontal=False,
    label_visibility="collapsed"
)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# =============================================================
# SEÇÃO 1 — Correntes hermenêuticas
# =============================================================
if secao == "🔍 Correntes Hermenêuticas":
    st.markdown("## Correntes Hermenêuticas")
    st.markdown(
        "A divergência interpretativa não é erro do sistema — é o sistema funcionando. "
        "As correntes hermenêuticas são vozes simultâneas que coexistem "
        "na jurisprudência brasileira — polifonia bakhtiniana (Bakhtin, 1895–1975) "
        "em ação permanente. Cada tensão do grafo tem uma corrente hermenêutica dominante."
    )

    for c in CORRENTES_HERMENEUTICAS:
        st.markdown(f"""
<div class="herm-card">
  <div class="herm-nome">{c['nome']}</div>
  <div class="herm-autor">{c['autor_principal']} ({c['datas']})</div>
  <div class="herm-obra">📖 {c['obra']}</div>
  <div class="herm-princ">{c['principio']}</div>
</div>""", unsafe_allow_html=True)

        with st.expander(f"Métodos, crítica e aplicação no Brasil — {c['autor_principal']}"):
            st.markdown("**Métodos:**")
            for m in c['metodos']:
                st.markdown(f"- {m}")
            st.markdown(
                f'<div class="herm-critica">⚡ Crítica: {c["critica"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="herm-brasil">🇧🇷 No Brasil: {c["no_brasil"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="herm-tensao">⚖️ Tensão normativa: {c["tensao_norma"]}</div>',
                unsafe_allow_html=True
            )

# =============================================================
# SEÇÃO 2 — Fontes do direito
# =============================================================
elif secao == "📐 Fontes do Direito":
    st.markdown("## Fontes do Direito Brasileiro")
    st.markdown(FONTES_DIREITO['introducao'])
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    for fonte in FONTES_DIREITO['fontes']:
        cor = fonte['cor']
        st.markdown(f"""
<div class="fonte-card" style="border-left-color:{cor};">
  <div class="fonte-nome" style="color:{cor};">{fonte['nome']}</div>
  <div class="fonte-desc">{fonte['descricao']}</div>
  <div class="fonte-ex">📱 Digital: {fonte['exemplo_digital']}</div>
  <div class="fonte-latim">*{fonte['latim']}*</div>
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 3 — Arco histórico CC
# =============================================================
elif secao == "📜 Arco Histórico do Código Civil":
    st.markdown("## Arco Histórico do Código Civil Brasileiro")
    st.markdown(ARCO_CC['introducao'])
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    for cc in ARCO_CC['codigos']:
        st.markdown(f"""
<div class="cc-card">
  <span class="cc-ano">{cc['ano']}</span>
  <span class="cc-nome">{cc['nome']}</span>
  <div class="cc-ctx">{cc['contexto']} · Vigência: {cc['vigencia']}</div>
  <div class="cc-char">{cc['caracteristica']}</div>
  <div class="cc-inf">📚 Influências: {cc['influencia']}</div>
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 4 — Brasil Império
# =============================================================
elif secao == "👑 Brasil Império":
    st.markdown("## Brasil Império como Camada do Ordenamento")
    st.markdown(BRASIL_IMPERIO['introducao'])
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    for marco in BRASIL_IMPERIO['marcos']:
        st.markdown(f"""
<div class="imp-card">
  <span class="imp-ano">{marco['ano']}</span>
  <span class="imp-nome">{marco['nome']}</span>
  <div class="imp-dest">🔑 {marco['destaque']}</div>
  <div class="imp-desc">{marco['descricao']}</div>
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 5 — Valor epistemológico do Lex-IO-Graph
# =============================================================
elif secao == "✨ O Valor Epistemológico do Lex-IO-Graph":
    st.markdown("## O Valor Epistemológico do Lex-IO-Graph")

    st.markdown("""
<div class="lexiograph-value">
<strong style="color:#d4a853;font-size:14px;">
O Lex-IO-Graph é o único atlas jurídico brasileiro que articula explicitamente
sete camadas simultâneas de inteligência:
</strong><br><br>

<strong style="color:#3dc8e6;">1. Norma positiva</strong> — o fato jurídico bruto: texto, hierarquia, status<br>
<strong style="color:#9b59b6;">2. Hermenêutica</strong> — a corrente interpretativa que molda o sentido da norma<br>
<strong style="color:#d4a853;">3. Inventário pancrônico</strong> — o arco histórico completo acessível simultaneamente<br>
<strong style="color:#2ecc71;">4. Direito comparado glocal</strong> (global + local, Robertson, 1990s) — a norma brasileira no campo mundial<br>
<strong style="color:#e67e22;">5. Multissemiose</strong> — literatura, arte, latim como camadas de fundamentação<br>
<strong style="color:#c44b4b;">6. Inteligência estratégica</strong> — o jogo de forças por trás da norma<br>
<strong style="color:#1abc9c;">7. Epistemologia do direito</strong> — de onde vem o conhecimento jurídico, como se forma, como se valida<br><br>

<strong style="color:#e8e4dc;">A interseção que nenhuma equipe de TI ou escritório de advocacia replicam sozinhos:</strong><br>
Schleiermacher → Dilthey → Gadamer → Habermas → Dworkin como arco epistemológico.<br>
Direito natural → positivo → tridimensional (Reale) como arco ontológico.<br>
Glosadores de Bolonha → comentadores → pandectistas → codificadores como arco metodológico.<br>
Bakhtin como método editorial — o ordenamento como sistema polifônico.<br><br>

<strong style="color:#d4a853;">O grafo não descreve o direito — compreende-o</strong>
(Verstehen, Dilthey, 1833–1911).<br>
<em style="color:#454040;">Lex-IO-Graph · Lexiograph | Hubstry Deep Tech · Rio de Janeiro · 2026</em>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### Fosso competitivo")
    st.markdown(
        "O que uma equipe de TI + advogados levaria para replicar este sistema:"
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Tempo mínimo estimado:**
- Mapear o corpus doutrinário: 3–6 meses
- Construir o arco histórico pancrônico: 2–4 meses
- Hermenêutica + epistemologia: 2–3 meses
- Multissemiose (literatura + arte): 1–2 meses
- Inteligência estratégica atualizada: contínuo
- **Total: 8–15 meses de equipe multidisciplinar**
""")
    with col2:
        st.markdown("""
**O que não se contrata:**
- 30 anos de repertório jurídico-filosófico
- Síntese tripartite: científico + artístico + empreendedor
- Capacidade de articular Bakhtin, Fuller e o Decreto 12.975/2026
  na mesma frase com precisão técnica
- O olhar pancrônico que conecta os glosadores de Bolonha
  ao ECA Digital de 2025
- **Esse perfil se forma — não se compra**
""")

render_footer()
