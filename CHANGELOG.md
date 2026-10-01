# Changelog — Lex-IO-Graph

## [v0.11.1] — 2026-10-01

### Radar: cadência no GitHub Actions, 4 temas novos e PDL

- GitHub Actions passa a ser o coletor principal: segunda 09h BRT; limite de 20 min.
- Temas novos: infraestrutura digital, mercados digitais, minerais críticos,
  soberania digital. Busca passa a incluir PDL (Projeto de Decreto Legislativo).
- Texto de cadência centralizado em `RADAR_CADENCIA` (lib/constants.py).
- Título "Fundamentação teórica" corrigido para "30 anos do Estado Regulador
  Brasileiro" na home e na página de Inteligência.

## [v0.11.0] — 2026-10-01

### REDATA, Direito Econômico e radar com reserva no GitHub Actions

- Corpus: novo nó `lei_15504_2026` (REDATA, sancionada em 15/09/2026), com
  arestas `cf88 → lei_15504_2026` (hierarquia, CF arts. 170, VI; 174; 219) e
  `lei_15504_2026 ↔ pl_ia` (complementaridade). 20 normas, 35 arestas.
- Novo vetor temático `direito_economico` (Direito Econômico e Regulação):
  `cf88`, `anpd` (agência reguladora, Lei 13.848/2019) e `lei_15504_2026`.
- Inteligência: caso estratégico "REDATA e Gás Natural — Quem Define
  'Baixa Emissão'", com a lente Direito Econômico / AED / Direito e
  Economia Política.
- Radar: blindagem passa a ser por fonte (Senado, Câmara, LexML), não por
  tema. Coleta sem resposta da Câmara não apaga mais a lista anterior.
- GitHub Actions volta como reserva: terça 09h BRT, e só coleta se o
  snapshot do notebook (segunda 21h) tiver mais de 36 horas.
- Constante `ODIN_URL`: link para o dossiê ODIN no rodapé, no Repositório
  e na página de Inteligência, apontando para
  hubstry-arquitetura-brasileira-ia.onrender.com.
- Inteligência: nova seção "Direito Econômico e Economia Política" — três
  lentes, genealogia em três momentos (Realismo Jurídico, CLS, LPE), contraponto
  da AED contratualista e referências ABNT (Blalock, 2022; Harris e Varellas,
  2020; Easterbrook e Fischel, 1991).

## [v0.9.0] — 2026-06-05

### Sprint 9 — Enriquecimento doutrinário do corpus

- Enriquecidos 9 nós com `autores`, `latim` e `direito_comparado`:
  `decreto_12975_2026`, `decreto_12976_2026`, `pl_misoginia`, `lei_15409_2026`,
  `magnifica_humanitas`, `stf_adimc`, `stj_resp`, `stj_resp_plat`, `anpd`
- IPII Engine: novas descobertas subiram de 10 para 21 após enriquecimento
- Cobertura do engine: 30% → 37%

## [v0.8.0] — 2026-06-05

### Sprint 8 — IPII Engine + Radar Legislativo

- IPII Engine — Interação Paramétrica Iterativa por Interoperabilidade
  (`lib/ipii/tokenizer.py`, `matcher.py`, `validator.py`, `ipii_engine.py`)
- Página 9: `9_🔬_IPII_Engine.py` com disclaimer de PI Hubstry Deep Tech
- Radar Legislativo: APIs Senado, Câmara, LexML com parse Atom correto
- Página 8: `8_📡_Radar_Legislativo.py`
- GitHub Action: `update-radar.yml` — PR semanal às 7h BRT
- Princípio de curadoria: o engine alerta, o curador decide

## [v0.7.0] — 2026-06-05

### Sprint 6 — Hermenêutica e fontes do direito

- Página 7: `7_⚖️_Hermeneutica.py`
- 6 correntes hermenêuticas (Savigny, Ihering, Gadamer, Dworkin, Habermas, Carlos Maximiliano)
- Fontes do direito com sistema cromático
- Arco histórico do Código Civil: 1603 (Ordenações Filipinas) → PL 4/2025
- 7 constituições brasileiras: 1824–1988 com conexões pancrônicas
- Brasil Império como camada do ordenamento
- In memoriam: Sandoval Gonçalves dos Santos (mestre em direito, 1982)
- Valor epistemológico do Lex-IO-Graph: 7 camadas simultâneas
- Seção "Fosso competitivo" — o que nenhuma equipe convencional replicaria

## [v0.6.0] — 2026-06-04

### Sprint 5 — Inteligência estratégica e epistemologia

- Página 6: `6_🎯_Inteligencia.py`
- 4 casos estratégicos: art. 19 guerra institucional tripartite, LGPD/ANPD,
  ECA Digital, Magnifica Humanitas
- Arco epistemológico: Schleiermacher → Dilthey → Gadamer → Habermas → Dworkin
- Arco ontológico: direito natural → positivo → tridimensional (Reale)
- Arco metodológico: glosadores Bolonha → comentadores → pandectistas → codificadores
- Direito natural contemporâneo: Fuller, Finnis, Reale
- O Alienista de Machado de Assis como metáfora da antinomia institucional
- Disclaimer Overall 720° e Gonçalves et Alii com links

## [v0.5.0] — 2026-06-04

### Sprint 4 — Multissemiose

- Página 5: `5_📚_Repositorio.py` (6 seções)
- `lib/multisemiose.py`: 8 citações literárias (Kafka ×2, Dostoiévski, Shakespeare,
  Machado ×2, Goethe, Jorge Amado, O Alienista)
- 4 obras de arte domínio público (Rafael, David, Debret, Cranach)
- Glossário jurídico: 10 verbetes com etimologia latina
- Magnifica Humanitas como seção do Repositório
- Rodapé editorial: Bakhtin como método editorial

## [v0.4.0] — 2026-06-03

### Sprint 3 — Repositório doutrinário

- `lib/repositorio.py`: 11 autores, 9 brocardos latinos, 4 tradições jurídicas
- Tradição judaica e islâmica no direito comparado glocal
- Magnifica Humanitas (Leão XIV, 25/05/2026)
- Enriquecimento de nós do corpus com `autores` e `latim`

## [v0.3.0] — 2026-06-02

### Sprint 2 — Grafo normativo

- Hierarquia espacial: CF/88 no topo, jurisprudência na base
- Semântica de cores e formas por tipo de norma
- Identidade visual Lex-IO-Graph (paleta tripartite)
- DEFAULT_THEMES: dados_pessoais, internet
- Sidebar doutrinária com legenda e filtros
- Busca textual com highlight de nós
- Toggle Lista/Grafo
- `lib/constants.py` com APP_NAME, APP_SUBTITLE, APP_VERSION
- `lib/footer.py` com rodapé Lexiograph | Hubstry

## [v0.2.0] — 2026-06-01

### Expansão do corpus

- 18 nós (de 11): decretos 12.975 e 12.976/2026, Lei 15.409/2026,
  STF Tema 987, PL misoginia, Magnifica Humanitas, NR-1 2026
- 30 arestas tipadas (de 15)
- Correções: NR-1 ano 2026, STF Tema 987 ementa com 24+ PDLs

## [v0.1.0] — 2026-05-30

### MVP — Lexiograph Compliance Map

- Grafo normativo interativo (11 nós, 15 arestas)
- Páginas: Grafo, Matriz Compliance, Comparação Normativa, Radar Riscos
- Deploy: Streamlit Cloud
- Repo: github.com/marcabru-tech/lex-io-graph
