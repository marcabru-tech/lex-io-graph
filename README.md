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

### Lex Quantum — Compliance Map

Dashboard interativo com grafos que mapeiam o ordenamento jurídico digital brasileiro — conexões entre Constituição, LGPD, Marco Civil, ECA Digital, PL 2.338 (IA), NR-1 e jurisprudência.

**Demo → [compliance-map.streamlit.app](https://compliance-map.streamlit.app)** (em breve)

---

## Estrutura do Projeto

O repositório está organizado para suportar tanto o site institucional quanto o dashboard interativo:

```
.
├── index.html          # Página principal (Institucional)
├── app.py              # Entrada do Dashboard Streamlit
├── requirements.txt    # Dependências do Dashboard
├── data/               # Dados do grafo e normas (JSON)
├── lib/                # Lógica de construção e constantes
├── pages/              # Páginas do dashboard interativo
├── assets/             # Ativos visuais
├── .streamlit/         # Configurações de tema do Streamlit
├── README.md
└── LICENSE             # Apache License 2.0
```

---

## Executar Localmente

### 1. Site Institucional
Basta abrir o arquivo `index.html` em qualquer navegador moderno.

### 2. Dashboard Lex Quantum (Streamlit)
Para executar o dashboard interativo em sua máquina:

```bash
# Clone do repositório
git clone https://github.com/marcabru-tech/lex-io-graph.git
cd lex-io-graph

# Criar e ativar ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar o dashboard
streamlit run app.py
```

---

## Deploy

O site institucional é deployado via GitHub Pages, enquanto o dashboard é configurado para o Streamlit Community Cloud. Qualquer push na branch `main` dispara os processos de atualização.

---

## Licenciamento

Este projeto está licenciado sob a **Apache License 2.0**. Consulte o arquivo [LICENSE](LICENSE) para o texto completo.

---

## Contato

**Guilherme Machado** — Fundador, Hubstry Deep Tech

📧 globaldeeptechecosystem@hubstry.dev
🔗 [LinkedIn](https://linkedin.com/in/) · [GitHub](https://github.com/guilherme-machado-ceo)

---

> *"Comunicar bem não é simplificar. É encontrar a forma exata em que a complexidade se torna navegável."*
