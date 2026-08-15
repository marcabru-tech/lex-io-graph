import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from lib.constants import APP_NAME, APP_SUBTITLE, APP_VERSION
from lib.footer import render_footer

st.set_page_config(
    page_title=f"{APP_NAME} — Radar Legislativo",
    layout="wide",
    page_icon="📡"
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
    .radar-card {
        background: rgba(30,173,156,0.05);
        border: 1px solid rgba(30,173,156,0.2);
        border-radius: 8px; padding: 14px; margin-bottom: 10px;
    }
    .radar-sigla  { color: #1abc9c; font-size:14px; font-weight:bold; font-family:monospace; }
    .radar-fonte  { color: #706a60; font-size:11px; font-family:monospace; margin: 3px 0; }
    .radar-ementa { color: #b8b2a6; font-size:12px; line-height:1.7; margin: 6px 0; }
    .radar-status { color: #e67e22; font-size:11px; }
    .novidade-badge {
        background: rgba(196,75,75,0.15);
        border: 1px solid rgba(196,75,75,0.4);
        border-radius: 4px; padding: 2px 8px;
        color: #c44b4b; font-size:10px; font-family:monospace;
        display: inline-block; margin-left: 8px;
    }
    .tema-header {
        color: #d4a853; font-size:14px; font-weight:bold;
        font-family:monospace; margin: 16px 0 8px 0;
        border-bottom: 1px solid rgba(212,168,83,0.2);
        padding-bottom: 6px;
    }
    .section-divider {
        border: none; border-top: 1px solid rgba(212,168,83,0.2);
        margin: 24px 0 20px 0;
    }
    .curadoria-box {
        background: rgba(212,168,83,0.06);
        border: 1px solid rgba(212,168,83,0.25);
        border-radius: 8px; padding: 14px; margin: 16px 0;
        font-family: monospace; font-size: 11px; color: #8a8478; line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📡 Radar Legislativo")
st.markdown(
    f'<div class="app-subtitle">{APP_NAME} · {APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)
st.markdown(
    "Monitoramento automático de PLs (Projetos de Lei), decretos e normas "
    "relevantes para o ordenamento jurídico digital brasileiro. "
    "Fontes: Senado Federal, Câmara dos Deputados e LexML. "
    "Atualização: toda segunda-feira via GitHub Actions."
)

# ---- Carregar dados do radar ----
RADAR_PATH = Path("data/radar_legislativo.json")

@st.cache_data(ttl=3600)
def carregar_radar() -> dict:
    if RADAR_PATH.exists():
        try:
            with open(RADAR_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"ultima_atualizacao": None, "temas": {}, "novidades_detectadas": [], "total_novidades": 0}

radar = carregar_radar()

# ---- Métricas de topo ----
ultima = radar.get("ultima_atualizacao", "Nunca")
if ultima and ultima != "Nunca":
    try:
        dt = datetime.fromisoformat(ultima)
        ultima = dt.strftime("%d/%m/%Y às %H:%M")
    except Exception:
        pass

total_novidades = radar.get("total_novidades", 0)
total_itens = sum(
    len(tema_data.get("senado", [])) +
    len(tema_data.get("camara", [])) +
    len(tema_data.get("lexml", []))
    for tema_data in radar.get("temas", {}).values()
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Última atualização", ultima)
col2.metric("Itens monitorados", total_itens)
col3.metric("Novidades detectadas", total_novidades)
col4.metric("Temas ativos", len(radar.get("temas", {})))

st.markdown("""
<div class="curadoria-box">
⚖️ <strong style="color:#d4a853;">Princípio de curadoria:</strong>
O radar alerta — o curador decide. Nenhum PL ou norma é adicionado automaticamente
ao grafo. As novidades detectadas aqui são alertas para revisão doutrinária.
Após curadoria, os itens relevantes entram no grafo como nós com fundamentação completa.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ---- Navegação ----
secao = st.radio(
    "Seção",
    ["🆕 Novidades", "📋 Por Tema", "🔍 Buscar"],
    horizontal=True,
    label_visibility="collapsed"
)

TEMA_LABELS = {
    "ia": "Inteligência Artificial (IA)",
    "dados": "Dados Pessoais",
    "menores": "Crianças e Adolescentes",
    "plataformas": "Plataformas Digitais",
    "trabalho_digital": "Trabalho Digital",
}

FONTE_LABELS = {
    "senado": "Senado Federal",
    "camara": "Câmara dos Deputados",
    "lexml": "LexML",
}

def render_item(item: dict, novidade: bool = False):
    badge = '<span class="novidade-badge">NOVO</span>' if novidade else ""
    url = item.get("url", "")
    link = f'<a href="{url}" target="_blank" style="color:#1abc9c;font-size:10px;">↗ ver fonte</a>' if url else ""
    st.markdown(f"""
<div class="radar-card">
  <div class="radar-sigla">{item.get('sigla', 'Sem sigla')}{badge} {link}</div>
  <div class="radar-fonte">{item.get('fonte', '')} · Detectado: {item.get('data_deteccao', '')[:10]}</div>
  <div class="radar-ementa">{item.get('ementa', 'Sem ementa disponível')}</div>
  <div class="radar-status">Status: {item.get('status', 'Desconhecido')}</div>
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 1 — Novidades
# =============================================================
if secao == "🆕 Novidades":
    st.markdown("## Novidades Detectadas")
    novidades = radar.get("novidades_detectadas", [])

    if not novidades:
        st.info(
            "Nenhuma novidade detectada na última atualização. "
            "O radar roda toda segunda-feira às 7h BRT. "
            "Para rodar manualmente: GitHub → Actions → Radar Legislativo → Run workflow."
        )
    else:
        st.markdown(f"**{len(novidades)} novidade(s) detectada(s)** — aguardando revisão doutrinária")
        for n in novidades:
            render_item(n, novidade=True)

# =============================================================
# SEÇÃO 2 — Por tema
# =============================================================
elif secao == "📋 Por Tema":
    st.markdown("## Itens por Tema")

    tema_sel = st.selectbox(
        "Selecionar tema",
        options=list(radar.get("temas", {}).keys()),
        format_func=lambda x: TEMA_LABELS.get(x, x)
    )

    if tema_sel:
        tema_data = radar["temas"].get(tema_sel, {})
        termos = tema_data.get("termos_monitorados", [])
        if termos:
            st.markdown(f"**Termos monitorados:** {', '.join(termos)}")

        for fonte in ["senado", "camara", "lexml"]:
            itens = tema_data.get(fonte, [])
            if itens:
                st.markdown(
                    f'<div class="tema-header">{FONTE_LABELS.get(fonte, fonte)} ({len(itens)})</div>',
                    unsafe_allow_html=True
                )
                for item in itens:
                    render_item(item)

        total_tema = sum(len(tema_data.get(f, [])) for f in ["senado", "camara", "lexml"])
        if total_tema == 0:
            st.info("Nenhum item coletado para este tema ainda. Execute o radar para atualizar.")

# =============================================================
# SEÇÃO 3 — Busca
# =============================================================
elif secao == "🔍 Buscar":
    st.markdown("## Buscar no Radar")
    busca = st.text_input(
        "Buscar nos itens coletados",
        placeholder="ex: inteligência artificial, proteção dados, ECA..."
    )

    if busca:
        encontrados = []
        for tema, tema_data in radar.get("temas", {}).items():
            for fonte in ["senado", "camara", "lexml"]:
                for item in tema_data.get(fonte, []):
                    texto = (
                        item.get("sigla", "") + " " +
                        item.get("ementa", "") + " " +
                        item.get("status", "")
                    ).lower()
                    if busca.lower() in texto:
                        item_com_tema = {**item, "tema": tema}
                        encontrados.append(item_com_tema)

        if encontrados:
            st.markdown(f"**{len(encontrados)} resultado(s) para '{busca}'**")
            for item in encontrados:
                st.markdown(
                    f'<div class="tema-header">{TEMA_LABELS.get(item.get("tema",""), item.get("tema",""))}</div>',
                    unsafe_allow_html=True
                )
                render_item(item)
        else:
            st.info(f"Nenhum resultado para '{busca}' nos dados coletados.")

render_footer()
