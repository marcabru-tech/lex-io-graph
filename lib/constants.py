"""
Constantes semióticas do Lex-IO-Graph.

Sistema de inteligência jurídico-estratégica com gramática
visual-cognitiva, fundamentação semiótica, inventário pancrônico
e vetor prospectivo.

Tríade cromática Lexiograph:
  Lex   → dourado (#d4a853) — lei, governança, razão, sol, intelecto
  IO    → ciano   (#3dc8e6) — fluxo, interação, interpretação
  Graph → vermelho (#c44b4b) — tensão, conflito, antinomia, sangue
"""

# ---- Identidade do produto ----
APP_NAME = "Lex-IO-Graph"
APP_SUBTITLE = (
    "Sistema de inteligência jurídico-estratégica com gramática "
    "visual-cognitiva, fundamentação semiótica, inventário pancrônico "
    "e vetor prospectivo"
)
APP_VERSION = "0.3.0"

# ---- Tríade cromática ----
LEX_COLOR   = "#d4a853"   # dourado — lei, governança, razão, sol
IO_COLOR    = "#3dc8e6"   # ciano   — fluxo, interação, interpretação
GRAPH_COLOR = "#c44b4b"   # vermelho — tensão, conflito, antinomia

# ---- Cores por tipo de nó — semântica semiótica ----
# Dourado/amarelo = razão, intelecto, norma fundamental (sol, luz)
# Ciano           = interpretação, fluxo jurisprudencial (água, movimento)
# Laranja         = regulamentação, operacionalização (calor, concretude)
# Roxo            = doutrina, hermenêutica (sabedoria, profundidade)
# Verde-esmeralda = ato do executivo (ação, implementação)
# Cinza           = prospectiva, PLs em tramitação (indefinição, futuro)
# Púrpura         = órgão institucional (autoridade, instituição)
# Ocre/terracota  = documento internacional, religioso (tradição, civilização)
NODE_COLORS = {
    "constituicao":       "#d4a853",  # ouro — norma fundamental, razão
    "lei":                "#3dc8e6",  # ciano — norma vigente, fluxo
    "pl":                 "#8b8b8b",  # cinza — prospectiva, tramitação
    "norma_regulamentar": "#e67e22",  # laranja — regulamentação
    "jurisprudencia":     "#c44b4b",  # vermelho — decisão, interpretação
    "orgao":              "#9b59b6",  # púrpura — instituição
    "decreto":            "#1abc9c",  # verde-esmeralda — ato executivo
    "documento_internacional": "#c8a96e",  # ocre — tradição, civilização
}

# ---- Formas geométricas por tipo de nó ----
# Círculo   = norma positiva vigente (completude, universalidade)
# Quadrado  = órgão/instituição (solidez, estrutura)
# Diamante  = jurisprudência (precisão, corte)
# Triângulo = PL/prospectiva (direção, movimento)
# Hexágono  = documento internacional (complexidade, rede)
NODE_SHAPES = {
    "constituicao":            "dot",      # círculo maior
    "lei":                     "dot",      # círculo
    "pl":                      "triangle", # triângulo — prospectiva
    "norma_regulamentar":      "dot",      # círculo
    "jurisprudencia":          "diamond",  # diamante — precisão
    "orgao":                   "square",   # quadrado — instituição
    "decreto":                 "dot",      # círculo
    "documento_internacional": "hexagon",  # hexágono — complexidade
}

# ---- Níveis de hierarquia espacial vertical ----
# CF/88 no topo; quanto menor o número, mais alto no grafo
HIERARCHY_LEVELS = {
    "constituicao":            0,   # topo absoluto
    "lei":                     2,   # abaixo da constituição
    "norma_regulamentar":      3,   # abaixo das leis
    "decreto":                 3,   # mesmo nível de regulamentar
    "jurisprudencia":          2,   # lateral — camada interpretativa
    "orgao":                   1,   # lateral institucional
    "pl":                      4,   # base — prospectiva
    "documento_internacional": 1,   # lateral — camada civilizatória
}

# ---- Cores por tipo de aresta ----
EDGE_COLORS = {
    "hierarquia":        "#d4a853",  # dourado sólido — subordinação
    "intersecao":        "#3dc8e6",  # ciano tracejado — coordenação
    "antinomia":         "#c44b4b",  # vermelho tracejado — conflito
    "complementaridade": "#2ecc71",  # verde tracejado — reforço mútuo
    "regulamenta":       "#e67e22",  # laranja sólido — concretização
    "interpreta":        "#9b59b6",  # roxo sólido — hermenêutica
}

# ---- Labels de tipo de nó ----
NODE_TYPE_LABELS = {
    "constituicao":            "Constituição",
    "lei":                     "Lei / Lei Complementar",
    "pl":                      "Projeto de Lei (PL)",
    "norma_regulamentar":      "Norma Regulamentar",
    "jurisprudencia":          "Jurisprudência",
    "orgao":                   "Órgão / Instituição",
    "decreto":                 "Decreto / Ato do Executivo",
    "documento_internacional": "Documento Internacional",
}

# ---- Labels de tipo de aresta ----
EDGE_TYPE_LABELS = {
    "hierarquia":        "Hierarquia normativa",
    "intersecao":        "Interseção temática",
    "antinomia":         "Antinomia / Conflito normativo",
    "complementaridade": "Complementaridade",
    "regulamenta":       "Regulamentação",
    "interpreta":        "Interpretação judicial",
}

# ---- Temas para filtros ----
THEMES = {
    "dados_pessoais": "Dados Pessoais",
    "menores":        "Crianças e Adolescentes",
    "ia":             "Inteligência Artificial (IA)",
    "trabalho":       "Trabalho Digital",
    "internet":       "Internet e Plataformas",
    "acesso":         "Acesso e Inclusão",
}

# ---- Empresas modelo para matriz de compliance ----
EMPRESAS_MODELO = [
    {
        "nome": "Startup SaaS (Software as a Service — software como serviço, 5-15 pessoas)",
        "setor": "Tecnologia",
        "risco_base": "alto",
        "descricao": "Coleta dados de usuários, usa IA para automação, contrata devs júnior sem revisão jurídica",
    },
    {
        "nome": "Software House (projetos para terceiros)",
        "setor": "Serviços de TI",
        "risco_base": "alto",
        "descricao": "Entrega projetos com dados de clientes dos clientes, sem DPO (Data Protection Officer — encarregado de proteção de dados), sem mapeamento de bases legais",
    },
    {
        "nome": "Edtech (plataforma educacional para menores)",
        "setor": "Educação",
        "risco_base": "muito_alto",
        "descricao": "Trata dados de crianças e adolescentes, precisa de consentimento parental, ECA Digital (Estatuto da Criança e do Adolescente Digital — Lei 15.211/2025) se aplica integralmente",
    },
    {
        "nome": "Fintech (pagamentos digitais)",
        "setor": "Financeiro",
        "risco_base": "muito_alto",
        "descricao": "Dados sensíveis financeiros, open banking, regulação BACEN (Banco Central do Brasil) + LGPD + Marco Civil",
    },
    {
        "nome": "Agência Digital (marketing + dados)",
        "setor": "Marketing",
        "risco_base": "medio",
        "descricao": "Tratamento de dados para profiling, cookies, remarketing — LGPD + Marco Civil",
    },
]

# ---- Status especiais de normas ----
STATUS_LABELS = {
    "vigente":              "Vigente",
    "vigente_com_ressalva": "Vigente (com ressalva judicial)",
    "tramitacao":           "Em tramitação",
    "pendente_embargos":    "Julgado — Embargos pendentes",
    "transitado_julgado":   "Transitado em julgado",
}

STATUS_COLORS = {
    "vigente":              "#2ecc71",
    "vigente_com_ressalva": "#e67e22",
    "tramitacao":           "#8b8b8b",
    "pendente_embargos":    "#c44b4b",
    "transitado_julgado":   "#3dc8e6",
}
