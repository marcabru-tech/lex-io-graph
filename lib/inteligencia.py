"""
Camada de inteligência jurídico-estratégica do Lex-IO-Graph.

Vetor analítico: não apenas o fato normativo, mas o jogo de forças
institucional, civilizatório e geopolítico por trás de cada tensão.
Estilo: analítico de consultoria — diagnóstico, frio, acionável.
Evitar: teoria da dependência, tom acusatório, framing conspiratório,
fechamentos moralizantes. Fatos como diagnóstico estratégico e oportunidade.
"""

# ---- Casos de inteligência estratégica ----
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
                    "O Congresso Nacional não aprovou o PL 2.630/2020 (PL das fake news) "
                    "por pressão de parlamentares ligados a plataformas digitais e a setores "
                    "que se beneficiaram da ausência de regulação de plataformas "
                    "de 2018 e 2022. O vácuo não foi acidente — foi produto de vetos cruzados "
                    "entre atores com interesses incompatíveis. O STF, ante a omissão legislativa "
                    "e a urgência de 2025 (pré-eleitoral, ex-presidente indiciado por golpe de Estado "
                    "— PL 2.253/2024), declarou a inconstitucionalidade parcial e progressiva "
                    "do art. 19 (Tema 987, RE 1.037.396, jun./2025). O Executivo regulamentou "
                    "via Decretos 12.975 e 12.976/2026 (21/05/2026). "
                    "Diagnóstico: o judiciário e o executivo preencheram o vácuo que o "
                    "legislativo deixou deliberadamente — não por omissão técnica, mas por "
                    "bloqueio político estrutural."
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
                "titulo": "Tensão 3 — A reação legislativa: 27 PDLs (base da Camara, 15/08/2026) e o paradoxo da oposição",
                "analise": (
                    "A oposição (PL, Republicanos, União Brasil, Novo) protocolou 27 PDLs (base da Camara, 15/08/2026) "
                    "(Projetos de Decreto Legislativo) para derrubar os Decretos 12.975 e "
                    "12.976/2026 sob o argumento de censura e usurpação de competência normativa. "
                    "O paradoxo estratégico: a mesma oposição que bloqueou o PL das fake news "
                    "por anos — criando o vácuo que levou o STF a agir — agora acusa o STF e o "
                    "Executivo de ultrapassar seus limites. O Congresso que não legislou invoca "
                    "sua competência normativa contra quem legislou no vácuo que ele criou. "
                    "Ano eleitoral (outubro/2026) amplifica todas as tensões: cada PDL é "
                    "simultaneamente ato jurídico e peça de campanha."
                )
            },
            {
                "titulo": "Tensão 4 — O vetor geopolítico: plataformas globais e soberania regulatória",
                "analise": (
                    "O debate não é apenas doméstico. A suspensão do X (ex-Twitter) no Brasil "
                    "pelo STF (ago./2024) e o retorno após acordo (out./2024) inseriram o "
                    "Brasil no mapa global da regulação de plataformas. Elon Musk como ator "
                    "geopolítico relevante — proprietário de plataforma com alcance global "
                    "da direita europeia — transforma a regulação brasileira em front de uma "
                    "disputa global entre soberania regulatória dos Estados e poder privado "
                    "das plataformas. O Decreto 12.975/2026 é lido por críticos como "
                    "modelo de censura estatal; pelo governo brasileiro como modelo de "
                    "responsabilidade de plataformas. Duas narrativas incompatíveis, "
                    "ambas estrategicamente corretas para seus proponentes."
                )
            }
        ],
        "prospectiva": {
            "12_meses": (
                "Eleições outubro/2026: qualquer partido que vença terá que lidar com o vácuo "
                "legislativo sobre moderação de conteúdo. Se a direita vencer, pressão para "
                "revogar os decretos e restringir o STF. Se a esquerda mantiver o governo, "
                "pressão para legislar o que os decretos fizeram por decreto."
            ),
            "36_meses": (
                "O EU AI Act (2024) e o DSA (2022) europeus já provaram que regulação estatal "
                "de plataformas é viável sem censura — o Brasil pode seguir esse modelo via "
                "legislação, não via decreto. A janela estratégica para o Congresso legislar "
                "é 2027–2028, após as eleições de 2026."
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
            "A ANPD (Autoridade Nacional de Proteção de Dados) foi criada pela LGPD em 2018 "
            "como autarquia federal. Levou 3 anos para ter estrutura funcional. Em 2026, "
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
                    "No Brasil, a ANPD depende de vontade política do Executivo."
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
                "replica o modelo europeu mas sem a mesma independência institucional."
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
                    "As plataformas de grande porte aceitaram o ECA Digital como troca implícita: "
                    "regras claras sobre menores em troca de não regulação mais ampla "
                    "de conteúdo para adultos. O ECA Digital é o oposto do PL das fake news: "
                    "legislação possível porque não ameaça o modelo de negócio das plataformas "
                    "da mesma forma que a moderação de conteúdo político ameaçaria."
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
            "globalmente, incluindo o Brasil (65% da população)."
        ),
        "camadas": [
            {
                "titulo": "Convergência histórica de maio/2026",
                "analise": (
                    "Na semana de 21–27 de maio de 2026, três instâncias independentes "
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
                    "do trabalhador. O resultado: influência direta na legislação trabalhista "
                    "do século XX, incluindo a CLT brasileira (1943). "
                    "Leão XIV / Magnifica Humanitas (2026): a Igreja entra no debate sobre "
                    "IA quando o Estado e o mercado ainda não têm vocabulário consolidado "
                    "para discutir dignidade na era digital. "
                    "Vetor prospectivo: se o padrão histórico se repetir, a encíclica "
                    "influenciará legislação de IA nas próximas duas décadas — "
                    "especialmente em países de maioria católica como o Brasil."
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
                "A ANPD (Autoridade Nacional de Proteção de Dados) é autarquia especial criada "
                "pela LGPD (Lei 13.709/2018, art. 55-J) com competências administrativas: "
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
    "fonte": "Gonçalves et Alii — Hubstry Deep Tech · guilhermemachado@hubstry.onmicrosoft.com",
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
    "fonte": "Guilherme Gonçalves Machado — Founder & CEO, Hubstry Deep Tech · guilhermemachado@hubstry.onmicrosoft.com",
}

