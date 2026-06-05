# ADR 003 — Pancronia como metodologia do atlas jurídico

**Data:** 2026-06-05
**Status:** Aceito
**Sprint:** Backlog (implementação Sprint 3+)

## Contexto

O ordenamento jurídico brasileiro é composto por normas de
épocas distintas que coexistem e dialogam simultaneamente —
desde o Código Comercial de 1850 (Brasil Império) até os
Decretos 12.975 e 12.976/2026. Uma abordagem sincrônica
(corte temporal fixo) ou diacrônica (evolução linear) seria
insuficiente para representar essa coexistência.

## Decisão

Adotar metodologia pancrônica (pan = todo, do grego):
o arco histórico completo acessível simultaneamente como
campo de camadas coexistentes, não como timeline.

Fundamento teórico: dialogismo e polifonia bakhtinianos
(Bakhtin, 1895–1975) — múltiplas vozes (legislador, juiz,
doutrinador, costume) que coexistem em tensão produtiva,
sem fusão em voz única autoritária.

Implementação prevista:
- Nós do Brasil Império como camada histórica visível
- Linha pancrônica navegável (não timeline linear)
- Conexões entre normas de épocas distintas explicitando
  a coexistência e o dialogismo

## Consequências

- O grafo representa um campo, não uma sequência
- Norma de 1850 e decreto de 2026 têm igual presença
- Requer curadoria doutrinária para cada conexão histórica
