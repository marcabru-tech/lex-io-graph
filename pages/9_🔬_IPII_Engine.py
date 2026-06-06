# Copyright © 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado
# Todos os direitos reservados.
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from lib.constants import APP_NAME, APP_SUBTITLE, APP_VERSION
from lib.footer import render_footer

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
(Integrated Polymorphic Intersection Intelligence aplicado ao corpus normativo do Lex-IO-Graph)
é propriedade intelectual exclusiva da
<strong style="color:#d4a853;">Hubstry Deep Tech</strong>
— Guilherme Gonçalves Machado, Rio de Janeiro, Brasil. © 2026.<br><br>
É expressamente proibido o uso comercial, reprodução, adaptação ou distribuição
desta implementação — incluindo tokenizer, matcher e validator — sem autorização
escrita da Hubstry Deep Tech.<br><br>
Para licenciamento comercial ou parcerias:
<a href="mailto:globaldeeptechecosystem@hubstry.dev"
   style="color:#d4a853;">globaldeeptechecosystem@hubstry.dev</a>
·
<a href="https://hubstry.dev" target="_blank"
   style="color:#3dc8e6;">hubstry.dev</a><br><br>
<strong style="color:#c44b4b;">Princípio de curadoria:</strong>
o engine alerta — o curador decide.
Nenhuma aresta é adicionada automaticamente ao grafo.
</div>
""", unsafe_allow_html=True)

# ---- Carregar resultado ----
RESULTADO_PATH = Path("data/ipii_resultado.json")

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
    <div class="metric-value">{resultado.get('total_existentes', 0) + resultado.get('novas', 0)}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Arestas sugeridas</div>
    <div class="metric-value">{resultado.get('total_sugeridas', 0)}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Confirmadas</div>
    <div class="metric-value">{resultado.get('confirmadas', 0)}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Novas descobertas</div>
    <div class="metric-value" style="color:#d4a853;">{resultado.get('novas', 0)}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Cobertura</div>
    <div class="metric-value">{resultado.get('cobertura', 0):.0%}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Precisão</div>
    <div class="metric-value">{resultado.get('precisao', 0):.0%}</div>
  </div>
</div>
<div style="font-family:monospace;font-size:10px;color:#454040;margin-bottom:16px;">
  Última rodagem: {gerado} · Threshold: {meta.get('threshold', 0.40)} · {meta.get('engine', 'IPII Engine')}
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ---- Navegação ----
secao = st.radio(
    "Seção",
    ["🆕 Novas arestas descobertas", "✅ Arestas confirmadas", "⚠️ Gap do engine"],
    horizontal=True,
    label_visibility="collapsed"
)

TIER_LABELS = {
    1: ("tier-1", "TIER 1 — FORTE (≥ 0.75)"),
    2: ("tier-2", "TIER 2 — FORTE (0.65–0.74)"),
    3: ("tier-3", "TIER 3 — MODERADA (0.55–0.64)"),
    4: ("tier-3", "TIER 4 — MODERADA (0.45–0.54)"),
    5: ("tier-3", "TIER 5 — FRACA (0.40–0.44)"),
}

TIPO_LABELS = {
    "hierarquia": "Hierarquia normativa",
    "interpreta": "Interpretação judicial",
    "regulamenta": "Regulamentação",
    "intersecao": "Interseção temática",
    "complementaridade": "Complementaridade",
    "antinomia": "Antinomia",
}

# =============================================================
if secao == "🆕 Novas arestas descobertas":
    novas = resultado.get("detalhe_novas", [])
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

    filtradas = [n for n in novas if n.get("tier", 5) <= tier_max]
    st.markdown(f"**{len(filtradas)}** aresta(s) exibida(s)")

    for n in filtradas:
        tier = n.get("tier", 5)
        css_class, tier_label = TIER_LABELS.get(tier, ("tier-3", f"TIER {tier}"))
        tipo_label = TIPO_LABELS.get(n.get("tipo_sugerido", ""), n.get("tipo_sugerido", ""))
        temas = ", ".join(n.get("temas_comuns", []))
        jurs = ", ".join(n.get("jurisdicoes_comuns", []))

        st.markdown(f"""
<div class="tier-card {css_class}">
  <div class="tier-label">{tier_label}</div>
  <div class="aresta-par">{n['source']} ↔ {n['target']}</div>
  <div class="aresta-score">Score: {n['score']} · {n['classificacao'].upper()}</div>
  <div class="aresta-tipo">Tipo sugerido: {tipo_label}</div>
  <div class="aresta-temas">Temas comuns: {temas or '—'}</div>
  {f'<div class="aresta-temas">Jurisdições: {jurs}</div>' if jurs else ''}
</div>""", unsafe_allow_html=True)

# =============================================================
elif secao == "✅ Arestas confirmadas":
    confirmadas = resultado.get("detalhe_confirmadas", [])
    st.markdown(f"## {len(confirmadas)} arestas confirmadas pelo engine")
    st.markdown(
        "Arestas que o engine sugeriu e já existem no grafo — validação da precisão do engine."
    )
    for c in confirmadas:
        match = c.get("match_tipo", False)
        tipo_sug = TIPO_LABELS.get(c.get("tipo_sugerido", ""), c.get("tipo_sugerido", ""))
        tipo_ex = TIPO_LABELS.get(c.get("tipo_existente", ""), c.get("tipo_existente", ""))
        st.markdown(f"""
<div class="tier-card tier-3">
  <div class="aresta-par">{c['source']} ↔ {c['target']}</div>
  <div class="aresta-score">Score: {c['score']}</div>
  <div class="aresta-tipo">Tipo sugerido: {tipo_sug} · Tipo existente: {tipo_ex} · {"✓ match" if match else "≠ divergente"}</div>
</div>""", unsafe_allow_html=True)

# =============================================================
elif secao == "⚠️ Gap do engine":
    gap = resultado.get("gap_engine", [])
    st.markdown(f"## {len(gap)} arestas não detectadas pelo engine")
    st.markdown(
        "Arestas que existem no grafo mas o engine não sugeriu. "
        "Indicam dimensões não capturadas — principalmente conexões institucionais "
        "(ANPD criada por lei, decreto atribui competência)."
    )
    for g in gap:
        tipo_label = TIPO_LABELS.get(g.get("tipo", ""), g.get("tipo", ""))
        st.markdown(f"""
<div class="tier-card tier-3">
  <div class="aresta-par">{g['par']}</div>
  <div class="aresta-tipo">Tipo: {tipo_label}</div>
  {f'<div class="aresta-temas">{g["descricao"]}</div>' if g.get('descricao') else ''}
</div>""", unsafe_allow_html=True)
    st.markdown(
        "**Diagnóstico:** o engine é forte em interseções temáticas e hierárquicas (detecta ~87%). "
        "É fraco em conexões institucionais orgânicas — `regulamenta` quando um decreto "
        "atribui competência a um órgão, não quando regula uma matéria temática. "
        "Solução prevista na próxima versão do engine: dimensão **vínculo institucional**."
    )

st.markdown(
    '<div class="principio">O engine alerta — o curador decide · IPII Engine © 2026 Hubstry Deep Tech</div>',
    unsafe_allow_html=True
)

render_footer()
