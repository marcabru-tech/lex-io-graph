"""
Formatação de textos de apresentação derivados do corpus.

Separação de responsabilidades: lib.validacao conta e valida; este módulo
transforma contagem em texto legível. Fica fora de app.py para que a
formatação seja importável e testável — um script Streamlit executa a página
inteira ao ser importado, o que impede teste unitário do que mora nele.

Sem dependência de Streamlit: só texto.
"""

import html

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


ANO_NAO_CONFIRMADO = "não confirmado"


def ano_exibicao(valor) -> str:
    """Ano para exibição; 'não confirmado' quando o corpus não afirma um ano.

    Um nó cujo ano não foi confirmado em fonte oficial carrega null, e não um
    ano provável. Exibir 'None' ou vazio no lugar devolveria ao leitor a
    impressão de defeito, quando o que há é lacuna declarada.
    """
    if valor is None or valor == "":
        return ANO_NAO_CONFIRMADO
    return str(valor)


def cartao_norma_html(node: dict) -> str:
    """HTML do cartão de norma da home.

    Todo texto vindo do corpus é escapado: o cartão é inserido com
    unsafe_allow_html, então conteúdo de dados não pode carregar marcação.
    Só o HTML estrutural deste módulo é literal.
    """
    tipo = node.get("tipo")
    if tipo == "constituicao":
        pilula = "pill--lex"
    elif tipo == "jurisprudencia":
        pilula = "pill--graph"
    else:
        pilula = "pill--io"

    def esc(valor) -> str:
        return html.escape(str(valor if valor is not None else ""))

    artigos = node.get("artigos_chave") or []
    partes = [
        '<div class="norma-item">',
        f'<span class="pill {pilula}">{esc(node.get("sigla"))}</span> ',
        f'<strong>{esc(node.get("nome"))}</strong>',
        f'<div class="norma-ementa">{esc(node.get("ementa"))}</div>',
    ]
    if artigos:
        partes.append(
            '<div class="norma-artigos">'
            + " | ".join(esc(a) for a in artigos)
            + "</div>"
        )
    partes.append(link_fonte_oficial(node.get("fonte_oficial_url")))
    partes.append("</div>")
    return "".join(partes)


def link_fonte_oficial(url) -> str:
    """Trecho HTML do link 'Fonte oficial' do cartão de norma.

    Devolve string vazia quando o nó não tem URL confirmada — campo nulo,
    ausente ou vazio —, para que o cartão simplesmente não exiba link, sem
    marcador de ausência.

    Só aceita http(s). URL de outro esquema não é renderizada: um dado
    malformado no corpus não deve virar link ativo na página. O valor é
    escapado porque o cartão é montado como HTML.
    """
    if not isinstance(url, str) or not url.startswith(("https://", "http://")):
        return ""
    seguro = html.escape(url, quote=True)
    return (
        '<div class="norma-fonte">'
        f'<a href="{seguro}" target="_blank" rel="noopener noreferrer">Fonte oficial ↗</a>'
        "</div>"
    )
