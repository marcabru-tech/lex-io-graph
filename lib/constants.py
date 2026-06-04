"""
Constantes semióticas do Lex Quantum Compliance Map.

Triade cromática:
  Lex   → dourado (#d4a853) — lei, governança, gravidade
  IO    → ciano (#3dc8e6)   — fluxo, interação, pulso
  Graph → vermelho (#c44b4b) — grafo, escrita, estrutura
"""

# ---- Cores da triade semiótica ----
LEX_COLOR = "#d4a853"
IO_COLOR = "#3dc8e6"
GRAPH_COLOR = "#c44b4b"

# ---- Cores por tipo de nó no grafo ----
NODE_COLORS = {
    "constituicao": "#d4a853",      # ouro — fundamento
    "lei": "#3dc8e6",               # ciano — norma vigente
    "pl": "#8b8b8b",                # cinza — em tramitação
    "norma_regulamentar": "#e67e22", # laranja — regulamentar
    "jurisprudencia": "#c44b4b",    # vermelho — decisão
    "orgao": "#9b59b6",             # púrpura — institucional
}

# ---- Cores por tipo de aresta ----
EDGE_COLORS = {
    "hierarquia": "#d4a853",
    "intersecao": "#3dc8e6",
    "antinomia": "#c44b4b",
    "complementaridade": "#2ecc71",
    "regulamenta": "#e67e22",
    "interpreta": "#9b59b6",
}

# ---- Labels de tipo de nó ----
NODE_TYPE_LABELS = {
    "constituicao": "Constituição",
    "lei": "Lei / Lei Complementar",
    "pl": "Projeto de Lei",
    "norma_regulamentar": "Norma Regulamentar",
    "jurisprudencia": "Jurisprudência",
    "orgao": "Órgão / Instituição",
}

# ---- Labels de tipo de aresta ----
EDGE_TYPE_LABELS = {
    "hierarquia": "Hierarquia normativa",
    "intersecao": "Interseção temática",
    "antinomia": "Antinomia / Conflito",
    "complementaridade": "Complementaridade",
    "regulamenta": "Regulamentação",
    "interpreta": "Interpretação judicial",
}

# ---- Temas para filtros ----
THEMES = {
    "dados_pessoais": "Dados Pessoais",
    "menores": "Crianças e Adolescentes",
    "ia": "Inteligência Artificial",
    "trabalho": "Trabalho Digital",
    "internet": "Internet e Plataformas",
    "acesso": "Acesso e Inclusão",
}

# ---- Empresas modelo para matriz de compliance ----
EMPRESAS_MODELO = [
    {
        "nome": "Startup SaaS (dev júnior, 5-15 pessoas)",
        "setor": "Tecnologia",
        "risco_base": "alto",
        "descricao": "Coleta dados de usuários, usa IA para automação, contrata devs júnior sem revisão jurídica",
    },
    {
        "nome": "Software House (projetos para terceiros)",
        "setor": "Serviços de TI",
        "risco_base": "alto",
        "descricao": "Entrega projetos com dados de clientes dos clientes, sem DPO, sem mapeamento de bases legais",
    },
    {
        "nome": "Edtech (plataforma para menores)",
        "setor": "Educação",
        "risco_base": "muito_alto",
        "descricao": "Trata dados de crianças e adolescentes, precisa de consentimento parental, ECA Digital se aplica integralmente",
    },
    {
        "nome": "Fintech (pagamentos digitais)",
        "setor": "Financeiro",
        "risco_base": "muito_alto",
        "descricao": "Dados sensíveis financeiros, open banking, regulação BACEN + LGPD + Marco Civil",
    },
    {
        "nome": "Agência Digital (marketing + dados)",
        "setor": "Marketing",
        "risco_base": "medio",
        "descricao": "Tratamento de dados para profiling, cookies, remarketing — LGPD + Marco Civil",
    },
]
