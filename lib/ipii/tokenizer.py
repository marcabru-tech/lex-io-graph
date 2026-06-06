# Copyright © 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado
# IPII Engine — implementação proprietária para Lex-IO-Graph / Lexiograph
# Todos os direitos reservados.
# Uso comercial, reprodução ou distribuição sem autorização escrita
# da Hubstry Deep Tech é expressamente proibido.
# Contato: globaldeeptechecosystem@hubstry.dev
# hubstry.dev/lex-io-graph
"""
Componente 1 — Token Normativo (GuruMatrix 5D aplicada ao corpus jurídico).

Extrai automaticamente de cada nó do normas.json cinco dimensões:
  (i) Categoria Ontológica — tipo da norma
  (j) Campo do Conhecimento — temas regulatórios
  (k) Nível Hermenêutico — autores, correntes, brocardos
  (t) Tempo — ano, status, vigência
  (l) Paradigma/Jurisdição — direito comparado glocal

Propriedade intelectual: Hubstry Deep Tech © 2026.
"""

import re


STOPWORDS = {
    "de", "do", "da", "dos", "das", "em", "no", "na", "num", "numa",
    "um", "uma", "uns", "umas", "e", "ou", "para", "com", "por", "que",
    "se", "ao", "os", "as", "o", "a", "é", "são", "foi", "ser", "ter",
    "como", "mais", "mas", "seu", "sua", "seus", "suas", "isso", "este",
    "esta", "esse", "essa", "pelo", "pela", "pelos", "pelas", "entre",
    "sobre", "após", "ante", "até", "desde", "durante", "contra", "sem",
}


def tokenizar_norma(norma: dict) -> dict:
    """Converte nó do normas.json em token normativo 5D (GuruMatrix)."""
    return {
        "id": norma["id"],

        # (i) Categoria Ontológica
        "ontologia": norma.get("tipo", "indefinido"),

        # (j) Campo do Conhecimento
        "temas": norma.get("temas", []),

        # (k) Nível Hermenêutico
        "hermeneutica": {
            "autores": [
                {"nome": a.get("nome", ""), "obra": a.get("obra", "")}
                for a in norma.get("autores", [])
            ],
            "brocardos": [
                lat.get("original", "")
                for lat in norma.get("latim", [])
            ],
            "correntes": _extrair_correntes(norma),
        },

        # (t) Tempo
        "temporal": {
            "ano": norma.get("ano", 0),
            "status": norma.get("status", "desconhecido"),
            "em_vigor": norma.get("status") in ("vigente", "vigente_com_ressalva"),
        },

        # (l) Paradigma/Jurisdição
        "jurisdicao": _extrair_jurisdicoes(norma),

        # Metadados auxiliares
        "artigos_chave": norma.get("artigos_chave", []),
        "orgao": norma.get("orgao", ""),
        "ementa_tokens": _tokenizar_ementa(norma.get("ementa", "")),
    }


def _extrair_correntes(norma: dict) -> list:
    """Extrai correntes hermenêuticas dos autores e da ementa."""
    correntes = []
    textos = [
        norma.get("ementa", ""),
        norma.get("historia", ""),
    ] + [
        a.get("contribuicao", "")
        for a in norma.get("autores", [])
    ]
    texto = " ".join(textos).lower()

    mapa = {
        "positivismo": ["kelsen", "positivismo", "norma pura", "grundnorm"],
        "integridade": ["dworkin", "integridade", "romance em cadeia"],
        "hermeneutica_filosofica": ["gadamer", "fusão de horizontes", "hermenêutica filosófica"],
        "teleologica": ["ihering", "teleológico", "fins sociais"],
        "historica": ["savigny", "volksgeist", "histórica"],
        "comunicativa": ["habermas", "ação comunicativa", "discurso"],
        "protecionista": ["proteção integral", "proteção de menores", "vulnerável"],
        "jusnaturalismo": ["direito natural", "dignidade humana", "finnis", "fuller"],
        "tridimensional": ["reale", "tridimensional", "fato valor norma"],
    }

    for corrente, termos in mapa.items():
        if any(t in texto for t in termos):
            correntes.append(corrente)

    return list(set(correntes))


def _extrair_jurisdicoes(norma: dict) -> list:
    """Extrai jurisdições mencionadas no direito comparado glocal."""
    texto = " ".join([
        norma.get("direito_comparado", ""),
        norma.get("historia", ""),
        norma.get("ementa", ""),
    ]).lower()

    mapa = {
        "UE": ["gdpr", "dsa", "ai act", "eu ai act", "união europeia", "europeu"],
        "EUA": ["ccpa", "section 230", "coppa", "estados unidos", "califórnia", "americano"],
        "Alemanha": ["bgb", "hgb", "alemanha", "alemão"],
        "França": ["code civil", "frança", "francês", "napoleônico"],
        "Itália": ["codice civile", "itália", "italiano"],
        "China": ["china", "chinês", "regulamento chinês"],
        "UK": ["reino unido", "common law inglês", "magna carta"],
        "Vaticano": ["vaticano", "encíclica", "leão xiv", "santa sé"],
        "ONU": ["onu", "nações unidas", "convenção da onu"],
    }

    jurisdicoes = []
    for jur, termos in mapa.items():
        if any(t in texto for t in termos):
            jurisdicoes.append(jur)

    return list(set(jurisdicoes))


def _tokenizar_ementa(ementa: str) -> list:
    """Extrai palavras-chave relevantes da ementa."""
    palavras = re.findall(r'\b[a-záéíóúâêôãõçàü]{4,}\b', ementa.lower())
    return list(set(p for p in palavras if p not in STOPWORDS))


def tokenizar_corpus(normas: list) -> dict:
    """Tokeniza todas as normas do corpus. Retorna dict id → token."""
    return {n["id"]: tokenizar_norma(n) for n in normas}
