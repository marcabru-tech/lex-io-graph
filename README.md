# Lex-IO-Graph

**Sistema de inteligência jurídico-estratégica com gramática visual-cognitiva, fundamentação semiótica, inventário pancrônico e vetor prospectivo.**

*Lex* (lei, governança) + *IO* (input/output, interação sistêmica) + *Graph* (grafo, estrutura semântica)

---

## O que é

Atlas interativo do ordenamento jurídico digital brasileiro — não um PDF de compliance, mas um sistema vivo que conecta normas, jurisprudência, doutrina, inteligência estratégica e radar legislativo automático.

**9 páginas · 18 normas mapeadas · 30 conexões normativas · IPII Engine proprietário**

### Páginas

| # | Página | O que é |
|---|---|---|
| 1 | Grafo Normativo | Atlas interativo com hierarquia espacial, busca textual, toggle lista/grafo |
| 2 | Matriz Compliance | Cruzamento perfil de empresa × norma × risco |
| 3 | Comparação Normativa | Side-by-side de normas com análise de divergência |
| 4 | Radar Riscos | Mapa de calor de exposição regulatória |
| 5 | Repositório | Inventário doutrinário, latim jurídico, direito comparado glocal, multissemiose |
| 6 | Inteligência | Casos estratégicos, epistemologia do direito, direito natural |
| 7 | Hermenêutica | Correntes hermenêuticas, fontes do direito, 7 constituições brasileiras |
| 8 | Radar Legislativo | APIs do Senado, Câmara e LexML — atualização automática via GitHub Actions |
| 9 | IPII Engine | Interação Paramétrica Iterativa por Interoperabilidade — descoberta assistida de arestas |

---

## Acesso

**App:** [lex-io-graph-compliance-map.streamlit.app](https://lex-io-graph-compliance-map.streamlit.app)
**Site:** [hubstry.dev/lex-io-graph](https://hubstry.dev/lex-io-graph)
**Demo / parceria:** globaldeeptechecosystem@hubstry.dev

---

## Arquitetura

```
lex-io-graph/
├── app.py                          # Home — métricas e alertas normativos
├── pages/
│   ├── 1_📊_Grafo_Normativo.py    # Grafo interativo (PyVis)
│   ├── 2_📋_Matriz_Compliance.py  # Matriz empresa × norma
│   ├── 3_⚖️_Comparacao_Normativa.py
│   ├── 4_🎯_Radar_Riscos.py
│   ├── 5_📚_Repositorio.py        # Atlas doutrinário
│   ├── 6_🎯_Inteligencia.py       # Inteligência estratégica
│   ├── 7_⚖️_Hermeneutica.py       # Hermenêutica e fontes
│   ├── 8_📡_Radar_Legislativo.py  # Radar de PLs e normas
│   └── 9_🔬_IPII_Engine.py        # Engine proprietário
├── lib/
│   ├── constants.py               # Identidade, paleta semiótica, constantes
│   ├── footer.py                  # Rodapé Lexiograph | Hubstry
│   ├── graph_builder.py           # Construção do grafo NetworkX
│   ├── radar.py                   # APIs Senado, Câmara, LexML
│   ├── repositorio.py             # Inventário doutrinário
│   ├── multisemiose.py            # Citações literárias, obras de arte, glossário
│   ├── inteligencia.py            # Casos estratégicos, epistemologia
│   ├── hermeneutica.py            # Correntes hermenêuticas, fontes, constituições
│   └── ipii/
│       ├── tokenizer.py           # GuruMatrix 5D aplicada ao corpus normativo
│       ├── matcher.py             # Matching contextual par-a-par
│       └── validator.py           # Validação e curadoria assistida
├── data/
│   ├── normas.json                # Corpus normativo curado (18 nós)
│   ├── arestas.json               # Conexões tipadas (30 arestas)
│   ├── jurisprudencia.json        # Jurisprudência vinculada
│   └── radar_legislativo.json     # Resultado do radar automático
├── docs/
│   └── adr/                       # Architecture Decision Records
├── ipii_engine.py                 # Runner IPII Engine
├── updater.py                     # Runner Radar Legislativo
├── .github/workflows/
│   └── update-radar.yml           # GitHub Action — atualização semanal
├── CHANGELOG.md
└── ARCHITECTURE.md
```

---

## Licença e propriedade intelectual

### Camada pública

O código das páginas, módulos de lib (exceto `lib/ipii/`) e dados normativos (`data/`) estão disponíveis sob **Apache License 2.0**.

### Camada proprietária — IPII Engine

O **IPII Engine** (Interação Paramétrica Iterativa por Interoperabilidade — `lib/ipii/`, `ipii_engine.py`) é propriedade intelectual exclusiva da **Hubstry Deep Tech** — Guilherme Gonçalves Machado © 2026.

**É expressamente proibido** o uso comercial, reprodução, adaptação ou distribuição desta implementação sem autorização escrita da Hubstry Deep Tech.

Para licenciamento comercial: globaldeeptechecosystem@hubstry.dev

### Princípio de curadoria

> O engine alerta — o curador decide. Nenhuma aresta é adicionada automaticamente ao grafo.

---

## Ecossistema Hubstry

O Lex-IO-Graph é parte do ecossistema **Hubstry Deep Tech** — venture building bootstrapped, Rio de Janeiro.

| Venture | O que é |
|---|---|
| **Lexiograph** | Marca do sistema de inteligência jurídico-estratégica |
| **Overall 720°** | Consultoria estratégica — [overall720.xyz](https://www.overall720.xyz/) |
| **Gonçalves et Alii** | Legaltech — radar regulatório e compliance |
| **Nautam / HPG** | Protocolo IoT com criptografia pós-quântica |
| **GuruDev®** | Linguagem de programação ontossemiótica |

**hubstry.dev** · ORCID: 0009-0008-1083-0784

---

## In memoriam

*Sandoval Gonçalves dos Santos — avô do curador deste atlas.*
*Mestre em Direito, Universidade Gama Filho, 1982.*
*Dissertação: O Mito da Intimidação da Pena.*
*Orientador: Prof. Dr. Juarez Estevam Xavier Tavares (UERJ).*

*A dissertação de 1982 sobre o mito da intimidação da pena e o debate atual sobre vieses algorítmicos compartilham o mesmo núcleo: a crítica ao sistema que pune sem explicar, que julga sem fundamentar. Sandoval recusou esse mito no direito penal; o Lex-IO-Graph o recusa no direito digital. A linhagem é real.*
