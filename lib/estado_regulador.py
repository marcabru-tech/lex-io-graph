"""
30 anos do Estado Regulador Brasileiro (1996-2026).

Linha do tempo das agencias reguladoras federais a partir do Quadro 1 de
CUNHA, B. Q. (org.). O Estado regulador brasileiro: tres decadas de reformas
e agencificacao (1996-2026). Rio de Janeiro: Ipea : MDIC, 2026, p. 27.
Notas de mudanca de denominacao e de conversao legal sao acrescimos do
Lexiograph, com a lei correspondente indicada.
"""

import plotly.graph_objects as go

FONTE_LIVRO = (
    "CUNHA, Bruno Queiroz (org.). <em>O Estado regulador brasileiro: três décadas de "
    "reformas e agencificação (1996-2026)</em>. Rio de Janeiro: Ipea : MDIC, 2026. "
    "364 p. ISBN 978-65-5635-095-0. DOI: 10.38116/978-65-5635-095-0."
)

# setor -> cor (paleta do app)
SETORES = {
    "Infraestrutura e energia": "#d4a853",
    "Telecomunicações e digital": "#3dc8e6",
    "Transportes": "#e67e22",
    "Saúde": "#2ecc71",
    "Recursos naturais": "#1abc9c",
    "Cultura": "#9b59b6",
    "Dados pessoais": "#c44b4b",
}

AGENCIAS = [
    {"sigla": "Aneel", "nome": "Agência Nacional de Energia Elétrica", "ato": "Lei 9.427",
     "data": "1996-12-26", "setor": "Infraestrutura e energia",
     "nota": "Marco inicial do modelo de agências no Brasil."},
    {"sigla": "Anatel", "nome": "Agência Nacional de Telecomunicações", "ato": "Lei 9.472 (Lei Geral de Telecomunicações)",
     "data": "1997-07-16", "setor": "Telecomunicações e digital", "nota": ""},
    {"sigla": "ANP", "nome": "Agência Nacional do Petróleo", "ato": "Lei 9.478",
     "data": "1997-08-06", "setor": "Infraestrutura e energia",
     "nota": "Hoje Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (Lei 11.097/2005)."},
    {"sigla": "Anvisa", "nome": "Agência Nacional de Vigilância Sanitária", "ato": "Lei 9.782",
     "data": "1999-01-26", "setor": "Saúde", "nota": ""},
    {"sigla": "ANS", "nome": "Agência Nacional de Saúde Suplementar", "ato": "Lei 9.961",
     "data": "2000-01-28", "setor": "Saúde", "nota": ""},
    {"sigla": "ANA", "nome": "Agência Nacional de Águas", "ato": "Lei 9.984",
     "data": "2000-07-17", "setor": "Recursos naturais",
     "nota": "Hoje Agência Nacional de Águas e Saneamento Básico (Lei 14.026/2020)."},
    {"sigla": "Antaq", "nome": "Agência Nacional de Transportes Aquaviários", "ato": "Lei 10.233",
     "data": "2001-06-05", "setor": "Transportes", "nota": "Criada pela mesma lei da ANTT."},
    {"sigla": "ANTT", "nome": "Agência Nacional de Transportes Terrestres", "ato": "Lei 10.233",
     "data": "2001-06-05", "setor": "Transportes", "nota": "Criada pela mesma lei da Antaq."},
    {"sigla": "Ancine", "nome": "Agência Nacional do Cinema", "ato": "MP 2.228",
     "data": "2001-09-06", "setor": "Cultura", "nota": "Única criada por medida provisória até a ANPD."},
    {"sigla": "Anac", "nome": "Agência Nacional de Aviação Civil", "ato": "Lei 11.182",
     "data": "2005-09-27", "setor": "Transportes", "nota": ""},
    {"sigla": "ANM", "nome": "Agência Nacional de Mineração", "ato": "Lei 13.575",
     "data": "2017-12-26", "setor": "Recursos naturais",
     "nota": "Sucede o DNPM (Departamento Nacional de Produção Mineral). Atua na PNMCE (Lei 15.506/2026)."},
    {"sigla": "ANPD", "nome": "Agência Nacional de Proteção de Dados", "ato": "MP 1.317",
     "data": "2025-09-17", "setor": "Dados pessoais",
     "nota": "Convertida na Lei 15.352/2026: primeira agência da regulação digital."},
]

MARCOS = [
    {"data": "2007-01-01", "rotulo": "PRO-REG (2007)",
     "texto": "Programa de Fortalecimento da Capacidade Institucional para Gestão em Regulação"},
    {"data": "2019-06-25", "rotulo": "Lei 13.848/2019",
     "texto": "Lei Geral das Agências Reguladoras"},
    {"data": "2026-02-25", "rotulo": "Lei 15.352/2026",
     "texto": "ANPD convertida em agência"},
]

SINTESE_LIVRO = [
    ("Origem", "As primeiras agências surgem a partir de 1996, nas reformas econômicas e "
     "administrativas dos anos 1990, para fiscalizar serviços públicos transferidos a "
     "operadores privados e mediar conflitos nesses setores. O precedente é o modelo "
     "norte-americano de reguladores independentes; a difusão contou com Banco Mundial, "
     "BID (Banco Interamericano de Desenvolvimento) e OCDE (Organização para a "
     "Cooperação e o Desenvolvimento Econômico) (CUNHA; FAGANELLO, 2026, p. 25-27)."),
    ("Expansão e normalização", "Doze agências setoriais depois, as agências passaram "
     "'da condição de novidade a um estado de normalidade': diante de novos problemas "
     "públicos, propor uma agência tornou-se resposta corrente (CUNHA; FAGANELLO, 2026, p. 28)."),
    ("Críticas", "Implantação 'de cima para baixo', dificuldade de adaptar padrões "
     "estrangeiros, fragmentação administrativa, traços de patrimonialismo, alta produção "
     "normativa, formalismo e imobilismo (CUNHA; FAGANELLO, 2026, p. 28)."),
    ("Respostas", "PRO-REG (2007) e Lei Geral das Agências Reguladoras (2019), "
     "complementados por uma sucessão de ações que tornam a sofisticação do sistema "
     "'atual e contínua' (CUNHA; FAGANELLO, 2026, p. 28-29)."),
    ("Adaptação local", "A reforma não eliminou empresas estatais, bancos públicos e "
     "poupança compulsória: o resultado é uma 'convergência divergente', em que o modelo "
     "é adaptado às condições locais (CUNHA; FAGANELLO, 2026, p. 31)."),
    ("Agenda atual", "Temas transversais — reindustrialização, desigualdade, "
     "descarbonização — exigem regulação ágil, capacidades internas e coordenação "
     "interinstitucional; a literatura passa a falar em pós-agencificação "
     "(CUNHA; FAGANELLO, 2026, p. 29, 33)."),
]


def figura_linha_do_tempo() -> go.Figure:
    """Linha do tempo interativa: cada agencia e um ponto com metadados no hover."""
    from datetime import date

    fig = go.Figure()
    # Empilha agencias criadas a menos de ~1 ano umas das outras,
    # para que rotulos proximos (Aneel/ANP, 2000-2001) nao se sobreponham.
    niveis, colocadas = {}, []
    for a in sorted(AGENCIAS, key=lambda x: x["data"]):
        d0 = date.fromisoformat(a["data"])
        ocupados = {n for (d1, n) in colocadas if abs((d0 - d1).days) < 330}
        n = next(i for i in range(10) if i not in ocupados)
        niveis[a["sigla"]] = n
        colocadas.append((d0, n))
    for setor, cor in SETORES.items():
        xs, ys, textos, hovers = [], [], [], []
        for a in AGENCIAS:
            if a["setor"] != setor:
                continue
            xs.append(a["data"])
            ys.append(1 + niveis[a["sigla"]] * 0.5)
            textos.append(a["sigla"])
            d = date.fromisoformat(a["data"]).strftime("%d/%m/%Y")
            nota = f"<br><i>{a['nota']}</i>" if a["nota"] else ""
            hovers.append(
                f"<b>{a['sigla']}</b> — {a['nome']}<br>"
                f"Criação: {a['ato']} ({d})<br>Setor: {setor}{nota}"
            )
        if not xs:
            continue
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="markers+text", name=setor,
            text=textos, textposition="top center",
            textfont=dict(family="DM Mono, monospace", size=12, color="#e8e4dc"),
            marker=dict(size=18, color=cor, line=dict(color="#0e1117", width=2)),
            hovertext=hovers, hoverinfo="text",
        ))

    for m in MARCOS:
        fig.add_vline(x=m["data"], line=dict(color="rgba(212,168,83,0.45)", dash="dot", width=1))
        fig.add_annotation(
            x=m["data"], y=0.35, text=m["rotulo"], showarrow=False, yanchor="top",
            font=dict(family="DM Mono, monospace", size=10, color="#d4a853"),
            hovertext=m["texto"],
        )

    fig.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono, monospace", color="#e8e4dc", size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        hoverlabel=dict(bgcolor="#1a1d24", font=dict(family="DM Mono, monospace", size=12)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(size=11)),
        xaxis=dict(range=["1995-06-01", "2027-06-01"], showgrid=False,
                   tickformat="%Y", dtick="M24", color="#8a8478"),
        yaxis=dict(visible=False, range=[0, 3.4]),
    )
    return fig
