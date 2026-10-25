# Copyright © 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado
# Licença: PolyForm Noncommercial 1.0.0 (ver lib/ipii/LICENSE).
import streamlit as st
import json
from html import escape
from pathlib import Path
from datetime import datetime
from lib.constants import APP_NAME, APP_SUBTITLE, APP_VERSION
from lib.footer import render_footer
from lib.ipii_pagina import (esc, filtrar_por_tier, html_aresta_confirmada, html_aresta_nova,
                             ler_total_normas, pct, rotulo_tipo, so_objetos)

st.set_page_config(
    page_title=f"{APP_NAME} — IPII Engine",
    layout="wide",
    page_icon="🔬"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { min-width: 280px; }
    .block-container { padding-top: 2rem; }
    .app-subtitle { font-family:monospace; font-size:11px; color:#706a60;
      letter-spacing:0.06em; line-height:1.6; margin-top:-8px; margin-bottom:16px; }
    .ip-box { background:rgba(196,75,75,0.06); border:1px solid rgba(196,75,75,0.3);
      border-radius:8px; padding:14px 18px; margin-bottom:20px;
      font-family:monospace; font-size:11px; color:#8a8478; line-height:1.9; }
    .ip-title { color:#c44b4b; font-size:13px; font-weight:bold; margin-bottom:8px; }
    .tier-card { border-radius:8px; padding:14px 16px; margin-bottom:10px; }
    .tier-1 { background:rgba(196,75,75,0.08); border:1px solid rgba(196,75,75,0.3); }
    .tier-2 { background:rgba(212,168,83,0.08); border:1px solid rgba(212,168,83,0.3); }
    .tier-3 { background:rgba(61,200,230,0.06); border:1px solid rgba(61,200,230,0.25); }
    .tier-label { font-size:10px; font-family:monospace; font-weight:bold; letter-spacing:0.1em; }
    .tier-1 .tier-label { color:#c44b4b; }
    .tier-2 .tier-label { color:#d4a853; }
    .tier-3 .tier-label { color:#3dc8e6; }
    .aresta-par { color:#e8e4dc; font-size:14px; font-weight:bold; font-family:monospace; }
    .aresta-score { color:#706a60; font-size:12px; font-family:monospace; margin:4px 0; }
    .aresta-tipo { color:#9b59b6; font-size:11px; font-family:monospace; }
    .aresta-temas { color:#8a8478; font-size:11px; margin-top:4px; }
    .metric-row { display:flex; gap:16px; flex-wrap:wrap; margin-bottom:20px; }
    .metric-box { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
      border-radius:6px; padding:10px 16px; min-width:120px; }
    .metric-label { font-size:11px; color:#706a60; font-family:monospace; }
    .metric-value { font-size:22px; font-weight:bold; color:#e8e4dc; }
    .section-divider { border:none; border-top:1px solid rgba(212,168,83,0.2); margin:24px 0; }
    .principio { font-family:monospace; font-size:12px; color:#d4a853;
      text-align:center; padding:10px; border-top:1px solid rgba(212,168,83,0.15); margin-top:16px; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔬 IPII Engine")
st.markdown(
    f'<div class="app-subtitle">{APP_NAME} · {APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)

# ---- Disclaimer de propriedade intelectual ----
st.markdown("""
<div class="ip-box">
<div class="ip-title">⚖️ Propriedade Intelectual — Hubstry Deep Tech</div>
O <strong style="color:#e8e4dc;">IPII Engine</strong>
(Interação Paramétrica Iterativa por Interoperabilidade aplicado ao corpus normativo do Lex-IO-Graph)
é propriedade intelectual exclusiva da
<strong style="color:#d4a853;">Hubstry Deep Tech</strong>
— Guilherme Gonçalves Machado, Rio de Janeiro, Brasil. © 2026.<br><br>
Licença <strong style="color:#e8e4dc;">PolyForm Noncommercial 1.0.0</strong>:
uso pessoal, estudo e pesquisa liberados. O uso comercial desta implementação —
incluindo tokenizer, matcher e validator — depende de autorização prévia e por
escrito da Hubstry Deep Tech.<br><br>
Para licenciamento comercial ou parcerias:
<a href="mailto:globaldeeptechecosystem@hubstry.dev"
   style="color:#d4a853;">globaldeeptechecosystem@hubstry.dev</a>
·
<a href="https://hubstry.dev/lex-io-graph/" target="_blank"
   style="color:#3dc8e6;">hubstry.dev/lex-io-graph</a><br><br>
<strong style="color:#c44b4b;">Princípio de curadoria:</strong>
o engine alerta — o curador decide.
Nenhuma aresta é adicionada automaticamente ao grafo.
</div>
""", unsafe_allow_html=True)

# ---- Carregar resultado ----
RAIZ = Path(__file__).resolve().parent.parent
RESULTADO_PATH = RAIZ / "data" / "ipii_resultado.json"

@st.cache_data(ttl=300)
def carregar_resultado() -> dict:
    if RESULTADO_PATH.exists():
        try:
            with open(RESULTADO_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

resultado = carregar_resultado()

if not resultado:
    st.info(
        "Resultado do IPII Engine não encontrado. "
        "Execute `python ipii_engine.py` para gerar o relatório."
    )
    render_footer()
    st.stop()

# ---- Métricas ----
meta = resultado.get("metadata", {})
# O resultado do engine contabiliza arestas; a quantidade de normas vem do corpus.
total_normas_corpus, erro_corpus = ler_total_normas(RAIZ / "data" / "normas.json")
if erro_corpus:
    st.error(f"{erro_corpus} A página do IPII precisa do corpus para exibir as métricas.")
    render_footer()
    st.stop()
gerado = meta.get("gerado_em", "")
if gerado:
    try:
        dt = datetime.fromisoformat(gerado)
        gerado = dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        pass

st.markdown(f"""
<div class="metric-row">
  <div class="metric-box">
    <div class="metric-label">Normas analisadas</div>
    <div class="metric-value">{total_normas_corpus}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Arestas sugeridas</div>
    <div class="metric-value">{esc(resultado.get('total_sugeridas', 0))}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Confirmadas</div>
    <div class="metric-value">{esc(resultado.get('confirmadas', 0))}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Novas descobertas</div>
    <div class="metric-value" style="color:#d4a853;">{esc(resultado.get('novas', 0))}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Cobertura</div>
    <div class="metric-value">{pct(resultado.get('cobertura'))}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Precisão</div>
    <div class="metric-value">{pct(resultado.get('precisao'))}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Precisão de tipo</div>
    <div class="metric-value">{pct(resultado.get('precisao_tipo'))}</div>
  </div>
</div>
<div style="font-family:monospace;font-size:10px;color:#454040;margin-bottom:16px;">
  Última rodagem: {esc(gerado)} · Threshold: {esc(meta.get('threshold', 0.40))} · {esc(meta.get('engine', 'IPII Engine'))}
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ---- Navegação ----
secao = st.radio(
    "Seção",
    ["🆕 Novas arestas descobertas", "✅ Arestas confirmadas", "⚠️ Gap do engine", "🚫 Fora do IPII"],
    horizontal=True,
    label_visibility="collapsed"
)

def _texto_completo(item: dict) -> None:
    """Mostra a descrição integral quando o resumo do relatório foi encurtado."""
    completa = str(item.get("descricao_completa") or "").strip()
    resumo = str(item.get("descricao") or "").strip()
    if completa and completa != resumo:
        with st.expander("Ver texto completo"):
            st.markdown(
                f'<div class="aresta-temas" style="white-space:pre-wrap">{escape(completa)}</div>',
                unsafe_allow_html=True,
            )


# TIER_LABELS e TIPO_LABELS vêm de lib/ipii_pagina.py

# =============================================================
if secao == "🆕 Novas arestas descobertas":
    novas = so_objetos(resultado.get("detalhe_novas", []))
    st.markdown(f"## {len(novas)} arestas novas descobertas")
    st.markdown(
        "Arestas que o engine detectou mas ainda não existem no grafo. "
        "Ordenadas por score. **Princípio:** o engine alerta — o curador decide. "
        "Revise cada par e adicione manualmente ao `arestas.json` se confirmar."
    )

    tier_sel = st.selectbox(
        "Filtrar por tier",
        ["Todos", "Tier 1 (≥ 0.75)", "Tier 2 (0.65–0.74)", "Tier 3 (0.55–0.64)"]
    )

    tier_map = {"Todos": 5, "Tier 1 (≥ 0.75)": 1, "Tier 2 (0.65–0.74)": 2, "Tier 3 (0.55–0.64)": 3}
    tier_max = tier_map[tier_sel]

    filtradas = filtrar_por_tier(novas, tier_max)
    st.markdown(f"**{len(filtradas)}** aresta(s) exibida(s)")

    for n in filtradas:
        st.markdown(html_aresta_nova(n), unsafe_allow_html=True)

# =============================================================
elif secao == "✅ Arestas confirmadas":
    confirmadas = so_objetos(resultado.get("detalhe_confirmadas", []))
    st.markdown(f"## {len(confirmadas)} arestas confirmadas pelo engine")
    st.markdown(
        "Arestas que o engine sugeriu e já existem no grafo — validação da precisão do engine."
    )
    for c in confirmadas:
        st.markdown(html_aresta_confirmada(c), unsafe_allow_html=True)

# =============================================================
elif secao == "⚠️ Gap do engine":
    gap = so_objetos(resultado.get("gap_engine", []))
    st.markdown(f"## {len(gap)} arestas não detectadas pelo engine")
    st.markdown(
        "Arestas que existem no grafo mas o engine não sugeriu. "
        "Indicam dimensões não capturadas — principalmente conexões institucionais "
        "(ANPD criada por lei, decreto atribui competência)."
    )
    for g in gap:
        tipo_label = escape(rotulo_tipo(g.get("tipo", "")))
        resumo = escape(str(g.get("descricao") or ""))
        st.markdown(f"""
<div class="tier-card tier-3">
  <div class="aresta-par">{escape(str(g.get('par', '')))}</div>
  <div class="aresta-tipo">Tipo: {tipo_label}</div>
  {f'<div class="aresta-temas">{resumo}</div>' if resumo else ''}
</div>""", unsafe_allow_html=True)
        _texto_completo(g)
    st.markdown(
        "**IPII experimental — apoio à curadoria.** O motor sugere relações com base nas "
        "dimensões implementadas; uma pontuação não comprova, por si só, uma relação jurídica. "
        "O curador deve verificar cada sugestão em fontes primárias antes de aceitá-la. "
        "A precisão e a cobertura apresentadas no topo desta página vêm do relatório atual "
        "`data/ipii_resultado.json` e são atualizadas quando o relatório é regenerado. "
        "**O motor sugere; o curador decide.**"
    )

# =============================================================
elif secao == "🚫 Fora do IPII":
    fora = so_objetos(resultado.get("fora_do_ipii", []))
    st.markdown(f"## {len(fora)} aresta(s) fora do IPII")
    st.markdown(
        "Relações existentes que envolvem ao menos uma norma excluída da formação de pares "
        "(por exemplo, decisão judicial em conferência). Permanecem visíveis para rastreabilidade, "
        "mas não entram nas métricas de precisão/cobertura nem são tratadas como falhas de detecção."
    )
    if not fora:
        st.info("Nenhuma aresta fora do IPII neste relatório.")
    for item in fora:
        par = escape(str(item.get("par", "Par não identificado")))
        tipo = escape(rotulo_tipo(item.get("tipo"), "Não especificado"))
        descricao = escape(str(item.get("descricao") or ""))
        st.markdown(f"""
<div class="tier-card tier-3">
  <div class="aresta-par">{par}</div>
  <div class="aresta-tipo">Tipo registrado: {tipo}</div>
  <div class="aresta-temas">{descricao}</div>
</div>""", unsafe_allow_html=True)
        _texto_completo(item)

st.markdown(
    '<div class="principio">O engine alerta — o curador decide · IPII Engine © 2026 Hubstry Deep Tech</div>',
    unsafe_allow_html=True
)

render_footer()
