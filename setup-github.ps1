# setup-github.ps1
# Sprint 10 — Configuracao de labels, milestones, issues e board no GitHub
# Executar UMA VEZ apos o push da Sprint 10
# Requer: gh auth login executado previamente

$REPO = "marcabru-tech/lex-io-graph"

Write-Host "=== Criando labels ===" -ForegroundColor Cyan

$labels = @(
    @{name="feature"; color="0e8a16"; description="Nova funcionalidade"},
    @{name="bug"; color="d73a4a"; description="Algo quebrado"},
    @{name="docs"; color="0075ca"; description="Documentacao"},
    @{name="enhancement"; color="a2eeef"; description="Melhoria de algo existente"},
    @{name="priority:high"; color="e4e669"; description="Fazer agora"},
    @{name="priority:low"; color="cfd3d7"; description="Quando tiver tempo"},
    @{name="sprint-2"; color="c44b4b"; description="Sprint 2"},
    @{name="sprint-3"; color="d4a853"; description="Sprint 3"},
    @{name="sprint-4"; color="9b59b6"; description="Sprint 4"},
    @{name="sprint-5"; color="3dc8e6"; description="Sprint 5"},
    @{name="sprint-6"; color="1abc9c"; description="Sprint 6"},
    @{name="sprint-7"; color="e67e22"; description="Sprint 7"},
    @{name="sprint-8"; color="2ecc71"; description="Sprint 8"},
    @{name="sprint-9"; color="e74c3c"; description="Sprint 9"},
    @{name="sprint-10"; color="8e44ad"; description="Sprint 10"}
)

foreach ($label in $labels) {
    gh label create $label.name --color $label.color --description $label.description --repo $REPO 2>$null
    Write-Host "  Label: $($label.name)"
}

Write-Host "`n=== Criando milestones ===" -ForegroundColor Cyan

$milestones = @(
    @{title="Sprint 2 — Grafo Normativo"; state="closed"; description="Hierarquia espacial, identidade visual, busca textual"},
    @{title="Sprint 3 — Repositório Doutrinário"; state="closed"; description="Autores, brocardos latinos, tradições jurídicas"},
    @{title="Sprint 4 — Multissemiose"; state="closed"; description="Citações literárias, obras de arte, glossário"},
    @{title="Sprint 5 — Inteligência Estratégica"; state="closed"; description="Casos estratégicos, epistemologia, direito natural"},
    @{title="Sprint 6 — Hermenêutica"; state="closed"; description="Correntes hermenêuticas, fontes, constituições"},
    @{title="Sprint 7 — Correções e Ajustes"; state="closed"; description="Bias dev júnior removido, tooltips corrigidos"},
    @{title="Sprint 8 — IPII Engine + Radar"; state="closed"; description="IPII Engine proprietário, Radar Legislativo, GitHub Action"},
    @{title="Sprint 9 — Enriquecimento do Corpus"; state="closed"; description="9 nós enriquecidos com autores, latim, direito comparado"},
    @{title="Sprint 10 — README e Infraestrutura"; state="open"; description="README, ARCHITECTURE, branch protection, board Kanban"}
)

foreach ($ms in $milestones) {
    gh api repos/$REPO/milestones --method POST `
        --field title=$ms.title `
        --field state=$ms.state `
        --field description=$ms.description | Out-Null
    Write-Host "  Milestone: $($ms.title)"
}

Write-Host "`n=== Criando issues por sprint ===" -ForegroundColor Cyan

$issues = @(
    @{title="Sprint 2: Hierarquia espacial e identidade visual do grafo"; labels="feature,sprint-2"; body="Implementado: hierarquia espacial CF/88 no topo, semântica de cores/formas, busca textual, toggle Lista/Grafo, sidebar doutrinária."; milestone=1},
    @{title="Sprint 3: Repositório doutrinário e brocardos latinos"; labels="feature,sprint-3"; body="Implementado: lib/repositorio.py com 11 autores, 9 brocardos, 4 tradições jurídicas, Magnifica Humanitas."; milestone=2},
    @{title="Sprint 4: Multissemiose — citações literárias e obras de arte"; labels="feature,sprint-4"; body="Implementado: lib/multisemiose.py com 8 citações literárias, 4 obras de arte, glossário jurídico."; milestone=3},
    @{title="Sprint 5: Inteligência estratégica e epistemologia do direito"; labels="feature,sprint-5"; body="Implementado: lib/inteligencia.py com 4 casos estratégicos, arco epistemológico, direito natural."; milestone=4},
    @{title="Sprint 6: Hermenêutica, fontes do direito e 7 constituições brasileiras"; labels="feature,sprint-6"; body="Implementado: lib/hermeneutica.py com 6 correntes, fontes, arco CC, 7 constituições, in memoriam Sandoval."; milestone=5},
    @{title="Sprint 7: Correções editoriais e de conteúdo"; labels="bug,sprint-7"; body="Corrigido: bias dev júnior removido de todas as páginas, tooltips com texto completo, foco de aplicação correto."; milestone=6},
    @{title="Sprint 8: IPII Engine e Radar Legislativo"; labels="feature,sprint-8"; body="Implementado: IPII Engine (Interação Paramétrica Iterativa por Interoperabilidade), Radar Legislativo com APIs públicas, GitHub Action com PR."; milestone=7},
    @{title="Sprint 9: Enriquecimento doutrinário de 9 nós do corpus"; labels="enhancement,sprint-9"; body="Enriquecidos: decreto_12975, decreto_12976, pl_misoginia, lei_15409, magnifica_humanitas, stf_adimc, stj_resp, stj_resp_plat, anpd com autores, latim e direito comparado."; milestone=8},
    @{title="Sprint 10: README, infraestrutura GitHub e correções"; labels="docs,feature,sprint-10,priority:high"; body="Em progresso: README profissional, ARCHITECTURE.md, .gitattributes, requirements.txt, branch protection, labels, milestones, board Kanban, ADR 005, correção nome IPII."; milestone=9}
)

foreach ($issue in $issues) {
    $result = gh issue create `
        --repo $REPO `
        --title $issue.title `
        --body $issue.body `
        --label $issue.labels 2>&1
    Write-Host "  Issue: $($issue.title.Substring(0, [Math]::Min(50, $issue.title.Length)))..."
}

Write-Host "`n=== Fechando issues das sprints concluidas ===" -ForegroundColor Cyan
# Fechar issues 1-8 (sprints 2-9 concluidas)
for ($i = 1; $i -le 8; $i++) {
    $issues_list = gh issue list --repo $REPO --state open --json number,title | ConvertFrom-Json
    foreach ($iss in $issues_list) {
        if ($iss.title -match "Sprint [2-9]:") {
            gh issue close $iss.number --repo $REPO 2>$null
        }
    }
}

Write-Host "`n=== Configurar branch protection ===" -ForegroundColor Cyan
Write-Host "Execute manualmente via GitHub UI:" -ForegroundColor Yellow
Write-Host "  Settings > Branches > Add rule > main" -ForegroundColor Yellow
Write-Host "  Marcar: Require a pull request before merging" -ForegroundColor Yellow
Write-Host "  Required approving reviews: 1" -ForegroundColor Yellow

Write-Host "`n=== Concluido ===" -ForegroundColor Green
Write-Host "Board Kanban: https://github.com/$REPO/projects" -ForegroundColor Green
