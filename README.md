# Lexiograph — Gramática Semiótica dos Sistemas Digitais

> Uma gramática visual que emerge da interseção entre compliance digital, interação sistêmica e estruturação do conhecimento.

**Live → [hubstry.dev/lex-io-graph](https://hubstry.dev/lex-io-graph/)**

---

## O que é a Lexiograph

Ao decompor **Lexiograph = Lex + IO + Graph**, revelamos uma arquitetura semiótica que traduz sistemas digitais em signos, fluxos e grafos.

| Camada | Domínio | Função |
|--------|---------|--------|
| **Lex** | Lei, compliance, governança digital | Princípios éticos e regulatórios aplicados a sistemas e algoritmos |
| **IO** | Input/output, interação e fluxo | Interfaces homem-máquina, protocolos, orquestração de eventos |
| **Graph** | Grafia, grafos e estrutura de conhecimento | Modelagem semântica, ontologias, visualizações navegáveis |

A assinatura **Lex Quantum** integra rigor técnico e estética semiótica em soluções que interpretam, codificam e comunicam sistemas complexos.

---

## Ecossistema

A Lexiograph nasce dentro do ecossistema **Hubstry Deep Tech** — holding mista operacional que reúne ventures em deep tech, compliance digital, linguística computacional e infraestrutura de conhecimento.

| Venture | Função |
|---------|--------|
| **Hubstry CaaS** | Compliance-as-a-service em Rust (ECA Digital / Lei 15.211/2025) |
| **GuruDev®** | Linguagem de programação ontológico-multissemiótica |
| **Gonçalves et Alii** | Escritório de direito digital e dados |
| **Instituto PCIH³** | Pesquisa independente em ICT |

---

## Produtos

### Lex Quantum — Compliance Map (Demonstração Aberta)

Dashboard interativo com grafos que mapeiam o ordenamento jurídico digital brasileiro — conexões entre Constituição, LGPD, Marco Civil, ECA Digital, PL 2.338 (IA), NR-1 e jurisprudência.

**Demo → [compliance-map.streamlit.app](https://compliance-map.streamlit.app)** (em breve)

**Repositório → [lex-quantum-compliance-map/](https://github.com/guilherme-machado-ceo/lex-quantum-compliance-map)** (em breve)

---

## Stack

- HTML5 + CSS3 (site estático)
- GitHub Pages (hospedagem)
- GitHub Actions (deploy CI/CD)

---

## Estrutura

├── index.html # Página principal
├── assets/
│ ├── lexiograph-logo.svg
│ └── logo-removebg.png
├── README.md
└── LICENSE # Apache License 2.0


---

## Deploy

O site é deployado automaticamente via GitHub Pages. Qualquer push na branch `main` dispara o rebuild.

```bash
# Clone
git clone https://github.com/USER/lexiograph-gramatica-semiotica.git
cd lexiograph-gramatica-semiotica

# Editar
# ... modificar index.html ...

# Deploy
git add .
git commit -m "feat: descrição da mudança"
git push origin main
# GitHub Actions faz o deploy automaticamente
Licenciamento

Este projeto está licenciado sob a Apache License 2.0. Consulte o arquivo LICENSE para o texto completo.



Contato

Guilherme Machado — Fundador, Hubstry Deep Tech


📧 
globaldeeptechecosystem@hubstry.dev

🔗 
LinkedIn
 · 
GitHub



"Comunicar bem não é simplificar. É encontrar a forma exata em que a complexidade se torna navegável."


---

## Parte 2 — Projeto Completo: Lex Quantum — Compliance Map

### Estrutura do repositório

lex-quantum-compliance-map/
├── README.md
├── requirements.txt
├── .streamlit/
│ └── config.toml
├── data/
│ ├── normas.json
│ ├── arestas.json
│ └── jurisprudencia.json
├── lib/
│ ├── init.py
│ ├── constants.py
│ └── graph_builder.py
├── app.py
└── pages/
├── 1_📊Grafo_Normativo.py
├── 2📋Matriz_Compliance.py
├── 3⚖️_Comparacao_Normativa.py
└── 4_🎯_Radar_Riscos.py


---

### `requirements.txt`

```txt
streamlit>=1.35.0
networkx>=3.3
pyvis>=0.3.2
plotly>=5.22.0
pandas>=2.2.0


