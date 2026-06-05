# CHANGELOG — Lex-IO-Graph

Sistema de inteligência jurídico-estratégica com gramática visual-cognitiva,
fundamentação semiótica, inventário pancrônico e vetor prospectivo.

---

## [0.3.0] — Sprint 2 — 2026-06-05

### Identidade
- Produto renomeado para `Lex-IO-Graph` (Lex + IO + Graph)
- Subtítulo institucional em todas as páginas e sidebar
- Versão semântica introduzida (SemVer)

### Visual
- Hierarquia espacial do grafo correspondendo ao ordenamento jurídico:
  CF/88 (Constituição Federal de 1988) ancorada no topo, leis abaixo,
  decretos e normas regulamentares abaixo, PLs (Projetos de Lei) na base
- Semântica das cores com fundamentação semiótica explícita:
  dourado = razão/intelecto/norma fundamental;
  vermelho = tensão/conflito/antinomia;
  verde = complementaridade; ciano = interpretação/fluxo
- Formas geométricas como camada semiótica adicional:
  círculo = norma vigente; diamante = jurisprudência;
  quadrado = órgão; triângulo = PL/prospectiva; hexágono = doc. internacional
- Legenda de cores com fundamentação semiótica na sidebar
- Legenda de formas geométricas na sidebar

### Conteúdo
- Toda sigla acompanhada do nome por extenso entre parênteses
  na primeira ocorrência
- Glocal (global + local, Robertson, 1990s) como termo padrão
- Referências doutrinais com datas: Kelsen (1881–1973),
  Bobbio (1909–2004), Canaris (1937–2021)

### Correções mantidas da Sprint 1
- Tooltip em texto puro (fix sandbox iframe PyVis)
- Filtros padrão: dados_pessoais + internet / constituicao + lei + jurisprudencia
- Footer Lexiograph | Hubstry Deep Tech em todas as páginas

---

## [0.2.0] — Sprint 1 — 2026-06-04

### Conteúdo normativo
- NR-1 (Norma Regulamentadora 1) corrigida: ano 2026,
  Portaria MTE (Ministério do Trabalho e Emprego) 1.419/2024,
  vigente desde 26/05/2026
- STF (Supremo Tribunal Federal) Tema 987 (RE 1.037.396):
  inconstitucionalidade parcial do art. 19 do Marco Civil
  da Internet (Lei 12.965/2014) — embargos pendentes
- Decretos 12.975/2026 e 12.976/2026 (proteção plataformas
  e mulheres no ambiente digital)
- PL (Projeto de Lei) 4/2025: Livro VI do Código Civil —
  Direito Civil Digital
- PL 896/2023: criminalização da misoginia
  (aprovado Senado, aguarda Câmara)
- Lei 15.409/2026: CNVM (Cadastro Nacional de Pessoas
  Condenadas por Violência contra a Mulher)
- Crise institucional tripartite: 24+ PDLs (Projetos de
  Decreto Legislativo) da oposição contra os Decretos
  12.975 e 12.976/2026

### Infraestrutura
- Footer Lexiograph | Hubstry Deep Tech em todas as páginas
- Legenda doutrinária das relações jurídicas na sidebar
- .gitignore com venv/ e *.ps1
- Tooltip corrigido para texto puro (fix sandbox iframe)

---

## [0.1.0] — MVP — 2026-06-03

### Lançamento inicial
- Grafo interativo do ordenamento jurídico digital brasileiro
- 13 nós: CF/88, LGPD, Marco Civil, ECA, ECA Digital,
  PL 2.338/2023, NR-1, ANPD, STF ADI 5527, STJ REsps
- 17 arestas tipadas: hierarquia, interseção, antinomia,
  complementaridade, regulamenta, interpreta
- 4 páginas: Grafo Normativo, Matriz Compliance,
  Comparação Normativa, Radar Riscos
- Deploy: Streamlit Cloud
  (lex-io-graph-compliance-map.streamlit.app)
- Repositório: github.com/marcabru-tech/lex-io-graph
