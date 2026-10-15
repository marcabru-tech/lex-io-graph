"""
Formatação de textos de apresentação derivados do corpus.

Separação de responsabilidades: lib.validacao conta e valida; este módulo
transforma contagem em texto legível. Fica fora de app.py para que a
formatação seja importável e testável — um script Streamlit executa a página
inteira ao ser importado, o que impede teste unitário do que mora nele.

Sem dependência de Streamlit: só texto.
"""

from lib.validacao import SEM_ESTADO, contar_estados


def quantidade(n: int, singular: str, plural: str) -> str:
    """Concorda em número com a contagem.

    Zero fica no plural, como em português: '0 verificados', '1 verificado',
    '3 verificados'.
    """
    return f"{n} {singular if n == 1 else plural}"


def resumo_verificacao(registros: list[dict]) -> str:
    """Legenda da métrica de jurisprudência: distribuição por estado.

    'sem estado' só entra quando há registro sem estado válido, para não
    anunciar categoria vazia nem esconder registro mal preenchido.
    """
    c = contar_estados(registros)
    partes = [
        quantidade(c["verificado"], "verificado", "verificados"),
        quantidade(c["pendente"], "pendente", "pendentes"),
        quantidade(c["contestado"], "contestado", "contestados"),
    ]
    if c[SEM_ESTADO]:
        partes.append(f"{c[SEM_ESTADO]} sem estado")
    return " · ".join(partes)
