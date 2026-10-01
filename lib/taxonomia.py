"""
Mapa unico entre as tres taxonomias do Lexiograph.

- Vetores do grafo: lib.constants.THEMES (classificam normas do corpus).
- Temas do Radar: lib.radar.TEMAS_RADAR (+ temas curados no JSON do radar).
- Tags do questionario: lib.conformidade (granulares, por norma e por perfil).

Este modulo liga Radar -> vetores do grafo, para que um PL detectado aponte
as normas do corpus com que dialoga. A ligacao e de orientacao ao curador:
nao cria no nem aresta.
"""

RADAR_PARA_VETORES = {
    "ia": ["ia"],
    "dados": ["dados_pessoais"],
    "menores": ["menores"],
    "plataformas": ["internet"],
    "trabalho_digital": ["trabalho"],
    "infraestrutura_digital": ["soberania_tecnologica", "direito_economico"],
    "mercados_digitais": ["direito_economico", "internet"],
    "minerais_criticos": ["direito_economico", "soberania_tecnologica"],
    "soberania_digital": ["soberania_tecnologica"],
    "acordos_internacionais": ["direito_internacional_publico", "direito_economico"],
    # temas curados
    "Sustação dos Decretos 12.975 e 12.976/2026": ["internet", "menores"],
    "Cibersegurança e Resiliência Digital": ["soberania_tecnologica", "dados_pessoais"],
}


def vetores_do_tema_radar(tema: str) -> list[str]:
    return RADAR_PARA_VETORES.get(tema, [])


def normas_relacionadas(tema: str, normas: list[dict]) -> list[dict]:
    """Normas do corpus que compartilham ao menos um vetor com o tema do radar."""
    vet = set(vetores_do_tema_radar(tema))
    return [n for n in normas if vet & set(n.get("temas") or [])]


# ---- Proposicoes que ja estao no corpus ----
import re as _re

_RE_PROP = _re.compile(r"\b(PLP|PL|PEC|MPV|MP|PDL)\s*(?:n[º°o.]\s*)?([\d.]+)\s*/\s*(\d{2,4})")


def chave_proposicao(texto: str):
    """'PL 2.780/2024', 'PL 2780/2024' e 'MP 1.317/2025' -> chaves normalizadas."""
    out = []
    for tipo, num, ano in _RE_PROP.findall(texto or ""):
        tipo = "MPV" if tipo == "MP" else tipo
        num = num.replace(".", "").lstrip("0") or "0"
        ano = ano if len(ano) == 4 else "20" + ano
        out.append(f"{tipo} {num}/{ano}")
    return out


def indice_corpus(normas: list[dict]) -> dict:
    """Chave da proposicao -> norma do corpus que a contem (como no ou como origem)."""
    idx = {}
    for n in normas:
        txt = " ".join(str(n.get(c, "")) for c in ("nome", "sigla", "ementa", "historia"))
        for k in chave_proposicao(txt):
            idx.setdefault(k, n)
    return idx


def norma_no_corpus(item: dict, indice: dict):
    """Se o item do radar ja esta no grafo, devolve a norma correspondente."""
    for k in chave_proposicao(item.get("sigla", "")):
        if k in indice:
            return indice[k]
    return None
