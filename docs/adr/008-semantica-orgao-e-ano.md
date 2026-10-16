# ADR 008 — Semântica dos campos `orgao`, `ano` e `sigla`

**Status:** aceito — ratificado em 16/10/2026 pelo mantenedor, após revisão
independente. As seis decisões em aberto da proposta estão registradas na seção
"Decisões ratificadas". A aplicação ao corpus ocorre na Sprint 3b, com fonte
primária para cada valor alterado. A ratificação aprova a semântica; não
valida nenhum valor do corpus.

## Contexto

`data/normas.json` reúne 29 nós de oito tipos (`lei` 8, `documento_internacional`
7, `jurisprudencia` 4, `pl` 3, `decreto` 3, `norma_regulamentar` 2,
`constituicao` 1, `orgao` 1). Os campos `orgao` e `ano` são usados com
significados implícitos e diferentes entre os tipos, e às vezes dentro do mesmo
tipo:

- `orgao` ora indica o emissor (`Presidência da República`), ora acumula emissor
  e fiscalizador (`Congresso Nacional / ANPD`), ora carrega estado processual
  (`Câmara dos Deputados (pendente)`).
- `ano` ora indica a emissão do instrumento (`lgpd: 2018`), ora a incorporação
  brasileira de um tratado (`convencao_viena_1969: 2009`), ora um marco
  posterior à identificação (`pl_misoginia: 2026` com sigla `PL 896/2023`).
- `sigla` ora é um identificador estável (`Lei 12.965/2014`), ora contém
  tramitação ou vigência (`PL 896/2023 (aprovado Senado — aguarda Câmara)`).

Esses campos são exibidos no Grafo Normativo e na Comparação Normativa e
alimentam o componente temporal do IPII (`lib/ipii/tokenizer.py`,
`lib/ipii/matcher.py`). Corrigir valores caso a caso, sem uma semântica
declarada, troca uma inconsistência por outra. A trava atual
`test_corpus_real_so_o_adi_5527_esta_sem_ano` só verifica presença de `ano`,
não seu significado.

## Princípios gerais

1. **Significado consistente por tipo.** Cada campo tem um único significado
   dentro de cada tipo, declarado neste ADR. O significado pode variar entre
   tipos, mas nunca dentro de um tipo. O **valor** pode mudar ao longo do tempo
   quando o significado declarado o exigir (caso de `orgao` em `pl`); nesse
   caso, `historia` registra a mudança e a data da última conferência.
2. **Campos estruturados, não narrativa.** `orgao`, `ano` e `sigla` guardam
   valores curtos e definidos por este ADR. Trajetória, tramitação, vigência de
   partes, alterações posteriores e marcos institucionais vão para `historia`.
   `status` continua sendo o rótulo de alto nível já existente (fora do escopo
   deste ADR).
3. **O nó representa o instrumento nomeado em `nome`.** Quando nome e campos
   apontarem para instrumentos diferentes (por exemplo, o tratado e o decreto
   que o promulga), prevalece o instrumento do `nome`.
4. **Desconhecido é `null`.** Como no ADR 007, um valor que não pôde ser
   conferido em fonte primária fica `null`, não é preenchido por suposição.
   Valores atuais não conferidos permanecem até a Sprint 3b, mas são listados
   no inventário abaixo.
5. **Múltiplos responsáveis.** `orgao` só usa `A / B` quando o próprio ato é
   emitido conjuntamente (ato conjunto, portaria interministerial, tratado
   multilateral). Fiscalizador, implementador ou regulamentador não entram em
   `orgao`; vão para `historia`.

## Decisão por tipo

### `constituicao`
- **`orgao`:** órgão que promulgou o texto originário.
- **`ano`:** ano da promulgação. Emendas ficam em `historia`.
- **Fonte de autoridade:** preâmbulo e fecho do texto constitucional (Planalto).

### `lei`
Inclui decretos-leis classificados como `lei` (caso `lindb`).
- **`orgao`:** órgão que editou o ato. Lei ordinária ou complementar federal:
  `Congresso Nacional`. Decreto-lei: `Presidência da República`.
- **`ano`:** ano constante da identificação oficial do ato (data de assinatura),
  que coincide com o ano do número (`Lei 13.709/2018` → 2018). Alterações e
  datas de vigência ficam em `historia`.
- **Fonte:** texto no Planalto.

### `decreto`
- **`orgao`:** `Presidência da República` (art. 84, IV, da CF). Órgão que
  propôs, regulamenta ou fiscaliza não entra.
- **`ano`:** ano constante da identificação oficial.
- **Fonte:** texto no Planalto.

### `norma_regulamentar`
- **`orgao`:** órgão emissor competente, na denominação atual (ministérios mudam
  de nome; a denominação histórica fica em `historia`).
- **`ano`:** ano de instituição da norma representada pelo nó. Substituições
  integrais de texto, inclusões de capítulos e vigências de partes ficam em
  `historia`.
- **Decisão ratificada (1):** o nó representa a norma como série contínua, não
  o ato que aprovou o texto hoje vigente, em coerência com o caráter de
  "inventário pancrônico" declarado no `README.md`. Para a NR-1, a série começa com a
  Portaria MTb nº 3.214, de 8 de junho de 1978, que aprovou as NRs (texto no
  portal do MTE); as alterações posteriores ficam em `historia`.
- **Fonte:** portaria de instituição e portarias de alteração, no DOU ou no
  portal oficial do órgão.

### `pl`
- **`orgao`:** Casa legislativa que analisa o projeto **atualmente** (decisão A
  do briefing), não a Casa de origem. Sem anotações de estado no valor
  (`(pendente)` sai). O significado é fixo; o valor muda quando o projeto muda
  de Casa (princípio 1). Cada mudança exige que `historia` registre a passagem
  entre as Casas e a data da última conferência no portal oficial.
- **Abrangência:** a regra vale para os três projetos do corpus: `pl_ia`,
  `pl_cc_digital` e `pl_misoginia`.
- **`ano`:** ano da apresentação da proposição, que coincide com o ano do
  número de identificação. Não o ano da votação mais recente.
- **`sigla`:** número de identificação, sem estado de tramitação.
- **Decisão ratificada (5):** a `sigla` canônica é o número original atribuído
  pela Casa de origem. Se a Casa revisora atribuir outro identificador, a
  referência cruzada vai para `historia`, com a data da conferência. Assim,
  `orgao` acompanha a tramitação e `sigla` preserva a identidade do projeto.
- **Fonte:** portais de tramitação da Câmara dos Deputados e do Senado Federal.

### `jurisprudencia`
- **`orgao`:** tribunal (`STF`, `STJ`). O órgão julgador interno (Plenário,
  Turma, Seção) já tem campo próprio, `orgao_julgador`, em
  `data/jurisprudencia.json`, e não é duplicado aqui.
- **`ano`:** ano da data de julgamento da **decisão efetivamente representada
  pelo registro** — uma única decisão por registro. Decisões anteriores ou
  posteriores do mesmo processo (embargos, fixação de tese em outro momento,
  modulação) ficam em `historia`, ou em registros separados quando o modelo
  justificar. A publicação fica em `data_publicacao` e nunca substitui o
  julgamento.
- **Sem inferência:** se a data de julgamento da decisão representada não
  estiver identificada em fonte oficial, `ano` não é preenchido a partir de
  outra data (publicação, autuação, outra decisão do processo). Valores atuais
  nessa situação são tratados como não verificados e não servem de base para
  promoção a `verificado` (ADR 007).
- **Coerência:** `ano` em `normas.json` e em `jurisprudencia.json` deve ser o
  mesmo para o mesmo `id`.
- **Fonte:** portal do tribunal (acompanhamento processual e inteiro teor).

### `orgao` (tipo)
- **`orgao`:** ente ao qual a instituição está vinculada administrativamente,
  conforme a lei que a rege — não o emissor do ato de criação **(decisão
  ratificada 2)**.
- **`ano`:** ano do ato legal que criou a entidade identificada no `nome`.
  Entidades predecessoras e transformações ficam em `historia`.
- **Decisão ratificada (3) — continuidade institucional:** quando uma lei cria
  uma entidade nova e a declara sucessora de outra, o nó representa a entidade
  identificada no `nome`, e a continuidade com a predecessora fica em
  `historia`. Caso concreto: a Lei 15.352/2026 cria a Agência Nacional de
  Proteção de Dados (novo art. 55-A da LGPD) e a declara sucessora da
  Autoridade Nacional de Proteção de Dados (art. 15). O nó `anpd` se chama
  Agência; logo, `ano` = 2026, com a trajetória da Autoridade em `historia`.
- **Fonte:** lei de criação e lei vigente de regência (Planalto).

### `documento_internacional`
- **`orgao`:** organização internacional que adotou o instrumento ou, se não
  houver, as partes que o celebraram. Para documento unilateral (encíclica), o
  emissor.
- **`ano`:** um único evento por categoria de instrumento, nunca o da
  incorporação brasileira:
  - **tratados e acordos:** ano da **assinatura** do texto (para tratado
    multilateral aberto a assinatura, a data de abertura registrada pelo
    depositário);
  - **documentos unilaterais** (encíclica, declaração de um único emissor): ano
    da **data do documento** (emissão), não o da apresentação ou divulgação;
  - **instrumentos adotados sem assinatura** (resolução ou declaração aprovada
    por organização internacional): ano da **adoção** pelo órgão competente.
    É o único caso em que a assinatura não se aplica.

  Motivos para não usar a incorporação: o `nome` identifica o instrumento; o tipo
  inclui documentos que nunca são incorporados (encíclica, acordo ainda não
  promulgado); e a incorporação já tem identificador próprio (o decreto de
  promulgação).
- **Decreto de promulgação:** registrado em `historia`. Se o produto precisar
  dele como dado estruturado, a decisão é criar campo próprio, não reutilizar
  `ano` ou `sigla`.
- **Decisão ratificada (4):** `ano` segue o instrumento internacional, pelas
  três regras acima, e não a incorporação brasileira.
- **Fonte:** depositário do tratado (assinatura), organização ou emissor
  oficial (adoção ou data do documento) e decreto de promulgação no Planalto.

## `sigla`, `historia` e `status`

- **`sigla`:** identificador estável e curto. Sem datas de vigência, estágio de
  tramitação ou datas de apresentação.
- **`historia`:** trajetória, tramitação, vigência de partes, marcos
  institucionais e a data da última conferência quando o dado for mutável.
- **`status`:** inalterado por este ADR.

**Revisão futura (decisão 6).** A PR #38 definiu as siglas de `nr1` e
`magnifica_humanitas` com datas de vigência e de apresentação, o que é
incompatível com a regra geral de `sigla`. Essas duas siglas **não** são
exceções permanentes: ficam reabertas para uma decisão específica, a ser
tomada fora deste ADR. Até essa decisão, os valores atuais são preservados, e
nem a Sprint 3b nem a regra geral de `sigla` os alteram:

- `nr1`: `NR-1 (cap. 1.5 incluído pela Portaria MTE 1.419/2024, vigência punitiva desde 26/05/2026)`
- `magnifica_humanitas`: `Magnifica Humanitas (Leão XIV, 15/05/2026; apresentada em 25/05/2026)`

## Inventário de divergências

Separado em dois grupos. Com a ratificação, as linhas do grupo A podem ser
corrigidas na Sprint 3b; as do grupo B dependem antes da fonte primária
indicada. Cada alteração exige fonte primária citada na própria PR.

### A. Divergências confirmadas pela própria identificação ou por fonte já lida

A semântica está ratificada; a última coluna lista o trabalho restante na
Sprint 3b. Mesmo aqui, nenhum valor é alterado sem a fonte primária citada na
PR correspondente.

| ID | Campo | Valor atual | Convenção aplicada | Evidência | Trabalho na Sprint 3b |
|---|---|---|---|---|---|
| `pl_misoginia` | `ano` | 2026 | ano da apresentação | O número `PL 896/2023` indica 2023 | Conferir a data de apresentação no portal; corrigir para o ano conferido |
| `pl_misoginia` | `orgao` | `Câmara dos Deputados (pendente)` | Casa atual, sem estado | Anotação de estado no valor | Conferir a Casa atual no portal; remover a anotação; registrar tramitação e data da conferência em `historia` |
| `pl_misoginia` | `sigla` | `PL 896/2023 (aprovado Senado — aguarda Câmara)` | número da Casa de origem, sem tramitação (decisão 5) | Estado de tramitação na sigla; a ficha da Câmara registra `PL 896/2023` com origem no Senado (conferência da revisão independente) | Reduzir a `PL 896/2023`; mover a tramitação para `historia` |
| `anpd` | `orgao` | `Governo Federal` | vinculação administrativa | Lei 15.352/2026, art. 1º (art. 55-A: autarquia vinculada ao Ministério da Justiça e Segurança Pública) | Corrigir para a vinculação prevista na lei, com o texto da Lei 15.352/2026 citado na PR |
| `cf88` | `orgao` | `Congresso Nacional` | órgão que promulgou o texto originário | Preâmbulo da CF/88 no Planalto: promulgada pela Assembleia Nacional Constituinte | Corrigir para `Assembleia Nacional Constituinte`, com o preâmbulo citado na PR |
| `nr1` | `ano` | 2026 | ano de instituição, série contínua (decisão 1) | Portaria MTb nº 3.214/1978 (portal do MTE) | Corrigir para 1978; registrar as alterações posteriores em `historia` |
| `anpd` | `ano` | 2020 | ano do ato que criou a entidade do `nome` (decisão 3) | Lei 15.352/2026, art. 1º (novo art. 55-A da LGPD) e art. 15 | Corrigir para 2026; registrar a trajetória da Autoridade em `historia` (efeito no IPII registrado na PR) |
| `lgpd` | `orgao` | `Congresso Nacional / ANPD` | só o emissor (princípio 5) | A Lei 13.709/2018 é ato do Congresso Nacional; a ANPD não é coautora da lei (sua criação é posterior, por ato próprio) | Corrigir para `Congresso Nacional`; registrar o papel da ANPD em `historia` se pertinente |

### B. Candidatos — exigem fonte primária antes de qualquer juízo

| ID | Campo | Valor atual | Convenção aplicada | Fonte primária necessária | Pendência |
|---|---|---|---|---|---|
| `eca`, `eca_digital` | `orgao` | `Congresso Nacional / ECA-TISEA` | só o emissor | Identificar o que é "ECA-TISEA" | Termo sem fonte identificada no corpus |
| `decreto_12975_2026` | `orgao` | `Presidência da República / ANPD` | só o emissor | Decreto 12.975/2026 | Verificar se há coautoria formal |
| `nr1` | `orgao` | `Ministério do Trabalho e Emprego` | emissor, denominação atual | — | Provavelmente compatível |
| `pl_ia` | `orgao` | `Senado Federal` | Casa atual | Portais do Senado e da Câmara | Confirmar tramitação atual |
| `pl_cc_digital` | `orgao` | `Senado Federal` | Casa atual | Portal do Senado | Confirmar tramitação atual |
| `pl_ia`, `pl_cc_digital` | `ano` | 2023, 2025 | ano da apresentação | Portais legislativos | Provavelmente compatíveis |
| `convencao_viena_1969` | `ano` | 2009 | ano da assinatura | Registro do depositário (ONU); Decreto 7.030/2009 | Conferir a data de assinatura no depositário; pela decisão 4, o valor esperado é 1969 |
| `convencao_viena_1969` | `sigla` | `CVDT — Decreto 7.030/2009` | identificador do instrumento | — | Decreto iria para `historia` |
| `tratado_assuncao_1991` | `orgao` | `Mercosul` | partes celebrantes | Texto do Tratado | O Mercosul foi constituído pelo próprio tratado |
| `acordo_mercosul_singapura`, `acordo_mercosul_efta`, `acordo_mercosul_ue_ita` | `ano`, `orgao`, `sigla` | 2026; `Mercosul`; decreto | ano de assinatura; partes; identificador do instrumento | Data de assinatura de cada acordo; decretos de promulgação | `orgao` hoje omite a contraparte |
| `acordo_mercosul_ue_empa` | `orgao`, `sigla` | `Mercosul`; `EMPA (assinado em 17/01/2026)` | partes; sigla sem data | Texto do acordo | Data iria para `historia` |
| `magnifica_humanitas` | `orgao` | `Santa Sé / Vaticano` | emissor único | Documento oficial da Santa Sé | Santa Sé e Estado da Cidade do Vaticano são entes distintos |
| `stf_tema987` | `ano` | 2025 | ano do julgamento | Portal do STF | Conferir na Sprint 4 |
| `stj_resp`, `stj_resp_plat` | `ano` | 2020, 2021 | ano do julgamento | Inteiro teor (Sprint 4) | Registros `pendente` sem `data_julgamento` |
| `stf_adimc` | `ano` | `null` | ano do julgamento | Portal do STF | Permanece `null` até conferência |

## Decisões ratificadas

| # | Questão | Decisão |
|---|---|---|
| 1 | `norma_regulamentar`: série contínua ou ato do texto vigente | Série contínua (inventário pancrônico); NR-1 desde 1978 |
| 2 | `orgao` no tipo institucional | Vinculação administrativa prevista na lei de regência |
| 3 | Continuidade institucional (`anpd`) | O nó representa a entidade do `nome`: Agência, 2026; continuidade em `historia` |
| 4 | `ano` em `documento_internacional` | Instrumento (assinatura, data do documento ou adoção), não incorporação |
| 5 | `sigla` de PL com número próprio na Casa revisora | Número original da Casa de origem; referência cruzada em `historia` |
| 6 | Siglas de `nr1` e `magnifica_humanitas` (PR #38) | Reabertas para decisão específica futura; valores atuais preservados até lá, sem caráter de exceção permanente |

## Consequências

- **Sprint 3b**, autorizada por esta ratificação, aplica as convenções com uma PR por tipo ou por grupo
  coerente de nós, cada uma com fonte primária por valor alterado.
- **Testes de semântica** serão escritos depois da ratificação, por tipo (por
  exemplo: `ano` de `lei`/`decreto`/`pl` igual ao ano do número em `sigla`;
  `orgao` sem anotações entre parênteses; `ano` igual entre `normas.json` e
  `jurisprudencia.json`). Nenhuma trava é criada nesta PR.
- **IPII:** mudanças de `ano` alteram o componente temporal das comparações
  (`lib/ipii/matcher.py`). A Sprint 3b deve registrar esse efeito.
- **Decisão específica pendente:** reavaliação das siglas de `nr1` e
  `magnifica_humanitas` (decisão 6), independente da Sprint 3b.
- **Fora do escopo:** `status`, o snapshot do radar legislativo (ADR 006) e o
  conteúdo editorial de `historia`.
