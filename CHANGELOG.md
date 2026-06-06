# Changelog — Lex-IO-Graph

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
