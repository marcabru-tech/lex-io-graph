import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Teoria dos Conjuntos Jurídicos",
    page_icon="🧩",
    layout="wide"
)

st.markdown("<h1 style='text-align:center; color:#0d6efd;'>🧩 Teoria dos Conjuntos Jurídicos</h1>", unsafe_allow_html=True)
st.caption("Arquitetura Sistêmica do Ordenamento Jurídico Brasileiro — Modelagem pela Teoria dos Conjuntos")

html_path = "docs/teoria-conjuntos-juridicos-v3.html"

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=10000)
