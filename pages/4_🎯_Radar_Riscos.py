"""
Página 4 — Radar de Riscos para Dev Júnior

Mapa de calor: quais entregas de dev júnior mais expõem
a empresa a risco jurídico, linkadas às normas específicas.
"""

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Radar de Riscos — Lex Quantum", layout="wide", page_icon="🎯")

st.markdown("# 🎯 Radar de Riscos — Dev Júnior")
st.markdown("Mapa de calor das exposições regulatórias mais comuns em entregas de desenvolvedores júnior.")

# ---- Base de riscos ----
riscos = [
    {
        "entrega": "Coleta de dados sem base legal",
        "risco": 9,
        "normas": ["LGPD art. 7º", "CF art. 5º"],
        "descricao": "Formulários que coletam CPF, e-mail, telefone sem consentimento explícito ou outra base legal.",
        "acao": "Mapear cada campo de dado coletado e documentar a base legal. Implementar checkbox de consentimento granular.",
    },
    {
        "entrega": "Dados de menores sem consentimento parental",
        "risco": 10,
        "normas": ["ECA Digital art. 10, 12", "LGPD art. 14"],
        "descricao": "Cadastro de menores de 14 anos sem verificação de idade e consentimento do responsável legal.",
        "acao": "Implementar fluxo de verificação de idade e consentimento parental qualificado conforme ECA Digital.",
    },
    {
        "entrega": "Logs sem retenção adequada",
        "risco": 7,
        "normas": ["Marco Civil art. 13, 15", "STF ADI 5527"],
        "descricao": "Aplicação não mantém registros de conexão e acesso por 6 meses a 1 ano conforme exigido.",
        "acao": "Configurar retenção de logs com período mínimo legal. Documentar política de retenção.",
    },
    {
        "entrega": "Banner de cookies genérico",
        "risco": 6,
        "normas": ["LGPD art. 7º", "TRF-4 (cookies)"],
        "descricao": "Botão 'aceitar todos' sem categorização (analytics, marketing, funcional) ou possibilidade de recusa.",
        "acao": "Implementar consentimento granular por categoria de cookie. Permitir recusa sem prejudicar funcionalidade.",
    },
    {
        "entrega": "IA sem governança ou transparência",
        "risco": 8,
        "normas": ["PL 2.338 art. 16, 19", "LGPD art. 20"],
        "descricao": "Sistema de IA que toma decisões automatizadas (aprovação, recomendação, scoring) sem direito à explicação.",
        "acao": "Documentar lógica do modelo. Implementar mecanismo de revisão humana conforme LGPD art. 20 e PL 2.338.",
    },
    {
        "entrega": "Monitoramento de produtividade sem base legal",
        "risco": 8,
        "normas": ["NR-1 item 1.5.3", "LGPD art. 7º"],
        "descricao": "Ferramenta de tracking de tempo/tela de funcionários sem avaliação de riscos psicossociais.",
        "acao": "Realizar PGR (Programa de Gerenciamento de Riscos) antes de implementar. Documentar base legal.",
    },
    {
        "entrega": "Sem HTTPS ou criptografia de dados em repouso",
        "risco": 9,
        "normas": ["LGPD art. 46", "STJ REsp 1.777.780"],
        "descricao": "Dados pessoais transmitidos em texto claro ou armazenados sem criptografia. Vazamento gera dano moral in re ipsa.",
        "acao": "Implementar TLS em todas as rotas. Criptografar dados sensíveis em repouso. Usar hash bcrypt para senhas.",
    },
    {
        "entrega": "Dark patterns em interface para menores",
        "risco": 10,
        "normas": ["ECA Digital art. 16", "LGPD art. 6º"],
        "descricao": "Interface que manipula crianças/adolescentes a consentir ou a fornecer dados além do necessário.",
        "acao": "Revisar UX com foco em design protegido. Eliminar elementos manipulativos. Princípio da necessidade.",
    },
    {
        "entrega": "Sem mecanismo de exclusão de dados",
        "risco": 7,
        "normas": ["LGPD art. 18", "Marco Civil art. 7º"],
        "descricao": "Sistema não permite ao usuário solicitar exclusão dos seus dados pessoais (direito ao esquecimento).",
        "acao": "Implementar endpoint de exclusão/anonimização. Documentar processo de atendimento ao titular.",
    },
    {
        "entrega": "Provedor de aplicação sem contato legal",
        "risco": 5,
        "normas": ["Marco Civil art. 7º, 15", "LGPD art. 41"],
        "descricao": "Aplicação sem identificação clara do controlador de dados ou canal de comunicação com o usuário.",
        "acao": "Publicar política de privacidade com dados do controlador. Disponibilizar canal direto para o titular.",
    },
]

# ---- Heatmap ----
st.markdown("### Mapa de Calor de Riscos")

entregas = [r["entrega"] for r in riscos]
niveis = [r["risco"] for r in riscos]

# Cores: verde (baixo) → amarelo (médio) → vermelho (alto)
colors = []
for n in niveis:
    if n <= 4:
        colors.append("#2ecc71")
    elif n <= 6:
        colors.append("#f39c12")
    elif n <= 8:
        colors.append("#e67e22")
    else:
        colors.append("#c44b4b")

fig = go.Figure()

fig.add_trace(go.Bar(
    y=entregas,
    x=niveis,
    orientation='h',
    marker=dict(
        color=colors,
        line=dict(color='rgba(255,255,255,0.1)', width=1),
    ),
    text=[f"{n}/10" for n in niveis],
    textposition='auto',
    textfont=dict(family="DM Mono, monospace", size=12, color="#e8e4dc"),
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Risco: %{x}/10<br>"
        "<extra></extra>"
    ),
))

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#e8e4dc", size=12),
    xaxis=dict(
        title="Nível de Risco",
        range=[0, 10.5],
        gridcolor="rgba(255,255,255,0.06)",
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        automargin=True,
        tickfont=dict(size=11),
    ),
    height=600,
    margin=dict(l=10, r=30, t=30, b=30),
)

st.plotly_chart(fig, use_container_width=True)

# ---- Detalhamento ----
st.markdown("---")
st.markdown("### Detalhamento por risco")

for risco in sorted(riscos, key=lambda x: x["risco"], reverse=True):
    emoji = "🔴" if risco["risco"] >= 8 else "🟡" if risco["risco"] >= 6 else "🟢"

    with st.expander(f"{emoji} {risco['entrega']} — Risco: {risco['risco']}/10"):
        st.markdown(f"**Descrição:** {risco['descricao']}")
        st.markdown(f"**Normas aplicáveis:** {' · '.join(risco['normas'])}")
        st.markdown(f"**Ação recomendada:** {risco['acao']}")

# ---- Insight ----
st.markdown("---")
st.markdown("""
### Insight: o padrão de risco em empresas com dev júnior

Os três riscos mais críticos (nota 9-10) compartilham um padrão:

1. **Envolvem dados de populações vulneráveis** (menores) ou **dados sensíveis** (CPF, saúde)
2. **A norma é recente ou em tramitação** (ECA Digital 2025, PL 2.338)
3. **O dev júnior não tem referência** — não é negligência, é lacuna de formação

O Compliance Map existe para **preencher essa lacuna visualmente** — antes que a entrega
vá para produção sem revisão jurídica.

> *"O risco não está no código. Está no que o código coleta, processa e decide
> sem que o desenvolvedor saiba que precisa saber."*
""")
