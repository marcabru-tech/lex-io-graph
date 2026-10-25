# ADR 007 — Estados de verificação da jurisprudência

**Status:** aceito

## Contexto

`data/jurisprudencia.json` guarda cinco registros cujos números, teses e anos
não foram conferidos em fonte oficial. Já há evidência de problemas: a tese de
`stf_adimc` diverge da controvérsia registrada no portal do STF, e o número de
`trf4_lgpd_cookies` não passa na verificação do dígito do padrão CNJ (esperado
32). Sem um estado explícito, um registro duvidoso é indistinguível de um
confirmado.

## Decisão

1. Cada registro passa a declarar `estado_verificacao` (`verificado`,
   `pendente` ou `contestado`), além de `fonte_oficial_url`, `orgao_julgador`,
   `relator`, `data_julgamento`, `data_publicacao`, `nivel_autoridade` e
   `proveniencia` (`origem`, `data_consulta`, `observacao`).
2. Distinguimos três coisas que não devem se misturar:
   - **dado recuperado** — o que uma fonte efetivamente disse (campos
     factuais e `proveniencia`);
   - **qualificação jurídica** — o que o dado significa (tese, resumo,
     `nivel_autoridade`);
   - **decisão editorial do curador** — a classificação em si
     (`estado_verificacao`) e sua justificativa (`observacao`).
3. Nenhum registro é promovido a `verificado` sem conferência humana em fonte
   oficial. Ferramentas automáticas podem sugerir, apontar divergência ou
   rebaixar, mas não promover.
4. Campo desconhecido é `null` (ou `desconhecido` em `nivel_autoridade`), nunca
   preenchido por suposição. `data_consulta` é a data real da consulta à fonte
   oficial; a data de uma migração ou edição não a substitui.
5. `lib/validacao.py::validar_jurisprudencia` impõe as regras: registro
   `verificado` exige fonte oficial, órgão julgador, relator, data de
   julgamento e autoridade conhecida. Divergência do dígito CNJ é erro em
   registro `verificado` e advertência em registro `pendente`/`contestado`.
   Assimetrias com `normas.json` são advertências.

## Consequências

- Dados existentes são preservados; resumos e números não são corrigidos até
  que haja conferência em fonte oficial.
- O grafo exibe o estado e um marcador para nós não verificados.
- Os cinco registros iniciais são `pendente` ou `contestado`; nenhum
  `verificado`.
- Pendência conhecida: a métrica "Jurisprudência vinculada" da página inicial
  ainda conta todos os registros sem distinguir estados.

## Atualização — 25/10/2026

Nota de contagem; a decisão acima não muda. O Contexto e as Consequências
descrevem o corpus na data da decisão, com cinco registros.

- **Contagem atual: 8 registros** em `data/jurisprudencia.json`, nenhum
  `verificado`: `stf_adimc` (`contestado`), `stj_resp` (`pendente`), `stj_resp_plat`
  (`pendente`), `stj_menor_online` (`pendente`), `tse_respel_0600359_pr`
  (`pendente`), `tse_agr_0600528_sp` (`pendente`), `tse_ed_0600528_sp`
  (`pendente`) e `tst_rr_0000284_pe` (`pendente`).
- Os quatro últimos (incluídos em 25/10/2026) vêm de inteiro teor assinado,
  fornecido pelo mantenedor (material do grupo de estudos GEDD). Seguem
  `pendente` até a conferência humana no portal oficial; os nós
  correspondentes em `normas.json` têm `status` `em_conferencia` e ficam fora
  do IPII.
- O quinto registro, `trf4_lgpd_cookies`, citado no Contexto pelo dígito CNJ
  divergente, foi removido do corpus em 16/10/2026 (commit `c0bb9d7`).
- A pendência sobre a métrica da página inicial continua: ela hoje se chama
  "Jurisprudência registrada" e ainda conta todos os registros, sem
  distinguir estados.
