import streamlit as st
from lib.footer import render_footer

st.set_page_config(
    page_title="Teoria dos Conjuntos Juridicos - Lex Quantum",
    layout="wide",
    page_icon="set;"
)

st.markdown("# set; Teoria dos Conjuntos Juridicos")
st.markdown("Campos do direito como conjuntos: enunciados formais e representacao visual simultaneos.")

html_path = "docs/teoria-conjuntos-juridicos.html"
try:
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=8000, scrolling=True)
except FileNotFoundError:
    st.error(f"Arquivo nao encontrado: {html_path}")
    st.info("Certifique-se de que o arquivo docs/teoria-conjuntos-juridicos.html existe no repositorio.")

render_footer()
