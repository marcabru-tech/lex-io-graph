# ADR 006 — Ingestão automatizada de dados

## Status: Aceito (outubro de 2026)

Substitui o item 4 do [ADR 005](005-branch-protection-pr-flow.md).

## Contexto

O ADR 005 determinou que GitHub Actions abrissem PR em vez de commitar em `main`. Na prática:

- Entre jul e ago/2026, o radar legislativo criou os ramos `data/radar-update-2026-07-27`,
  `-08-03` e `-08-10`, mas a criação das PRs falhava e os ramos acumularam sem merge.
- Desde ago/2026 o workflow `update-radar.yml` commita direto em `main`, contrariando o ADR 005
  sem registro formal.
- PRs abertas com o `GITHUB_TOKEN` não disparam outros workflows. Validar a PR exigiria um token
  pessoal guardado como segredo, mais proteção de branch com verificação obrigatória e auto-merge.

O snapshot do radar é **alerta**, não norma: nenhuma proposição entra no grafo sem decisão do
curador em `normas.json`. Ainda assim, é evidência de um sistema de inteligência regulatória e
precisa ser auditável.

## Decisão

1. O robô do radar pode commitar direto em `main`, **somente** em `data/radar_legislativo.json`.
2. Antes do commit, o workflow executa duas travas; qualquer falha encerra o job sem commit:
   - **validação** — `python -m lib.validacao --radar` (estrutura, ids, coleta não vazia);
   - **escopo** — qualquer arquivo alterado fora do permitido aborta o job.
3. Todo snapshot grava um bloco `proveniencia`: executor, URL da execução, data da coleta,
   hash SHA-256 do conteúdo, e, por fonte, estado declarado (ativa, parcial, desativada),
   itens coletados e temas herdados do snapshot anterior.
4. Código, corpus (`normas.json`, `arestas.json`) e teoria continuam sob o ADR 005.
5. Toda nova automação que precise escrever no repositório exige ADR próprio ou emenda a este.

## Consequências

- Auditabilidade vem do histórico do Git (quem, quando, o quê) somado à proveniência no dado
  (de onde, em que estado estava cada fonte, o que foi herdado).
- Não há segredo adicional a gerenciar.
- Um snapshot quebrado não chega a `main`, e portanto não chega ao Streamlit Cloud.
- O juízo humano permanece onde já estava: na promoção de uma proposição a nó do corpus.
  Princípio: o radar alerta, o curador decide.

## Alternativa considerada

PR automática com CI e auto-merge. Rejeitada por exigir token pessoal, por depender de
configuração que o ADR 005 previa mas não estava ativa, e por repetir o modo de falha observado
em jul-ago/2026 caso o auto-merge não esteja configurado.
