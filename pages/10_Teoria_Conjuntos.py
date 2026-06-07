import streamlit as st
import streamlit.components.v1 as components
from lib.footer import render_footer

st.set_page_config(
    page_title="Teoria dos Conjuntos Jurídicos",
    page_icon="🧩",
    layout="wide"
)

st.markdown("<h1 style='text-align:center; color:#d4a853; font-family:Cormorant Garamond,serif;'>🧩 Teoria dos Conjuntos Jurídicos</h1>", unsafe_allow_html=True)
st.caption("Arquitetura Sistêmica do Ordenamento Jurídico Brasileiro — Lexiograph")

html_path = "docs/teoria-conjuntos-juridicos-v3.html"

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=6200, scrolling=True)

render_footer()
