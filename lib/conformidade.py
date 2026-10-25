"""
lib/conformidade.py
Quadro de Conformidade — Lexiograph v2
Questionário + Radar de Conformidade + Relatório
As respostas do questionário não são armazenadas nem enviadas; o contador de
visitas (lib/telemetria.py) é descrito em render_disclaimer.
"""

import streamlit as st
from lib.constants import STATUS_COLORS, rotulo_status
from datetime import datetime
from html import escape as _esc


NORMA_TAGS = {
    "cf88": [
        "fundamental", "constitucional", "liberdade_expressao",
        "protecao_dados", "dignidade", "igualdade", "devido_processo",
        "privacidade", "seguranca", "trabalho", "consumidor",
        "discriminacao", "crianca_adolescente",
    ],
    "lgpd": [
        "dados_pessoais", "consentimento", "bases_legais", "dpo",
        "transferencia_internacional", "direito_titular", "sancao",
        "dados_sensiveis", "menores", "impacto_protecao",
        "seguranca_dados", "incidente", "anonimizacao",
        "controlador", "operador", "encarregado",
    ],
    "marco_civil": [
        "internet", "plataformas", "responsabilidade_plataformas",
        "guarda_logs", "neutralidade_rede", "sigilo_comunicacao",
        "liberdade_expressao", "remocao_conteudo", "moderacao_conteudo",
        "provedor_aplicacao", "dados_usuario",
    ],
    "eca": [
        "crianca_adolescente", "protecao_integral", "violencia_infantil",
        "exploracao", "educacao", "saude_infantil",
    ],
    "eca_digital": [
        "crianca_adolescente", "ambiente_digital", "consentimento_pais",
        "verificacao_idade", "dados_menores", "publicidade_infantil",
        "protecao_integral", "geolocalizacao_menores",
        "violencia_digital_menores",
    ],
    "anpd": [
        "dados_pessoais", "fiscalizacao", "sancao", "regulamentacao",
        "orientacao", "dpo", "relatorio_impacto",
    ],
    "stj_resp": [
        "dados_pessoais", "dano_moral", "vazamento_dados",
        "responsabilidade_civil", "seguranca_dados", "incidente",
    ],
    "stj_resp_plat": [
        "plataformas", "remocao_conteudo", "notificacao",
        "responsabilidade_civil", "internet", "conteudo_ilicito",
    ],
    "stf_adimc": [
        "marco_civil", "constitucionalidade", "guarda_logs",
        "sancao_civil", "internet",
    ],
    "stf_tema987": [
        "plataformas", "responsabilidade_plataformas", "remocao_conteudo",
        "dever_proativo", "moderacao_conteudo", "liberdade_expressao",
        "inconstitucionalidade", "ordem_judicial",
    ],
    "pl_ia": [
        "inteligencia_artificial", "alto_risco", "transparencia_algoritmos",
        "discriminacao_algoritmica", "responsabilidade_ia", "impacto_social",
        "direitos_humanos", "auditoria_ia", "governanca_ia",
        "decisao_automatizada", "vies_algoritmico",
    ],
    "decreto_12975_2026": [
        "plataformas", "responsabilidade_plataformas", "dever_proativo",
        "moderacao_conteudo", "remocao_conteudo", "transparencia",
        "anpd_fiscalizacao", "fiscalizacao_plataformas",
    ],
    "decreto_12976_2026": [
        "violencia_genero", "deepfake", "conteudo_intimo",
        "remocao_conteudo", "protecao_mulher", "violencia_digital",
        "imagem_sexual", "plataformas",
    ],
    "pl_cc_digital": [
        "direito_civil_digital", "personalidade_digital", "dados_pessoais",
        "plataformas", "responsabilidade_civil", "danos_digitais",
        "identidade_digital",
    ],
    "pl_misoginia": [
        "violencia_genero", "discriminacao", "misoginia", "crime_odio",
        "conteudo_ilicito", "plataformas", "moderacao_conteudo",
    ],
    "nr1": [
        "seguranca_trabalho", "riscos_psicossociais", "monitoramento",
        "automacao_trabalho", "saude_mental", "ergonomia_digital",
        "vigilancia_trabalhador", "ia_ambiente_trabalho",
    ],
    "lei_15409_2026": [
        "violencia_genero", "feminicidio", "cadastro_agressor",
        "protecao_mulher", "reincidencia",
    ],
    "acordo_mercosul_singapura": [
        "comercio_exterior", "acordo_comercial", "regras_origem", "certificado_origem",
        "tarifas", "comercio_eletronico",
    ],
    "acordo_mercosul_efta": [
        "comercio_exterior", "acordo_comercial", "regras_origem", "certificado_origem", "tarifas",
    ],
    "acordo_mercosul_ue_ita": [
        "comercio_exterior", "acordo_comercial", "regras_origem", "certificado_origem", "tarifas",
    ],
    "lindb": ["contratos_internacionais", "lei_aplicavel", "transferencia_internacional"],
    "res_cnj_615": [
        "inteligencia_artificial", "governanca_ia", "auditoria_ia",
        "poder_judiciario", "supervisao_humana", "transparencia_algoritmos",
    ],
    "lei_15504_2026": [
        "datacenter", "computacao_nuvem", "energia", "incentivo_fiscal",
        "infraestrutura_digital", "soberania_tecnologica", "direito_economico",
    ],
    "lei_15506_2026": [
        "minerais_criticos", "mineracao", "incentivo_fiscal", "investimento_estrangeiro",
        "rastreabilidade", "energia", "soberania_tecnologica", "direito_economico",
    ],
    "decreto_13118_2026": [
        "minerais_criticos", "investimento_estrangeiro", "controle_societario",
        "soberania_tecnologica",
    ],
    "magnifica_humanitas": [
        "etica_ia", "dignidade_humana", "direitos_humanos",
        "responsabilidade_ia", "vigilancia", "trabalho_digno",
        "exclusao_digital", "comum_humanidade",
    ],
}

PERFIL_TEMA_MAP = {
    "setor": {
        "Fintech / Serviços Financeiros": [
            "dados_pessoais", "consentimento", "seguranca_dados",
            "bases_legais", "incidente", "transferencia_internacional",
            "impacto_protecao",
        ],
        "Healthtech / Saúde Digital": [
            "dados_sensiveis", "consentimento", "seguranca_dados",
            "anonimizacao",
        ],
        "Edtech / Educação Digital": [
            "crianca_adolescente", "consentimento_pais",
            "verificacao_idade", "dados_menores", "protecao_integral",
        ],
        "E-commerce / Marketplace": [
            "consumidor", "plataformas", "responsabilidade_plataformas",
            "dados_pessoais", "remocao_conteudo",
        ],
        "Govtech / Órgão Público": [
            "dados_pessoais", "transparencia", "seguranca",
        ],
        "Mídia / Comunicação": [
            "liberdade_expressao", "moderacao_conteudo",
            "plataformas", "responsabilidade_plataformas",
            "remocao_conteudo",
        ],
        "Escritório de Advocacia / Jurídico": [
            "dados_pessoais", "dados_sensiveis", "sigilo_comunicacao",
            "bases_legais", "seguranca_dados", "dpo", "direito_titular",
            "incidente", "privacidade", "poder_judiciario",
        ],
        "Infraestrutura Digital / Data Center / Nuvem": [
            "datacenter", "computacao_nuvem", "energia", "incentivo_fiscal",
            "infraestrutura_digital", "seguranca_dados",
            "transferencia_internacional", "soberania_tecnologica",
        ],
        "Comércio Exterior / Exportação": [
            "comercio_exterior", "regras_origem", "certificado_origem",
            "acordo_comercial", "transferencia_internacional",
        ],
        "Mineração / Minerais Críticos": [
            "minerais_criticos", "mineracao", "investimento_estrangeiro",
            "controle_societario", "rastreabilidade", "energia", "incentivo_fiscal",
        ],
        "Outro": ["dados_pessoais", "internet"],
    },
    "usa_ia": {
        "Sim": [
            "inteligencia_artificial", "alto_risco",
            "transparencia_algoritmos", "decisao_automatizada",
            "auditoria_ia", "governanca_ia", "responsabilidade_ia",
            "vies_algoritmico", "discriminacao_algoritmica", "etica_ia",
        ],
        "Não": [],
        "Estou avaliando": ["inteligencia_artificial", "governanca_ia", "etica_ia"],
    },
    "trata_dados": {
        "Sim — clientes": [
            "dados_pessoais", "consentimento", "bases_legais",
            "dpo", "direito_titular", "seguranca_dados",
        ],
        "Sim — funcionários": [
            "dados_pessoais", "riscos_psicossociais", "monitoramento",
            "vigilancia_trabalhador", "seguranca_trabalho",
        ],
        "Sim — ambos": [
            "dados_pessoais", "consentimento", "bases_legais", "dpo",
            "direito_titular", "seguranca_dados", "riscos_psicossociais",
            "monitoramento", "vigilancia_trabalhador",
        ],
        "Não": [],
        "Não sei": ["dados_pessoais", "consentimento"],
    },
    "online": {
        "Sim — plataforma / app": [
            "plataformas", "responsabilidade_plataformas",
            "moderacao_conteudo", "remocao_conteudo",
            "guarda_logs", "dados_usuario", "dever_proativo",
            "conteudo_ilicito", "deepfake", "violencia_genero",
        ],
        "Sim — site institucional": [
            "internet", "dados_pessoais", "consentimento",
        ],
        "Não": [],
    },
    "porte": {
        "Startup / MEI": [],
        # "governanca" e "compliance" saíram (25/10/2026): nenhuma norma nem
        # ação usava essas tags, que só inflavam o perfil sem correspondência.
        "PME (10–250 funcionários)": [],
        "Grande empresa (250+)": ["relatorio_impacto", "dpo"],
        "Órgão público": ["transparencia"],
    },
}

PERGUNTAS = {
    "setor": {
        "label": "Setor de atuação",
        "opcoes": list(PERFIL_TEMA_MAP["setor"].keys()),
    },
    "usa_ia": {
        "label": "Usa inteligência artificial?",
        "opcoes": list(PERFIL_TEMA_MAP["usa_ia"].keys()),
    },
    "trata_dados": {
        "label": "Trata dados pessoais?",
        "opcoes": list(PERFIL_TEMA_MAP["trata_dados"].keys()),
    },
    "online": {
        "label": "Atua online (plataforma, app, site)?",
        "opcoes": list(PERFIL_TEMA_MAP["online"].keys()),
    },
    "porte": {
        "label": "Porte da empresa",
        "opcoes": list(PERFIL_TEMA_MAP["porte"].keys()),
    },
}

# Aviso exibido UMA vez, antes das ações do Decreto 12.976/2026, quando
# alguma delas aparece (tela e relatório).
ENQUADRAMENTO_DECRETO_12976 = (
    "Verifique o enquadramento: o questionário não confirma se a aplicação intermedeia conteúdo gerado por terceiros nem identifica todas as suas funcionalidades de IA. Os deveres dos arts. 4º, 5º e 8º pressupõem intermediação de conteúdo gerado por terceiros; o art. 6º disciplina as providências do provedor após o recebimento de notificação; os arts. 7º, 9º e 10 tratam de hipóteses específicas relacionadas à remoção de conteúdo íntimo e à geração ou modificação desse conteúdo por inteligência artificial, incluindo salvaguardas aplicáveis aos provedores baseados em IA; o art. 12 estabelece prazos transitórios até a regulamentação pela autoridade competente, sem afastar o prazo de até duas horas previsto no art. 7º, § 1º. A aplicação de cada dispositivo depende das características do serviço."
)
TAGS_DECRETO_12976 = frozenset({"deepfake", "violencia_genero"})

# Aviso para quem usa ou avalia IA em serviço online sem ação do decreto
# (decisão da Luna, 25/10/2026): informativo, não cria obrigação nem ação.
ENQUADRAMENTO_DECRETO_12976_IA = (
    "Verifique o enquadramento: o perfil indica uso ou avaliação de inteligência artificial "
    "em serviço online. O questionário não determina a incidência jurídica de cada dispositivo "
    "do decreto. Confira se a empresa oferece uma aplicação de internet. Confira também se essa "
    "aplicação disponibiliza funcionalidades de IA e se elas entram nas hipóteses específicas do "
    "decreto. O art. 9º veda aos provedores de aplicações de internet gerar ou modificar conteúdo "
    "íntimo de terceiros mediante inteligência artificial ou outro recurso tecnológico que altere a "
    "imagem ou o som da vítima. O art. 10 exige dos provedores de aplicações baseados em "
    "funcionalidades de IA ou tecnologia equivalente salvaguardas técnicas e procedimentais para "
    "identificar e bloquear solicitações de geração desse conteúdo, conforme a regulamentação da "
    "autoridade competente. O simples uso de IA pela empresa "
    "não atrai, por si só, essas obrigações."
)
USA_IA_AVISO_DECRETO = frozenset({"Sim", "Estou avaliando"})
ONLINE_AVISO_DECRETO = frozenset({"Sim — site institucional", "Sim — plataforma / app"})


def aviso_decreto_12976(perfil: dict, acoes: list) -> str | None:
    """Texto do aviso de enquadramento do Decreto 12.976/2026, ou None.

    Um aviso só: com ação do decreto, o enquadramento das ações; sem ação, mas
    com IA (Sim ou Estou avaliando) em serviço online, o aviso informativo.
    """
    if any(a.get("tag_origem") in TAGS_DECRETO_12976 for a in acoes):
        return ENQUADRAMENTO_DECRETO_12976
    if perfil.get("usa_ia") in USA_IA_AVISO_DECRETO and perfil.get("online") in ONLINE_AVISO_DECRETO:
        return ENQUADRAMENTO_DECRETO_12976_IA
    return None

ACOES_POR_TAG = {
    "regras_origem": {
        "prioridade": "alta",
        "acao": "Verificar, por NCM, a regra de origem e o cronograma de desgravação no acordo aplicável ao destino (Singapura, EFTA ou União Europeia)",
        "base": "Decretos 13.081/2026, 13.126/2026 e 12.953/2026; manuais do MDIC/Siscomex",
    },
    "certificado_origem": {
        "prioridade": "alta",
        "acao": "Emitir a prova de origem exigida pelo acordo e pelo país de destino antes de embarcar",
        "base": "Regras de origem dos Decretos 13.081/2026, 13.126/2026 e 12.953/2026",
    },
    "acordo_comercial": {
        "prioridade": "media",
        "acao": "Confirmar a vigência por país de destino: Mercosul–EFTA aplica-se com a Islândia desde 01/10/2026 e, com a Noruega, a partir de 01/11/2026 (Suíça e Liechtenstein dependem de internalização); o acordo com a UE está em aplicação provisória desde 01/05/2026",
        "base": "Decreto 13.126/2026; Decreto 12.953/2026, art. 23.3 do Acordo",
    },
    "datacenter": {
        "prioridade": "alta",
        "acao": "Avaliar habilitação ao REDATA e mapear as contrapartidas: 10% da capacidade ao mercado interno, 2% em P&D e eficiência hídrica de até 0,05 L/kWh",
        "base": "Lei 11.196/2005, art. 11-B, § 1º (Lei 15.504/2026)",
    },
    "energia": {
        "prioridade": "media",
        "acao": "Documentar a origem da energia contratada; o critério de 'baixa emissão' do REDATA ainda depende de regulamento",
        "base": "Lei 11.196/2005, art. 11-B, § 1º, III",
    },
    "minerais_criticos": {
        "prioridade": "alta",
        "acao": "Verificar enquadramento do projeto na PNMCE e acompanhar a lista oficial de minerais do CIMCE",
        "base": "Lei 15.506/2026, arts. 5º e 41",
    },
    "investimento_estrangeiro": {
        "prioridade": "critica",
        "acao": "Mapear mudanças de controle e participação estrangeira relevante sujeitas à homologação do CIMCE",
        "base": "Lei 15.506/2026, art. 3º, § 2º, e art. 41; Decreto 13.118/2026",
    },
    "rastreabilidade": {
        "prioridade": "alta",
        "acao": "Estruturar registros de origem, licença ambiental e outorga mineral para o sistema de rastreabilidade",
        "base": "Lei 15.506/2026, art. 44",
    },
    "consentimento": {
        "prioridade": "critica",
        "acao": "Quando a base legal escolhida for o consentimento, coletá-lo de forma livre, informada e inequívoca, para finalidades determinadas",
        "base": "LGPD art. 7º, I (uma das hipóteses do art. 7º); art. 8º",
    },
    "bases_legais": {
        "prioridade": "critica",
        "acao": "Mapear e documentar bases legais para cada finalidade de tratamento",
        "base": "LGPD art. 7º",
    },
    "dpo": {
        "prioridade": "critica",
        "acao": "Indicar encarregado (DPO), observada a dispensa regulamentar para agentes de tratamento de pequeno porte, que devem manter canal de comunicação com o titular",
        "base": "LGPD art. 41, caput e § 3º; Resolução CD/ANPD nº 2/2022",
    },
    "seguranca_dados": {
        "prioridade": "critica",
        "acao": "Implementar medidas técnicas e administrativas de segurança",
        "base": "LGPD art. 46",
    },
    "incidente": {
        "prioridade": "alta",
        "acao": "Estabelecer plano de resposta a incidentes de dados",
        "base": "LGPD art. 48",
    },
    "inteligencia_artificial": {
        "prioridade": "alta",
        "acao": "Boa prática (não é obrigação vigente): documentar componentes, dados e versões do modelo",
        "base": "Referência, não obrigação vigente: PL 2.338/2023 (em tramitação na Câmara); NIST AI RMF 1.0 (norma técnica)",
    },
    "alto_risco": {
        "prioridade": "alta",
        "acao": "Boa prática (não é obrigação vigente): avaliar o impacto de sistemas de IA de maior risco",
        "base": "Referência, não obrigação vigente: PL 2.338/2023 (em tramitação; numeração de artigos sujeita à versão do texto)",
    },
    "transparencia_algoritmos": {
        "prioridade": "alta",
        "acao": "Informar, quando solicitado, os critérios e procedimentos de decisões automatizadas e assegurar o direito do titular de solicitar sua revisão",
        "base": "LGPD art. 20, caput e § 1º",
    },
    "discriminacao_algoritmica": {
        "prioridade": "alta",
        "acao": "Avaliar o modelo quanto a efeitos discriminatórios",
        "base": "LGPD art. 6º, IX (princípio da não discriminação); referência, não obrigação vigente: PL 2.338/2023 (em tramitação)",
    },
    "decisao_automatizada": {
        "prioridade": "alta",
        "acao": "Garantir canal para o titular solicitar a revisão de decisões tomadas unicamente com base em tratamento automatizado que afetem seus interesses (a LGPD não exige que a revisão seja feita por pessoa natural)",
        "base": "LGPD art. 20",
    },
    "responsabilidade_plataformas": {
        "prioridade": "alta",
        "acao": "Revisar política de moderação de conteúdo (pós-Tema 987)",
        "base": "STF RE 1.037.396 + Decreto 12.975/2026",
    },
    "dever_proativo": {
        "prioridade": "alta",
        "acao": "Verificar se o serviço está no âmbito do Decreto 12.975/2026, que trata de forma diferente cada tipo de serviço, e, se estiver, adotar os deveres de prevenção e resposta nele previstos",
        "base": "Decreto 12.975/2026",
    },
    "crianca_adolescente": {
        "prioridade": "critica",
        "acao": "Avaliar se o produto ou serviço é direcionado a crianças e adolescentes ou de acesso provável por eles (ECA Digital art. 1º) e, se for, aplicar os mecanismos de idade e supervisão cabíveis ao tipo de serviço",
        "base": "ECA Digital arts. 1º, 10 a 18 e 24; LGPD art. 14",
    },
    "consentimento_pais": {
        "prioridade": "critica",
        "acao": "Definir a base legal de cada tratamento de dados de crianças e adolescentes, sempre no seu melhor interesse (as hipóteses dos arts. 7º e 11 são admitidas). Quando a base for o consentimento, para crianças ele deve ser específico e em destaque, dado por ao menos um dos pais ou responsável. Verificar à parte as obrigações do ECA Digital que dependem do serviço: consentimento dos responsáveis para download em lojas de aplicativos (art. 12, § 2º) e vinculação de contas de usuários de até 16 anos à de um responsável em redes sociais (art. 24)",
        "base": "LGPD art. 14, caput e § 1º; Enunciado CD/ANPD nº 1/2023; ECA Digital arts. 12, § 2º, e 24",
    },
    "verificacao_idade": {
        "prioridade": "critica",
        "acao": "Para conteúdo, produto ou serviço impróprio, inadequado ou proibido a menores de 18 anos: adotar mecanismo confiável de verificação de idade a cada acesso, vedada a autodeclaração",
        "base": "ECA Digital art. 9º, § 1º",
    },
    "riscos_psicossociais": {
        "prioridade": "alta",
        "acao": "Avaliar os fatores de risco psicossociais relacionados ao trabalho, incluindo, na leitura do Lexiograph, os ligados ao uso de IA na organização do trabalho",
        "base": "NR-1 item 1.5.3.1.4",
    },
    "monitoramento": {
        "prioridade": "alta",
        "acao": "Garantir transparência sobre monitoramento algorítmico de trabalhadores",
        "base": "NR-1 item 1.5.4.4 alínea e",
    },
    "vigilancia_trabalhador": {
        "prioridade": "alta",
        "acao": "Limitar vigilância contínua — direito à desconexão",
        "base": "Boa prática (a CLT não prevê expressamente o direito à desconexão); NR-1, gerenciamento de riscos ocupacionais",
    },
    "remocao_conteudo": {
        "prioridade": "alta",
        "acao": "Revisar procedimento de remoção de conteúdo (pós-Tema 987)",
        "base": "MCI art. 19 + STF Tema 987",
    },
    "moderacao_conteudo": {
        "prioridade": "media",
        "acao": "Documentar política de moderação e critérios de remoção",
        "base": "Decreto 12.975/2026",
    },
    "violencia_genero": {
        "prioridade": "critica",
        "acao": "Manter canal oficial de notificação que informe o Ligue 180 (art. 5º, § 1º); confirmar o recebimento, decidir e comunicar o fundamento e os meios de contestação ao notificante e, se houver remoção, a quem publicou (art. 6º); adotar medidas técnicas e proporcionais para reduzir o alcance de ataques coordenados contra mulheres, mesmo sem notificação (art. 8º). A falha sistêmica na indisponibilização gera responsabilização (art. 4º)",
        "base": "Decreto 12.976/2026, arts. 4º, 5º, 6º e 8º (o PL 896/2023 é proposta em tramitação, não obrigação)",
    },
    "deepfake": {
        "prioridade": "critica",
        "acao": "Conteúdo íntimo de terceiro divulgado sem autorização, inclusive o produzido ou manipulado por IA: indisponibilizar em até 2h após a notificação (art. 7º, § 1º; art. 3º, I). Até regulamentação pela autoridade competente, demais casos de violência contra a mulher no ambiente digital: remover o conteúdo ou comunicar ao notificante o fundamento da manutenção e os meios de contestação em até 6h, quando o conteúdo for manifestamente ilegal (art. 12, I), ou em até 24h, nos demais casos (art. 12, II). Aplicações que geram conteúdo por IA: vedada a geração ou modificação de conteúdo íntimo de terceiro (art. 9º) e exigidas salvaguardas para bloquear essas solicitações, conforme regulamento (art. 10)",
        "base": "Decreto 12.976/2026, arts. 3º, I, 7º, 9º, 10 e 12",
    },
    "transferencia_internacional": {
        "prioridade": "media",
        "acao": "Revisar transferências internacionais de dados",
        "base": "LGPD art. 33",
    },
    "dados_sensiveis": {
        "prioridade": "critica",
        "acao": "Identificar a hipótese legal de cada tratamento de dado sensível: consentimento específico e destacado (art. 11, I) ou uma das hipóteses do art. 11, II",
        "base": "LGPD art. 11, I e II",
    },
    "guarda_logs": {
        "prioridade": "alta",
        "acao": "Provedor de aplicações constituído como pessoa jurídica que exerça a atividade de forma organizada, profissional e com fins econômicos: guardar os registros de acesso a aplicações por 6 meses (art. 15). A guarda de registros de conexão por 1 ano (art. 13) cabe ao provedor de conexão",
        "base": "Marco Civil arts. 13 e 15",
    },
    "etica_ia": {
        "prioridade": "media",
        "acao": "Boa prática (não é obrigação vigente): adotar princípios éticos de IA (dignidade, transparência, não discriminação)",
        "base": "Referência, não obrigação vigente: PL 2.338/2023 (em tramitação); encíclica Magnifica Humanitas (referência ética)",
    },
}


def render_disclaimer():
    st.info(
        "**Privacidade:** As respostas deste questionário são enviadas ao "
        "servidor do app apenas para calcular o quadro e ficam na memória da "
        "sua sessão enquanto ela durar; não são gravadas em banco de dados nem "
        "em arquivo. Nenhum dado identificável (nome, email, CPF, "
        "CNPJ) é solicitado. O app mantém um contador de visitas: na primeira "
        "abertura de cada página, registra a página, a data e a hora, o "
        "ambiente e um código aleatório de sessão nos registros da "
        "hospedagem (Google Cloud), guardados por até 12 meses para estatística "
        "agregada. O contador não usa cookies e não grava "
        "IP, navegador nem localização. Como qualquer servidor, a hospedagem "
        "registra por tempo limitado dados técnicos de cada acesso (como o IP)."
    )


def render_disclaimer_rodape():
    st.markdown("---")
    st.caption(
        "⚠️ Triagem informativa, não é certificação de conformidade nem parecer jurídico. "
        "Os percentuais medem a interseção temática entre o perfil e cada norma do corpus "
        "curado, considerando só os temas que o questionário consegue avaliar e que alguma "
        "norma pontuada do corpus aborda (indicador "
        "heurístico); não medem risco jurídico nem obrigação aplicável. "
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )


def render_questionario():
    st.markdown("### Quais normas se aplicam ao seu negócio?")
    st.markdown(
        "Responda 5 perguntas. O IPII Engine calcula as normas aplicáveis "
        "ao seu perfil, identifica riscos e sugere ações."
    )

    with st.form("quadro_conformidade"):
        cols = st.columns(2)
        perfil = {}

        for i, (chave, pergunta) in enumerate(PERGUNTAS.items()):
            with cols[i % 2]:
                perfil[chave] = st.selectbox(
                    pergunta["label"],
                    options=pergunta["opcoes"],
                    key=f"q_{chave}",
                )

        submitted = st.form_submit_button(
            "🔍 Gerar meu quadro de conformidade",
            type="primary",
            use_container_width=True,
        )

    return perfil, submitted


def _temas_do_perfil(perfil: dict) -> set:
    tags = set()
    for chave, resposta in perfil.items():
        tags.update(PERFIL_TEMA_MAP.get(chave, {}).get(resposta, []))
    return tags


def _tags_norma(norma_id: str, norma: dict) -> set:
    tags = set(norma.get("temas", []))
    tags.update(NORMA_TAGS.get(norma_id, []))
    return tags


def _tags_observaveis() -> set:
    """Temas que o questionário consegue avaliar (gerados por alguma resposta)."""
    tags = set()
    for respostas in PERFIL_TEMA_MAP.values():
        for lista in respostas.values():
            tags.update(lista)
    return tags


TAGS_OBSERVAVEIS = _tags_observaveis()

# Status que nunca entram no percentual de interseção temática: o documento
# não tem força jurídica no direito brasileiro. Quando tem tema em comum com o
# perfil, aparece à parte, sem percentual (ver gerar_radar e render_radar).
STATUS_FORA_DA_PONTUACAO = frozenset({"referencia_etica"})


def _score_norma(norma: dict, tags_perfil: set) -> float:
    """Interseção temática entre o perfil e a norma.

    Considera só os temas da norma que o questionário consegue avaliar
    (TAGS_OBSERVAVEIS). Temas fora do questionário não entram na conta e são
    informados à parte (ver gerar_radar), para não penalizar a norma em
    silêncio nem sugerir uma avaliação que o questionário não faz.
    """
    norma_id = norma["id"]
    if norma.get("status") in STATUS_FORA_DA_PONTUACAO:
        return 0.0
    tags_norma = _tags_norma(norma_id, norma) & TAGS_OBSERVAVEIS

    if not tags_perfil or not tags_norma:
        return 0.0

    intersecao = tags_perfil & tags_norma
    uniao = tags_perfil | tags_norma

    if not uniao:
        return 0.0

    jaccard = len(intersecao) / len(uniao)
    cobertura = len(intersecao) / len(tags_perfil) if tags_perfil else 0
    score = (jaccard * 0.35) + (cobertura * 0.65)

    if norma.get("status") in ("vigente", "vigente_com_ressalva"):
        score *= 1.1
    if norma.get("tipo") == "constituicao":
        score = max(score, 0.25)

    return min(round(score, 3), 1.0)


def _gerar_acoes(perfil: dict) -> list:
    tags = _temas_do_perfil(perfil)
    acoes = []

    for tag in sorted(tags):
        if tag in ACOES_POR_TAG:
            acao = dict(ACOES_POR_TAG[tag])
            acao["tag_origem"] = tag
            acoes.append(acao)

    vistos = set()
    acoes_unicas = []
    for a in acoes:
        if a["acao"] not in vistos:
            vistos.add(a["acao"])
            acoes_unicas.append(a)

    ordem = {"critica": 0, "alta": 1, "media": 2, "baixa": 3}
    # Desempate explícito pela tag, para a ordem não variar entre execuções.
    acoes_unicas.sort(key=lambda x: (ordem.get(x["prioridade"], 4), x["tag_origem"], x["acao"]))
    return acoes_unicas




# Classificação explícita de TODO status conhecido. Status fora desta tabela
# não cai em "vigente": vai para "desconhecido", exibido à parte para conferência.
GRUPO_POR_STATUS = {
    "vigente": "vigente",
    "vigente_com_ressalva": "vigente",
    "vigente_parcial": "vigente",
    "aplicacao_provisoria": "vigente",
    # Grupo visual próprio: o instrumento não foi incorporado ao direito brasileiro.
    # A pontuação não muda (continua pontuado como antes); só o título da seção.
    "instrumento_externo": "nao_incorporado",
    "pendente_embargos": "vigente",
    "transitado_julgado": "vigente",
    "tramitacao": "proposta",
    "em_conferencia": "em_conferencia",
    "referencia_etica": "referencia",
}


def _grupo(status: str) -> str:
    """Separa o que é norma vigente do que não pode ser lido como obrigação."""
    return GRUPO_POR_STATUS.get(status, "desconhecido")


def _tags_pontuaveis(normas: list) -> set:
    """Temas que o questionário avalia E que alguma norma pontuável carrega.

    Tag do perfil que só aciona ação (sem nenhuma norma pontuável com ela) não
    entra no denominador da cobertura: senão diluiria a nota de todas as normas.
    """
    tags = set()
    for n in normas:
        if n.get("status") not in STATUS_FORA_DA_PONTUACAO:
            tags |= _tags_norma(n["id"], n)
    return tags & TAGS_OBSERVAVEIS


# Grupos cujas arestas não recebem risco automático (A6-d).
GRUPOS_SO_REFERENCIA = frozenset({"nao_incorporado", "desconhecido", "referencia"})


def gerar_radar(perfil: dict, normas: list, arestas: list) -> dict:
    tags_perfil = _temas_do_perfil(perfil)
    tags_perfil_pontuaveis = tags_perfil & _tags_pontuaveis(normas)

    normas_scored = []
    for norma in normas:
        score = _score_norma(norma, tags_perfil_pontuaveis)
        if score > 0.05:
            tags_match = tags_perfil & _tags_norma(norma["id"], norma)
            normas_scored.append({
                "id": norma["id"],
                "nome": norma.get("nome", norma["id"]),
                "tipo": norma.get("tipo", ""),
                "status": norma.get("status", ""),
                "grupo": _grupo(norma.get("status", "")),
                "score": score,
                "pct": int(score * 100),
                "tags_match": sorted(tags_match),
                "temas_fora_do_questionario": len(_tags_norma(norma["id"], norma) - TAGS_OBSERVAVEIS),
                # Piso de 25% da Constituição sem nenhum tema em comum: é critério
                # de inclusão (base do ordenamento), não interseção temática.
                "base_constitucional": norma.get("tipo") == "constituicao" and not tags_match,
                "artigos_chave": norma.get("artigos_chave", []),
            })

    normas_scored.sort(key=lambda x: x["score"], reverse=True)
    ids_relevantes = {n["id"] for n in normas_scored}

    grupo_de = {n["id"]: n["grupo"] for n in normas_scored}
    arestas_filtradas = [
        dict(e) for e in arestas  # cópia: não altera os dados do corpus
        if e["source"] in ids_relevantes and e["target"] in ids_relevantes
    ]

    for a in arestas_filtradas:
        grupos = {grupo_de.get(a["source"]), grupo_de.get(a["target"])}
        tipo = a.get("tipo", "")
        if "em_conferencia" in grupos:
            a["risco"] = "em_conferencia"
        elif grupos & GRUPOS_SO_REFERENCIA:
            # A6-d (decisão da Luna, 25/10/2026): relação com instrumento não
            # incorporado, de status não reconhecido ou não vinculante não recebe
            # risco automático. Fica visível como referência, fora da priorização
            # e de "Maior interseção entre vigentes".
            a["risco"] = "referencia"
        elif "proposta" in grupos:
            a["risco"] = "prospectivo"
        elif tipo == "antinomia":
            a["risco"] = "alto"
        elif tipo == "intersecao":
            a["risco"] = "medio"
        else:
            a["risco"] = "baixo"

    arestas_filtradas.sort(
        key=lambda x: ORDEM_RISCO.get(x["risco"], 9)
    )

    # Referências não vinculantes com tema em comum: listadas à parte, sem percentual.
    referencias = []
    for norma in normas:
        if norma.get("status") not in STATUS_FORA_DA_PONTUACAO:
            continue
        comuns = tags_perfil & _tags_norma(norma["id"], norma) & TAGS_OBSERVAVEIS
        if comuns:
            referencias.append({
                "id": norma["id"],
                "nome": norma.get("nome", norma["id"]),
                "status": norma.get("status", ""),
                "rotulo": rotulo_status(norma.get("status", "")),
                "tags_match": sorted(comuns),
            })
    referencias.sort(key=lambda x: x["nome"])

    acoes = _gerar_acoes(perfil)
    return {
        "total_corpus": len(normas),
        "tags_perfil": sorted(tags_perfil),
        "normas": normas_scored,
        "referencias": referencias,
        "arestas": arestas_filtradas,
        "acoes": acoes,
        "aviso_decreto_12976": aviso_decreto_12976(perfil, acoes),
    }


RISCO_ICO = {"alto": "🔴", "medio": "🟡", "baixo": "🟢", "prospectivo": "🔵", "em_conferencia": "⚠️",
             "referencia": "📎"}
RISCO_ROTULO = {
    "prospectivo": "envolve proposta em tramitação (risco prospectivo, não obrigação vigente)",
    "em_conferencia": "envolve decisão em conferência (não utilizar como precedente)",
    "referencia": ("envolve instrumento não incorporado, não vinculante ou de status não reconhecido "
                   "(referência, sem classificação de risco)"),
}
ORDEM_RISCO = {"alto": 0, "medio": 1, "baixo": 2, "prospectivo": 3, "em_conferencia": 4, "referencia": 5}
TITULOS_GRUPO = {
    "vigente": "Normas vigentes com interseção temática",
    "proposta": "Propostas em tramitação — risco prospectivo, não obrigação vigente",
    "em_conferencia": "Decisões em conferência — não utilizar como precedente",
    "nao_incorporado": "Instrumentos externos — não incorporados ao direito brasileiro",
    "desconhecido": "Status não reconhecido — conferir antes de usar",
}
ORDEM_GRUPOS = ("vigente", "proposta", "nao_incorporado", "em_conferencia", "desconhecido")
PRIO_ICO = {"critica": "🔴", "alta": "🟠", "media": "🟡", "baixa": "🟢"}
TEXTO_NAO_INCORPORADO = (
    "Tratados e acordos ainda não incorporados ao ordenamento jurídico interno não são "
    "apresentados aqui como normas internas vigentes. A eventual vinculação internacional do "
    "Brasil deve ser verificada conforme o instrumento e sua situação jurídica."
)
TEXTO_REFERENCIAS = (
    "Documentos sem força jurídica no direito brasileiro, com tema em comum com o perfil. "
    "Aparecem para contexto ético e não entram no percentual de interseção temática."
)


def _por_grupo(radar: dict) -> dict:
    grupos = {"vigente": [], "proposta": [], "nao_incorporado": [], "em_conferencia": [],
              "desconhecido": [], "referencia": []}
    for n in radar["normas"]:
        grupos.setdefault(n.get("grupo", "vigente"), []).append(n)
    return grupos


def render_radar(radar: dict):
    st.markdown("---")
    st.markdown("### Seu Quadro de Conformidade")
    st.caption(
        "Triagem informativa: os percentuais medem a interseção temática entre o seu perfil "
        "e cada norma do corpus curado, considerando só os temas que este questionário "
        "consegue avaliar e que alguma norma pontuada do corpus aborda. Não confirmam conformidade ou desconformidade nem "
        "substituem parecer jurídico."
    )

    grupos = _por_grupo(radar)
    n_criticas = len([a for a in radar["acoes"] if a["prioridade"] == "critica"])
    riscos_vigentes = [a["risco"] for a in radar["arestas"] if a["risco"] in ("alto", "medio", "baixo")]
    risco_max = riscos_vigentes[0] if riscos_vigentes else "nenhum"
    risco_display = {
        "alto": "🔴 Alto", "medio": "🟡 Médio",
        "baixo": "🟢 Baixo", "nenhum": "⚪ Nenhum",
    }.get(risco_max, "⚪")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Normas vigentes relacionadas", len(grupos["vigente"]))
    c2.metric("Interseções", len(radar["arestas"]))
    c3.metric(
        "Ações críticas", n_criticas,
        help=("Inclui ações do Decreto 12.976/2026 condicionadas ao enquadramento indicado "
              "na seção de ações." if any(a.get("tag_origem") in TAGS_DECRETO_12976
                                          for a in radar["acoes"]) else None),
    )
    c4.metric("Maior interseção entre vigentes", risco_display)

    for chave in ORDEM_GRUPOS:
        lista = grupos[chave]
        if not lista:
            continue
        st.markdown(f"#### {TITULOS_GRUPO[chave]}")
        if chave == "em_conferencia":
            st.warning(
                "Registros judiciais ainda não conferidos na fonte oficial (ADR 007). "
                "Aparecem só para transparência; não são precedente utilizável."
            )
        if chave == "nao_incorporado":
            st.caption(TEXTO_NAO_INCORPORADO)
        for norma in lista[:15]:
            if chave == "vigente":
                ico = "🔴" if norma["pct"] >= 60 else "🟡" if norma["pct"] >= 30 else "🟢"
            else:
                ico = {"proposta": RISCO_ICO["prospectivo"], "nao_incorporado": "🌐"}.get(
                    chave, RISCO_ICO["em_conferencia"])
            rotulo = ("incluída como base constitucional, sem tema em comum com o perfil"
                      if norma.get("base_constitucional")
                      else f"interseção temática {norma['pct']}%")
            with st.expander(f"{ico} {norma['nome']} — {rotulo}"):
                st.markdown(f"**Tipo:** {norma['tipo']} · **Status:** {rotulo_status(norma['status'])}")
                if norma["tags_match"]:
                    st.markdown(f"**Temas em comum:** {', '.join(norma['tags_match'][:8])}")
                if norma["artigos_chave"]:
                    st.markdown(f"**Artigos-chave:** {', '.join(norma['artigos_chave'][:5])}")
                if norma.get("temas_fora_do_questionario"):
                    # Base constitucional não exibe percentual (A6-g): a legenda não o cita.
                    st.caption(
                        f"{norma['temas_fora_do_questionario']} tema(s) desta norma não são "
                        "avaliados por este questionário"
                        + ("." if norma.get("base_constitucional") else " e ficaram fora do percentual.")
                    )

    if radar.get("referencias"):
        st.markdown("#### Referências não vinculantes relacionadas")
        st.caption(TEXTO_REFERENCIAS)
        for r in radar["referencias"]:
            st.markdown(f"- **{r['nome']}** — :violet[{r['rotulo']}] · temas em comum: {', '.join(r['tags_match'][:6])}")

    if radar["arestas"]:
        st.markdown("#### Interseções regulatórias")
        for a in radar["arestas"][:10]:
            ico = RISCO_ICO.get(a["risco"], "ℹ️")
            st.markdown(
                f"{ico} **{a['source']} ↔ {a['target']}** ({a.get('tipo', '')})"
            )
            if a["risco"] in RISCO_ROTULO:
                st.caption(f"⚑ {RISCO_ROTULO[a['risco']]}")
            if a.get("descricao"):
                st.caption(a["descricao"])

    aviso_decreto = radar.get("aviso_decreto_12976")
    if radar["acoes"] or aviso_decreto:
        st.markdown("#### Ações recomendadas")
        if aviso_decreto:
            st.info(f"**Decreto 12.976/2026.** {aviso_decreto}")
        for a in radar["acoes"]:
            ico = PRIO_ICO.get(a["prioridade"], "⚪")
            st.markdown(f"{ico} **{a['acao']}**")
            st.caption(f"Base legal: {a['base']}")


# HTML FIXO E CONFIÁVEL: texto do código, com marcação proposital (<strong>).
# Não interpolar aqui nenhum valor variável ou vindo do usuário; esses passam por _esc.
AVISO_TRIAGEM_HTML = (
    "<strong>Triagem informativa — não é certificação de conformidade.</strong> "
    "Os percentuais medem a interseção temática entre o perfil e cada norma do corpus curado, "
    "considerando só os temas que o questionário consegue avaliar e que alguma norma pontuada "
    "do corpus aborda. "
    "Os indicadores não confirmam conformidade ou desconformidade, não garantem a identificação "
    "de todas as obrigações aplicáveis e não constituem auditoria, certificação ou parecer jurídico. "
    "Consulte os textos oficiais e submeta decisões relevantes a profissional habilitado."
)


def gerar_relatorio_html(radar: dict, perfil: dict) -> str:
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    e = lambda v: _esc(str(v))  # todo valor interpolado é escapado
    grupos = _por_grupo(radar)

    rows_perfil = "".join(
        f"<tr><td>{e(PERGUNTAS.get(k, {}).get('label', k))}</td><td>{e(v)}</td></tr>"
        for k, v in perfil.items()
    )

    def tabela_normas(lista):
        return "".join(
            f"<tr><td>{i}</td><td>{e(n['nome'])}</td>"
            + ("<td>base constitucional, sem tema em comum</td>" if n.get("base_constitucional")
               else f"<td>{n['pct']}%</td>")
            + f"<td>{n.get('temas_fora_do_questionario', 0)}</td>"
            f"<td>{e(rotulo_status(n['status']))}</td><td>{e(', '.join(n['tags_match'][:3]))}</td></tr>"
            for i, n in enumerate(lista[:15], 1)
        )

    secoes_normas = ""
    for chave in ORDEM_GRUPOS:
        lista = grupos[chave]
        if not lista:
            continue
        nota = ""
        if chave == "nao_incorporado":
            nota = f'<p style="font-size:13px">{e(TEXTO_NAO_INCORPORADO)}</p>'
        if chave == "em_conferencia":
            nota = ('<p style="font-size:13px;color:#a05a00">Registros judiciais ainda não '
                    "conferidos na fonte oficial; aparecem só para transparência e não são "
                    "precedente utilizável.</p>")
        secoes_normas += (
            f"<h2>{e(TITULOS_GRUPO[chave])} ({len(lista)})</h2>{nota}"
            "<table><tr><th>#</th><th>Norma</th><th>Interseção temática</th>"
            "<th>Temas fora do questionário</th><th>Status</th><th>Temas em comum</th></tr>"
            f"{tabela_normas(lista)}</table>"
        )

    secao_referencias = ""
    if radar.get("referencias"):
        itens = "".join(
            f"<tr><td>{e(r['nome'])}</td>"
            f"<td style=\"color:{STATUS_COLORS.get(r['status'], '#333')};font-weight:600\">{e(r['rotulo'])}</td>"
            f"<td>{e(', '.join(r['tags_match'][:6]))}</td></tr>"
            for r in radar["referencias"]
        )
        secao_referencias = (
            f"<h2>Referências não vinculantes relacionadas ({len(radar['referencias'])})</h2>"
            f'<p style="font-size:13px">{e(TEXTO_REFERENCIAS)}</p>'
            "<table><tr><th>Documento</th><th>Natureza</th><th>Temas em comum</th></tr>"
            f"{itens}</table>"
        )

    rows_arestas = "".join(
        f"<tr><td>{RISCO_ICO.get(a['risco'],'ℹ️')}</td>"
        f"<td>{e(a['source'])} ↔ {e(a['target'])}</td>"
        f"<td>{e(a.get('tipo',''))}</td>"
        f"<td>{e(a.get('descricao',''))}"
        + (f"<br><em>{e(RISCO_ROTULO[a['risco']])}</em>" if a['risco'] in RISCO_ROTULO else "")
        + "</td></tr>"
        for a in radar["arestas"][:10]
    )
    rows_acoes = "".join(
        f"<tr><td>{PRIO_ICO.get(a['prioridade'],'⚪')}</td>"
        f"<td>{e(a['acao'])}</td><td>{e(a['base'])}</td></tr>"
        for a in radar["acoes"]
    )
    total_corpus = radar.get("total_corpus", "")
    aviso_decreto = (
        f'<p class="aviso"><strong>Decreto 12.976/2026.</strong> {e(radar["aviso_decreto_12976"])}</p>'
        if radar.get("aviso_decreto_12976") else ""
    )

    return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Lexiograph — Quadro de Conformidade</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 800px;
         margin: 40px auto; color: #1a1a1a; line-height: 1.6; }}
  h1 {{ font-size: 1.5rem; border-bottom: 2px solid #d4a853; padding-bottom: 8px; }}
  h2 {{ font-size: 1.1rem; margin-top: 32px; color: #333; }}
  table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }}
  th {{ background: #f5f5f5; text-align: left; padding: 8px;
       border-bottom: 2px solid #ddd; font-size: 11px; text-transform: uppercase; }}
  td {{ padding: 8px; border-bottom: 1px solid #eee; }}
  .meta {{ font-size: 12px; color: #888; }}
  .aviso {{ font-size: 13px; background: #fff8e6; border-left: 3px solid #d4a853; padding: 10px 14px; }}
  @media print {{ body {{ margin: 20px; }} }}
</style>
</head>
<body>
<h1>Lexiograph — Quadro de Conformidade</h1>
<p class="meta">Gerado em: {now} · Triagem temática heurística · Corpus curado: {total_corpus} normas · Hubstry Deep Tech</p>
<p class="aviso">{AVISO_TRIAGEM_HTML}</p>
<h2>Perfil</h2>
<table><tr><th>Dimensão</th><th>Resposta</th></tr>{rows_perfil}</table>
<h2>Temas do perfil ({len(radar['tags_perfil'])})</h2>
<p style="font-size:13px">{e(', '.join(radar['tags_perfil'][:30]))}</p>
{secoes_normas}
{secao_referencias}
<h2>Interseções Regulatórias ({len(radar['arestas'])})</h2>
<table><tr><th>Risco</th><th>Par</th><th>Tipo</th><th>Descrição</th></tr>
{rows_arestas}</table>
<h2>Ações Recomendadas ({len(radar['acoes'])})</h2>
{aviso_decreto}
<table><tr><th>Prioridade</th><th>Ação</th><th>Base Legal</th></tr>
{rows_acoes}</table>
<p class="meta" style="margin-top:40px; border-top:1px solid #eee; padding-top:16px;">
  ⚠️ Triagem informativa. Não substitui assessoria jurídica ou técnica especializada.<br>
  Lexiograph · Hubstry Deep Tech · 2026
</p>
</body></html>"""


def render_botao_limpar():
    if st.button("🔄 Limpar e recomeçar", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith("q_") or key in ("radar_gerado", "radar_perfil"):
                del st.session_state[key]
        st.rerun()
