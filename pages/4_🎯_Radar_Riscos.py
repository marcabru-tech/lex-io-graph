"""
Página 4 — Radar de Riscos Regulatórios

Mapa de calor: exposição regulatória por perfil de empresa e norma
a empresa a risco jurídico, linkadas às normas específicas.
"""

import streamlit as st
import plotly.graph_objects as go
from lib.footer import render_footer

st.set_page_config(page_title="Radar de Riscos — Lexiograph", layout="wide", page_icon="🎯")

st.markdown("# 🎯 Radar de Riscos Regulatórios")
st.markdown("Mapa de calor das exposições regulatórias mais comuns em entregas de desenvolvedores júnior.")
st.info(
    "**Indicadores ilustrativos.** As notas de 1 a 10 são exemplos definidos pela curadoria do "
    "Lexiograph para entregas típicas de software; não resultam de avaliação da sua empresa, "
    "não são diagnóstico de conformidade e não constituem parecer jurídico."
)

# ---- Base de riscos ----
riscos = [
    {
        "entrega": "Coleta de dados sem base legal",
        "risco": 9,
        "normas": ["LGPD art. 7º", "CF art. 5º"],
        "descricao": "Formulários que coletam CPF, e-mail, telefone sem base legal identificada (o consentimento é uma das hipóteses do art. 7º).",
        "acao": "Mapear cada campo de dado coletado e documentar a base legal. Se a base for o consentimento, coletá-lo por finalidade.",
    },
    {
        "entrega": "Dados de crianças e adolescentes sem base legal adequada",
        "risco": 10,
        "normas": ["LGPD art. 14, caput e § 1º", "ECA Digital arts. 10 e 24"],
        "descricao": "Tratamento de dados de crianças e adolescentes sem base legal definida no seu melhor interesse, ou sem os mecanismos de idade e supervisão exigidos para o tipo de serviço.",
        "acao": "Definir a base legal no melhor interesse (para crianças, consentimento específico de um dos pais ou responsável quando essa for a base) e aplicar os mecanismos do ECA Digital cabíveis ao serviço.",
    },
    {
        "entrega": "Logs sem retenção adequada",
        "risco": 7,
        "normas": ["Marco Civil art. 13 (conexão)", "Marco Civil art. 15 (aplicações)"],
        "descricao": "Provedor de aplicações não mantém registros de acesso a aplicações por 6 meses (art. 15); provedor de conexão não mantém registros de conexão por 1 ano (art. 13).",
        "acao": "Configurar retenção de logs com período mínimo legal. Documentar política de retenção.",
    },
    {
        "entrega": "Banner de cookies genérico",
        "risco": 6,
        "normas": ["LGPD art. 7º", "LGPD art. 8º"],
        "descricao": "Botão 'aceitar todos' sem categorização (analytics, marketing, funcional) ou possibilidade de recusa.",
        "acao": "Para cookies não essenciais baseados em consentimento, coletá-lo por categoria e permitir a recusa sem prejudicar a funcionalidade.",
    },
    {
        "entrega": "IA sem governança ou transparência",
        "risco": 8,
        "normas": ["LGPD art. 20", "PL 2.338/2023 (referência, em tramitação)"],
        "descricao": "Sistema de IA que toma decisões automatizadas (aprovação, recomendação, scoring) sem direito à explicação.",
        "acao": "Permitir que o titular solicite a revisão de decisões automatizadas e informar os critérios utilizados (LGPD art. 20). Como boa prática, documentar a lógica do modelo.",
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
        "normas": ["LGPD art. 46", "LGPD arts. 42 e 52"],
        "descricao": "Dados pessoais transmitidos em texto claro ou armazenados sem criptografia. O vazamento expõe a responsabilização civil (LGPD art. 42) e a sanções administrativas (art. 52); para dados pessoais comuns, o STJ decidiu que o vazamento, por si só, não gera dano moral presumido (AREsp 2.130.619/SP, 2ª Turma, 07/03/2023).",
        "acao": "Implementar TLS em todas as rotas. Criptografar dados sensíveis em repouso. Usar hash bcrypt para senhas.",
    },
    {
        "entrega": "Interface manipulativa ou coleta excessiva de dados de crianças",
        "risco": 10,
        "normas": ["ECA Digital art. 18, § 2º", "LGPD art. 14, § 4º", "LGPD art. 6º, III"],
        "descricao": "(a) Interface projetada ou manipulada para comprometer a autonomia ou a escolha do usuário, sobretudo se enfraquece a supervisão parental ou salvaguardas (ECA Digital art. 18, § 2º); (b) condicionar a participação de crianças em jogos ou aplicações ao fornecimento de dados além dos estritamente necessários (LGPD art. 14, § 4º). Outros padrões de design manipulativo entram como avaliação de risco, sem atribuição legal específica.",
        "acao": "Revisar UX com foco em design protegido. Eliminar elementos manipulativos. Princípio da necessidade.",
    },
    {
        "entrega": "Sem mecanismo de exclusão de dados",
        "risco": 7,
        "normas": ["LGPD art. 18, IV e VI", "Marco Civil art. 7º, X"],
        "descricao": "Sistema não permite ao usuário solicitar a eliminação dos seus dados pessoais (direito de eliminação, LGPD art. 18).",
        "acao": "Implementar endpoint de exclusão/anonimização. Documentar processo de atendimento ao titular.",
    },
    {
        "entrega": "Provedor de aplicação sem contato legal",
        "risco": 5,
        "normas": ["LGPD art. 9º, IV", "LGPD art. 41", "Marco Civil art. 7º, VI e VIII"],
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
        st.markdown(f"**Normas relacionadas:** {' · '.join(risco['normas'])}")
        st.markdown(f"**Ação recomendada:** {risco['acao']}")

# ---- Insight ----
st.markdown("---")
st.markdown("""
### Insight: o gap entre entrega técnica e conformidade regulatória

Os quatro riscos mais críticos (nota 9–10) compartilham um padrão:

1. **Envolvem dados de populações vulneráveis** (menores) ou **dados pessoais** de identificação (ex.: CPF) e **sensíveis** (ex.: saúde)
2. **A norma é recente ou em tramitação** (ECA Digital 2025; PL 2.338/2023 em tramitação, sem efeito obrigatório)
3. **A equipe técnica não tem referência regulatória** — não é negligência, é lacuna de processo

O Compliance Map existe para **preencher essa lacuna visualmente** — antes que a entrega
vá para produção sem revisão jurídica.

> *"O risco não está no código. Está no que o código coleta, processa e decide
> sem que o desenvolvedor saiba que precisa saber."*
""")

render_footer()
