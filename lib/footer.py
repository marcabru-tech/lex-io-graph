import streamlit as st


def render_footer():
    st.markdown("---")
    st.markdown("""
<div style="font-family: monospace; font-size: 12px; color: #706a60; line-height: 2; padding: 8px 0;">

<div style="margin-bottom: 8px;">
<span style="color: #d4a853; font-size: 14px; font-weight: bold; letter-spacing: 0.08em;">
Lexiograph
</span>
<span style="color: #3dc8e6; margin: 0 6px;">|</span>
<span style="color: #c44b4b; font-size: 13px; letter-spacing: 0.06em;">Hubstry Deep Tech</span>
</div>

<div style="color: #8a8478; font-size: 11px; max-width: 800px; line-height: 1.8; margin-bottom: 10px;">
Comunicar sistemas digitais de forma clara, etica e estetica — unindo governanca <span style="color:#d4a853">(Lex)</span>, interacao <span style="color:#3dc8e6">(IO)</span> e estrutura semantica <span style="color:#c44b4b">(Graph)</span> sob a assinatura <strong style="color:#e8e4dc">Lex Quantum</strong>.<br>
A Lexiograph e mais do que uma marca — e uma linguagem. Uma gramatica visual que emerge da intersecao entre compliance digital, interacao sistemica e estruturacao do conhecimento.<br>
<strong style="color:#8a8478">Lexiograph = Lex + IO + Graph</strong> — arquitetura semiotica que traduz sistemas digitais em signos, fluxos e grafos.<br>
Parte do ecossistema <strong style="color:#e8e4dc">Hubstry Deep Tech</strong> — venture building bootstrapped, Rio de Janeiro.
</div>

<div style="display: flex; gap: 20px; flex-wrap: wrap;">
<a href="https://hubstry.dev/lex-io-graph/" target="_blank"
   style="color: #d4a853; text-decoration: none; font-size: 11px; letter-spacing: 0.05em;">
&#x2197; Site Lexiograph
</a>
<a href="https://hubstry.dev/lex-io-graph/#pricing" target="_blank"
   style="color: #2ecc71; text-decoration: none; font-size: 11px; letter-spacing: 0.05em;">
&#x2197; Pricing
</a>
<a href="https://github.com/marcabru-tech/lex-io-graph" target="_blank"
   style="color: #3dc8e6; text-decoration: none; font-size: 11px; letter-spacing: 0.05em;">
&#x2197; GitHub
</a>
<a href="https://facebook.com/goncalvesetalii" target="_blank"
   style="color: #9b59b6; text-decoration: none; font-size: 11px; letter-spacing: 0.05em;">
&#x2197; Goncalves et Alii
</a>
<a href="https://goncalvesetalii.github.io/" target="_blank"
   style="color: #9b59b6; text-decoration: none; font-size: 11px; letter-spacing: 0.05em;">
&#x2197; goncalvesetalii.github.io
</a>
<a href="https://www.hubstry.dev" target="_blank"
   style="color: #c44b4b; text-decoration: none; font-size: 11px; letter-spacing: 0.05em;">
&#x2197; hubstry.dev
</a>
<a href="mailto:globaldeeptechecosystem@hubstry.dev"
   style="color: #c44b4b; text-decoration: none; font-size: 11px; letter-spacing: 0.05em;">
&#x2197; contato
</a>
<span style="color: #454040; font-size: 11px;">Apache License 2.0 | 2026 Lexiograph</span>
</div>

</div>
""", unsafe_allow_html=True)