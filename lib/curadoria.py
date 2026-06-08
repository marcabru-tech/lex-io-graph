"""
lib/curadoria.py — Princípio de Curadoria Humana Inalienável
Único ponto de verdade. Importado onde necessário.
Não modifica nenhum arquivo existente.
"""

import streamlit as st

ZENODO_DOI = "https://doi.org/10.5281/zenodo.20597727"
SITE_CURADORIA = "https://hubstry.dev/lex-io-graph/#curadoria"
CALENDLY = "https://calendly.com/guilhermegmachado22/30min"

TEXTO_ABERTURA = """
O IPII Engine calcula scoring de relevância normativa com base no seu perfil — \
matemática determinística sobre corpus curado, sem alucinação, com base legal real \
em cada ação recomendada. Isso é o que você vê abaixo.

Mas há uma distinção que consideramos inegociável, e que precisa ser dita \
antes de você usar o quadro.
"""

DOMINIOS = [
    {
        "titulo": "Construção de confiança",
        "texto": (
            "A confiança entre uma organização e seus clientes, parceiros, reguladores "
            "e equipes é construída por pessoas em relação — pela palavra dada em momento "
            "crítico, pela responsabilidade assumida pessoalmente, pela presença quando o "
            "risco se materializa. Nenhum score de conformidade chega lá. O engine mapeia "
            "o terreno; a confiança é construída por quem caminha nele."
        ),
    },
    {
        "titulo": "Formação (Bildung)",
        "texto": (
            "O que a tradição alemã chama de Bildung — de Humboldt a Gadamer — é o "
            "processo pelo qual informação se transforma em julgamento. PMEs, startups, "
            "scaleups e órgãos públicos que operam sob pressão regulatória crescente "
            "precisam de pessoas que desenvolvam essa capacidade internamente, como "
            "competência instalada. O engine é instrumento de aceleração desse processo "
            "— não pode substituí-lo, porque a formação acontece em quem decide, não "
            "no software que informa a decisão."
        ),
    },
    {
        "titulo": "Cultura organizacional sob pressão",
        "texto": (
            "Seja ataque cibernético, crise reputacional em redes sociais, ou ruptura "
            "interna — a identidade institucional de uma organização não se sustenta por "
            "compliance documentado. Sustenta-se por pessoas que construíram essa identidade "
            "antes da crise e sabem o que defender quando ela chega. O Lexiograph pode "
            "contribuir para a robustez regulatória da organização; não pode construir "
            "sua espinha dorsal cultural."
        ),
    },
    {
        "titulo": "Decisão em alta ambiguidade",
        "texto": (
            "Quando a situação não tem precedente normativo suficiente — nova tecnologia, "
            "lacuna regulatória, antinomia ainda não resolvida pelo Judiciário — o "
            "julgamento pertence ao decisor humano. O engine sinaliza onde o corpus "
            "termina. A travessia além dessa fronteira é responsabilidade de quem decide."
        ),
    },
]

FECHAMENTO = (
    "Esses quatro domínios não são limitações provisórias do engine — são a definição "
    "do que é insubstituível no trabalho jurídico, de compliance e de governança. "
    "Reconhecê-los não é fraqueza do produto. É a condição para que o produto seja "
    "honesto sobre o que entrega."
)

GATEWAY = (
    "O mapa customizado — corpus do seu segmento, IPII Engine recalibrado, curador "
    "humano na decisão — é o produto entregável. Este app é o que o engine faz quando "
    "opera sobre corpus genérico. O produto é o que acontece quando ele opera sobre "
    "o seu contexto específico, com um especialista responsável pelo resultado."
)


def render_principio_curadoria():
    """
    Bloco de curadoria — Opção A:
    Título + abertura sempre visíveis.
    4 domínios + fechamento em expander.
    Gateway comercial sempre visível.
    """

    st.markdown(
        "<div style='"
        "border:1px solid rgba(212,168,83,0.25);"
        "border-radius:8px;"
        "padding:24px 28px;"
        "background:rgba(212,168,83,0.03);"
        "margin-bottom:24px;"
        "'>"
        "<div style='"
        "font-family:monospace;font-size:10px;color:#706a60;"
        "letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;"
        "'>PRINCÍPIO DE CURADORIA · IPII Engine v2</div>"
        "<div style='"
        "font-family:\"Cormorant Garamond\",Georgia,serif;"
        "font-size:20px;font-weight:300;color:#e8e4dc;margin-bottom:16px;"
        "'>O IPII Engine calcula. O curador decide.</div>"
        f"<p style='font-family:monospace;font-size:12px;color:#b8b2a6;line-height:1.8;margin:0;'>"
        f"{TEXTO_ABERTURA.strip()}"
        f"</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("Ver fundamento completo — os 4 domínios da curadoria humana"):

        for dominio in DOMINIOS:
            st.markdown(
                f"<div style='margin-bottom:20px;padding-left:16px;"
                f"border-left:2px solid rgba(212,168,83,0.3);'>"
                f"<div style='font-family:monospace;font-size:10px;color:#d4a853;"
                f"letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;'>"
                f"{dominio['titulo']}</div>"
                f"<p style='font-family:monospace;font-size:12px;color:#b8b2a6;"
                f"line-height:1.8;margin:0;'>{dominio['texto']}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            f"<p style='font-family:monospace;font-size:12px;color:#b8b2a6;"
            f"line-height:1.8;margin:16px 0;font-style:italic;'>{FECHAMENTO}</p>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<p style='font-family:monospace;font-size:10px;color:#706a60;"
            f"line-height:1.7;margin-top:16px;'>"
            f"Fundamento teórico: Gonçalves Machado, G. "
            f"<em>Teoria Geral do Direito: Natural, Pancrônico e Comparado.</em> "
            f"Zenodo, 2026. "
            f"<a href='{ZENODO_DOI}' target='_blank' "
            f"style='color:#3dc8e6;text-decoration:none;'>"
            f"doi.org/10.5281/zenodo.20597727</a></p>",
            unsafe_allow_html=True,
        )

    # Gateway comercial — sempre visível
    st.markdown(
        f"<div style='margin-top:16px;padding:16px 20px;"
        f"background:rgba(61,200,230,0.04);"
        f"border:1px solid rgba(61,200,230,0.15);border-radius:6px;'>"
        f"<p style='font-family:monospace;font-size:12px;color:#b8b2a6;"
        f"line-height:1.8;margin:0 0 12px 0;'>{GATEWAY}</p>"
        f"<div style='display:flex;gap:16px;flex-wrap:wrap;'>"
        f"<a href='{SITE_CURADORIA}' target='_blank' "
        f"style='font-family:monospace;font-size:11px;color:#d4a853;"
        f"text-decoration:none;'>↗ Princípio completo</a>"
        f"<a href='{CALENDLY}' target='_blank' "
        f"style='font-family:monospace;font-size:11px;color:#3dc8e6;"
        f"text-decoration:none;'>📅 Agendar 30 minutos</a>"
        f"</div></div>",
        unsafe_allow_html=True,
    )
