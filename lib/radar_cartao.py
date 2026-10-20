"""
HTML do cartão de um item do Radar Legislativo.

Função pura, separada da página para ser testável: todo valor vindo do radar
ou do corpus fica numa linha só (normalizar_espacos) e passa por html.escape,
e o link só aparece se url_segura o aceitar. A linha única importa porque
st.markdown encerra o bloco HTML na primeira linha em branco e lê o resto
como Markdown. O HTML e as classes CSS são os mesmos definidos na página 8.
"""

from html import escape

from lib.seguranca import normalizar_espacos, url_segura


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
