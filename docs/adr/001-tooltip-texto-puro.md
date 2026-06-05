# ADR 001 — Tooltip em texto puro (sem HTML)

**Data:** 2026-06-04
**Status:** Aceito
**Sprint:** 1

## Contexto

O PyVis renderiza o campo `title` dos nós dentro de um `<iframe>`
com sandbox `allow-scripts allow-same-origin` do Streamlit.
O vis.js escapa automaticamente qualquer HTML passado no `title`,
convertendo `<div>` em `&lt;div&gt;` — o tooltip exibia código HTML
literal em vez de conteúdo formatado.

Tentativas de fix via MutationObserver e injeção de JS no iframe
falharam por restrição do sandbox do Streamlit.

## Decisão

Usar texto puro no campo `title` com formatação via caracteres
ASCII (`-` como separador, `\n` como quebra de linha).
O CSS `.vis-tooltip { white-space: pre-wrap }` é injetado no HTML
gerado pelo PyVis para preservar as quebras de linha.

## Alternativas consideradas

- MutationObserver no iframe — descartado (sandbox Streamlit bloqueia)
- Componente customizado vis.js — descartado (complexidade excessiva para MVP)
- Substituir PyVis por D3.js — backlog futuro (Sprint 7+)

## Consequências

- Tooltip funcional e legível em todos os browsers
- Perda de formatação rica (negrito, cores por campo)
- Ganho de estabilidade e zero dependência de JS externo
