"""
HTML dos blocos do Radar Legislativo com dados externos.

Funções puras, separadas da página para serem testáveis: todo valor vindo do
radar ou do corpus fica numa linha só (normalizar_espacos) e passa por
html.escape, e um link só aparece se a validação correspondente o aceitar.

Por que HTML e não Markdown: num bloco HTML o st.markdown não aplica a sintaxe
de Markdown nem o autolink do GFM, que transforma www.x.com e a@x.com em link
mesmo com escape por barra invertida. Duas condições para o texto ficar
inerte: o bloco começa com <div> (um <span> no início da linha não abre bloco
HTML no CommonMark, e o texto voltaria a ser lido como Markdown) e não tem
linha em branco, que encerra o bloco.
"""

from html import escape

from lib.seguranca import normalizar_espacos, url_execucao_segura, url_segura

# st.caption no tema do app (.streamlit/config.toml): fonte 0.875rem e
# textColor #e8e4dc com 60% de opacidade.
_ESTILO_LEGENDA = "font-size:0.875rem;color:rgba(232,228,220,0.6);"


def _texto(valor) -> str:
    """Conteúdo de elemento: sem atributo envolvido, as aspas ficam como estão."""
    return escape(normalizar_espacos(valor), quote=False)


def _txt(valor) -> str:
    return escape(normalizar_espacos(valor))


def html_cartao(item: dict, no_corpus: dict | None = None, novidade: bool = False) -> str:
    """Cartão do item. `no_corpus` é a norma do grafo que já contém a proposição."""
    if no_corpus:
        rotulo = no_corpus.get("sigla") or no_corpus.get("nome")
        badge = (f'<span style="margin-left:8px;padding:2px 8px;border-radius:999px;font-size:10px;'
                 f'background:rgba(46,204,113,0.12);border:1px solid rgba(46,204,113,0.35);color:#2ecc71;">'
                 f'JÁ NO GRAFO · {_txt(rotulo)}</span>')
    else:
        badge = '<span class="novidade-badge">NOVO</span>' if novidade else ""
    if item.get("fontes"):
        # Cartão consolidado: um link por Casa que trouxe a proposição.
        links = []
        for f in item["fontes"]:
            u = url_segura(f.get("url", ""))
            if u:
                links.append(f'<a href="{escape(u, quote=True)}" target="_blank" '
                             f'style="color:#1abc9c;font-size:10px;">↗ {_texto(f.get("fonte", "fonte"))}</a>')
        link = " ".join(links)
    else:
        url = url_segura(item.get("url", ""))
        link = (f'<a href="{escape(url, quote=True)}" target="_blank" style="color:#1abc9c;font-size:10px;">'
                f'↗ ver fonte</a>') if url else ""
    return f"""
<div class="radar-card">
  <div class="radar-sigla">{_txt(item.get('sigla', 'Sem sigla'))}{badge} {link}</div>
  <div class="radar-fonte">{_txt(item.get('fonte', ''))} · Detectado: {_txt(normalizar_espacos(item.get('data_deteccao') or '')[:10])}</div>
  <div class="radar-ementa">{_txt(item.get('ementa', 'Sem ementa disponível'))}</div>
  <div class="radar-status">Status: {_txt(item.get('status', 'Desconhecido'))}</div>
</div>"""


def html_termos_monitorados(termos: list) -> str:
    """Linha "Termos monitorados:" da seção Por Tema."""
    lista = ", ".join(_texto(t) for t in termos)
    return f"<div><strong>Termos monitorados:</strong> {lista}</div>"


def html_proveniencia(executor, execucao_url, sha256_temas) -> str:
    """Legenda de proveniência do snapshot (ADR 006)."""
    partes = [f"Proveniência do snapshot: coletado por {_texto(executor)}"]
    url = url_execucao_segura(execucao_url)
    if url:
        partes.append(f' (<a href="{escape(url, quote=True)}" target="_blank" '
                      f'rel="noopener noreferrer">ver execução</a>)')
    hash_curto = normalizar_espacos(sha256_temas or "")[:12]
    if hash_curto:
        partes.append(f" · sha256 {_texto(hash_curto)}…")
    return f'<div style="{_ESTILO_LEGENDA}">{"".join(partes)}</div>'
