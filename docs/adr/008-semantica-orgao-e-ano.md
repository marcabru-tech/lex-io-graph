# ADR 008 — Semântica dos campos `orgao`, `ano` e `sigla`

**Status:** proposto para revisão — não ratificado. Nenhum dado do corpus deve
ser alterado com base neste documento antes da ratificação explícita.

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

## Princípios gerais (propostos)

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

## Decisão proposta por tipo

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
- **Ponto a ratificar:** se o nó representa a norma como série contínua ou o
  ato que aprovou o texto hoje vigente. A proposta é a série contínua, por
  coerência com o `nome`. Para a NR-1, a série começa com a Portaria MTb
  nº 3.214, de 8 de junho de 1978, que aprovou as NRs (texto no portal do MTE).
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
- **Ponto a ratificar:** quando a Casa revisora atribui número próprio ao
  projeto, qual número é a `sigla` estável. Depende de confirmação nos portais
  da Câmara e do Senado.
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
  conforme a lei que a rege. Alternativa a ratificar: o emissor do ato de
  criação.
- **`ano`:** ano do ato legal que criou a entidade identificada no `nome`.
  Entidades predecessoras e transformações ficam em `historia`.
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
- **Ponto a ratificar:** se a prioridade do produto é o direito brasileiro
  vigente, a alternativa é `ano` = ano da incorporação. Este ADR recomenda o
  instrumento.
- **Fonte:** depositário do tratado (assinatura), organização ou emissor
  oficial (adoção ou data do documento) e decreto de promulgação no Planalto.

## `sigla`, `historia` e `status`

- **`sigla`:** identificador estável e curto. Sem datas de vigência, estágio de
  tramitação ou datas de apresentação.
- **`historia`:** trajetória, tramitação, vigência de partes, marcos
  institucionais e a data da última conferência quando o dado for mutável.
- **`status`:** inalterado por este ADR.

**Conflito com decisão ratificada.** A PR #38 definiu as siglas de `nr1` e
`magnifica_humanitas` com datas de vigência e de apresentação. A regra acima as
tornaria incompatíveis. Este ADR **não** propõe revertê-las: aplicar a regra
de `sigla` a esses dois nós reabriria uma decisão já ratificada e exige
autorização explícita própria.

## Inventário de divergências

Separado em dois grupos. Nenhuma linha autoriza alteração antes da ratificação.

### A. Divergências confirmadas pela própria identificação ou por fonte já lida

| ID | Campo | Valor atual | Convenção aplicada | Evidência | Decisão pendente |
|---|---|---|---|---|---|
| `pl_misoginia` | `ano` | 2026 | ano da apresentação | O número `PL 896/2023` indica 2023 | Confirmar data de apresentação no portal; ratificar regra de `pl` |
| `pl_misoginia` | `orgao` | `Câmara dos Deputados (pendente)` | Casa atual, sem estado | Anotação de estado no valor | Confirmar Casa atual; ratificar decisão A |
| `pl_misoginia` | `sigla` | `PL 896/2023 (aprovado Senado — aguarda Câmara)` | identificador sem tramitação | Estado de tramitação na sigla | Confirmar número na Casa atual |
| `anpd` | `ano` | 2020 | ano do ato que criou a entidade do `nome` | Lei 15.352/2026, art. 1º (novo art. 55-A da LGPD: "Fica criada a Agência Nacional de Proteção de Dados") e art. 15 (sucessora da Autoridade) | Ratificar se o nó representa a Agência (2026) ou a instituição contínua desde a Autoridade (MP 869/2018) |
| `anpd` | `orgao` | `Governo Federal` | vinculação administrativa | Lei 15.352/2026, art. 1º (art. 55-A: autarquia vinculada ao Ministério da Justiça e Segurança Pública) | Ratificar regra do tipo `orgao` |
| `cf88` | `orgao` | `Congresso Nacional` | órgão que promulgou o texto originário | Preâmbulo da CF/88 no Planalto: promulgada pela Assembleia Nacional Constituinte | Ratificar regra de `constituicao` |

### B. Candidatos — exigem fonte primária antes de qualquer juízo

| ID | Campo | Valor atual | Convenção aplicada | Fonte primária necessária | Decisão pendente |
|---|---|---|---|---|---|
| `lgpd` | `orgao` | `Congresso Nacional / ANPD` | só o emissor | Lei 13.709/2018 | A ANPD não emitiu a lei |
| `eca`, `eca_digital` | `orgao` | `Congresso Nacional / ECA-TISEA` | só o emissor | Identificar o que é "ECA-TISEA" | Termo sem fonte identificada no corpus |
| `decreto_12975_2026` | `orgao` | `Presidência da República / ANPD` | só o emissor | Decreto 12.975/2026 | Verificar se há coautoria formal |
| `nr1` | `ano` | 2026 | ano de instituição (série contínua) | Portaria MTb nº 3.214/1978 (portal do MTE) sustenta 1978 | Ratificar série contínua × ato que aprovou o texto vigente |
| `nr1` | `orgao` | `Ministério do Trabalho e Emprego` | emissor, denominação atual | — | Provavelmente compatível |
| `pl_ia` | `orgao` | `Senado Federal` | Casa atual | Portais do Senado e da Câmara | Confirmar tramitação atual |
| `pl_cc_digital` | `orgao` | `Senado Federal` | Casa atual | Portal do Senado | Confirmar tramitação atual |
| `pl_ia`, `pl_cc_digital` | `ano` | 2023, 2025 | ano da apresentação | Portais legislativos | Provavelmente compatíveis |
| `convencao_viena_1969` | `ano` | 2009 | ano da assinatura | Registro do depositário (ONU); Decreto 7.030/2009 | 1969 se ratificada a regra do instrumento |
| `convencao_viena_1969` | `sigla` | `CVDT — Decreto 7.030/2009` | identificador do instrumento | — | Decreto iria para `historia` |
| `tratado_assuncao_1991` | `orgao` | `Mercosul` | partes celebrantes | Texto do Tratado | O Mercosul foi constituído pelo próprio tratado |
| `acordo_mercosul_singapura`, `acordo_mercosul_efta`, `acordo_mercosul_ue_ita` | `ano`, `orgao`, `sigla` | 2026; `Mercosul`; decreto | ano de assinatura; partes; identificador do instrumento | Data de assinatura de cada acordo; decretos de promulgação | `orgao` hoje omite a contraparte |
| `acordo_mercosul_ue_empa` | `orgao`, `sigla` | `Mercosul`; `EMPA (assinado em 17/01/2026)` | partes; sigla sem data | Texto do acordo | Data iria para `historia` |
| `magnifica_humanitas` | `orgao` | `Santa Sé / Vaticano` | emissor único | Documento oficial da Santa Sé | Santa Sé e Estado da Cidade do Vaticano são entes distintos |
| `stf_tema987` | `ano` | 2025 | ano do julgamento | Portal do STF | Conferir na Sprint 4 |
| `stj_resp`, `stj_resp_plat` | `ano` | 2020, 2021 | ano do julgamento | Inteiro teor (Sprint 4) | Registros `pendente` sem `data_julgamento` |
| `stf_adimc` | `ano` | `null` | ano do julgamento | Portal do STF | Permanece `null` até conferência |

## Consequências

- **Sprint 3b só começa após ratificação**, com uma PR por tipo ou por grupo
  coerente de nós, cada uma com fonte primária por valor alterado.
- **Testes de semântica** serão escritos depois da ratificação, por tipo (por
  exemplo: `ano` de `lei`/`decreto`/`pl` igual ao ano do número em `sigla`;
  `orgao` sem anotações entre parênteses; `ano` igual entre `normas.json` e
  `jurisprudencia.json`). Nenhuma trava é criada nesta PR.
- **IPII:** mudanças de `ano` alteram o componente temporal das comparações
  (`lib/ipii/matcher.py`). A Sprint 3b deve registrar esse efeito.
- **Fora do escopo:** `status`, o snapshot do radar legislativo (ADR 006) e o
  conteúdo editorial de `historia`.
