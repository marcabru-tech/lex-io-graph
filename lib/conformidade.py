"""
lib/conformidade.py
Quadro de Conformidade — Lexiograph v2
Questionário + Radar de Conformidade + Relatório
Não coleta dados pessoais. LGPD compliant.
"""

import streamlit as st
from datetime import datetime


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
        "guarda_logs", "neutridade_rede", "sigilo_comunicacao",
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
        "decisao_automatizada", "viies_algoritmico",
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
            "dados_pessoais", "transparencia", "governanca", "seguranca",
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
            "viies_algoritmico", "discriminacao_algoritmica",
        ],
        "Não": [],
        "Estou avaliando": ["inteligencia_artificial", "governanca_ia"],
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
            "conteudo_ilicito",
        ],
        "Sim — site institucional": [
            "internet", "dados_pessoais", "consentimento",
        ],
        "Não": [],
    },
    "porte": {
        "Startup / MEI": [],
        "PME (10–250 funcionários)": ["governanca", "compliance"],
        "Grande empresa (250+)": [
            "governanca", "compliance", "relatorio_impacto", "dpo",
        ],
        "Órgão público": ["governanca", "compliance", "transparencia"],
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
        "acao": "Confirmar a vigência por país de destino: Mercosul–EFTA vale com a Islândia desde 01/10/2026; o acordo com a UE está em aplicação provisória desde 01/05/2026",
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
        "base": "Lei 15.506/2026, art. 41; Decreto 13.118/2026",
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
        "acao": "Avaliar riscos psicossociais de IA no ambiente de trabalho",
        "base": "NR-1 item 1.5.3",
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
        "acao": "Implementar protocolo de remoção rápida para deepfakes e conteúdo íntimo",
        "base": "Decreto 12.976/2026, arts. 4º a 8º e 12 (o PL 896/2023 é proposta em tramitação, não obrigação)",
    },
    "deepfake": {
        "prioridade": "critica",
        "acao": "Conteúdo íntimo de terceiro divulgado sem autorização, inclusive o produzido ou manipulado por IA: indisponibilizar em até 2h após a notificação (art. 7º, § 1º; art. 3º, I). Até regulamentação pela autoridade competente, demais hipóteses de violência contra a mulher no ambiente digital: no prazo de 6h (art. 12, I) ou de 24h (art. 12, II), remover o conteúdo ou comunicar ao notificante o fundamento da manutenção e os meios de contestação. Aplicações que geram conteúdo por IA: vedada a geração ou modificação de conteúdo íntimo de terceiro (art. 9º) e exigidas salvaguardas para bloquear essas solicitações, conforme regulamento (art. 10)",
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
        "**Privacidade:** Este aplicativo não coleta, armazena nem "
        "compartilha dados pessoais. As respostas são processadas "
        "exclusivamente durante a sua sessão e não são persistidas. "
        "Nenhum dado identificável (nome, email, CPF, CNPJ) é solicitado. "
        "LGPD (Lei 13.709/2018)."
    )


def render_disclaimer_rodape():
    st.markdown("---")
    st.caption(
        "⚠️ Quadro de diagnóstico preliminar. "
        "Não substitui assessoria jurídica ou técnica especializada. "
        "Scores calculados pelo IPII Engine com base no corpus atualizado. "
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


def _score_norma(norma: dict, tags_perfil: set) -> float:
    norma_id = norma["id"]
    tags_norma = _tags_norma(norma_id, norma)

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

    for tag in tags:
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
    acoes_unicas.sort(key=lambda x: ordem.get(x["prioridade"], 4))
    return acoes_unicas


def gerar_radar(perfil: dict, normas: list, arestas: list) -> dict:
    tags_perfil = _temas_do_perfil(perfil)

    normas_scored = []
    for norma in normas:
        score = _score_norma(norma, tags_perfil)
        if score > 0.05:
            tags_match = tags_perfil & _tags_norma(norma["id"], norma)
            normas_scored.append({
                "id": norma["id"],
                "nome": norma.get("nome", norma["id"]),
                "tipo": norma.get("tipo", ""),
                "status": norma.get("status", ""),
                "score": score,
                "pct": int(score * 100),
                "tags_match": sorted(tags_match),
                "artigos_chave": norma.get("artigos_chave", []),
            })

    normas_scored.sort(key=lambda x: x["score"], reverse=True)
    ids_relevantes = {n["id"] for n in normas_scored}

    arestas_filtradas = [
        e for e in arestas
        if e["source"] in ids_relevantes and e["target"] in ids_relevantes
    ]

    for a in arestas_filtradas:
        tipo = a.get("tipo", "")
        if tipo == "antinomia":
            a["risco"] = "alto"
        elif tipo == "intersecao":
            a["risco"] = "medio"
        else:
            a["risco"] = "baixo"

    arestas_filtradas.sort(
        key=lambda x: {"alto": 0, "medio": 1, "baixo": 2}.get(x["risco"], 3)
    )

    return {
        "tags_perfil": sorted(tags_perfil),
        "normas": normas_scored,
        "arestas": arestas_filtradas,
        "acoes": _gerar_acoes(perfil),
    }


RISCO_ICO = {"alto": "🔴", "medio": "🟡", "baixo": "🟢"}
PRIO_ICO = {"critica": "🔴", "alta": "🟠", "media": "🟡", "baixa": "🟢"}


def render_radar(radar: dict):
    st.markdown("---")
    st.markdown("### Seu Quadro de Conformidade")

    n_criticas = len([a for a in radar["acoes"] if a["prioridade"] == "critica"])
    risco_max = (
        radar["arestas"][0]["risco"] if radar["arestas"] else "nenhum"
    )
    risco_display = {
        "alto": "🔴 Alto", "medio": "🟡 Médio",
        "baixo": "🟢 Baixo", "nenhum": "⚪ Nenhum",
    }.get(risco_max, "⚪")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Normas aplicáveis", len(radar["normas"]))
    c2.metric("Interseções", len(radar["arestas"]))
    c3.metric("Ações críticas", n_criticas)
    c4.metric("Risco máximo", risco_display)

    st.markdown("#### Normas aplicáveis")
    for norma in radar["normas"][:15]:
        ico = "🔴" if norma["pct"] >= 60 else "🟡" if norma["pct"] >= 30 else "🟢"
        with st.expander(f"{ico} {norma['nome']} — relevância {norma['pct']}%"):
            st.markdown(f"**Tipo:** {norma['tipo']} · **Status:** {norma['status']}")
            if norma["tags_match"]:
                st.markdown(f"**Tags em comum:** {', '.join(norma['tags_match'][:8])}")
            if norma["artigos_chave"]:
                st.markdown(f"**Artigos-chave:** {', '.join(norma['artigos_chave'][:5])}")

    if radar["arestas"]:
        st.markdown("#### Interseções regulatórias")
        for a in radar["arestas"][:10]:
            ico = RISCO_ICO.get(a["risco"], "ℹ️")
            st.markdown(
                f"{ico} **{a['source']} ↔ {a['target']}** ({a.get('tipo', '')})"
            )
            if a.get("descricao"):
                st.caption(a["descricao"])

    if radar["acoes"]:
        st.markdown("#### Ações recomendadas")
        for a in radar["acoes"]:
            ico = PRIO_ICO.get(a["prioridade"], "⚪")
            st.markdown(f"{ico} **{a['acao']}**")
            st.caption(f"Base legal: {a['base']}")


def gerar_relatorio_html(radar: dict, perfil: dict) -> str:
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    rows_perfil = "".join(
        f"<tr><td>{PERGUNTAS[k]['label']}</td><td>{v}</td></tr>"
        for k, v in perfil.items()
    )
    rows_normas = "".join(
        f"<tr><td>{i}</td><td>{n['nome']}</td><td>{n['pct']}%</td>"
        f"<td>{n['status']}</td><td>{', '.join(n['tags_match'][:3])}</td></tr>"
        for i, n in enumerate(radar["normas"][:15], 1)
    )
    rows_arestas = "".join(
        f"<tr><td>{RISCO_ICO.get(a['risco'],'ℹ️')}</td>"
        f"<td>{a['source']} ↔ {a['target']}</td>"
        f"<td>{a.get('tipo','')}</td>"
        f"<td>{a.get('descricao','')}</td></tr>"
        for a in radar["arestas"][:10]
    )
    rows_acoes = "".join(
        f"<tr><td>{PRIO_ICO.get(a['prioridade'],'⚪')}</td>"
        f"<td>{a['acao']}</td><td>{a['base']}</td></tr>"
        for a in radar["acoes"]
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
  @media print {{ body {{ margin: 20px; }} }}
</style>
</head>
<body>
<h1>Lexiograph — Quadro de Conformidade</h1>
<p class="meta">Gerado em: {now} · Engine IPII v0.2.0 · Corpus: 18 normas · Hubstry Deep Tech</p>
<h2>Perfil</h2>
<table><tr><th>Dimensão</th><th>Resposta</th></tr>{rows_perfil}</table>
<h2>Tags do Perfil ({len(radar['tags_perfil'])})</h2>
<p style="font-size:13px">{', '.join(radar['tags_perfil'][:30])}</p>
<h2>Normas Aplicáveis ({len(radar['normas'])})</h2>
<table><tr><th>#</th><th>Norma</th><th>Relevância</th><th>Status</th><th>Tags</th></tr>
{rows_normas}</table>
<h2>Interseções Regulatórias ({len(radar['arestas'])})</h2>
<table><tr><th>Risco</th><th>Par</th><th>Tipo</th><th>Descrição</th></tr>
{rows_arestas}</table>
<h2>Ações Recomendadas ({len(radar['acoes'])})</h2>
<table><tr><th>Prioridade</th><th>Ação</th><th>Base Legal</th></tr>
{rows_acoes}</table>
<p class="meta" style="margin-top:40px; border-top:1px solid #eee; padding-top:16px;">
  ⚠️ Diagnóstico preliminar. Não substitui assessoria jurídica ou técnica especializada.<br>
  Lexiograph · Hubstry Deep Tech · 2026
</p>
</body></html>"""


def render_botao_limpar():
    if st.button("🔄 Limpar e recomeçar", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith("q_") or key in ("radar_gerado", "radar_perfil"):
                del st.session_state[key]
        st.rerun()
