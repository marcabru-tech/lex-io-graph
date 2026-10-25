# Lex-IO-Graph

**Sistema de inteligência jurídico-estratégica com gramática visual-cognitiva, fundamentação semiótica, inventário pancrônico e vetor prospectivo.**

*Lex* (lei, governança) + *IO* (input/output, interação sistêmica) + *Graph* (grafo, estrutura semântica)

---

## O que é

Atlas interativo do ordenamento jurídico digital brasileiro — não um PDF de compliance, mas um sistema vivo que conecta normas, jurisprudência, doutrina, inteligência estratégica e radar legislativo automático.

**10 páginas · 33 nós no corpus · 49 conexões no grafo · IPII Engine proprietário**

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
| 10 | Teoria dos Conjuntos Jurídicos | Conjuntos do corpus calculados a partir de `normas.json` e arquitetura teórica |

---

## Acesso

**App:** [lexiograph.hubstry.dev](https://lexiograph.hubstry.dev) · reserva: [lex-io-graph-compliance-map.streamlit.app](https://lex-io-graph-compliance-map.streamlit.app)
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
│   ├── 9_🔬_IPII_Engine.py        # Engine proprietário
│   └── 10_Teoria_Conjuntos.py     # Conjuntos do corpus e arquitetura teórica
├── lib/
│   ├── __init__.py                # Pacote de módulos do Lexiograph
│   ├── conformidade.py            # Questionário, radar e relatório de conformidade
│   ├── conjuntos.py               # Operações sobre conjuntos calculados do corpus
│   ├── constants.py               # Identidade, paleta semiótica, constantes
│   ├── curadoria.py               # Princípio de curadoria humana
│   ├── estado_regulador.py        # Linha do tempo das agências reguladoras
│   ├── footer.py                  # Rodapé Lexiograph | Hubstry
│   ├── formato.py                 # Formatação de textos derivados do corpus
│   ├── graph_builder.py           # Construção do grafo NetworkX
│   ├── hermeneutica.py            # Correntes hermenêuticas, fontes, constituições
│   ├── inteligencia.py            # Casos estratégicos, epistemologia
│   ├── ipii/
│   │   ├── tokenizer.py           # GuruMatrix 5D aplicada ao corpus normativo
│   │   ├── matcher.py             # Matching contextual par-a-par
│   │   └── validator.py           # Validação e curadoria assistida
│   ├── multisemiose.py            # Citações literárias, obras de arte, glossário
│   ├── natureza.py                # Selos de natureza epistêmica das afirmações
│   ├── radar.py                   # APIs Senado, Câmara, LexML
│   ├── repositorio.py             # Inventário doutrinário
│   ├── taxonomia.py               # Ligação entre temas do radar e vetores do grafo
│   ├── telemetria.py              # Contagem de visitas sem dados pessoais
│   └── validacao.py               # Validação de integridade do corpus e dados derivados
├── data/
│   ├── normas.json                # Corpus normativo curado (33 nós)
│   ├── arestas.json               # Conexões tipadas (49 arestas)
│   ├── jurisprudencia.json        # Jurisprudência vinculada
│   ├── radar_legislativo.json     # Resultado do radar automático
│   ├── teoria.json                # Arquitetura teórica vinculada ao corpus
│   └── referencias_externas.json  # Referências citadas fora do corpus normativo
├── docs/
│   └── adr/                       # Architecture Decision Records
├── ipii_engine.py                 # Runner IPII Engine
├── updater.py                     # Runner Radar Legislativo
├── .github/workflows/
│   ├── ci.yml                     # CI — testes unitários + smoke test
│   └── update-radar.yml           # GitHub Action — atualização semanal do radar
├── cloudbuild.yaml                # Cloud Build — testes, build e deploy no Cloud Run
├── requirements.in                # Dependências diretas (editar este)
├── requirements.txt               # Versões exatas, geradas a partir do .in
├── CHANGELOG.md
└── ARCHITECTURE.md
```

---

## Deploy e reversão

**Produção:** Cloud Run, serviço `lexiograph` (região `us-central1`), domínio `lexiograph.hubstry.dev`. A reserva no Streamlit Community Cloud não é o ambiente oficial.

**Fluxo:** todo push na `main` dispara o gatilho do Cloud Build, que roda o `cloudbuild.yaml` em sequência: **testes unitários e smoke test → build com buildpacks (`Procfile`, Python de `.python-version`) → deploy**. Se um teste falhar, nada é publicado e o site segue na revisão anterior. A CI do GitHub Actions roda os mesmos testes em cada PR, antes do merge.

**Reversão** (Cloud Shell):

```bash
# 1. Ver as revisões recentes
gcloud run revisions list --service=lexiograph --region=us-central1 --limit=5

# 2. Mandar 100% do tráfego para a revisão boa
gcloud run services update-traffic lexiograph --region=us-central1 --to-revisions=NOME_DA_REVISAO=100

# 3. Depois de corrigir, voltar a seguir a revisão mais recente (obrigatório)
gcloud run services update-traffic lexiograph --region=us-central1 --to-latest
```

Atenção: enquanto o tráfego estiver fixado numa revisão (passo 2), os deploys novos são publicados mas **não recebem visitas** até o passo 3.

**Deploy manual** (console ou `gcloud run deploy`): só em emergência, porque pula os testes do gatilho. Registrar o motivo no CHANGELOG.

---

## Licença e propriedade intelectual

O projeto tem duas licenças, uma por componente (ver `NOTICE`).

### Camada pública — Apache License 2.0

Tudo o que não é IPII: páginas, módulos de `lib/` (exceto `lib/ipii/`) e dados normativos (`data/`). Texto integral em `LICENSE`.

### IPII Engine — PolyForm Noncommercial 1.0.0

O **IPII Engine** (Interação Paramétrica Iterativa por Interoperabilidade — `lib/ipii/`, `ipii_engine.py` e a página `9_🔬_IPII_Engine.py`) é de Guilherme Gonçalves Machado / Hubstry Deep Tech © 2026, sob a **PolyForm Noncommercial 1.0.0**. Texto integral em `lib/ipii/LICENSE`.

- ✅ **Permitido:** uso pessoal (estudo, hobby, experimento) e uso acadêmico / pesquisa.
- ❌ **Proibido:** qualquer uso comercial sem autorização prévia e por escrito do titular.
- 💼 **Licença comercial:** [globaldeeptechecosystem@hubstry.dev](mailto:globaldeeptechecosystem@hubstry.dev).

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
