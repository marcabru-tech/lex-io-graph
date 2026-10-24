"""Alertas regulatórios com prazo, exibidos na home.

Cada alerta guarda a base do prazo (data de publicação e número de dias) e a
data nominal calculada, com a ressalva sobre a regra de contagem. A situação
exibida muda sozinha com a data: prazo em curso, último dia ou encerrado.
"""
from datetime import date

ALERTAS_PRAZO = [
    {
        "id": "nidus_cadastro_2026",
        "categoria": "ECA Digital",
        "tipo": "Prazo regulatório",
        "atualizado_em": date(2026, 10, 24),
        "titulo": "Cadastro no Sistema NIDUS (Polícia Federal): prazo de 60 dias",
        "texto": (
            "A Portaria DG/PF nº 19.107/2026 (DOU de 20/10/2026) abriu o cadastro de fornecedores "
            "de produtos e serviços de tecnologia no Sistema NIDUS, do Centro Nacional de Proteção à "
            "Criança e ao Adolescente (CNCA). É a primeira etapa do fluxo de notificação de crimes "
            "graves contra crianças e adolescentes em ambientes digitais (Portaria MJSP nº 1.312/2026)."
        ),
        "escopo": (
            "Fornecedores de serviços direcionados a crianças e adolescentes no Brasil ou de acesso "
            "provável por esse público, e fornecedores de conteúdo pornográfico ou de serviços sexuais, "
            "mesmo sem esse público-alvo, devem verificar o enquadramento conforme os critérios da "
            "portaria. O prazo não vale para toda empresa, e o cadastro voluntário não significa, por si "
            "só, sujeição ao ECA Digital."
        ),
        "etapa_seguinte": (
            "O envio das notificações será disciplinado por ato posterior da Polícia Federal. O cadastro "
            "pendente não suspende os deveres legais de comunicação, remoção e preservação de conteúdo."
        ),
        "publicacao": date(2026, 10, 20),
        "prazo_dias": 60,
        "vencimento_nominal": date(2026, 12, 19),
        "ressalva_prazo": (
            "Data nominal calculada (60 dias corridos a partir de 20/10/2026), que cai num sábado: "
            "confirmar a regra de contagem e eventual prorrogação antes de tratá-la como vencimento definitivo."
        ),
        "fontes": [
            ("CNCA — orientações e cadastro para plataformas", "https://www.gov.br/cnca/pt-br/para-empresas"),
        ],
    },
]


def situacao_prazo(alerta: dict, hoje: date) -> str:
    """Texto curto da situação do prazo nominal na data informada."""
    venc = alerta["vencimento_nominal"]
    restantes = (venc - hoje).days
    data = venc.strftime("%d/%m/%Y")
    if restantes > 1:
        return f"Faltam {restantes} dias para a data nominal ({data})."
    if restantes == 1:
        return f"Falta 1 dia para a data nominal ({data})."
    if restantes == 0:
        return (f"Hoje é a data nominal do prazo ({data}); a eventual prorrogação por dia "
                "não útil ainda precisa ser confirmada.")
    return (f"O prazo nominal chegou ao fim em {data}; a eventual prorrogação por dia não útil "
            "ainda precisa ser confirmada.")
