import streamlit as st
from lib.constants import APP_NAME, APP_SUBTITLE, APP_VERSION
from lib.hermeneutica import (
    CORRENTES_HERMENEUTICAS, FONTES_DIREITO, ARCO_CC, BRASIL_IMPERIO
)
from lib.footer import render_footer

st.set_page_config(
    page_title=f"{APP_NAME} — Hermenêutica e Fontes do Direito",
    layout="wide",
    page_icon="⚖️"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { min-width: 280px; }
    .block-container { padding-top: 2rem; }
    .app-subtitle {
        font-family: monospace; font-size: 11px; color: #706a60;
        letter-spacing: 0.06em; line-height: 1.6;
        margin-top: -8px; margin-bottom: 16px; max-width: 800px;
    }
    .herm-card {
        background: rgba(212,168,83,0.05);
        border: 1px solid rgba(212,168,83,0.2);
        border-radius: 8px; padding: 16px; margin-bottom: 14px;
    }
    .herm-nome   { color: #d4a853; font-size:15px; font-weight:bold; font-family:monospace; }
    .herm-autor  { color: #9b59b6; font-size:12px; font-family:monospace; margin: 4px 0; }
    .herm-obra   { color: #3dc8e6; font-size:11px; font-style:italic; margin: 4px 0; }
    .herm-princ  { color: #e8e4dc; font-size:13px; line-height:1.7; margin: 8px 0; }
    .herm-critica{ color: #706a60; font-size:11px; line-height:1.6; margin-top: 6px; }
    .herm-brasil { color: #3dc8e6; font-size:11px; line-height:1.6; margin-top: 6px; }
    .herm-tensao { color: #c44b4b; font-size:10px; font-family:monospace; margin-top: 6px; }
    .fonte-card {
        background: rgba(61,200,230,0.04);
        border-left: 3px solid;
        padding: 12px 16px; margin-bottom: 10px; border-radius: 0 6px 6px 0;
    }
    .fonte-nome  { font-size:14px; font-weight:bold; font-family:monospace; }
    .fonte-desc  { color: #b8b2a6; font-size:12px; line-height:1.7; margin: 6px 0; }
    .fonte-ex    { color: #3dc8e6; font-size:11px; }
    .fonte-latim { color: #d4a853; font-size:10px; font-style:italic; margin-top:4px; }
    .cc-card {
        background: rgba(30,173,156,0.05);
        border: 1px solid rgba(30,173,156,0.2);
        border-radius: 8px; padding: 14px; margin-bottom: 12px;
    }
    .cc-ano    { color: #1abc9c; font-size:18px; font-weight:bold; font-family:monospace; }
    .cc-nome   { color: #e8e4dc; font-size:14px; font-weight:bold; margin-left: 10px; }
    .cc-ctx    { color: #706a60; font-size:11px; font-style:italic; margin: 4px 0; }
    .cc-char   { color: #b8b2a6; font-size:12px; line-height:1.7; margin: 8px 0; }
    .cc-inf    { color: #9b59b6; font-size:11px; }
    .imp-card {
        background: rgba(212,168,83,0.04);
        border: 1px solid rgba(212,168,83,0.15);
        border-radius: 8px; padding: 14px; margin-bottom: 12px;
    }
    .imp-ano     { color: #d4a853; font-size:16px; font-weight:bold; font-family:monospace; }
    .imp-nome    { color: #e8e4dc; font-size:13px; font-weight:bold; margin-left:8px; }
    .imp-dest    { color: #3dc8e6; font-size:11px; font-style:italic; margin: 4px 0; }
    .imp-desc    { color: #b8b2a6; font-size:12px; line-height:1.7; margin: 8px 0; }
    .section-divider {
        border: none; border-top: 1px solid rgba(212,168,83,0.2);
        margin: 32px 0 24px 0;
    }
    .lexiograph-value {
        background: rgba(212,168,83,0.08);
        border: 1px solid rgba(212,168,83,0.3);
        border-radius: 8px; padding: 20px; margin: 20px 0;
        font-family: monospace; font-size: 12px; color: #b8b2a6; line-height: 1.9;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚖️ Hermenêutica e Fontes do Direito")
st.markdown(
    f'<div class="app-subtitle">{APP_NAME} · {APP_SUBTITLE} · v{APP_VERSION}</div>',
    unsafe_allow_html=True
)
st.markdown(
    "A camada hermenêutica como pano de fundo permanente do ordenamento — "
    "é ela que explica por que as tensões do grafo existem. "
    "Sem hermenêutica, o mapa normativo é estático; com ela, é vivo."
)

secao = st.radio(
    "Seção",
    [
        "🔍 Correntes Hermenêuticas",
        "📐 Fontes do Direito",
        "🇧🇷 Constituições Brasileiras",
        "📜 Arco Histórico do Código Civil",
        "👑 Brasil Império",
        "✨ O Valor Epistemológico do Lex-IO-Graph"
    ],
    horizontal=False,
    label_visibility="collapsed"
)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# =============================================================
# SEÇÃO 1 — Correntes hermenêuticas
# =============================================================
if secao == "🔍 Correntes Hermenêuticas":
    st.markdown("## Correntes Hermenêuticas")
    st.markdown(
        "A divergência interpretativa não é erro do sistema — é o sistema funcionando. "
        "As correntes hermenêuticas são vozes simultâneas que coexistem "
        "na jurisprudência brasileira — polifonia bakhtiniana (Bakhtin, 1895–1975) "
        "em ação permanente. Cada tensão do grafo tem uma corrente hermenêutica dominante."
    )

    for c in CORRENTES_HERMENEUTICAS:
        st.markdown(f"""
<div class="herm-card">
  <div class="herm-nome">{c['nome']}</div>
  <div class="herm-autor">{c['autor_principal']} ({c['datas']})</div>
  <div class="herm-obra">📖 {c['obra']}</div>
  <div class="herm-princ">{c['principio']}</div>
</div>""", unsafe_allow_html=True)

        with st.expander(f"Métodos, crítica e aplicação no Brasil — {c['autor_principal']}"):
            st.markdown("**Métodos:**")
            for m in c['metodos']:
                st.markdown(f"- {m}")
            st.markdown(
                f'<div class="herm-critica">⚡ Crítica: {c["critica"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="herm-brasil">🇧🇷 No Brasil: {c["no_brasil"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="herm-tensao">⚖️ Tensão normativa: {c["tensao_norma"]}</div>',
                unsafe_allow_html=True
            )

# =============================================================
# SEÇÃO 2 — Fontes do direito
# =============================================================
elif secao == "📐 Fontes do Direito":
    st.markdown("## Fontes do Direito Brasileiro")
    st.markdown(FONTES_DIREITO['introducao'])
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    for fonte in FONTES_DIREITO['fontes']:
        cor = fonte['cor']
        st.markdown(f"""
<div class="fonte-card" style="border-left-color:{cor};">
  <div class="fonte-nome" style="color:{cor};">{fonte['nome']}</div>
  <div class="fonte-desc">{fonte['descricao']}</div>
  <div class="fonte-ex">📱 Digital: {fonte['exemplo_digital']}</div>
  <div class="fonte-latim">*{fonte['latim']}*</div>
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 3 — Arco histórico CC
# =============================================================
elif secao == "🇧🇷 Constituições Brasileiras":
    st.markdown("## Arco Histórico das Constituições Brasileiras")
    st.markdown(
        "O Brasil teve sete constituições em 164 anos — cada uma é um projeto político "
        "que reflete a correlação de forças do seu tempo. "
        "Pancronia: todas dialogam com a CF/88 atual — "
        "seja como superação, seja como substrato histórico que persiste."
    )

    constituicoes = [
        {
            "ano": 1824,
            "nome": "Constituição do Império",
            "contexto": "Outorgada por Pedro I após dissolução da Assembleia Constituinte",
            "vigencia": "65 anos — a mais longeva da história brasileira",
            "destaque": "Poder Moderador — Benjamin Constant (1767–1830)",
            "descricao": (
                "Quatro poderes: Legislativo, Executivo, Judiciário e Moderador — "
                "influência de Benjamin Constant. O Poder Moderador era privativo do Imperador: "
                "'chave de toda a organização política'. "
                "Contraponto a Montesquieu (três poderes): a concentração que ele quis evitar "
                "foi constitucionalizada. Garantia a escravidão implicitamente — "
                "o sujeito de direitos era o cidadão livre, não o ser humano. "
                "Pancronia: o debate sobre o Poder Moderador ressurge toda vez que "
                "o STF age como árbitro entre os demais poderes — Tema 987 incluso."
            ),
            "conexao_digital": "Precedente histórico para o debate atual sobre concentração de poder no STF"
        },
        {
            "ano": 1891,
            "nome": "Constituição da República",
            "contexto": "Primeira República — proclamação por Deodoro da Fonseca (1889)",
            "vigencia": "39 anos",
            "destaque": "Federalismo, separação Igreja/Estado, voto descoberto (sem sigilo)",
            "descricao": (
                "Influência direta da Constituição americana de 1787 — "
                "federalismo presidencialista, separação dos poderes sem Moderador. "
                "Separação formal entre Igreja e Estado — laicidade como projeto republicano. "
                "Voto descoberto e censitário: só votavam homens alfabetizados, "
                "excluindo a maioria da população. "
                "A 'política do café com leite' (SP e MG) como oligarquia constitucional. "
                "Rui Barbosa como grande constitucionalista da era — "
                "habeas corpus como remédio hermenêutico expansivo ('teoria brasileira do HC')."
            ),
            "conexao_digital": "Laicidade constitucional: fundamento para a neutralidade estatal no debate sobre regulação religiosa da IA (Magnifica Humanitas vs. PL 2.338/2023)"
        },
        {
            "ano": 1934,
            "nome": "Constituição da Era Vargas",
            "contexto": "Revolução de 1930 — Getúlio Vargas ao poder",
            "vigencia": "3 anos",
            "destaque": "Primeira constituição brasileira com direitos sociais",
            "descricao": (
                "Influência da Constituição de Weimar (Alemanha, 1919) — "
                "primeira a incluir direitos econômicos e sociais numa constituição. "
                "Voto secreto, voto feminino, Justiça Eleitoral, Justiça do Trabalho. "
                "A CLT (1943) é o desdobramento infraconstitucional dessa virada social. "
                "Direitos trabalhistas como direitos fundamentais — "
                "Ihering (1818–1892) aplicado: o direito serve a fins sociais concretos. "
                "Pancronia: a NR-1 com riscos psicossociais de IA (2026) é herdeira "
                "direta dos direitos trabalhistas de 1934."
            ),
            "conexao_digital": "Direitos trabalhistas → CLT (1943) → NR-1 (2026): arco de 92 anos de proteção do trabalhador, agora incluindo riscos de IA"
        },
        {
            "ano": 1937,
            "nome": "Constituição do Estado Novo ('A Polaca')",
            "contexto": "Golpe de Vargas — ditadura do Estado Novo (1937–1945)",
            "vigencia": "9 anos (parcialmente suspensa na prática)",
            "destaque": "Constituição autoritária — modelo polonês (daí 'Polaca')",
            "descricao": (
                "Inspirada na Constituição polonesa de 1935 — regime autoritário. "
                "Concentração de poderes no Executivo, intervenção federal, "
                "suspensão do Legislativo. Nunca foi plenamente aplicada — "
                "Vargas governou por decretos-lei. "
                "Primeiro caso brasileiro de constituição outorgada e não respeitada "
                "pelo próprio outorgante. "
                "Fuller (1902–1978): a Polaca viola todos os 8 critérios de moralidade "
                "interna do direito — não era lei, era instrumento de dominação. "
                "Pancronia: o debate sobre 'constituição que não se aplica' ressurge "
                "no contexto dos decretos executivos que tentam legislar sem o Congresso."
            ),
            "conexao_digital": "Precedente para o debate sobre legitimidade dos Decretos 12.975 e 12.976/2026: ato do executivo sem base legislativa — quando o decreto vira substituto da lei"
        },
        {
            "ano": 1946,
            "nome": "Constituição da Redemocratização",
            "contexto": "Fim da II Guerra Mundial — queda do Estado Novo",
            "vigencia": "21 anos",
            "destaque": "Restauração democrática, direitos fundamentais, autonomia municipal",
            "descricao": (
                "Promulgada pela Assembleia Constituinte democraticamente eleita. "
                "Restaurou direitos civis e políticos suspensos desde 1937. "
                "Influência da Declaração Universal dos Direitos Humanos (ONU, 1948). "
                "O período 1946–1964 é o único de democracia plena antes da CF/88. "
                "Goulart deposto pelo golpe de 1964 — a constituição de 1946 "
                "sucumbiu ao mesmo processo que a de 1934: golpe antes do amadurecimento democrático."
            ),
            "conexao_digital": "Democracia como condição da regulação digital legítima — a CF/88 herda da tradição de 1946 o compromisso com direitos fundamentais como limite do Estado"
        },
        {
            "ano": 1967,
            "nome": "Constituição da Ditadura Militar",
            "contexto": "Golpe de 1964 — regime militar (1964–1985)",
            "vigencia": "21 anos (com EC 1/1969 considerada nova constituição por parte da doutrina)",
            "destaque": "Segurança nacional, centralização, AI-5 (1968) como ruptura dentro da ruptura",
            "descricao": (
                "Constituição outorgada pelo regime militar — legitimidade questionada. "
                "A EC 1/1969 (editada pela junta militar após incapacidade de Costa e Silva) "
                "é considerada por doutrinadores como Manoel Gonçalves Ferreira Filho "
                "uma nova constituição — não mera emenda. "
                "O AI-5 (Ato Institucional nº 5, 1968) suspendeu direitos constitucionais "
                "e é o marco mais autoritário da história republicana brasileira. "
                "Pancronia: o AI-5 é a referência implícita em todo debate sobre "
                "estado de exceção no Brasil — incluindo a tentativa de golpe de 2022 "
                "(ex-presidente indiciado no PL 2.253/2024)."
            ),
            "conexao_digital": "O AI-5 como antecedente histórico do debate sobre limites do poder executivo — vetor de inteligência estratégica para o contexto pré-eleitoral de 2026"
        },
        {
            "ano": 1988,
            "nome": "Constituição Cidadã",
            "contexto": "Redemocratização — fim da ditadura militar (1985), Diretas Já (1984)",
            "vigencia": "Vigente — 38 anos",
            "destaque": "Ulysses Guimarães: 'Esta é a Constituição Cidadã'",
            "descricao": (
                "Promulgada em 5 de outubro de 1988 após 21 anos de ditadura. "
                "A mais extensa constituição brasileira — 250 artigos originais. "
                "Incorporou direitos de três gerações: civis/políticos (1ª), "
                "sociais/econômicos (2ª) e difusos/coletivos (3ª). "
                "EC 115/2022: direito fundamental à proteção de dados pessoais "
                "(art. 5º, LXXIX) — a constituição que se atualiza por emendas "
                "sem precisar ser substituída. "
                "Influências: Constituição portuguesa de 1976, Lei Fundamental alemã (1949), "
                "Constituição espanhola de 1978. "
                "Kelsen aplicado: a CF/88 como Grundnorm — norma fundamental "
                "que confere validade a todo o ordenamento digital brasileiro."
            ),
            "conexao_digital": "EC 115/2022 (proteção de dados como direito fundamental) + art. 5º como fundamento do Marco Civil, LGPD, ECA Digital e PL 2.338/2023"
        }
    ]

    for c in constituicoes:
        st.markdown(f"""
<div class="cc-card">
  <span class="cc-ano">{c['ano']}</span>
  <span class="cc-nome">{c['nome']}</span>
  <div class="cc-ctx">{c['contexto']} · Vigência: {c['vigencia']}</div>
  <div style="color:#d4a853;font-size:11px;font-style:italic;margin:4px 0;">
    🔑 {c['destaque']}
  </div>
  <div class="cc-char">{c['descricao']}</div>
  <div class="cc-inf">💻 Conexão digital: {c['conexao_digital']}</div>
</div>""", unsafe_allow_html=True)

elif secao == "📜 Arco Histórico do Código Civil":
    st.markdown("## Arco Histórico do Código Civil Brasileiro")
    st.markdown(ARCO_CC['introducao'])
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    for cc in ARCO_CC['codigos']:
        st.markdown(f"""
<div class="cc-card">
  <span class="cc-ano">{cc['ano']}</span>
  <span class="cc-nome">{cc['nome']}</span>
  <div class="cc-ctx">{cc['contexto']} · Vigência: {cc['vigencia']}</div>
  <div class="cc-char">{cc['caracteristica']}</div>
  <div class="cc-inf">📚 Influências: {cc['influencia']}</div>
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 4 — Brasil Império
# =============================================================
elif secao == "👑 Brasil Império":
    st.markdown("## Brasil Império como Camada do Ordenamento")
    st.markdown(BRASIL_IMPERIO['introducao'])
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    for marco in BRASIL_IMPERIO['marcos']:
        st.markdown(f"""
<div class="imp-card">
  <span class="imp-ano">{marco['ano']}</span>
  <span class="imp-nome">{marco['nome']}</span>
  <div class="imp-dest">🔑 {marco['destaque']}</div>
  <div class="imp-desc">{marco['descricao']}</div>
</div>""", unsafe_allow_html=True)

# =============================================================
# SEÇÃO 5 — Valor epistemológico do Lex-IO-Graph
# =============================================================
elif secao == "✨ O Valor Epistemológico do Lex-IO-Graph":
    st.markdown("## O Valor Epistemológico do Lex-IO-Graph")

    st.markdown("""
<div class="lexiograph-value">
<strong style="color:#d4a853;font-size:14px;">
O Lex-IO-Graph é o único atlas jurídico brasileiro que articula explicitamente
sete camadas simultâneas de inteligência:
</strong><br><br>

<strong style="color:#3dc8e6;">1. Norma positiva</strong> — o fato jurídico bruto: texto, hierarquia, status<br>
<strong style="color:#9b59b6;">2. Hermenêutica</strong> — a corrente interpretativa que molda o sentido da norma<br>
<strong style="color:#d4a853;">3. Inventário pancrônico</strong> — o arco histórico completo acessível simultaneamente<br>
<strong style="color:#2ecc71;">4. Direito comparado glocal</strong> (global + local, Robertson, 1990s) — a norma brasileira no campo mundial<br>
<strong style="color:#e67e22;">5. Multissemiose</strong> — literatura, arte, latim como camadas de fundamentação<br>
<strong style="color:#c44b4b;">6. Inteligência estratégica</strong> — o jogo de forças por trás da norma<br>
<strong style="color:#1abc9c;">7. Epistemologia do direito</strong> — de onde vem o conhecimento jurídico, como se forma, como se valida<br><br>

<strong style="color:#e8e4dc;">A interseção que nenhuma equipe de TI ou escritório de advocacia replicam sozinhos:</strong><br>
Schleiermacher → Dilthey → Gadamer → Habermas → Dworkin como arco epistemológico.<br>
Direito natural → positivo → tridimensional (Reale) como arco ontológico.<br>
Glosadores de Bolonha → comentadores → pandectistas → codificadores como arco metodológico.<br>
Bakhtin como método editorial — o ordenamento como sistema polifônico.<br><br>

<strong style="color:#d4a853;">O grafo não descreve o direito — compreende-o</strong>
(Verstehen, Dilthey, 1833–1911).<br>
<em style="color:#454040;">Lex-IO-Graph · Lexiograph | Hubstry Deep Tech · Rio de Janeiro · 2026</em>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### Fosso competitivo")
    st.markdown(
        "O que uma equipe de TI + advogados levaria para replicar este sistema:"
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Tempo mínimo estimado:**
- Mapear o corpus doutrinário: 3–6 meses
- Construir o arco histórico pancrônico: 2–4 meses
- Hermenêutica + epistemologia: 2–3 meses
- Multissemiose (literatura + arte): 1–2 meses
- Inteligência estratégica atualizada: contínuo
- **Total: 8–15 meses de equipe multidisciplinar**
""")
    with col2:
        st.markdown("""
**O que não se contrata:**
- 30 anos de repertório jurídico-filosófico
- Síntese tripartite: científico + artístico + empreendedor
- Capacidade de articular Bakhtin, Fuller e o Decreto 12.975/2026
  na mesma frase com precisão técnica
- O olhar pancrônico que conecta os glosadores de Bolonha
  ao ECA Digital de 2025
- **Esse perfil se forma — não se compra**
""")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:monospace;font-size:11px;color:#706a60;
  line-height:2;padding:16px 0;max-width:700px;">
<span style="color:#d4a853;font-size:13px;letter-spacing:0.06em;">
In memoriam
</span><br>
<strong style="color:#e8e4dc;">Sandoval Gonçalves dos Santos</strong> — avô do curador deste atlas<br>
Mestre em Direito — Universidade Gama Filho, 1982<br>
Dissertação: <em>O Mito da Intimidação da Pena</em><br>
Orientador: Prof. Dr. Juarez Estevam Xavier Tavares (UERJ)<br><br>
<span style="color:#8a8478;font-size:10px;">
Este atlas jurídico-estratégico continua, pela via empreendedora e tecnológica,
a tradição de rigor doutrinário de uma linhagem familiar comprometida com o direito
como instrumento de proteção da dignidade humana — não de intimidação.
A dissertação de 1982 sobre o mito da intimidação da pena dialoga, quarenta e quatro anos depois,
com o debate sobre vieses algorítmicos e IA no direito: a máquina que julga sem explicar
reproduz o mesmo mito que Sandoval recusou em sua pesquisa.
<br><br>
<em>Gonçalves et Alii · Hubstry Deep Tech · Rio de Janeiro · 2026</em>
</span>
</div>
""", unsafe_allow_html=True)

render_footer()
