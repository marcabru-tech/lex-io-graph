import html
import re

import streamlit as st
import streamlit.components.v1 as components

from lib.constants import THEMES
from lib.conjuntos import carregar, conjuntos, lacunas, relacoes_no_par, figura_matriz, pares_em_frases
from lib.validacao import ids_externos
from lib.graph_builder import load_json
from lib.footer import render_footer

st.set_page_config(
    page_title="Teoria dos Conjuntos Jurídicos",
    page_icon="🧩",
    layout="wide"
)

st.markdown("<h1 style='text-align:center; color:#d4a853; font-family:Cormorant Garamond,serif;'>🧩 Teoria dos Conjuntos Jurídicos</h1>", unsafe_allow_html=True)
st.caption("Arquitetura Sistêmica do Ordenamento Jurídico Brasileiro — Lexiograph")

aba_corpus, aba_teoria = st.tabs(["Conjuntos do corpus (calculados)", "Arquitetura teórica"])

# =============================================================
# Conjuntos calculados a partir de normas.json
# =============================================================
with aba_corpus:
    normas, arestas = carregar()
    por_id = {n["id"]: n for n in normas}
    cj = conjuntos(normas)
    vazios = lacunas(cj)

    st.markdown(
        "Cada vetor temático do Lexiograph é um conjunto: "
        "**A = { x | x é norma do corpus marcada com o vetor A }**. "
        "Os números abaixo são calculados a partir do corpus curado — um vetor ou uma "
        "norma nova entra aqui sem edição manual."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Vetores (conjuntos)", len(cj))
    c2.metric("Normas no corpus", len(normas))
    c3.metric("Pares com interseção", sum(
        1 for i, a in enumerate(cj) for b in list(cj)[i + 1:] if cj[a] & cj[b]))
    c4.metric("Pares disjuntos", len(vazios))

    st.markdown("#### Quantas normas cada par de vetores compartilha — |A ∩ B|")
    st.caption(
        "Cruze uma linha com uma coluna: o número é a quantidade de normas marcadas com os dois "
        "vetores. Só aparece a metade inferior porque A ∩ B = B ∩ A — a outra metade repetiria "
        "os mesmos números. Na diagonal, o total de normas de cada vetor. Passe o mouse para ver o par."
    )
    st.plotly_chart(figura_matriz(cj), use_container_width=True, config={"displayModeBar": False})

    nome_curto = lambda i: por_id[i].get("sigla") or por_id[i]["nome"]
    frases, disjuntos = pares_em_frases(cj, nome_curto)
    with st.expander(f"Ler a matriz em frases — {len(frases)} pares com normas em comum"):
        for f in frases:
            st.markdown(f"- {f}")
        if disjuntos:
            st.markdown(f"**Sem norma em comum no corpus atual ({len(disjuntos)} pares):** "
                        + " · ".join(disjuntos))

    st.markdown("#### Examinar um par de conjuntos")
    temas = list(cj)
    col_a, col_b = st.columns(2)
    a = col_a.selectbox("Conjunto A", temas, index=temas.index("direito_economico") if "direito_economico" in temas else 0,
                        format_func=lambda t: THEMES[t])
    b = col_b.selectbox("Conjunto B", temas, index=temas.index("soberania_tecnologica") if "soberania_tecnologica" in temas else 1,
                        format_func=lambda t: THEMES[t])

    A, B = cj[a], cj[b]
    nome = lambda i: por_id[i].get("sigla") or por_id[i]["nome"]

    def lista(ids):
        return " · ".join(sorted(nome(i) for i in ids)) if ids else "∅"

    st.markdown(f"**A ∩ B** ({len(A & B)}): {lista(A & B)}")
    st.markdown(f"**A \\ B** ({len(A - B)}): {lista(A - B)}")
    st.markdown(f"**B \\ A** ({len(B - A)}): {lista(B - A)}")

    if a != b:
        rel = relacoes_no_par(A, B, arestas)
        if rel:
            st.markdown(f"**Arestas entre A e B no grafo** ({len(rel)}):")
            for e in rel:
                st.markdown(f"- {nome(e['source'])} → {nome(e['target'])} · *{e['tipo']}*")
        elif A & B:
            st.info("Os conjuntos se intersectam, mas não há aresta curada entre eles: "
                    "candidato a exame pelo IPII Engine e pelo curador.")
        if not (A & B):
            st.warning("Interseção vazia no corpus atual. Pode ser lacuna normativa real ou "
                       "lacuna de curadoria — o corpus é um recorte, não o ordenamento inteiro.")

    st.markdown("#### Conjunto não é aresta")
    st.markdown(
        "Conjuntos **classificam**: dizem a que campo uma norma pertence. O grafo "
        "**relaciona**: diz de onde a norma retira validade, o que regulamenta e quem a "
        "interpreta. Pertencer ao mesmo conjunto não cria relação, e uma relação não "
        "exige pertencer ao mesmo conjunto — a Constituição fundamenta a LGPD sem que "
        "ambas tenham os mesmos vetores. Por isso a afirmação 'toda norma digital é "
        "constitucional' é melhor lida como relação de validade (existe uma cadeia de "
        "arestas até a CF/88) do que como inclusão de conjuntos."
    )

    st.markdown("#### Campos acrescentados em 2026")
    st.markdown(
        "- **Direito Econômico e Regulação** — conjunto do corpus; na arquitetura teórica, "
        "pertence à camada 06 (regulação de sistemas complexos).\n"
        "- **Soberania Tecnológica** — conjunto do corpus; na arquitetura, funciona como "
        "eixo transversal, como o processual e a propriedade intelectual: atravessa "
        "infraestrutura (REDATA), recursos minerais (PNMCE) e dados (LGPD, transferência internacional).\n"
        "- **Direito Internacional Público** — conjunto do corpus (tratados e sua "
        "incorporação: Convenção de Viena, Tratado de Assunção, acordos do Mercosul); na "
        "arquitetura, já figura na camada 01, ao lado do Direito Comunitário.\n"
        "- **Direito Internacional Privado** — conjunto do corpus (LINDB, arts. 7º a 17); na "
        "arquitetura, é eixo transversal: atravessa Civil, Empresarial, Trabalho e Consumidor "
        "sempre que a relação privada tem elemento estrangeiro. Um acordo comercial é tratado "
        "(DIP), não norma de DIPr, ainda que produza efeitos em relações privadas.\n"
        "- **Direito e Economia Política** — não é conjunto: é lente de leitura. "
        "Marcá-la em normas tornaria a pertença arbitrária; ela opera na página de "
        "Inteligência, sobre os conjuntos já existentes."
    )

# =============================================================
# Documento teórico (v3)
# =============================================================
with aba_teoria:
    # ---------------------------------------------------------
    # Complementos 2026 — conteúdo novo vem de data/teoria.json
    # ---------------------------------------------------------
    teoria = load_json("teoria.json")
    ROTULO_NATUREZA = {"fato": ("FATO", "#2ecc71"), "interpretacao": ("INTERPRETAÇÃO", "#d4a853"),
                       "metafora": ("METÁFORA", "#8a8478")}

    def selo(natureza):
        r, c = ROTULO_NATUREZA.get(natureza, (natureza.upper(), "#8a8478"))
        return (f"<span style='font-family:DM Mono,monospace;font-size:10px;letter-spacing:.08em;"
                f"color:{c};border:1px solid {c};border-radius:3px;padding:1px 6px'>{r}</span>")

    def exemplos(ids):
        if not ids:
            return ""
        return " · ".join((por_id[i].get("sigla") or por_id[i]["nome"]) if i in por_id else i for i in ids)

    ht = teoria["hierarquia_tratados"]
    with st.expander("Complementos 2026 — " + ht["titulo"], expanded=True):
        st.markdown(ht["introducao"])
        st.markdown("##### 1. Posição no direito interno")
        for r in ht["posicao_interna"]:
            ex = exemplos(r["exemplos_corpus"])
            st.markdown(
                f"{selo(r['natureza'])} **{r['regime']}** — {r['posicao']}<br>"
                f"<span style='color:#8a8478'>{r['abrange']}.</span> {r['fundamento']}"
                + (f"<br><span style='color:#8a8478'>No corpus:</span> {ex}" if ex else ""),
                unsafe_allow_html=True)
        pr = ht["procedimento"]
        st.markdown("##### 2. Procedimento de incorporação")
        st.markdown(selo(pr["natureza"]) + "<br>" + "<br>".join(
            f"{n}. {p}" for n, p in enumerate(pr["passos"], 1)) + f"<br><em>{pr['exemplo']}</em>",
            unsafe_allow_html=True)
        fi = ht["forca_internacional"]
        st.markdown("##### 3. Força no plano internacional")
        st.markdown(f"{selo(fi['natureza'])} {fi['texto']}", unsafe_allow_html=True)
        ni = ht["nao_incorporados"]
        st.markdown("##### Instrumentos não incorporados")
        st.markdown(f"{selo(ni['natureza'])} {ni['texto']}<br><span style='color:#8a8478'>No corpus:</span> "
                    f"{exemplos(ni['exemplos_corpus'])}", unsafe_allow_html=True)
        lk = ht["leitura_kelseniana"]
        st.markdown(f"{selo(lk['natureza'])} {lk['texto']}", unsafe_allow_html=True)
        for m in teoria.get("metaforas", []):
            st.markdown(f"{selo(m['natureza'])} **“{m['termo']}”** ({m['onde']}): {m['leitura']}",
                        unsafe_allow_html=True)
        st.caption("Fonte destes complementos: data/teoria.json. O documento abaixo é o texto "
                   "original da arquitetura teórica, preservado sem edição.")

    with open("docs/teoria-conjuntos-juridicos-v3.html", "r", encoding="utf-8") as f:
        html_teoria = f.read()

    # O documento legado não é editado: a ligação com o corpus é feita na
    # renderização. Cada id citado ganha a descrição do nó (se está no corpus)
    # ou é marcado como referência externa declarada em referencias_externas.json.
    _externos = ids_externos()

    def _marcar(m):
        i = m.group(1).strip()
        if i in por_id:
            dica = (por_id[i].get("sigla") or por_id[i]["nome"]) + " — nó do corpus"
            return f'<span class="int-norma-tag" title="{html.escape(dica)}">{i}</span>'
        if i in _externos:
            dica = _externos[i]["nome"] + " — referência externa, fora do corpus"
            return (f'<span class="int-norma-tag int-norma-externa" title="{html.escape(dica)}">'
                    f'{i} ↗</span>')
        return m.group(0)

    html_teoria = re.sub(r'<span class="int-norma-tag">([^<]+)</span>', _marcar, html_teoria)
    html_teoria = html_teoria.replace(
        "</style>",
        ".int-norma-externa{outline:1px dashed currentColor;outline-offset:-1px;opacity:.8}</style>", 1)
    st.caption("Na seção de interseções, ids com ↗ e borda tracejada são referências externas: "
               "identificadas, mas fora do corpus atual. Passe o mouse sobre qualquer id para ver a norma.")
    components.html(html_teoria, height=6200, scrolling=True)

render_footer()
