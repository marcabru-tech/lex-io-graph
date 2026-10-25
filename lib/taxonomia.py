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

# O ano é capturado inteiro (\d+) e validado depois: só 2 ou 4 dígitos valem.
_RE_PROP = _re.compile(r"\b(PLP|PL|PEC|MPV|MP|PDL)\s*(?:n[º°o.]\s*)?([\d.]+)\s*/\s*(\d+)")


def _ano_completo(ano: str, pivo: int) -> str | None:
    """'2024' -> '2024'; '23' -> '2023'; '98' -> '1998'; 3 ou 5+ dígitos -> None.

    Ano de 2 dígitos vai para o século atual se não passar do ano corrente
    (pivo = dois últimos dígitos do ano corrente); senão, para o século XX.
    Nunca concatena "20" a um ano já longo (antes: '205' virava '20205').
    """
    if len(ano) == 4:
        return ano
    if len(ano) == 2:
        return ("20" if int(ano) <= pivo else "19") + ano
    return None


def chave_proposicao(texto: str, pivo: int | None = None):
    """'PL 2.780/2024', 'PL 2780/2024' e 'MP 1.317/2025' -> chaves normalizadas.

    Entradas com ano inválido (3 dígitos, 5 ou mais) não geram chave.
    """
    if pivo is None:
        from datetime import date
        pivo = date.today().year % 100
    out = []
    for tipo, num, ano in _RE_PROP.findall(texto or ""):
        ano_ok = _ano_completo(ano, pivo)
        if ano_ok is None:
            continue
        tipo = "MPV" if tipo == "MP" else tipo
        num = num.replace(".", "").lstrip("0") or "0"
        out.append(f"{tipo} {num}/{ano_ok}")
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
