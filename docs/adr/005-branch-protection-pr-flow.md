# ADR 005 — Branch Protection e Fluxo de PR

## Status: Aceito

## Contexto

Durante as Sprints 2–9, múltiplos `git push --force` direto na `main` causaram
perda de arquivos, quebra do app em produção e horas de retrabalho.
O repositório é público e o Streamlit Cloud faz deploy automático de qualquer
push na `main` — qualquer arquivo corrompido quebra o produto imediatamente.

## Decisão

1. Branch protection ativada na `main` — nenhum push direto permitido
2. Todo código entra via Pull Request
3. PR requer ao menos 1 aprovação (self-review para repositório solo)
4. GitHub Actions não fazem commit direto — abrem PR para revisão

## Consequências

- Elimina o problema raiz dos force pushes acidentais
- Adiciona ~30 segundos por entrega (abrir e aprovar PR)
- GitHub Actions de radar e IPII já implementados com fluxo de PR
- Histórico do repositório preservado — sem rebase forçado

## Implementação

```bash
gh api repos/marcabru-tech/lex-io-graph/branches/main/protection \
  --method PUT \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field enforce_admins=false
```

## Atualização — outubro de 2026

- **Item 4 substituído pelo [ADR 006](006-ingestao-automatizada-de-dados.md).** O radar
  legislativo deixou de abrir PR em ago/2026 e passou a commitar direto em `main`. O ADR 006
  formaliza essa exceção e a restringe a um único arquivo de dados, com validação e proveniência.
- **Verificação automática.** O workflow `.github/workflows/ci.yml` roda `smoke_test.py` em todo
  PR e todo push para `main`. Pode ser marcado como verificação obrigatória na proteção de branch.
- **Nota de implementação.** Com `enforce_admins=false`, o administrador do repositório não é
  barrado pela proteção. Os itens 1 a 3 valem como regra de conduta, não como trava técnica.
