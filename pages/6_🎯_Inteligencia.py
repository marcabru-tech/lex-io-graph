import streamlit as st
from lib.constants import APP_NAME, APP_SUBTITLE, APP_VERSION
from lib.inteligencia import CASOS_ESTRATEGICOS, EPISTEMOLOGIA, DIREITO_NATURAL
from lib.footer import render_footer

st.set_page_config(
    page_title=f"{APP_NAME} — Inteligência Estratégica",
    layout="wide",
    page_icon="🎯"
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
    .caso-card {
        background: rgba(196,75,75,0.06);
        border: 1px solid rgba(196,75,75,0.25);
        border-radius: 8px; padding: 16px; margin-bottom: 16px;
    }
    .caso-titulo { color: #c44b4b; font-size:16px; font-weight:bold; font-family:monospace; }
    .caso-status { color: #e67e22; font-size:11px; font-family:monospace; margin: 4px 0; }
    .caso-sintese { color: #e8e4dc; font-size:13px; line-height:1.7; margin: 10px 0; }
    .tensao-titulo { color: #d4a853; font-size:13px; font-weight:bold; margin: 12px 0 6px 0; }
    .tensao-analise { color: #b8b2a6; font-size:12px; line-height:1.8; }
    .prosp-label { color: #3dc8e6; font-size:11px; font-weight:bold; font-family:monospace; }
    .prosp-text  { color: #8a8478; font-size:11px; line-height:1.7; }
    .epist-card {
        background: rgba(155,89,182,0.06);
        border: 1px solid rgba(155,89,182,0.2);
        border-radius: 8px; padding: 14px; margin-bottom: 12px;
    }
    .epist-autor { color: #9b59b6; font-size:14px; font-weight:bold; font-family:monospace; }
    .epist-datas { color: #706a60; font-size:11px; margin-left:6px; }
    .epist-contrib { color: #e8e4dc; font-size:12px; line-height:1.7; margin: 8px 0; }
    .epist-dir { color: #3dc8e6; font-size:11px; line-height:1.6; }
    .nivel-critico  { color: #c44b4b; font-weight:bold; }
    .nivel-moderado { color: #e67e22; font-weight:bold; }
    .nivel-baixo    { color: #2ecc71; font-weight:bold; }
    .nivel-estrategico { color: #d4a853; font-weight:bold; }
    .section-divider {
        border: none; border-top: 1px solid rgba(212,168,83,0.2);
        margin: 32px 0 24px 0;
    }
    .disclaimer {
        font-family: monospace; font-size: 10px; color: #454040;
        line-height: 1.8; padding: 12px; margin-top: 16px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🎯 Inteligência Jurídico-Estratégica")
st.markdown(
    f'<div class="app-subtitle">{APP_NAME} · {APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)
st.markdown(
    "Análise do jogo de forças institucional, civilizatório e geopolítico "
    "por trás de cada tensão normativa. Estilo: analítico de consultoria — "
    "analítico, diagnóstico, acionável. "
    "O fato normativo como sintoma — a inteligência estratégica como diagnóstico."
)

secao = st.radio(
    "Seção",
    [
        "⚡ Casos Estratégicos",
        "🧠 Epistemologia do Direito",
        "⚖️ Direito Natural e Positivo",
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# =============================================================
# SEÇÃO 1 — Casos estratégicos
# =============================================================
if secao == "⚡ Casos Estratégicos":
    st.markdown("## Casos de Inteligência Estratégica")
    st.markdown(
        "Cada caso analisa: atores e interesses, vácuos normativos, "
        "vetores de força, consequências estratégicas e prospectiva "
        "12–36 meses. Fatos tratados como diagnóstico estratégico — "
        "sem tom acusatório ou framing conspiratório."
    )

    nivel_cores = {
        "crítico": "nivel-critico",
        "moderado": "nivel-moderado",
        "baixo": "nivel-baixo",
        "estratégico": "nivel-estrategico"
    }

    for caso in CASOS_ESTRATEGICOS:
        nivel_class = nivel_cores.get(caso['nivel_tensao'], "")
        st.markdown(f"""
<div class="caso-card">
  <div class="caso-titulo">{caso['titulo']}</div>
  <div class="caso-status">
    Status: {caso['status']} ·
    Tensão: <span class="{nivel_class}">{caso['nivel_tensao'].upper()}</span>
  </div>
  <div class="caso-sintese">{caso['sintese']}</div>
</div>""", unsafe_allow_html=True)

        with st.expander(f"Análise detalhada — {caso['titulo']}"):
            for camada in caso['camadas']:
                st.markdown(
                    f'<div class="tensao-titulo">{camada["titulo"]}</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="tensao-analise">{camada["analise"]}</div>',
                    unsafe_allow_html=True
                )
                st.markdown("")

            st.markdown("---")
            st.markdown("**Prospectiva**")
            prosp = caso['prospectiva']
            st.markdown(
                f'<div class="prosp-label">12 meses</div>'
                f'<div class="prosp-text">{prosp["12_meses"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="prosp-label">36 meses</div>'
                f'<div class="prosp-text">{prosp["36_meses"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="prosp-label">Lacuna remanescente</div>'
                f'<div class="prosp-text">{prosp["lacuna_remanescente"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown("""
<div class="disclaimer">
Voz analítica:
<a href="https://www.overall720.xyz/" target="_blank"
   style="color:#d4a853;text-decoration:none;">Overall 720°</a>
e
<a href="https://goncalvesetalii.github.io" target="_blank"
   style="color:#d4a853;text-decoration:none;">Gonçalves et Alii</a>
—
<a href="https://www.linkedin.com/company/overall-consultoria-720%C2%BA" target="_blank"
   style="color:#3dc8e6;text-decoration:none;">LinkedIn Overall 720°</a>
· Ambas ventures do ecossistema
<a href="https://hubstry.dev" target="_blank"
   style="color:#d4a853;text-decoration:none;">Hubstry Deep Tech</a>
— venture building bootstrapped, Rio de Janeiro.<br>
Diagnóstico estratégico baseado em fontes públicas.
Diagnóstico estratégico baseado em fontes públicas — não assessoria jurídica.<br>
Lex-IO-Graph · Lexiograph | Hubstry Deep Tech · Rio de Janeiro · 2026
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 2 — Epistemologia do direito
# =============================================================
elif secao == "🧠 Epistemologia do Direito":
    st.markdown("## Epistemologia do Direito")
    st.markdown(EPISTEMOLOGIA['introducao'])

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### Arco epistemológico")
    st.markdown(
        "Schleiermacher → Dilthey → Gadamer → Habermas → Dworkin — "
        "a hermenêutica geral como fundamento da hermenêutica jurídica. "
        "O Lex-IO-Graph como instrumento de *Verstehen* jurídico "
        "(compreensão, Dilthey), não de mera *Erklären* (explicação)."
    )
    for ep in EPISTEMOLOGIA['arco_epistemologico']:
        st.markdown(f"""
<div class="epist-card">
  <span class="epist-autor">{ep['autor']}</span>
  <span class="epist-datas">{ep['datas']}</span>
  <div class="epist-contrib">{ep['contribuicao']}</div>
  <div class="epist-dir">⚖️ {ep['conexao_direito']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### Arco metodológico — dos glosadores ao direito digital")
    st.markdown(
        "A hermenêutica jurídica ocidental compartilha epistemologia "
        "com as tradições judaica e islâmica — glosa, comentário, comentário "
        "do comentário. Bolonha (séc. XI–XIII) como espaço pancrônico de "
        "diálogo entre Irnerius, Maimônides e Averróis."
    )
    for arco in EPISTEMOLOGIA['arco_metodologico']:
        with st.expander(f"{arco['periodo']}"):
            st.markdown(f"**Figura central:** {arco['figura_central']}")
            st.markdown(f"**Método:** {arco['metodo']}")
            st.markdown(
                f'<div class="epist-dir">🔗 Conexão pancrônica: {arco["conexao_pancronica"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### O valor epistemológico do Lex-IO-Graph")
    st.markdown("""
O Lex-IO-Graph é o único atlas jurídico brasileiro que articula explicitamente:

- **Hermenêutica geral** (Schleiermacher, Dilthey, Gadamer) como fundamento da hermenêutica jurídica
- **Teoria do conhecimento** (Verstehen vs. Erklären) como critério de avaliação dos métodos jurídicos  
- **Pancronia bakhtiniana** como metodologia de acesso ao arco histórico simultâneo
- **Direito comparado glocal** (global + local, Robertson, 1990s) como camada de contextualização
- **Inteligência estratégica** como vetor prospectivo

Cada nó do grafo é simultaneamente: fato normativo, evento histórico, 
produto de método hermenêutico, objeto de direito comparado e vetor estratégico.
O grafo não descreve o direito — *compreende-o* (Dilthey, Gadamer).
""")

# =============================================================
# SEÇÃO 3 — Direito natural e positivo
# =============================================================
elif secao == "⚖️ Direito Natural e Positivo":
    st.markdown("## Direito Natural e Direito Positivo")
    st.markdown(DIREITO_NATURAL['introducao'])

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    for autor in DIREITO_NATURAL['autores_chave']:
        with st.expander(f"{autor['nome']} ({autor['datas']})"):
            if 'obra' in autor:
                st.markdown(f"**Obra:** {autor['obra']}")
            st.markdown(f"**Tese:** {autor['tese']}")
            st.markdown(
                f'<div class="epist-dir">🇧🇷 {autor["relevancia"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### Arco ontológico — das quatro leis ao CC/2002")

    for arco in EPISTEMOLOGIA['arco_ontologico']:
        with st.expander(f"{arco['posicao']}"):
            st.markdown(f"**Autores:** {arco['autores']}")
            st.markdown(f"**Tese:** {arco['tese']}")
            st.markdown(
                f'<div class="epist-dir">🇧🇷 {arco["relevancia_brasil"]}</div>',
                unsafe_allow_html=True
            )

render_footer()
