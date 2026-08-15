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
    "consentimento": {
        "prioridade": "critica",
        "acao": "Implementar mecanismo de consentimento granular",
        "base": "LGPD art. 7º, I",
    },
    "bases_legais": {
        "prioridade": "critica",
        "acao": "Mapear e documentar bases legais para cada finalidade de tratamento",
        "base": "LGPD art. 7º",
    },
    "dpo": {
        "prioridade": "critica",
        "acao": "Nomear DPO (Encarregado de Proteção de Dados)",
        "base": "LGPD art. 41",
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
        "acao": "Documentar AI BOM (Bill of Materials) do modelo",
        "base": "PL 2.338 + NIST AI RMF 1.0",
    },
    "alto_risco": {
        "prioridade": "alta",
        "acao": "Realizar Relatório de Impacto (RIPA) para sistema de alto risco",
        "base": "PL 2.338 art. 12",
    },
    "transparencia_algoritmos": {
        "prioridade": "alta",
        "acao": "Implementar transparência algorítmica e direito de revisão humana",
        "base": "LGPD art. 20 + PL 2.338",
    },
    "discriminacao_algoritmica": {
        "prioridade": "alta",
        "acao": "Auditar modelo para viés discriminatório",
        "base": "PL 2.338 + CF art. 5º",
    },
    "decisao_automatizada": {
        "prioridade": "alta",
        "acao": "Garantir revisão humana para decisões automatizadas com impacto",
        "base": "LGPD art. 20",
    },
    "responsabilidade_plataformas": {
        "prioridade": "alta",
        "acao": "Revisar política de moderação de conteúdo (pós-Tema 987)",
        "base": "STF RE 1.037.396 + Decreto 12.975/2026",
    },
    "dever_proativo": {
        "prioridade": "alta",
        "acao": "Implementar deveres proativos de remoção de conteúdo ilícito",
        "base": "Decreto 12.975/2026",
    },
    "crianca_adolescente": {
        "prioridade": "critica",
        "acao": "Implementar verificação de idade e consentimento parental",
        "base": "LGPD art. 14 + ECA Digital",
    },
    "consentimento_pais": {
        "prioridade": "critica",
        "acao": "Obter consentimento específico de ao menos 1 responsável",
        "base": "LGPD art. 14, I + ECA Digital art. 12",
    },
    "verificacao_idade": {
        "prioridade": "critica",
        "acao": "Implementar mecanismo verificável de idade",
        "base": "ECA Digital + LGPD art. 14",
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
        "base": "CLT art. 227-A + NR-1",
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
        "base": "Decreto 12.976/2026 + PL 896/2023",
    },
    "deepfake": {
        "prioridade": "critica",
        "acao": "Detector de deepfake + remoção em até 24h",
        "base": "Decreto 12.976/2026",
    },
    "transferencia_internacional": {
        "prioridade": "media",
        "acao": "Revisar transferências internacionais de dados",
        "base": "LGPD art. 33",
    },
    "dados_sensiveis": {
        "prioridade": "critica",
        "acao": "Tratamento de dados sensíveis requer consentimento específico e destacado",
        "base": "LGPD art. 11",
    },
    "guarda_logs": {
        "prioridade": "alta",
        "acao": "Implementar guarda de logs de conexão por 1 ano",
        "base": "Marco Civil art. 13",
    },
    "etica_ia": {
        "prioridade": "media",
        "acao": "Adotar princípios éticos de IA (dignidade, transparência, não-discriminação)",
        "base": "PL 2.338 art. 5º + Magnifica Humanitas",
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
