"""
Página 2 — Matriz de Compliance

Tabela cruzada: empresas modelo × normas, com indicadores de risco.
Foco em empresas de tecnologia com exposição regulatória.
"""

import streamlit as st
import pandas as pd

from lib.graph_builder import build_compliance_matrix, load_json
from lib.constants import EMPRESAS_MODELO
from lib.footer import render_footer

st.set_page_config(page_title="Matriz de Compliance — Lex Quantum", layout="wide", page_icon="📋")

st.markdown("# 📋 Matriz de Compliance")
st.markdown("Tabela cruzada: perfis de empresa × normas do ordenamento jurídico digital.")

# ---- Construir matriz ----
matrix = build_compliance_matrix()
raw_nodes = load_json("normas.json")["nodes"]
leis = [n for n in raw_nodes if n["tipo"] in ("lei", "constituicao", "norma_regulamentar")]
lei_siglas = [n["sigla"] for n in leis]

# ---- DataFrame ----
df = pd.DataFrame(matrix)

# ---- Legenda ----
st.markdown("""
| Cor | Significado |
|-----|-------------|
| 🔴 **Alto** | Interseção direta com múltiplas normas — alto risco de não-conformidade |
| 🟡 **Médio** | Interseção parcial — risco moderado, requer atenção |
| 🟢 **Baixo** | Interseção mínima — risco baixo, mas não nulo |
| ⚪ **Aplicável** | Norma fundamental que se aplica a todos |
""")

# ---- Tabela interativa ----
st.markdown("### Empresas × Normas")

for idx, empresa in enumerate(EMPRESAS_MODELO):
    row = matrix[idx]

    with st.expander(f"**{empresa['nome']}** — Risco geral: **{empresa['risco_base'].upper()}**", expanded=(idx == 0)):
        st.markdown(f"*{empresa['descricao']}*")

        cols = st.columns(len(leis))
        for j, lei in enumerate(leis):
            sigla = lei["sigla"]
            risco = row.get(sigla, "baixo")
            emoji = {"alto": "🔴", "medio": "🟡", "baixo": "🟢", "aplicavel": "⚪"}.get(risco, "⚪")
            with cols[j]:
                st.metric(label=sigla.split("—")[0].strip(), value=f"{emoji} {risco.upper()}")

# ---- Tabela consolidada ----
st.markdown("### Visão consolidada")

display_df = df[["empresa", "risco"] + [s for s in lei_siglas if s in df.columns]].copy()
display_df.columns = ["Empresa", "Risco Geral"] + [s.split("—")[0].strip() for s in lei_siglas if s in df.columns]

# Substituir valores por emoji
emoji_map = {"alto": "🔴 Alto", "medio": "🟡 Médio", "baixo": "🟢 Baixo", "aplicavel": "⚪ Aplicável", "muito_alto": "🔴 Muito Alto"}
for col in display_df.columns[2:]:
    display_df[col] = display_df[col].map(lambda x: emoji_map.get(x, x))
display_df["Risco Geral"] = display_df["Risco Geral"].map(lambda x: emoji_map.get(x, x))

st.dataframe(display_df, use_container_width=True, hide_index=True)

# ---- Insight ----
st.markdown("---")
st.markdown("""
### Insight: por que a ausência de processo regulatório aumenta o risco?

O risco não está no nível técnico do desenvolvedor — está na **ausência de revisão jurídica**
antes da entrega. Quando uma equipe técnica implementa uma feature sem mapear:

1. **Quais dados estão sendo coletados** → LGPD art. 7º (base legal)
2. **Se há menores envolvidos** → ECA Digital (consentimento parental, design protegido)
3. **Se decisões são automatizadas** → PL 2.338 (classificação de risco)
4. **Se funcionários estão sendo monitorados** → NR-1 (riscos psicossociais)
5. **Se logs estão sendo retidos corretamente** → Marco Civil (6 meses a 1 ano)

...a empresa fica exposta a sanções administrativas (ANPD), responsabilização civil
(STJ — dano moral in re ipsa) e, nos casos mais graves, ação penal.

**O Lex Quantum Compliance Map existe para tornar essas interseções visíveis
antes que se tornem problemas.**
""")

render_footer()
