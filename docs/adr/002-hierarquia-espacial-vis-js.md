# ADR 002 — Hierarquia espacial via coordenada Y fixa no vis.js

**Data:** 2026-06-05
**Status:** Aceito
**Sprint:** 2

## Contexto

A Sprint 2 exige que a posição espacial dos nós no grafo
corresponda à hierarquia do ordenamento jurídico brasileiro:
CF/88 (Constituição Federal de 1988) no topo, leis abaixo,
decretos e normas regulamentares abaixo, PLs (Projetos de Lei)
na base. O movimento do grafo deve ser preservado.

## Decisão

Definir coordenada `y` fixa por tipo normativo via `HIERARCHY_LEVELS`
em `constants.py`, passada como parâmetro `y` no `net.add_node()`.
A física do vis.js (forceAtlas2Based) é mantida ativa (`physics=True`)
para o movimento, mas parte de posições iniciais ancoradas.

Mapeamento Y (coordenadas vis.js — negativo = topo):
- Constituição: y = -600 (topo absoluto)
- Órgãos / docs internacionais: y = -300 (lateral superior)
- Leis / jurisprudência: y = -100
- Decretos / normas regulamentares: y = 150
- PLs (prospectiva): y = 400 (base)

## Alternativas consideradas

- Hierarquia via `level` do vis.js (modo hierárquico nativo) —
  descartado pois desativa física e elimina o movimento
- Layout manual por nó — descartado (não escalável)

## Consequências

- CF/88 parte do topo e tende a permanecer lá
- Física pode deslocar nós após estabilização — comportamento esperado
- Usuário pode reorganizar arrastando — intencional
