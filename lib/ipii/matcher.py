# Copyright © 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado
# IPII (Interação Paramétrica Iterativa por Interoperabilidade) para Lex-IO-Graph / Lexiograph
# Todos os direitos reservados.
# Uso comercial, reprodução ou distribuição sem autorização escrita
# da Hubstry Deep Tech é expressamente proibido.
# Contato: globaldeeptechecosystem@hubstry.dev
# hubstry.dev/lex-io-graph
"""
Componente 2 — Matching Contextual Par-a-Par.

Calcula score de interseção entre dois tokens normativos em 6 dimensões:
  Temas (0.30) · Hierarquia (0.15) · Hermenêutica (0.15)
  Comparado (0.15) · Temporal (0.10) · Ementa (0.15)

Propriedade intelectual: Hubstry Deep Tech © 2026.
"""

from itertools import combinations


HIERARQUIA_NIVEL = {
    "constituicao": 5,
    "lei": 4,
    "pl": 3,
    "decreto": 3,
    "norma_regulamentar": 3,
    "jurisprudencia": 3,
    "documento_internacional": 3,
    "orgao": 2,
}

PESOS = {
    "temas": 0.30,
    "hierarquia": 0.15,
    "hermeneutica": 0.15,
    "comparado": 0.15,
    "temporal": 0.10,
    "ementa": 0.15,
}

THRESHOLD_FORTE = 0.75
THRESHOLD_MODERADA = 0.55
THRESHOLD_FRACA = 0.40


def calcular_intersecao(token_a: dict, token_b: dict) -> dict:
    """Calcula score de interseção entre dois tokens normativos."""

    scores = {}

    # 1. Temas em comum
    temas_a = set(token_a["temas"])
    temas_b = set(token_b["temas"])
    uniao = temas_a | temas_b
    intersecao = temas_a & temas_b
    scores["temas"] = len(intersecao) / len(uniao) if uniao else 0.0

    # 2. Hierarquia normativa
    nivel_a = HIERARQUIA_NIVEL.get(token_a["ontologia"], 1)
    nivel_b = HIERARQUIA_NIVEL.get(token_b["ontologia"], 1)
    diff = abs(nivel_a - nivel_b)
    if diff >= 2:
        scores["hierarquia"] = 1.0
    elif diff == 1:
        scores["hierarquia"] = 0.7
    else:
        scores["hierarquia"] = 0.3

    # 3. Hermenêutica — correntes e brocardos
    correntes_a = set(token_a["hermeneutica"].get("correntes", []))
    correntes_b = set(token_b["hermeneutica"].get("correntes", []))
    brocardos_a = set(token_a["hermeneutica"].get("brocardos", []))
    brocardos_b = set(token_b["hermeneutica"].get("brocardos", []))

    u_correntes = correntes_a | correntes_b
    i_correntes = correntes_a & correntes_b
    u_brocardos = brocardos_a | brocardos_b
    i_brocardos = brocardos_a & brocardos_b

    score_c = len(i_correntes) / len(u_correntes) if u_correntes else 0.0
    score_b = len(i_brocardos) / len(u_brocardos) if u_brocardos else 0.0
    scores["hermeneutica"] = (score_c * 0.7) + (score_b * 0.3)

    # 4. Direito comparado — jurisdições
    jur_a = set(token_a["jurisdicao"])
    jur_b = set(token_b["jurisdicao"])
    u_jur = jur_a | jur_b
    i_jur = jur_a & jur_b
    scores["comparado"] = len(i_jur) / len(u_jur) if u_jur else 0.0

    # 5. Temporal — proximidade histórica
    ano_a = token_a["temporal"]["ano"]
    ano_b = token_b["temporal"]["ano"]
    diff_anos = abs(ano_a - ano_b) if (ano_a and ano_b) else 100
    if diff_anos <= 2:
        scores["temporal"] = 1.0
    elif diff_anos <= 10:
        scores["temporal"] = 0.7
    elif diff_anos <= 30:
        scores["temporal"] = 0.4
    else:
        scores["temporal"] = 0.2

    # 6. Ementa — vocabulário comum
    ementa_a = set(token_a["ementa_tokens"])
    ementa_b = set(token_b["ementa_tokens"])
    u_ementa = ementa_a | ementa_b
    i_ementa = ementa_a & ementa_b
    scores["ementa"] = len(i_ementa) / len(u_ementa) if u_ementa else 0.0

    # Score final ponderado
    score_final = sum(scores[k] * PESOS[k] for k in PESOS)

    # Classificação
    if score_final >= THRESHOLD_FORTE:
        classificacao = "forte"
        tier = 1
    elif score_final >= THRESHOLD_MODERADA:
        classificacao = "moderada"
        tier = 2 if score_final >= 0.65 else 3
    elif score_final >= THRESHOLD_FRACA:
        classificacao = "fraca"
        tier = 4 if score_final >= 0.50 else 5
    else:
        classificacao = "irrelevante"
        tier = 0

    tipo_sugerido = _sugerir_tipo(scores, token_a, token_b, intersecao)

    return {
        "source": token_a["id"],
        "target": token_b["id"],
        "score": round(score_final, 3),
        "classificacao": classificacao,
        "tier": tier,
        "tipo_sugerido": tipo_sugerido,
        "scores_parciais": {k: round(v, 3) for k, v in scores.items()},
        "temas_comuns": sorted(list(intersecao)),
        "jurisdicoes_comuns": sorted(list(i_jur)),
        "correntes_comuns": sorted(list(i_correntes)),
    }


def _sugerir_tipo(
    scores: dict,
    token_a: dict,
    token_b: dict,
    temas_comuns: set
) -> str:
    """Sugere tipo de aresta com base nos scores e ontologias."""

    ont_a = token_a["ontologia"]
    ont_b = token_b["ontologia"]

    # Hierarquia: constituição fundamenta norma inferior
    if ont_a == "constituicao" or ont_b == "constituicao":
        return "hierarquia"

    # Interpreta: jurisprudência interpreta lei ou decreto
    if ont_a == "jurisprudencia" and ont_b in ("lei", "decreto", "norma_regulamentar"):
        return "interpreta"
    if ont_b == "jurisprudencia" and ont_a in ("lei", "decreto", "norma_regulamentar"):
        return "interpreta"

    # Regulamenta: decreto regulamenta lei
    if (ont_a == "decreto" and ont_b == "lei") or \
       (ont_b == "decreto" and ont_a == "lei"):
        return "regulamenta"

    # ANTINOMIA DESATIVADA (ago/2026): a regra anterior inferia conflito
    # normativo a partir de "mesmo nivel hierarquico + temas sobrepostos".
    # Similaridade de conjuntos nao prova incompatibilidade de comandos:
    # duas normas podem partilhar tema e nivel por se complementarem, por
    # disciplinarem situacoes distintas ou por serem decisoes sucessivas
    # sobre a mesma materia. Antinomia exige comandos incompativeis,
    # aplicaveis ao mesmo caso, com coexistencia temporal — e isso o motor
    # nao consegue verificar. Pares com essa assinatura caem em intersecao
    # (a afirmacao mais fraca), e a qualificacao fica com o curador.

    # Complementaridade: scores altos em múltiplas dimensões
    if scores["temas"] > 0.4 and (scores["comparado"] > 0.3 or scores["hermeneutica"] > 0.3):
        return "complementaridade"

    # Default: interseção temática
    return "intersecao"


def calcular_todas_intersecoes(
    tokens: dict,
    threshold: float = THRESHOLD_FRACA
) -> list:
    """Calcula interseção para todos os pares do corpus."""

    resultados = []
    ids = list(tokens.keys())

    for id_a, id_b in combinations(ids, 2):
        resultado = calcular_intersecao(tokens[id_a], tokens[id_b])
        if resultado["score"] >= threshold:
            resultados.append(resultado)

    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados
