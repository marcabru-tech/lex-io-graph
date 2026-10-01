"""
Natureza epistêmica das afirmações exibidas no Lex-IO-Graph.

Quatro selos com semântica explícita. Não formam uma escala única:
FATO e HIPÓTESE dizem respeito à evidência; INTERPRETAÇÃO é análise;
METÁFORA é recurso retórico.

    fato          — afirmação sustentada por fonte (norma, decisão, dado oficial)
    interpretacao — leitura analítica do Lexiograph
    hipotese      — inferência não demonstrada
    metafora      — formulação analógica, não proposição factual
"""

import html as _html

SELOS = {
    "fato": ("FATO", "#2ecc71", "Afirmação sustentada por fonte: norma, decisão ou dado oficial."),
    "interpretacao": ("INTERPRETAÇÃO", "#d4a853", "Leitura analítica do Lexiograph."),
    "hipotese": ("HIPÓTESE", "#e67e22", "Inferência não demonstrada."),
    "metafora": ("METÁFORA", "#8a8478", "Formulação analógica, não proposição factual."),
}


def selo(natureza: str) -> str:
    """Selo HTML inline com a definição no title (aparece ao passar o mouse)."""
    rotulo, cor, definicao = SELOS.get(natureza, (natureza.upper(), "#8a8478", ""))
    return (f"<span title='{_html.escape(definicao)}' style='font-family:DM Mono,monospace;"
            f"font-size:10px;letter-spacing:.08em;color:{cor};border:1px solid {cor};"
            f"border-radius:3px;padding:1px 6px;white-space:nowrap'>{rotulo}</span>")


def legenda() -> str:
    """Linha de legenda com os quatro selos e suas definições."""
    return " &nbsp; ".join(f"{selo(k)} <span style='color:#8a8478;font-size:12px'>{d}</span>"
                           for k, (_, _, d) in SELOS.items())
