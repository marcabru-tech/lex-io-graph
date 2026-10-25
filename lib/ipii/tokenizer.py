# Copyright © 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado
# IPII (Interação Paramétrica Iterativa por Interoperabilidade) para Lex-IO-Graph / Lexiograph
# Licença: PolyForm Noncommercial 1.0.0 (ver lib/ipii/LICENSE).
# Estudo e pesquisa liberados; uso comercial somente com autorização
# prévia e por escrito do titular.
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


_RE_LEI = re.compile(r"\bLei\s*(?:n[º°o.]\s*)?(\d[\d.]*)\s*/\s*(\d{4})\b", re.IGNORECASE)


def _numeros_de_lei(texto: str) -> set:
    """'Lei 12.965/2014' e 'Lei nº 12965/2014' -> {'12965/2014'}."""
    return {f"{num.replace('.', '').lstrip('0')}/{ano}" for num, ano in _RE_LEI.findall(texto or "")}


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

        # Evidência textual para "regulamenta" (A4): o número da própria lei,
        # tirado da sigla, e as leis que a norma cita na ementa ou na história.
        "numero_lei": (sorted(_numeros_de_lei(norma.get("sigla", "")))[:1] or [None])[0]
                      if norma.get("tipo") == "lei" else None,
        "leis_citadas": sorted(_numeros_de_lei(" ".join([norma.get("ementa", ""), norma.get("historia", "")]))),
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
        "EUA": ["eua", "ccpa", "section 230", "coppa", "estados unidos", "califórnia", "americano"],
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
        if any(_menciona(texto, t) for t in termos):
            jurisdicoes.append(jur)

    return list(set(jurisdicoes))


# Contexto negativo explícito: "distintos dos da União Europeia" contrasta,
# não toma a jurisdição como referência. Vale dentro da mesma oração.
_NEGACAO_ANTES = re.compile(r"\b(distint[oa]s?|diferentes?)\b[^.;:()]*$")
_LETRA = "a-z0-9à-ü"


def _menciona(texto: str, termo: str) -> bool:
    """O termo aparece como palavra inteira e fora de contexto negativo?

    Palavra inteira evita casar dentro de outra palavra (ex.: "dsa"). Uma
    ocorrência precedida, na mesma oração, por "distinto(s)/diferente(s)" não
    conta. Basta uma ocorrência válida.
    """
    padrao = re.compile(rf"(?<![{_LETRA}]){re.escape(termo)}(?![{_LETRA}])")
    for m in padrao.finditer(texto):
        antes = texto[max(0, m.start() - 60):m.start()]
        if not _NEGACAO_ANTES.search(antes):
            return True
    return False


def _tokenizar_ementa(ementa: str) -> list:
    """Extrai palavras-chave relevantes da ementa."""
    palavras = re.findall(r'\b[a-záéíóúâêôãõçàü]{4,}\b', ementa.lower())
    return list(set(p for p in palavras if p not in STOPWORDS))


def tokenizar_corpus(normas: list) -> dict:
    """Tokeniza todas as normas do corpus. Retorna dict id → token."""
    return {n["id"]: tokenizar_norma(n) for n in normas}
