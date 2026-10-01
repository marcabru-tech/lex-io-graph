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
