"""
Camada de inteligência jurídico-estratégica do Lex-IO-Graph.

Vetor analítico: não apenas o fato normativo, mas o jogo de forças
institucional, civilizatório e geopolítico por trás de cada tensão.
Estilo: analítico de consultoria — diagnóstico, frio, acionável.
Evitar: teoria da dependência, tom acusatório, framing conspiratório,
fechamentos moralizantes. Fatos como diagnóstico estratégico e oportunidade.
"""

# ---- Casos de inteligência estratégica ----
# Selo padrão de natureza (Fase 0): caso sem rótulo próprio é leitura
# analítica. Separar fato verificado de interpretação é contrato do produto.
NATUREZA_CASO_PADRAO = (
    "Leitura analítica do Lexiograph: interpretação sobre fatos citados, com prospectiva "
    "em cenários. Não é fonte normativa nem previsão."
)
NATUREZA_ENSAIO_PADRAO = (
    "Ensaio doutrinário autoral: interpretação fundamentada nas normas e na doutrina citadas."
)

CASOS_ESTRATEGICOS = [
    {
        "id": "art19_guerra_institucional",
        "titulo": "Art. 19 do Marco Civil — Guerra Institucional Tripartite",
        "normas_relacionadas": ["marco_civil", "stf_tema987", "decreto_12975_2026", "decreto_12976_2026"],
        "nivel_tensao": "crítico",
        "status": "em curso — eleições outubro/2026",
        "sintese": (
            "O campo normativo do art. 19 do Marco Civil da Internet (Lei 12.965/2014) "
            "é o epicentro da maior crise institucional do direito digital brasileiro. "
            "Três poderes entraram no mesmo campo em direções incompatíveis, "
            "em contexto de ano eleitoral com instabilidade institucional elevada."
        ),
        "camadas": [
            {
                "titulo": "Tensão 1 — O vácuo legislativo como campo de batalha",
                "analise": (
                    "O PL 2.630/2020 (PL das fake news) foi retirado de pauta na Câmara em "
                    "02/05/2023 e não voltou ao Plenário; o art. 19 permaneceu sem revisão "
                    "legislativa. O STF declarou a inconstitucionalidade parcial e progressiva "
                    "do art. 19 (Tema 987, RE 1.037.396, jun./2025), com tese definitiva fixada "
                    "em 17/06/2026, após os embargos. O Executivo regulamentou o tema pelos "
                    "Decretos 12.975 e 12.976, de 20/05/2026. "
                    "Leitura: na ausência de lei nova, o Judiciário e o Executivo passaram a "
                    "ocupar o espaço que o Legislativo não redefiniu. As razões do impasse "
                    "legislativo são disputadas e não são objeto desta análise."
                )
            },
            {
                "titulo": "Tensão 2 — A antinomia bacamartiana: o Estado contra sua própria norma",
                "analise": (
                    "Machado de Assis, O Alienista (1882): Simão Bacamarte cria os critérios "
                    "de sanidade, interna metade da vila, revê os critérios, interna a outra "
                    "metade, e no fim interna a si mesmo. O Estado brasileiro criou o art. 19 "
                    "do Marco Civil (2014) como proteção à liberdade de expressão e ao "
                    "desenvolvimento da internet. Doze anos depois, o mesmo Estado — via STF — "
                    "declara essa norma insuficiente e a reconstrói sem base legislativa. "
                    "A insegurança jurídica resultante não é patologia do sistema — é o sistema "
                    "funcionando sem o componente que deveria funcionar: o Congresso. "
                    "Bacamarte é Montesquieu às avessas: concentração de poder diagnóstico, "
                    "terapêutico e sancionador nas mesmas mãos."
                )
            },
            {
                "titulo": "Tensão 3 — A reação legislativa: 27 PDLs (base da Câmara, 15/08/2026) e o argumento de competência",
                "analise": (
                    "Parlamentares de partidos de oposição (PL, Republicanos, União Brasil, Novo) "
                    "protocolaram 27 PDLs (Projetos de Decreto Legislativo; base da Câmara, "
                    "15/08/2026) para sustar os Decretos 12.975 e 12.976/2026, com fundamento na "
                    "extrapolação do poder regulamentar (CF, art. 49, V) e na proteção à liberdade "
                    "de expressão. A tensão institucional: o argumento de que a matéria é de "
                    "competência do Congresso convive com a ausência de lei aprovada sobre o tema. "
                    "O calendário eleitoral (outubro/2026) aumenta a visibilidade política da disputa."
                )
            },
            {
                "titulo": "Tensão 4 — O vetor geopolítico: plataformas globais e soberania regulatória",
                "analise": (
                    "O debate não é apenas doméstico. A suspensão do X (ex-Twitter) no Brasil "
                    "pelo STF (ago./2024) e o retorno após acordo (out./2024) inseriram o "
                    "Brasil no mapa global da regulação de plataformas e colocaram a regulação "
                    "brasileira no centro de uma disputa global entre soberania regulatória "
                    "dos Estados e poder privado das plataformas. O Decreto 12.975/2026 é lido por críticos como "
                    "modelo de censura estatal; pelo governo brasileiro como modelo de "
                    "responsabilidade de plataformas. Duas narrativas incompatíveis, "
                    "ambas estrategicamente corretas para seus proponentes."
                )
            }
        ],
        "prospectiva": {
            "12_meses": (
                "Eleições outubro/2026: qualquer governo eleito terá de lidar com a ausência "
                "de lei sobre moderação de conteúdo. Cenário A: revogação ou alteração dos "
                "decretos, com retorno da questão ao Congresso. Cenário B: continuidade dos "
                "decretos e pressão para converter em lei o que hoje está em regulamento."
            ),
            "36_meses": (
                "O AI Act (2024) e o DSA (Digital Services Act, 2022) europeus são o principal "
                "referencial de regulação de IA e de plataformas por lei; a avaliação de sua "
                "eficácia e de seus efeitos sobre a liberdade de expressão ainda está em curso. "
                "Um caminho para o Brasil é legislar, em vez de regulamentar por decreto; a "
                "janela provável é 2027–2028, após as eleições de 2026."
            ),
            "lacuna_remanescente": (
                "Mesmo com legislação, o problema estrutural persiste: a assimetria de "
                "capacidade técnica entre Estado e plataformas de grande porte. Nenhum decreto ou lei resolve "
                "o problema de quem tem competência para auditar algoritmos de moderação. "
                "Essa é a lacuna que o PL 2.338/2023 (Marco Legal da IA) precisa endereçar."
            )
        }
    },
    {
        "id": "lgpd_anpd_poder",
        "titulo": "LGPD e ANPD — A Construção Incremental de uma Autoridade Regulatória",
        "normas_relacionadas": ["lgpd", "anpd"],
        "nivel_tensao": "moderado",
        "status": "em consolidação — ANPD ganha competências via Decreto 12.975/2026",
        "sintese": (
            "A ANPD (Agência Nacional de Proteção de Dados) foi criada em 2018 (MP 869/2018, "
            "convertida na Lei 13.853/2019) como órgão da Presidência da República; tornou-se "
            "autarquia de natureza especial em 2022 (Lei 14.460) e agência reguladora em 2026 "
            "(Lei 15.352). A estrutura funcional começou a se formar com a posse do Conselho "
            "Diretor, em novembro de 2020. Em 2026, "
            "o Decreto 12.975 expandiu suas competências para fiscalizar o Marco Civil — "
            "movimento que transforma a ANPD de autoridade de dados em autoridade digital."
        ),
        "camadas": [
            {
                "titulo": "O modelo europeu e a diferença brasileira",
                "analise": (
                    "O GDPR (2016) criou autoridades supervisoras nacionais com independência "
                    "e recursos. A ANPD nasceu subordinada à Presidência da República — "
                    "tensão com o princípio da independência regulatória. A expansão de "
                    "competências via decreto (não via lei) replica o problema estrutural: "
                    "regulação robusta sendo construída por instrumento frágil. "
                    "Glocal (global + local, Robertson, 1990s): o modelo europeu funciona "
                    "porque as autoridades de proteção de dados têm independência constitucional. "
                    "No Brasil, a autonomia foi construída por etapas: autarquia em 2022 e "
                    "agência reguladora em 2026 (Lei 15.352)."
                )
            }
        ],
        "prospectiva": {
            "12_meses": (
                "A ANPD vai editar regulamentos sobre IA generativa e decisões automatizadas "
                "— primeiro teste real de sua capacidade técnica e política."
            ),
            "36_meses": (
                "Se o PL 2.338/2023 for aprovado, a ANPD pode se tornar a autoridade "
                "regulatória de IA no Brasil — concentração de poder regulatório que "
                "replica o modelo europeu; o teste será se a autonomia de agência se traduz "
                "em independência efetiva."
            ),
            "lacuna_remanescente": (
                "Capacidade técnica: a ANPD não tem quadro de especialistas em IA e "
                "algoritmos para fiscalizar o que os decretos determinam. "
                "Problema estrutural não resolvido por nenhuma norma em tramitação."
            )
        }
    },
    {
        "id": "eca_digital_menores",
        "titulo": "ECA Digital — A Proteção de Menores como Consenso Raro",
        "normas_relacionadas": ["eca", "eca_digital", "lgpd"],
        "nivel_tensao": "baixo",
        "status": "vigente — implementação em curso",
        "sintese": (
            "O ECA Digital (Lei 15.211/2025) é um dos poucos casos de consenso legislativo "
            "no direito digital brasileiro — aprovado com amplo apoio, sem a polarização "
            "que bloqueou o PL das fake news. A proteção de menores em ambiente digital "
            "é o terreno onde diferentes atores políticos, governo e oposição, plataformas e "
            "reguladores encontraram denominador comum."
        ),
        "camadas": [
            {
                "titulo": "Por que o consenso foi possível aqui",
                "analise": (
                    "A proteção de crianças é um dos poucos valores que transcende "
                    "a polarização política — nenhum ator político se beneficia de "
                    "aparecer como defensor de plataformas que expõem menores. "
                    "O ECA Digital contrasta com o PL das fake news: o tema dos menores "
                    "reuniu apoio que a moderação de conteúdo político não reuniu."
                ),
                "hipotese": (
                    "As plataformas de grande porte teriam aceitado o ECA Digital como troca "
                    "implícita: regras claras sobre menores em troca de não regulação mais ampla "
                    "de conteúdo para adultos, porque a lei não ameaça o modelo de negócio da "
                    "mesma forma que a moderação de conteúdo político ameaçaria. Não há "
                    "evidência documental de negociação nesse sentido."
                )
            }
        ],
        "prospectiva": {
            "12_meses": (
                "Fiscalização efetiva começa em 2026 — o teste real é se as plataformas "
                "implementam a verificação de idade e o design protegido. "
                "Precedente internacional: o UK Children's Code (2021) levou 2 anos "
                "para ter efeito real."
            ),
            "36_meses": (
                "O ECA Digital pode se tornar o modelo para legislação regional na "
                "América Latina — primeiro diploma abrangente de proteção digital "
                "de menores da região."
            ),
            "lacuna_remanescente": (
                "Verificação de idade efetiva sem violar privacidade — problema técnico "
                "não resolvido em nenhum ordenamento do mundo. "
                "A lei exige o resultado mas não prescreve a tecnologia."
            )
        }
    },
    {
        "id": "magnifica_humanitas_vaticano",
        "titulo": "Magnifica Humanitas — O Vaticano como Ator Normativo Global em IA",
        "normas_relacionadas": ["magnifica_humanitas", "pl_ia", "decreto_12975_2026"],
        "nivel_tensao": "estratégico",
        "status": "ativo — maio/2026",
        "sintese": (
            "A encíclica Magnifica Humanitas (Leão XIV, 25/05/2026) posiciona a Igreja "
            "Católica como ator normativo global no debate sobre IA — não apenas ético, "
            "mas com capacidade de influenciar legisladores em 1,3 bilhão de católicos "
            "globalmente, incluindo o Brasil (cerca de 57% da população, Censo 2022 do IBGE)."
        ),
        "camadas": [
            {
                "titulo": "Convergência histórica de maio/2026",
                "analise": (
                    "Entre 20 e 27 de maio de 2026, três instâncias independentes "
                    "convergiram no mesmo campo normativo: (1) Executivo brasileiro — "
                    "Decretos 12.975 e 12.976/2026; (2) Vaticano — Magnifica Humanitas; "
                    "(3) Congresso — 27 PDLs (base da Camara, 15/08/2026) para derrubar os decretos. "
                    "A convergência Vaticano-Executivo e a divergência Congresso-STF "
                    "mapeiam o campo de forças: de um lado, atores que priorizam "
                    "proteção de direitos fundamentais; de outro, atores que priorizam "
                    "liberdade de expressão e não-interferência estatal. "
                    "A presença de Chris Olah (Anthropic) no lançamento da encíclica "
                    "sinaliza que as empresas de IA reconhecem o Vaticano como "
                    "interlocutor normativo relevante — não apenas moral."
                )
            },
            {
                "titulo": "Rerum Novarum → Magnifica Humanitas: o arco de 135 anos",
                "analise": (
                    "Leão XIII / Rerum Novarum (1891): a Igreja entrou no debate sobre "
                    "as condições de trabalho na Revolução Industrial — quando o Estado "
                    "e o mercado ainda não tinham vocabulário para discutir dignidade "
                    "do trabalhador. "
                    "Leão XIV / Magnifica Humanitas (2026): a Igreja entra no debate sobre "
                    "IA quando o Estado e o mercado ainda não têm vocabulário consolidado "
                    "para discutir dignidade na era digital."
                ),
                "hipotese": (
                    "A Rerum Novarum teria influenciado a legislação trabalhista do século XX, "
                    "inclusive a CLT brasileira (1943) — relação sustentada por parte da "
                    "historiografia, não demonstrada aqui. Se o padrão se repetir, a encíclica "
                    "influenciará a legislação de IA nas próximas duas décadas, especialmente "
                    "em países de maioria católica como o Brasil."
                )
            }
        ],
        "prospectiva": {
            "12_meses": (
                "O PL 2.338/2023 (Marco Legal da IA) pode incorporar linguagem da "
                "Magnifica Humanitas sobre dignidade humana como limite da IA — "
                "especialmente se parlamentares católicos forem relatores."
            ),
            "36_meses": (
                "A encíclica pode se tornar referência doutrinária nos debates da ONU "
                "sobre governança global de IA — o Vaticano tem status de observador "
                "permanente e capacidade de mobilizar coalizões de países."
            ),
            "lacuna_remanescente": (
                "A encíclica diagnostica sem prescrever tecnicamente — não define "
                "o que é 'IA desarmada' em termos jurídicos operacionais. "
                "A ponte entre o princípio moral e a norma técnica é o trabalho "
                "que o PL 2.338/2023 precisa fazer."
            )
        }
    },
    {
        "id": "redata_gas_natural",
        "titulo": "REDATA e Gás Natural — Quem Define 'Baixa Emissão'",
        "normas_relacionadas": ["lei_15504_2026", "cf88", "pl_ia"],
        "nivel_tensao": "estratégico",
        "status": "lei vigente desde 15/09/2026 — regulamento das fontes de energia pendente",
        "sintese": (
            "A Lei 15.504/2026 condiciona o REDATA (Regime Especial de Tributação "
            "para Serviços de Datacenter) ao suprimento elétrico integral por fontes "
            "'renováveis ou de baixa emissão, na forma de regulamento'. A lei não diz "
            "se o gás natural cabe nessa expressão. A decisão foi transferida do "
            "Congresso para o Executivo — e, dentro do Executivo, ficou entre dois "
            "ministérios com leituras opostas."
        ),
        "camadas": [
            {
                "titulo": "Tensão 1 — Uma expressão aberta como ponto de decisão",
                "analise": (
                    "No Senado, a exigência passou de fontes 'renováveis ou limpas' para "
                    "'renováveis ou de baixa emissão' (Lei 11.196/2005, art. 11-B, § 1º, III, "
                    "na redação da Lei 15.504/2026). A troca não resolveu o conteúdo: deslocou-o. "
                    "Quem regulamentar 'baixa emissão' decide, na prática, quais projetos "
                    "acessam a desoneração. Diagnóstico: o vetor decisivo do regime não está "
                    "na lei, está no decreto e na portaria interministerial que ainda virão."
                )
            },
            {
                "titulo": "Tensão 2 — Fazenda e Minas e Energia: duas métricas para o mesmo megawatt",
                "analise": (
                    "O Ministério de Minas e Energia (MME) defende a inclusão do gás natural "
                    "como fonte firme que compensa a intermitência de eólica e solar e, segundo "
                    "o ministério, classificada pela Agência Internacional de Energia (IEA — "
                    "International Energy Agency) como combustível de transição. O Ministério "
                    "da Fazenda ancora-se na Taxonomia Sustentável Brasileira, que não "
                    "enquadra o gás, e admite inclusão apenas com captura de carbono "
                    "(CCUS — Carbon Capture, Utilization and Storage) ou compensação por "
                    "créditos. Os dois argumentos são internamente coerentes: um mede "
                    "confiabilidade de suprimento, o outro mede intensidade de carbono. "
                    "O regulamento terá de escolher a métrica ou combiná-las."
                )
            },
            {
                "titulo": "Tensão 3 — Federação e território: o gás como política regional",
                "analise": (
                    "Governos de Sergipe e do Amazonas, estados com oferta de gás, enviaram "
                    "ofícios à Presidência pedindo critérios de desempenho ambiental e "
                    "energético em vez de exclusão prévia de tecnologias. Em Sergipe, o "
                    "debate está ligado a um complexo de data centers projetado para a Zona "
                    "de Processamento de Exportação (ZPE) e à oferta do projeto Sergipe Águas "
                    "Profundas. A lei já reduz em 20% os compromissos de mercado interno e "
                    "P&D nas regiões Norte, Nordeste e Centro-Oeste (art. 11-B, § 7º): a "
                    "política regional está no texto; a energética, ainda não."
                )
            },
            {
                "titulo": "Tensão 4 — Três lentes sobre o mesmo incentivo",
                "analise": (
                    "Direito Econômico: o REDATA é instrumento de política econômica e deve "
                    "ser lido à luz da ordem econômica constitucional, que inclui a defesa do "
                    "meio ambiente entre seus princípios (CF, art. 170, VI). "
                    "Análise Econômica do Direito: a escolha da fonte altera custo de capital, "
                    "risco de ativo encalhado e atratividade relativa entre regiões — "
                    "incentivos mal calibrados selecionam projetos pelo preço imediato do "
                    "megawatt-hora. Direito e Economia Política: a definição de 'baixa "
                    "emissão' distribui capacidade de computar entre territórios e cadeias "
                    "de suprimento; não é escolha técnica neutra, é alocação de poder "
                    "econômico mediada por regulamento. As três lentes não se excluem: "
                    "a primeira dá o parâmetro, a segunda mede o efeito, a terceira "
                    "pergunta quem ganha capacidade."
                )
            }
        ],
        "prospectiva": {
            "12_meses": (
                "Edição do decreto e da portaria interministerial. Cenários: (a) exclusão "
                "do gás, com risco de reação legislativa — há sinalização de projeto de "
                "decreto legislativo no Senado; (b) inclusão condicionada a CCUS ou "
                "créditos de carbono; (c) critério de desempenho por intensidade de "
                "emissões, neutro quanto à tecnologia. Nova composição do governo após "
                "as eleições de outubro/2026 pode reabrir a arbitragem."
            ),
            "36_meses": (
                "Habilitações no regime revelarão a geografia efetiva dos data centers. "
                "O teste será se as contrapartidas (10% mercado interno, 2% P&D, eficiência "
                "hídrica) produzem acesso nacional a capacidade computacional ou apenas "
                "capacidade instalada para exportação de serviços."
            ),
            "lacuna_remanescente": (
                "A lei não define método de cálculo de emissões (direta, ciclo de vida, "
                "por contrato ou por hora de consumo) nem prazo de transição. Sem isso, "
                "'baixa emissão' permanece categoria política, não parâmetro verificável."
            )
        }
    },
    {
        "id": "minerais_criticos_valor_territorio",
        "titulo": "Minerais Críticos — Valor no Território",
        "normas_relacionadas": ["lei_15506_2026", "decreto_13118_2026", "cf88", "lei_15504_2026"],
        "nivel_tensao": "estratégico",
        "status": "lei vigente desde 16/09/2026 — CIMCE instalado, lista de minerais e FGAM pendentes",
        "sintese": (
            "A Lei 15.506/2026 desloca a política mineral da extração para o beneficiamento, "
            "o refino e a transformação no País. O instrumento decisivo não é o incentivo: "
            "é o CIMCE (Conselho Nacional para Industrialização de Minerais Críticos e "
            "Estratégicos), que homologa mudança de controle societário e participação "
            "estrangeira relevante em titulares de direitos minerários."
        ),
        "camadas": [
            {
                "titulo": "Tensão 1 — Incentivo anunciado versus incentivo disponível",
                "analise": (
                    "Três instrumentos costumam ser somados no debate público e não devem ser. "
                    "O FGAM (Fundo Garantidor da Atividade Mineral) admite participação da União "
                    "até R$ 2 bilhões, mas não havia sido capitalizado até 30/09/2026. O PFMCE "
                    "(crédito fiscal ao beneficiamento) tem teto de R$ 1 bilhão por ano entre 2030 "
                    "e 2034 — crédito futuro, não caixa. A chamada BNDES–Finep, anterior à lei, selecionou em junho "
                    "de 2025 56 planos de negócios que somam R$ 45,8 bilhões em investimentos "
                    "previstos — valor dos planos, não recurso público contratado; a chamada "
                    "disponibilizou inicialmente até R$ 5 bilhões em instrumentos financeiros, "
                    "montante distinto do teto do PFMCE. Diagnóstico: no curto prazo, o canal "
                    "em operação é o dos bancos de fomento; a lei estrutura o médio prazo."
                )
            },
            {
                "titulo": "Tensão 2 — Capital estrangeiro e soberania: o primeiro caso-teste",
                "analise": (
                    "Em 30/09/2026 a australiana Lynas Rare Earths anunciou acordo para adquirir "
                    "a Meteoric Resources, dona do Projeto Caldeira (Caldas, MG), em operação "
                    "estimada em R$ 3,5 bilhões, com plano de avaliar a separação de terras raras "
                    "no Brasil. A operação combina os elementos que a lei submete ao CIMCE: "
                    "mudança de controle, capital estrangeiro e mineral estratégico, antes de haver "
                    "decreto específico sobre o rito de triagem. O caso definirá se a triagem opera como filtro de "
                    "segurança ou como instrumento de negociação de contrapartidas industriais."
                )
            },
            {
                "titulo": "Tensão 3 — Rastreabilidade como condição de eficácia",
                "analise": (
                    "A lei cria sistema de rastreabilidade da origem à reciclagem, com registro "
                    "obrigatório de transações, licença ambiental e outorga mineral (art. 44). "
                    "Sem integração entre ANM (Agência Nacional de Mineração), fiscalização "
                    "aduaneira e cadeia formal, lista de minerais e incentivos atuam sobre a parte "
                    "visível do mercado."
                )
            },
            {
                "titulo": "Tensão 4 — Da mina ao data center",
                "analise": (
                    "Minerais críticos e data centers são elos da mesma cadeia de capacidade "
                    "computacional. A PNMCE e o REDATA usam a mesma técnica — incentivo fiscal "
                    "condicionado a contrapartidas no território — e enfrentam o mesmo teste: "
                    "produzir capacidade decisória nacional, não apenas volume físico instalado."
                )
            }
        ],
        "prospectiva": {
            "12_meses": (
                "Publicação da lista oficial de minerais pelo CIMCE; decreto de triagem de "
                "operações; decisão sobre Lynas–Meteoric; regulamentação do FGAM e do Certificado "
                "Mineral de Baixo Carbono. O calendário eleitoral de outubro/2026 é variável de "
                "risco regulatório."
            ),
            "36_meses": (
                "O indicador de sucesso é a primeira planta de separação ou refino de terras raras "
                "em operação no País, não o volume de reservas anunciado."
            ),
            "lacuna_remanescente": (
                "A lei não define critérios objetivos para a homologação de operações "
                "estrangeiras; até o decreto de triagem, a discricionariedade do CIMCE é ampla."
            )
        }
    },
    {
        "id": "tres_acordos_tres_velocidades",
        "titulo": "Três Acordos, Três Velocidades — Mercosul com Singapura, EFTA e União Europeia",
        "natureza": "Leitura analítica do Lexiograph sobre fatos verificados em fonte primária — não é fonte normativa.",
        "normas_relacionadas": ["acordo_mercosul_singapura", "acordo_mercosul_efta", "acordo_mercosul_ue_ita",
                                "tratado_assuncao_1991", "convencao_viena_1969", "cf88"],
        "matriz_vigencia": ["acordo_mercosul_singapura", "acordo_mercosul_efta", "acordo_mercosul_ue_ita"],
        "nivel_tensao": "estratégico",
        "status": "em implementação — matriz de vigência verificada em 01/10/2026",
        "sintese": (
            "Em 2026 o Brasil passou a operar três acordos comerciais externos do Mercosul, "
            "cada um em um estágio jurídico diferente: um em vigor, um em vigor apenas com "
            "parte dos parceiros e um em aplicação provisória, ainda sem entrada em vigor. "
            "A pergunta empresarial deixa de ser 'o acordo existe?' e passa a ser 'vale para "
            "este produto, neste destino, nesta data?'."
        ),
        "camadas": [
            {
                "titulo": "Tensão 1 — Três estágios jurídicos",
                "analise": (
                    "Singapura: em vigor para o Brasil desde 01/08/2026 (Decreto 13.081/2026). "
                    "EFTA: em vigor para o Brasil desde 01/10/2026, mas, segundo a própria EFTA, "
                    "apenas com a Islândia; Noruega, Suíça, Liechtenstein e os demais sócios do "
                    "Mercosul seguem pendentes (Decreto 13.126/2026). União Europeia: o Acordo "
                    "Provisório de Comércio (ITA) é aplicado provisoriamente desde 01/05/2026 e "
                    "ainda não entrou em vigor (Decreto 12.953/2026, art. 23); o Acordo de Parceria "
                    "(EMPA) é instrumento distinto. Diagnóstico: 'vigente' deixou de ser um atributo "
                    "binário — exige matriz por Parte."
                )
            },
            {
                "titulo": "Tensão 2 — Aplicação provisória e a reserva brasileira",
                "analise": (
                    "O Brasil ratificou a Convenção de Viena com reserva ao art. 25, que trata da "
                    "aplicação provisória de tratados. No caso do ITA, a aplicação provisória começou "
                    "depois da aprovação pelo Congresso (Decreto Legislativo 14/2026). A prática "
                    "preserva o controle parlamentar e, ao mesmo tempo, permite antecipar efeitos "
                    "comerciais enquanto o acordo não entra em vigor."
                )
            },
            {
                "titulo": "Tensão 3 — Fronteira de observabilidade",
                "analise": (
                    "Nos três casos, a aprovação parlamentar ocorreu por projeto de decreto "
                    "legislativo, etapa que o Radar Legislativo capta. A promulgação por decreto "
                    "presidencial e a vigência para cada parceiro estrangeiro ocorrem fora do "
                    "Congresso — no Diário Oficial e nas fontes oficiais das contrapartes — e "
                    "entram no Lexiograph por curadoria."
                )
            },
            {
                "titulo": "Tensão 4 — Preferência tarifária não é exportação",
                "analise": (
                    "A redução tarifária abre acesso, mas a utilização depende de regra de origem, "
                    "prova de origem, habilitação sanitária, logística e escala de fornecimento. "
                    "O indicador relevante é a taxa de utilização das preferências, não o número "
                    "de linhas tarifárias liberalizadas. Do ponto de vista de soberania, os três "
                    "acordos diversificam parceiros (Sudeste Asiático, EFTA e UE) sem alterar, por "
                    "si, a capacidade produtiva doméstica."
                )
            }
        ],
        "prospectiva": {
            "12_meses": (
                "01/11/2026: início previsto Brasil–Noruega (MDIC) e Argentina–Singapura "
                "(anunciado por Singapura). Suíça: aprovação parlamentar em 16/09/2026, com "
                "referendo anunciado. União Europeia: entrada em vigor do ITA depende das "
                "notificações do art. 23.2; EMPA segue rito próprio."
            ),
            "36_meses": (
                "Dados de comércio por produto permitirão medir a utilização das preferências e "
                "identificar setores que efetivamente se beneficiaram."
            ),
            "lacuna_remanescente": (
                "As relações entre os capítulos de comércio eletrônico e a LGPD, e entre o acordo "
                "com a UE e a PNMCE, dependem de leitura textual dos capítulos e não foram "
                "registradas como arestas."
            )
        }
    }
]

# ---- Epistemologia do direito ----
EPISTEMOLOGIA = {
    "introducao": (
        "O Lex-IO-Graph faz uma interseção que nenhum app jurídico articula: "
        "hermenêutica geral, teoria do conhecimento e direito positivo como camadas "
        "de um mesmo sistema. O grafo não é apenas mapa normativo — é instrumento "
        "de Verstehen jurídico (compreensão, Dilthey, 1833–1911) e não apenas "
        "de Erklären (explicação — ciências naturais). Essa distinção epistemológica "
        "é o fundamento do valor do Lex-IO-Graph."
    ),
    "arco_epistemologico": [
        {
            "autor": "Friedrich Schleiermacher",
            "datas": "1768–1834",
            "contribuicao": "Fundador da hermenêutica moderna como disciplina geral — antes da aplicação ao direito. O círculo hermenêutico: compreender o todo pelo parte e a parte pelo todo. A interpretação como diálogo entre intérprete e texto.",
            "conexao_direito": "Base de toda hermenêutica jurídica subsequente — o texto legal como texto a ser compreendido, não apenas aplicado mecanicamente"
        },
        {
            "autor": "Wilhelm Dilthey",
            "datas": "1833–1911",
            "contribuicao": "Distinção entre Erklären (explicar — ciências naturais) e Verstehen (compreender — ciências do espírito). O direito pertence ao domínio do Verstehen: normas não se explicam como fenômenos físicos, compreendem-se como expressões de vida histórica.",
            "conexao_direito": "Fundamenta a impossibilidade de uma ciência jurídica puramente positivista — o direito exige compreensão histórica e cultural, não apenas lógica formal"
        },
        {
            "autor": "Hans-Georg Gadamer",
            "datas": "1900–2002",
            "contribuicao": "Verdade e Método (1960): fusão de horizontes — intérprete e texto se transformam mutuamente. O preconceito (Vorurteil) como condição de compreensão, não obstáculo. A tradição como horizonte que possibilita o novo.",
            "conexao_direito": "Mutações constitucionais do STF como fusão de horizontes — CF/88 de 1988 compreendida à luz de 2026; a tradição como possibilidade, não prisão"
        },
        {
            "autor": "Jürgen Habermas",
            "datas": "1929–",
            "contribuicao": "Teoria da ação comunicativa (1981): a legitimidade do direito deriva de procedimento discursivo racional — a norma é válida se derivada de processo em que todos os afetados puderam participar em condições de igualdade.",
            "conexao_direito": "Fundamenta o processo legislativo participativo do Marco Civil da Internet (2009–2014) — construído via plataforma online com participação da sociedade civil; e questiona a legitimidade dos Decretos 12.975/2026 (não passaram pelo debate habermasiano)"
        },
        {
            "autor": "Ronald Dworkin",
            "datas": "1931–2013",
            "contribuicao": "O Império do Direito (1986): o direito como romance em cadeia — cada decisão judicial continua a narrativa anterior mantendo coerência de princípios. Distinção regras/princípios. A integridade como virtude do sistema jurídico.",
            "conexao_direito": "STF Tema 987 como romance em cadeia: continuidade interpretativa dos direitos fundamentais, não ruptura arbitrária — o juiz como co-autor de uma narrativa coletiva"
        }
    ],
    "arco_ontologico": [
        {
            "posicao": "Direito Natural Clássico",
            "autores": "Aristóteles (384–322 a.C.), Cícero (106–43 a.C.), São Tomás de Aquino (1225–1274)",
            "tese": "Existe uma ordem jurídica natural, anterior e superior ao direito positivo, derivada da natureza humana ou da razão divina. A lei positiva injusta não é lei — lex iniusta non est lex (Agostinho/Tomás).",
            "relevancia_brasil": "Influência na CF/88 via jusnaturalismo constitucional — os direitos fundamentais como direitos naturais positivados; a dignidade humana (art. 1º, III) como valor suprapositivo"
        },
        {
            "posicao": "Direito Natural Contemporâneo",
            "autores": "Lon Fuller (1902–1978), John Finnis (1940–)",
            "tese": "Fuller (A Moralidade do Direito, 1964): a lei precisa satisfazer critérios mínimos de moralidade interna — generalidade, publicidade, não retroatividade, clareza, não contradição — para ser válida. Finnis (Lei Natural e Direitos Naturais, 1980): direito natural como fundamento dos direitos humanos sem recorrer à teologia.",
            "relevancia_brasil": "Os decretos 12.975 e 12.976/2026 violam o critério fullerniano de publicidade processual — foram editados sem debate parlamentar prévio. A 'moralidade interna do direito' como critério crítico dos decretos."
        },
        {
            "posicao": "Positivismo Jurídico",
            "autores": "Jeremy Bentham (1748–1832), John Austin (1790–1859), Hans Kelsen (1881–1973), H.L.A. Hart (1907–1992)",
            "tese": "O direito é o que é, não o que deveria ser. Separação radical entre direito e moral. A validade da norma deriva da conformidade com o procedimento de criação, não do conteúdo.",
            "relevancia_brasil": "Base do controle de constitucionalidade do STF — a norma é inválida se violou o procedimento constitucional, não se é 'injusta'. Kelsen como fundamento da hierarquia normativa brasileira."
        },
        {
            "posicao": "Teoria Tridimensional do Direito",
            "autores": "Miguel Reale (1910–2006)",
            "tese": "O direito é simultaneamente fato (dimensão sociológica), valor (dimensão axiológica) e norma (dimensão normativa). A síntese brasileira que recusa a exclusão entre natural e positivo — o valor está na norma, não fora dela.",
            "relevancia_brasil": "Miguel Reale foi o principal redator do CC/2002 — a teoria tridimensional está no Código Civil brasileiro. A função social do contrato e da propriedade como valores incorporados à norma. O contemporâneo não vê exclusão entre natural e positivo — é camada de diálogo."
        }
    ],
    "arco_metodologico": [
        {
            "periodo": "Glosadores de Bolonha (séc. XI–XIII)",
            "figura_central": "Irnerius (c.1050–1130) — fundador; Acúrsio (†1263) — Glossa Ordinaria",
            "metodo": "Ressurreição do Corpus Iuris Civilis de Justiniano (533 d.C.) — comentário linha por linha do texto romano. Glosa marginal e interlinear. Método idêntico ao Talmude — não coincidência: Bolonha e Sicília (séc. XI–XIII) eram espaços de diálogo entre tradições jurídicas judaica, islâmica e cristã.",
            "conexao_pancronica": "Os glosadores operavam na mesma época e nos mesmos espaços que Maimônides (1135–1204) escrevia o Mishné Torá e Averróis (1126–1198) comentava Aristóteles. A hermenêutica jurídica ocidental compartilha epistemologia com as tradições judaica e islâmica — glosa, comentário, comentário do comentário."
        },
        {
            "periodo": "Comentadores / Pós-glosadores (séc. XIV–XV)",
            "figura_central": "Bártolo de Sassoferrato (1313–1357), Baldo degli Ubaldi (1327–1400)",
            "metodo": "Superação da glosa pura — aplicação do direito romano ao direito local (statuta). Primeiro método comparatístico: como o direito romano geral se relaciona com o direito particular da cidade? Antecipação do direito comparado glocal (global + local, Robertson, 1990s).",
            "conexao_pancronica": "Bártolo é o precursor do direito internacional privado — quid iuris quando dois estatutos conflitam? O problema de Bártolo no séc. XIV é o problema da LGPD e do GDPR no séc. XXI: qual lei aplica quando o dado cruza fronteiras?"
        },
        {
            "periodo": "Pandectistas alemães (séc. XIX)",
            "figura_central": "Savigny (1779–1861), Ihering (1818–1892), Windscheid (1817–1892)",
            "metodo": "Sistematização científica do direito romano — a Pandektenwissenschaft. O direito como ciência com conceitos gerais, dogmática rigorosa, sistema fechado. Base do BGB alemão (1896) que influenciou o CC/1916 brasileiro.",
            "conexao_pancronica": "Os pandectistas construíram a dogmática que Kelsen formalizou — a hierarquia normativa como sistema fechado é produto do séc. XIX alemão, não do direito romano. O positivismo jurídico é historicamente situado, não universal."
        },
        {
            "periodo": "Codificadores modernos (séc. XIX–XX)",
            "figura_central": "Napoleão (Code Civil, 1804), Clóvis Beviláqua (CC/1916), Miguel Reale (CC/2002)",
            "metodo": "Transposição da dogmática para código — o direito como sistema positivo escrito, completo, acessível. A codificação como projeto político de modernização e unificação nacional.",
            "conexao_pancronica": "O CC/2002 de Reale é o último grande código brasileiro — o PL 4/2025 (Livro VI Digital) é o primeiro pós-digital. A codificação como projeto político continua: agora o objeto é o ambiente digital."
        }
    ]
}

# ---- Direito natural no diálogo doutrinário ----
DIREITO_NATURAL = {
    "introducao": (
        "O contemporâneo não vê exclusão entre direito natural e direito positivo — "
        "é mais uma camada de diálogo. A tradição tomista, o jusnaturalismo moderno "
        "e a teoria tridimensional de Reale (1910–2006) convergem: o valor está na "
        "norma, não fora dela. O direito positivo que viola princípios fundamentais "
        "de dignidade não é apenas injusto — é norma de eficácia questionável "
        "(Fuller, 1902–1978)."
    ),
    "autores_chave": [
        {
            "nome": "São Tomás de Aquino",
            "datas": "1225–1274",
            "tese": "Lex iniusta non est lex — a lei injusta não é lei. Quatro tipos de lei: eterna (razão divina), natural (participação humana na lei eterna), humana (derivada da natural) e divina (revelada). A lei positiva é válida se derivada da lei natural.",
            "relevancia": "Fundamento do jusnaturalismo ocidental — influência direta na CF/88 via direitos fundamentais como direitos naturais positivados"
        },
        {
            "nome": "Lon Fuller",
            "datas": "1902–1978",
            "obra": "A Moralidade do Direito (The Morality of Law), 1964",
            "tese": "8 critérios de moralidade interna do direito: generalidade, publicidade, não retroatividade, clareza, não contradição, possibilidade de cumprimento, estabilidade, congruência entre norma e aplicação. Lei que viola sistematicamente esses critérios não é lei — é fracasso do projeto jurídico.",
            "relevancia": "Critério crítico dos Decretos 12.975 e 12.976/2026 — editados sem publicidade processual adequada (debate parlamentar). Também critério para o PL 2.338/2023 sobre transparência algorítmica."
        },
        {
            "nome": "John Finnis",
            "datas": "1940–",
            "obra": "Lei Natural e Direitos Naturais (Natural Law and Natural Rights), 1980",
            "tese": "Direito natural sem teologia — 7 bens humanos básicos (vida, conhecimento, jogo, experiência estética, sociabilidade, razoabilidade prática, religião) como fundamento dos direitos humanos. A dignidade humana como dado da razão prática, não da fé.",
            "relevancia": "Fundamenta a Magnifica Humanitas de Leão XIV (2026) sem recorrer à teologia — a dignidade humana como limite da IA é argumento de razão prática, acessível a crentes e não-crentes"
        },
        {
            "nome": "Miguel Reale",
            "datas": "1910–2006",
            "obra": "Teoria Tridimensional do Direito, 1968",
            "tese": "O direito é simultaneamente fato, valor e norma — síntese que recusa tanto o positivismo puro (só norma) quanto o jusnaturalismo puro (só valor). O valor está imanente na norma, não transcendente a ela.",
            "relevancia": "Principal redator do CC/2002 — a teoria tridimensional está no Código Civil brasileiro. A função social do contrato (art. 421) e da propriedade como valores incorporados à norma positiva."
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# CASOS NOVOS — Sprint 12
# ─────────────────────────────────────────────────────────────────────────────

CASO_ANPD_JUDICIARIO = {
    "id": "anpd_nao_vincula_judiciario",
    "titulo": "ANPD não vincula o Judiciário — o iceberg normativo",
    "subtitulo": "Compliance administrativo não é blindagem jurídica",
    "area": "direito digital, direito administrativo, direito civil",
    "normas": ["lgpd", "cf88", "marco_civil", "decreto_12975_2026"],
    "tensoes": [
        {
            "titulo": "Tensão 1 — ANPD: regulação administrativa, não jurisdição",
            "descricao": (
                "A ANPD (Agência Nacional de Proteção de Dados) é agência reguladora federal (Lei 15.352/2026), autarquia de natureza especial prevista "
                "na LGPD (Lei 13.709/2018, art. 55-A; competências no art. 55-J) com competências administrativas: "
                "regulamentar, fiscalizar, orientar e aplicar sanções. "
                "Suas decisões não possuem efeito vinculante sobre o Poder Judiciário. "
                "O art. 5º, XXXV, CF/88 — inafastabilidade da jurisdição — garante que "
                "nenhum ato administrativo cria porto seguro definitivo contra escrutínio judicial. "
                "Um juiz pode considerar a manifestação da ANPD como elemento técnico informativo, "
                "mas não está juridicamente obrigado a segui-la."
            )
        },
        {
            "titulo": "Tensão 2 — O Ministério Público age independentemente",
            "descricao": (
                "Direitos de crianças e adolescentes têm tutela constitucional qualificada "
                "(CF/88 art. 227 — prioridade absoluta). São direitos difusos: "
                "transindividuais, indivisíveis, de titularidade indeterminada. "
                "O MP (art. 129, III, CF/88) pode promover ação civil pública para proteção "
                "de interesses difusos e coletivos independentemente de qualquer decisão prévia da ANPD. "
                "Compliance com a LGPD reduz riscos — não elimina responsabilidade judicial."
            )
        },
        {
            "titulo": "Tensão 3 — O iceberg normativo: a ANPD é a parte visível",
            "descricao": (
                "A ANPD, como toda agência reguladora, opera em nível administrativo infralegal: "
                "não cria lei, não reinterpreta a Constituição de forma definitiva, não exerce jurisdição, "
                "não produz coisa julgada. É a ponta do iceberg. "
                "O volume submerso: CF/88, leis formais, princípios gerais do direito, "
                "controle judicial, atuação do Ministério Público, responsabilidade civil objetiva. "
                "Confundir regulação administrativa com encerramento jurídico do risco "
                "é o erro estratégico mais comum no discurso corporativo de compliance."
            )
        },
    ],
    "doutrina": [
        "Pontes de Miranda — distinção entre ilícito e responsabilidade civil (Tratado, 1954)",
        "CF/88 art. 5º, XXXV — inafastabilidade da jurisdição",
        "CF/88 art. 227 — prioridade absoluta dos direitos da criança",
        "CDC art. 81, par. único, I — conceito de direitos difusos",
    ],
    "prospectiva": (
        "O risco principal para compliance officers não é a ANPD — é a confusão institucional. "
        "Empresas que acreditam que 'estar em compliance' fecha o risco jurídico "
        "criam exatamente o que antecede crises reputacionais, judiciais e financeiras. "
        "A hierarquia real: ANPD regula, Judiciário decide, MP vela pelos direitos difusos."
    ),
    "fonte": "Gonçalves et Alii — Hubstry Deep Tech · guilhermemachado.ceo@hubstry.dev",
}

CASO_PARADIGMA_PREVENTIVO = {
    "id": "paradigma_preventivo_inibitorio",
    "titulo": "Da Reparação à Prevenção — a mutação do ethos jurídico-regulatório",
    "subtitulo": "Compliance by design como vetor jurídico, econômico e estratégico",
    "area": "direito civil, direito digital, análise econômica do direito",
    "normas": ["cf88", "lgpd", "marco_civil", "stf_tema987", "pl_ia"],
    "tensoes": [
        {
            "titulo": "Tensão 1 — A crise do paradigma reparatório diante da IA",
            "descricao": (
                "O ordenamento brasileiro foi edificado sobre o princípio da reparação integral "
                "(restitutio in integrum) como eixo da responsabilidade civil. "
                "A premissa — que o dano pode ser reparado por equivalente pecuniário — "
                "torna-se epistemologicamente frágil diante dos riscos algorítmicos: "
                "Como reparar discriminação sistêmica por algoritmo de credit scoring? "
                "Como indenizar dano psíquico coletivo por amplificação de desinformação? "
                "Danos algorítmicos são massivos, difusos, opacos e frequentemente irreversíveis."
            )
        },
        {
            "titulo": "Tensão 2 — Pontes de Miranda: o ilícito é anterior ao dano",
            "descricao": (
                "Pontes de Miranda (Tratado de Direito Privado, 1954) estabelecia com rigor "
                "que o ato ilícito — a violação do dever jurídico — é categoria autônoma, "
                "logicamente anterior e ontologicamente independente do dano patrimonial. "
                "O dano gera o dever de indenizar, mas não é condição de existência do ilícito. "
                "Essa distinção, negligenciada pela prática forense, é central na era da IA: "
                "violação de transparência algorítmica, tratamento discriminatório automatizado, "
                "dark patterns — todos configuram ilícitos autônomos cuja tutela adequada é prevenção."
            )
        },
        {
            "titulo": "Tensão 3 — O paradigma preventivo como imperativo constitucional",
            "descricao": (
                "A convergência de múltiplos vetores aponta para o paradigma preventivo: "
                "reforma do Código Civil (nova redação do art. 186 — ilícito sem dano), "
                "STF Tema 987 (falha sistêmica — responsabilidade ex ante, não apenas ex post), "
                "ECA Digital (proibição de profiling de menores — tutela inibitória por natureza), "
                "PL 2338/2023 — AI Act brasileiro (abordagem baseada em risco — controle antes do deployment). "
                "Compliance by design, safety by default e governança algorítmica "
                "operam como vetor simultaneamente jurídico, econômico e estratégico."
            )
        },
    ],
    "doutrina": [
        "Pontes de Miranda — autonomia do ilícito (Tratado de Direito Privado, 1954)",
        "Calabresi — custos dos acidentes e eficiência alocativa (1970)",
        "Marinoni — tutela inibitória individual e coletiva (2012)",
        "Tepedino / Bodin de Moraes — constitucionalização do direito civil",
        "AI Act europeu — Regulamento UE 2024/1689",
    ],
    "prospectiva": (
        "Organizações que anteciparem a transição — incorporando compliance by design, "
        "auditorias algorítmicas e governança preventiva — estarão posicionadas para capturar "
        "os dividendos econômicos da confiança institucional. "
        "A prevenção não é apenas opção regulatória. É imperativo civilizatório. "
        "Para deep techs como a Hubstry, a consolidação do paradigma preventivo "
        "não representa ameaça — é oportunidade estrutural."
    ),
    "fonte": "Guilherme Gonçalves Machado — Founder & CEO, Hubstry Deep Tech · guilhermemachado.ceo@hubstry.dev",
}



# ---- Direito Econômico, AED e Direito e Economia Política ----
# Fontes consultadas diretamente: Blalock (2022), Harris e Varellas (2020),
# Easterbrook e Fischel (1991). Autores citados por meio delas usam "apud".
DIREITO_ECONOMIA = {
    "introducao": (
        "O grafo mostra como as normas se conectam. Esta seção trata de outra "
        "pergunta: como as normas constroem mercados — quem recebe incentivo, "
        "quem controla infraestrutura, quem regula dados. Três lentes respondem "
        "de modos diferentes, e o Lexiograph as usa como instrumentos de leitura, "
        "não como categorias normativas do grafo."
    ),
    "lentes": [
        {
            "nome": "Direito Econômico",
            "pergunta": "Como o direito organiza a economia concreta?",
            "foco": (
                "Normas, instituições, política industrial, concorrência e regulação "
                "como instrumentos que distribuem capacidade econômica. No Brasil, o "
                "parâmetro é a ordem econômica constitucional (CF, arts. 170 a 181)."
            ),
            "no_grafo": "REDATA (art. 170, VI e art. 174) · ANPD como agência reguladora (Lei 13.848/2019)",
        },
        {
            "nome": "Análise Econômica do Direito (AED)",
            "pergunta": "Que incentivos e custos a regra produz?",
            "foco": (
                "Regras alteram custos de transação, risco, entrada e alocação de recursos. "
                "Na formulação contratualista de Easterbrook e Fischel, a empresa é um "
                "'nexo de contratos', e o direito societário funciona como contrato-padrão: "
                "supre os termos que as partes teriam negociado se negociar cada contingência "
                "fosse barato — é 'habilitador, não diretivo' (EASTERBROOK; FISCHEL, 1991, p. 12, 15)."
            ),
            "no_grafo": "Contrapartidas do REDATA (10% mercado interno, 2% P&D) como desenho de incentivos",
        },
        {
            "nome": "Direito e Economia Política (LPE — Law and Political Economy)",
            "pergunta": "Quem ganha poder com a forma jurídica do mercado?",
            "foco": (
                "Mercados, empresas, contratos, propriedade e a própria moeda são "
                "'criaturas do direito e da política', não esferas anteriores ao Estado "
                "(HARRIS; VARELLAS, 2020, p. 5). A eficiência é informação relevante, "
                "mas não esgota perguntas sobre distribuição, poder e democracia."
            ),
            "no_grafo": "Plataformas e art. 19 do Marco Civil · dados pessoais como relação jurídica construída",
        },
    ],
    "genealogia_fonte": (
        "Genealogia proposta por Corinne Blalock (2022, p. 226-229) e por "
        "Harris e Varellas (2020, p. 8-10): a crítica jurídica norte-americana à "
        "separação entre política e economia aparece em três momentos, separados por "
        "longos períodos de esquecimento."
    ),
    "genealogia": [
        {
            "momento": "1. Realismo Jurídico Norte-Americano",
            "periodo": "décadas de 1920 e 1930",
            "autores": "Robert Hale, Morris Cohen",
            "contexto": (
                "Surge quando a desigualdade cresce e a concentração empresarial abala a "
                "crença num mercado competitivo descentralizado e 'natural' (HORWITZ, 1992 "
                "apud BLALOCK, 2022, p. 226)."
            ),
            "tese": (
                "O poder de barganha das partes no mercado não é natural: é afetado pela "
                "distribuição prévia de propriedade e de titularidades, criada pelo direito "
                "(HALE, 1923 apud BLALOCK, 2022, p. 226). A troca 'voluntária' pode esconder "
                "coerção. Por isso o Realismo contesta a divisão entre direito privado "
                "(contratos, propriedade, responsabilidade civil) e direito público."
            ),
            "destino": (
                "A crítica foi posta de lado pela Segunda Guerra, pelo New Deal e pela "
                "teoria do processo jurídico (HARRIS; VARELLAS, 2020, p. 8)."
            ),
        },
        {
            "momento": "2. Critical Legal Studies (CLS — Estudos Jurídicos Críticos)",
            "periodo": "décadas de 1970 e 1980",
            "autores": "Duncan Kennedy, Karl Klare",
            "contexto": (
                "Retoma o Realismo quando o debate jurídico estava centrado nos tribunais "
                "e na adjudicação de direitos da Suprema Corte."
            ),
            "tese": (
                "Todo direito privado — a propriedade, por exemplo — implica uma privação "
                "correspondente e é, portanto, regulação pública tanto quanto um tributo "
                "(KENNEDY, 1991 apud BLALOCK, 2022, p. 226). O direito é indeterminado e "
                "'é política'. Kennedy argumenta ainda que a economia neoclássica absorveu "
                "a dicotomia entre mercado livre e coerção estatal (HARRIS; VARELLAS, 2020, p. 8)."
            ),
            "destino": (
                "As críticas feminista e racial levaram à separação da Critical Race Theory "
                "e da teoria feminista do direito; a análise de classe saiu da conversa "
                "(BLALOCK, 2022, p. 227)."
            ),
        },
        {
            "momento": "3. Law and Political Economy (LPE — Direito e Economia Política)",
            "periodo": "a partir do fim dos anos 2000",
            "autores": "Angela Harris, Amy Kapczynski, K. Sabeel Rahman, Lina Khan",
            "contexto": (
                "Responde a três décadas de hegemonia do Law and Economics (AED) nas "
                "faculdades norte-americanas, associado a Coase, Director e Posner "
                "(BLALOCK, 2022, p. 227-228, 235). O movimento ClassCrits (2007) é uma "
                "das origens institucionais (HARRIS; VARELLAS, 2020, p. 10)."
            ),
            "tese": (
                "Recusa a separação entre política e economia. Mostra como a AED está "
                "incorporada à governança — por exemplo, na exigência de análise de "
                "custo-benefício para regulação federal e no padrão estreito de prova "
                "anticompetitiva no antitruste (BLALOCK, 2022, p. 229)."
            ),
            "destino": (
                "Agenda ativa: antitruste, regulação administrativa, tributação e o "
                "direito do capitalismo informacional (COHEN, 2019; PASQUALE, 2015 apud "
                "HARRIS; VARELLAS, 2020, p. 10)."
            ),
        },
    ],
    "contraponto": (
        "Contraponto necessário: a AED não é só o alvo da LPE. Em Easterbrook e Fischel "
        "(1991), a pergunta é por que o direito societário deixa decisões críticas à "
        "discricionariedade dos administradores e deixa a correção ao jogo de atores "
        "interessados, não a reguladores (p. 15). A resposta contratualista é uma "
        "hipótese testável sobre custos de transação; a resposta da LPE é uma pergunta "
        "sobre quem definiu os termos do contrato-padrão. O Lexiograph mantém as duas "
        "perguntas abertas."
    ),
    "leitura_lexiograph": [
        (
            "REDATA",
            "Direito Econômico dá o parâmetro (defesa do meio ambiente como princípio da "
            "ordem econômica); AED mede o efeito do critério de 'baixa emissão' sobre "
            "custo de capital e localização; LPE pergunta que territórios e cadeias de "
            "suprimento ganham capacidade de computar."
        ),
        (
            "ANPD",
            "Como agência reguladora, a ANPD é objeto do Direito Econômico da regulação. "
            "Para a AED, consentimento e transparência reduzem assimetria informacional; "
            "para a LPE, o 'dado pessoal' é relação jurídica construída, e a forma da "
            "regulação define quem extrai valor dele."
        ),
        (
            "Plataformas e art. 19",
            "A AED lê a responsabilidade de intermediários como alocação de custos de "
            "moderação; a LPE lê a mesma regra como distribuição de poder sobre a esfera "
            "pública — conexão com o antitruste de plataformas."
        ),
    ],
    "referencias": [
        "BLALOCK, Corinne. Introduction: law and the critique of capitalism. "
        "<em>The South Atlantic Quarterly</em>, Durham, v. 121, n. 2, p. 223-236, abr. 2022. "
        "DOI: 10.1215/00382876-9663562.",
        "EASTERBROOK, Frank H.; FISCHEL, Daniel R. <em>The economic structure of corporate "
        "law</em>. Cambridge, MA: Harvard University Press, 1991.",
        "HARRIS, Angela P.; VARELLAS, James J. Introduction: law and political economy in a "
        "time of accelerating crises. <em>Journal of Law and Political Economy</em>, Davis, "
        "v. 1, n. 1, p. 1-27, 2020. DOI: 10.5070/LP61150254.",
    ],
}


# ---- Soberania tecnológica ----
SOBERANIA = {
    "introducao": (
        "Soberania tecnológica não se mede pela localização do servidor nem pelo volume da "
        "reserva mineral. Mede-se pela capacidade verificável de decidir, operar, substituir "
        "e recuperar sistemas críticos. O vetor organiza normas e casos do Lexiograph por "
        "essa pergunta."
    ),
    "dimensoes": [
        ("Soberania de dados",
         "Onde estão os dados, sob qual jurisdição, com quais regras de acesso, retenção, "
         "transferência e proteção.",
         "LGPD · ANPD · Cloud Act (EUA, 2018), que alcança dados sob controle de provedores "
         "norte-americanos onde quer que estejam armazenados"),
        ("Soberania operacional",
         "Quem opera a infraestrutura, controla contas administrativas, detém chaves, monitora "
         "incidentes, executa recuperação e responde pela continuidade.",
         "REDATA (capacidade instalada não equivale a controle operacional) · resiliência: "
         "backup isolado, testes de restauração, plano de saída de fornecedor"),
        ("Soberania tecnológica",
         "Quem domina arquitetura, código, padrões, integrações, componentes críticos, "
         "formação técnica e capacidade de evolução.",
         "PNMCE (do minério ao refino) · PONTARIA (PL 1.074/2026, IA brasileira)"),
    ],
    "principio": (
        "Soberania sem isolamento: o critério não é que todos os componentes sejam nacionais, "
        "mas o grau de controle sobre dependências críticas — chaves, administração, "
        "jurisdição, suporte, licenciamento, portabilidade e recuperação."
    ),
    "fontes": [
        "As três dimensões seguem a formulação do debate público sobre a Nuvem Brasileira "
        "(MGI — Ministério da Gestão e da Inovação em Serviços Públicos; Serpro, "
        "'Soberania sem isolamento', 2026).",
        "A camada de resiliência operacional dialoga com GARTNER, apresentação de Leonardo "
        "Jardino e Hélio Mariano no Fórum RNP+ Tendências 2026.",
        "Leitura estendida no dossiê ODIN — A Arquitetura Brasileira de Inteligência Artificial.",
    ],
}
