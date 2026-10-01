import streamlit as st
import streamlit.components.v1 as components

from lib.constants import THEMES
from lib.conjuntos import carregar, conjuntos, lacunas, relacoes_no_par, figura_matriz
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

    st.markdown("#### Matriz de interseções |A ∩ B|")
    st.caption("A diagonal é a cardinalidade de cada conjunto. Passe o mouse para ver o par.")
    st.plotly_chart(figura_matriz(cj), use_container_width=True, config={"displayModeBar": False})

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
    with open("docs/teoria-conjuntos-juridicos-v3.html", "r", encoding="utf-8") as f:
        components.html(f.read(), height=6200, scrolling=True)

render_footer()
