# Arquitetura — Lex-IO-Graph

## Visão geral

O Lex-IO-Graph é uma aplicação Streamlit multi-página com arquitetura em três camadas:

1. **Camada de dados** — corpus normativo curado em JSON
2. **Camada de lógica** — módulos `lib/` com lógica de domínio
3. **Camada de apresentação** — páginas Streamlit com visualizações PyVis e HTML

---

## Decisão de arquitetura central

> **O curador humano é parte da arquitetura.**

Nenhum dado entra no grafo automaticamente. O IPII Engine sugere — o curador valida. O Radar Legislativo detecta — o curador decide. Isso é design intencional, não limitação técnica: a profundidade doutrinária do corpus é o fosso competitivo do produto.

---

## Estrutura de dados

### `normas.json`

Cada nó do grafo contém 12+ campos:

```json
{
  "id": "lgpd",
  "sigla": "LGPD",
  "nome": "Lei Geral de Proteção de Dados Pessoais",
  "tipo": "lei",
  "ano": 2018,
  "status": "vigente",
  "temas": ["dados_pessoais", "privacidade", "ia"],
  "ementa": "...",
  "historia": "...",
  "artigos_chave": ["art. 6º", "art. 7º", "art. 18º"],
  "orgao": "ANPD",
  "autores": [...],
  "latim": [...],
  "direito_comparado": "..."
}
```

### `arestas.json`

6 tipos de aresta tipadas: `hierarquia`, `interpreta`, `regulamenta`, `intersecao`, `complementaridade`, `antinomia`.

---

## IPII Engine

**Interação Paramétrica Iterativa por Interoperabilidade**

Engine proprietário de descoberta assistida de arestas. Analisa os pares do corpus em 6 dimensões (GuruMatrix 5D aplicada ao corpus jurídico):

| Dimensão | Peso | O que mede |
|---|---|---|
| Temas | 0.30 | Interseção de temas regulatórios |
| Hierarquia | 0.15 | Relação hierárquica normativa |
| Hermenêutica | 0.15 | Correntes e brocardos comuns |
| Direito comparado | 0.15 | Jurisdições glocais compartilhadas |
| Temporal | 0.10 | Proximidade histórica |
| Ementa | 0.15 | Vocabulário jurídico comum |

Propriedade intelectual: Hubstry Deep Tech © 2026.

---

## Radar Legislativo

Consulta APIs públicas semanalmente via GitHub Actions:

- **Senado Federal** — `legis.senado.leg.br/dadosabertos`
- **Câmara dos Deputados** — `dadosabertos.camara.leg.br/api/v2`
- **LexML** — `lexml.gov.br/busca/search` (output Atom XML)

**Princípio:** o radar alerta via PR — o curador aprova o merge.

---

## ADRs (Architecture Decision Records)

Ver `docs/adr/` para decisões de arquitetura documentadas.

---

## Stack

| Componente | Tecnologia |
|---|---|
| Framework | Streamlit |
| Grafo | NetworkX + PyVis |
| APIs | requests |
| Dados | JSON curado |
| Deploy | Streamlit Cloud |
| CI/CD | GitHub Actions |
| IP proprietária | lib/ipii/ (licença comercial Hubstry) |
