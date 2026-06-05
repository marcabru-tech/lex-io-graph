"""
Camada hermenêutica e de fontes do direito do Lex-IO-Graph.

Sprint 6 — Hermenêutica, fontes do direito, arco histórico
do Código Civil brasileiro e Brasil Império como camada do ordenamento.

O Lex-IO-Graph faz a interseção que nenhum app jurídico articula:
hermenêutica geral, teoria do conhecimento e direito positivo
como camadas de um mesmo sistema de inteligência.
"""

# ---- Correntes hermenêuticas ----
CORRENTES_HERMENEUTICAS = [
    {
        "id": "historica",
        "nome": "Hermenêutica Histórica",
        "autor_principal": "Friedrich Carl von Savigny",
        "datas": "1779–1861",
        "obra": "Sistema do Direito Romano Atual (System des heutigen römischen Rechts), 1840",
        "principio": (
            "A lei deve ser interpretada pela intenção original do legislador "
            "e pelo espírito do povo (Volksgeist). O direito é produto orgânico "
            "da história de cada nação — não pode ser transplantado artificialmente."
        ),
        "metodos": [
            "Gramatical — sentido literal das palavras",
            "Lógico — estrutura interna do raciocínio jurídico",
            "Histórico — intenção original do legislador",
            "Sistemático — posição da norma no ordenamento"
        ],
        "critica": (
            "Ihering (1818–1892): o Volksgeist é uma ficção — o direito serve a fins "
            "sociais concretos, não a um espírito nacional abstrato. "
            "A hermenêutica histórica pode congelar o direito no passado."
        ),
        "no_brasil": (
            "Influência no CC/1916 de Clóvis Beviláqua. "
            "Interpretação originalista ainda presente na jurisprudência conservadora — "
            "especialmente em votos que invocam 'a vontade do constituinte originário' "
            "para resistir a mutações constitucionais."
        ),
        "tensao_norma": "CF/88 art. 2º — separação dos poderes: interpretação originalista vs. mutação constitucional"
    },
    {
        "id": "teleologica",
        "nome": "Hermenêutica Teleológica",
        "autor_principal": "Rudolf von Ihering",
        "datas": "1818–1892",
        "obra": "O Fim no Direito (Der Zweck im Recht), 1877",
        "principio": (
            "'O fim é o criador de todo o direito.' A lei deve ser interpretada "
            "pelos fins sociais que visa atingir, não pela intenção histórica do legislador. "
            "O direito como instrumento de organização social orientado a objetivos."
        ),
        "metodos": [
            "Teleológico — fins sociais da norma",
            "Sociológico — efeitos reais na sociedade",
            "Comparativo — como outros ordenamentos resolvem o mesmo problema"
        ],
        "critica": (
            "Risco de o intérprete substituir os fins do legislador pelos seus próprios. "
            "Gadamer (1900–2002): não existe acesso neutro aos 'fins sociais' — "
            "o intérprete sempre parte de seu horizonte histórico."
        ),
        "no_brasil": (
            "Influência no CC/2002 — função social do contrato (art. 421) e da propriedade. "
            "Interpretação teleológica da LGPD pela ANPD (Autoridade Nacional de Proteção de Dados): "
            "a proteção de dados como fim, não como formalidade."
        ),
        "tensao_norma": "LGPD — função social dos dados pessoais; CC/2002 art. 421 — função social do contrato"
    },
    {
        "id": "filosofica",
        "nome": "Hermenêutica Filosófica",
        "autor_principal": "Hans-Georg Gadamer",
        "datas": "1900–2002",
        "obra": "Verdade e Método (Wahrheit und Methode), 1960",
        "principio": (
            "Fusão de horizontes (Horizontverschmelzung): intérprete e texto "
            "se transformam mutuamente no ato de interpretação. "
            "O preconceito (Vorurteil) como condição de compreensão, não obstáculo. "
            "A tradição como horizonte que possibilita o novo — não prisão, mas solo."
        ),
        "metodos": [
            "Círculo hermenêutico — compreender o todo pela parte e a parte pelo todo",
            "Fusão de horizontes — diálogo entre texto histórico e contexto presente",
            "Consciência da história dos efeitos (Wirkungsgeschichte)"
        ],
        "critica": (
            "Habermas (1929–): Gadamer é conservador — valoriza a tradição mas não "
            "oferece critério para criticá-la. A hermenêutica precisa de dimensão crítica "
            "e emancipatória, não apenas compreensiva."
        ),
        "no_brasil": (
            "Fundamenta as mutações constitucionais do STF (Supremo Tribunal Federal) — "
            "a CF/88 interpretada à luz de novos contextos históricos. "
            "O Tema 987 como fusão de horizontes: o art. 19 do Marco Civil de 2014 "
            "compreendido à luz da desinformação e das eleições de 2026."
        ),
        "tensao_norma": "STF Tema 987 — mutação constitucional sobre responsabilidade de plataformas"
    },
    {
        "id": "integridade",
        "nome": "Hermenêutica da Integridade",
        "autor_principal": "Ronald Dworkin",
        "datas": "1931–2013",
        "obra": "O Império do Direito (Law's Empire), 1986",
        "principio": (
            "O direito como romance em cadeia — cada decisão judicial continua "
            "a narrativa anterior mantendo coerência de princípios. "
            "Distinção entre regras (aplicação tudo-ou-nada) e princípios "
            "(dimensão de peso). A integridade como virtude política do sistema jurídico."
        ),
        "metodos": [
            "Interpretação construtiva — a melhor interpretação que faz o direito o melhor possível",
            "Juiz Hércules — intérprete ideal com conhecimento e sabedoria ilimitados",
            "Coerência de princípios — a decisão deve ser consistente com o sistema como um todo"
        ],
        "critica": (
            "Critical Legal Studies: o direito não é coerente — é campo de luta política. "
            "A 'integridade' de Dworkin mascara escolhas ideológicas como necessidades jurídicas. "
            "Posner (1939–): o juiz real não é Hércules — é um ator racional com limitações."
        ),
        "no_brasil": (
            "Influência direta na jurisprudência principiológica do STF pós-CF/88. "
            "O Tema 987 como romance em cadeia: continuidade interpretativa da proteção "
            "de direitos fundamentais desde a ADPF 130 (liberdade de imprensa, 2009) "
            "até a responsabilidade de plataformas digitais (2025)."
        ),
        "tensao_norma": "STF — jurisprudência principiológica; CF/88 art. 5º como sistema de princípios"
    },
    {
        "id": "comunicativa",
        "nome": "Hermenêutica Comunicativa",
        "autor_principal": "Jürgen Habermas",
        "datas": "1929–",
        "obra": "Teoria da Ação Comunicativa (Theorie des kommunikativen Handelns), 1981",
        "principio": (
            "A legitimidade do direito deriva de procedimento discursivo racional — "
            "a norma é válida se derivada de processo em que todos os afetados puderam "
            "participar em condições de igualdade. O direito como sistema de normas "
            "que integra facticidade (coerção) e validade (legitimidade discursiva)."
        ),
        "metodos": [
            "Situação ideal de fala — ausência de coerção, igualdade de participação",
            "Discurso prático — argumentação orientada ao entendimento mútuo",
            "Procedimento legislativo democrático como fonte de legitimidade"
        ],
        "critica": (
            "A situação ideal de fala é contrafactual — nenhum processo legislativo real "
            "satisfaz essas condições. Schmitt (1888–1985): a política é conflito, não diálogo."
        ),
        "no_brasil": (
            "Fundamenta o processo participativo do Marco Civil da Internet (2009–2014) — "
            "construído via plataforma online com participação da sociedade civil. "
            "Questiona a legitimidade dos Decretos 12.975 e 12.976/2026 — editados "
            "sem debate parlamentar prévio, violando o procedimento habermasiano."
        ),
        "tensao_norma": "Marco Civil da Internet — processo participativo; Decretos 12.975/2026 — deficit democrático"
    },
    {
        "id": "brasileira",
        "nome": "Hermenêutica Jurídica Brasileira",
        "autor_principal": "Carlos Maximiliano Pereira dos Santos",
        "datas": "1873–1960",
        "obra": "Hermenêutica e Aplicação do Direito, 1924",
        "principio": (
            "Síntese dos métodos: gramatical, lógico, histórico, sistemático e teleológico. "
            "A interpretação como arte e ciência — não algoritmo mecânico. "
            "O direito como sistema: a norma isolada não tem sentido fora do conjunto."
        ),
        "metodos": [
            "Gramatical — análise linguística do texto",
            "Lógico — coerência interna do raciocínio",
            "Histórico — antecedentes legislativos e doutrinários",
            "Sistemático — posição no ordenamento",
            "Teleológico — fins sociais da norma"
        ],
        "critica": (
            "Ausência de critério para resolver conflitos entre os métodos — "
            "quando o gramatical e o teleológico apontam em direções opostas, "
            "Carlos Maximiliano não oferece hierarquia clara."
        ),
        "no_brasil": (
            "Referência obrigatória no STJ (Superior Tribunal de Justiça) e STF — "
            "citado em votos sobre interpretação de normas digitais (LGPD, Marco Civil, ECA Digital). "
            "A obra de 1924 continua sendo o manual prático mais citado na jurisprudência brasileira."
        ),
        "tensao_norma": "Toda norma do ordenamento digital brasileiro — método pluralista de interpretação"
    }
]

# ---- Fontes do direito ----
FONTES_DIREITO = {
    "introducao": (
        "As fontes do direito respondem à pergunta: de onde vem a norma jurídica? "
        "Identificar a fonte é identificar a legitimidade e a hierarquia da norma. "
        "No Brasil, a tradição romano-germânica privilegia a lei escrita, "
        "mas a jurisprudência vinculante do STF (súmulas vinculantes, repercussão geral) "
        "aproxima o sistema do common law. A doutrina orienta; "
        "os costumes são subsidiários; os princípios são supranormativos."
    ),
    "fontes": [
        {
            "nome": "Lei (norma escrita positivada)",
            "cor": "#d4a853",
            "hierarquia": 1,
            "descricao": (
                "Principal fonte do direito na tradição romano-germânica (civil law). "
                "Inclui: Constituição Federal, Emendas Constitucionais, Leis Complementares, "
                "Leis Ordinárias, Medidas Provisórias, Decretos Legislativos, Resoluções."
            ),
            "exemplo_digital": "LGPD (Lei 13.709/2018), Marco Civil da Internet (Lei 12.965/2014), ECA Digital (Lei 15.211/2025)",
            "latim": "Lex scripta — a lei escrita como expressão da vontade geral (Rousseau, 1712–1778)"
        },
        {
            "nome": "Jurisprudência (decisões judiciais)",
            "cor": "#3dc8e6",
            "hierarquia": 2,
            "descricao": (
                "Conjunto de decisões reiteradas dos tribunais sobre determinada matéria. "
                "No Brasil: súmulas vinculantes do STF têm força de lei; "
                "repercussão geral vincula todos os tribunais; "
                "precedentes do STJ orientam sem vincular formalmente. "
                "Aproximação crescente com o common law via CPC/2015."
            ),
            "exemplo_digital": "STF Tema 987 (art. 19 Marco Civil), STJ REsp 1.777.780 (dano moral por vazamento de dados)",
            "latim": "Stare decisis — respeitar o que foi decidido (common law); no Brasil: força vinculante restrita às súmulas"
        },
        {
            "nome": "Doutrina (produção científica dos juristas)",
            "cor": "#9b59b6",
            "hierarquia": 3,
            "descricao": (
                "Estudos, obras e pareceres dos juristas que interpretam e sistematizam o direito. "
                "Não é fonte formal — não cria norma — mas orienta legisladores, juízes e advogados. "
                "No direito digital brasileiro: Laura Schertel Mendes (LGPD), "
                "Ronaldo Lemos (Marco Civil), Fabiano Hartmann Peixoto (IA)."
            ),
            "exemplo_digital": "Danilo Doneda, Da Privacidade à Proteção de Dados Pessoais (2006) — base doutrinária da LGPD",
            "latim": "Opinio doctorum — a opinião dos doutores do direito como fonte de autoridade"
        },
        {
            "nome": "Costumes (práticas reiteradas com convicção de obrigatoriedade)",
            "cor": "#2ecc71",
            "hierarquia": 4,
            "descricao": (
                "Práticas sociais reiteradas acompanhadas da convicção de que são juridicamente "
                "obrigatórias (opinio iuris sive necessitatis). "
                "No direito digital: os termos de uso e políticas de privacidade como costumes "
                "empresariais que a LGPD transformou em obrigações legais."
            ),
            "exemplo_digital": "Cookies e consentimento: prática consuetudinária das plataformas que o GDPR e a LGPD positivaram",
            "latim": "Consuetudo — costume; opinio iuris — convicção de obrigatoriedade jurídica"
        },
        {
            "nome": "Princípios gerais do direito",
            "cor": "#ecf0f1",
            "hierarquia": 2,
            "descricao": (
                "Valores fundamentais que orientam todo o ordenamento — "
                "boa-fé, proporcionalidade, razoabilidade, dignidade humana, isonomia. "
                "No pós-positivismo (Dworkin, Alexy): os princípios têm força normativa própria "
                "e podem prevalecer sobre regras em casos de colisão."
            ),
            "exemplo_digital": "Princípio da proporcionalidade: limitação da coleta de dados ao mínimo necessário (LGPD art. 6º, III — minimização)",
            "latim": "Bona fides — boa-fé; aequitas — equidade; proportionalitas — proporcionalidade"
        },
        {
            "nome": "Tratados internacionais",
            "cor": "#1a5276",
            "hierarquia": 2,
            "descricao": (
                "No Brasil: status supralegal (acima das leis ordinárias, abaixo da CF/88) "
                "para tratados comuns — RE 466.343/STF (2008). "
                "Tratados de direitos humanos aprovados com quórum de EC: status constitucional. "
                "No direito digital: Convenção 108+ do Conselho da Europa sobre proteção de dados "
                "influencia o padrão brasileiro."
            ),
            "exemplo_digital": "Convenção da ONU sobre Direitos da Criança (1989) — base do ECA e do ECA Digital; GDPR como parâmetro glocal para a LGPD",
            "latim": "Pacta sunt servanda — os pactos devem ser cumpridos; ius cogens — norma imperativa do direito internacional"
        }
    ]
}

# ---- Arco histórico do Código Civil ----
ARCO_CC = {
    "introducao": (
        "O Código Civil brasileiro percorreu um arco de 170 anos — do Império à era digital. "
        "Cada código é um projeto político: o CC/1916 era o Brasil da Primeira República "
        "agrária e patriarcal; o CC/2002 é o Brasil da redemocratização e do Estado social; "
        "o PL 4/2025 é o Brasil da era digital tentando legislar o que ainda não existe plenamente. "
        "Pancronia: todos coexistem no ordenamento atual — o CC/1916 ainda produz efeitos "
        "via direitos adquiridos e situações jurídicas constituídas."
    ),
    "codigos": [
        {
            "nome": "Ordenações Filipinas",
            "ano": 1603,
            "contexto": "Brasil colonial — Portugal sob domínio espanhol (Filipe II)",
            "vigencia": "1603–1916 — 313 anos de vigência parcial no Brasil",
            "caracteristica": (
                "Direito medieval português com influência do direito romano, canônico e germânico. "
                "Vigoraram no Brasil por mais de três séculos — da colônia até a Primeira República. "
                "Pancronia exemplar: norma de 1603 produzindo efeitos até 1916."
            ),
            "influencia": "Direito romano via Corpus Iuris Civilis; direito canônico medieval; direito germânico costumeiro"
        },
        {
            "nome": "Código Comercial de 1850",
            "ano": 1850,
            "contexto": "Brasil Império — segundo ano do reinado de Pedro II",
            "vigencia": "1850–2002 (parte terrestre); parte marítima ainda vigente",
            "caracteristica": (
                "Lei 556/1850 — inspirado no Code de Commerce francês (1807) e no Código "
                "Comercial português (1833). Segundo ano do reinado de Pedro II — "
                "o mesmo ano da Lei Eusébio de Queirós (abolição do tráfico de escravizados) "
                "e da Lei de Terras. O CC/2002 absorveu a parte terrestre — "
                "comparação glocal (global + local, Robertson, 1990s): Itália unificou em 1942, "
                "Alemanha mantém o HGB (Handelsgesetzbuch — Código Comercial alemão, 1897) separado até hoje."
            ),
            "influencia": "Code de Commerce francês (1807); Código Comercial português (1833)"
        },
        {
            "nome": "Código Civil de 1916",
            "ano": 1916,
            "contexto": "Primeira República — Brasil agrário, elites rurais, patriarcalismo",
            "vigencia": "1916–2003",
            "caracteristica": (
                "Obra de Clóvis Beviláqua (1859–1944) — fortemente influenciada pelo BGB alemão "
                "(Bürgerliches Gesetzbuch, 1896) e pela Pandektenwissenschaft (pandectismo alemão). "
                "Paradigma patrimonialista e individualista — o sujeito de direito como proprietário. "
                "Ignorava mulheres casadas (relativamente incapazes até 1962), trabalhadores, consumidores. "
                "Savigny (1779–1861) como matriz hermenêutica dominante."
            ),
            "influencia": "BGB alemão (1896); pandectismo de Windscheid (1817–1892); Savigny"
        },
        {
            "nome": "Código Civil de 2002",
            "ano": 2002,
            "contexto": "Redemocratização — Brasil urbano, Estado social, CF/88",
            "vigencia": "2003–presente",
            "caracteristica": (
                "Lei 10.406/2002 — obra de Miguel Reale (1910–2006) e comissão de juristas. "
                "Teoria tridimensional do direito (fato + valor + norma) como fundamento. "
                "Três cláusulas gerais estruturantes: boa-fé objetiva (art. 422), "
                "função social do contrato (art. 421) e função social da propriedade. "
                "Absorveu o Código Comercial de 1850 — unificação do direito privado. "
                "Ihering (1818–1892) como matriz hermenêutica dominante — fins sociais."
            ),
            "influencia": "Teoria tridimensional de Reale; CC italiano de 1942; CF/88"
        },
        {
            "nome": "Reforma do Código Civil — PL 4/2025",
            "ano": 2025,
            "contexto": "Era digital — IA, dados pessoais, plataformas, identidade digital",
            "vigencia": "Em tramitação no Senado Federal",
            "caracteristica": (
                "Proposta de comissão de juristas presidida pelo Min. Luís Felipe Salomão (STJ). "
                "Livro VI — Do Direito Civil Digital: personalidade digital, responsabilidade "
                "de plataformas, assinatura eletrônica, patrimônio digital, IA como instrumento jurídico. "
                "Resgate da doutrina de Pontes de Miranda (1892–1979): distinção ato ilícito / "
                "responsabilidade civil — virada do paradigma reparatório para o preventivo. "
                "Tensão antinômica com LGPD e Marco Civil — alertas da ANPD e do CGI.br (Comitê Gestor da Internet no Brasil)."
            ),
            "influencia": "Pontes de Miranda; GDPR europeu; CC italiano de 1942; doutrina de Salomão"
        }
    ]
}

# ---- Brasil Império como camada do ordenamento ----
BRASIL_IMPERIO = {
    "introducao": (
        "O Brasil Império (1822–1889) produziu marcos jurídicos que ainda dialogam "
        "com o ordenamento atual — pancronia em ação. A independência de 1822 não "
        "criou um sistema jurídico do zero: as Ordenações Filipinas (1603) continuaram "
        "vigentes até 1916. O Império legislou sobre um substrato colonial de três séculos."
    ),
    "marcos": [
        {
            "nome": "Constituição de 1824",
            "ano": 1824,
            "destaque": "Poder Moderador — Benjamin Constant (1767–1830)",
            "descricao": (
                "Outorgada por Pedro I após dissolução da Assembleia Constituinte. "
                "Quatro poderes: Legislativo, Executivo, Judiciário e Moderador — "
                "influência de Benjamin Constant (1767–1830), teórico liberal francês. "
                "O Poder Moderador era privativo do Imperador: 'chave de toda a organização política'. "
                "Contraponto ao modelo de Montesquieu (três poderes): a concentração "
                "que Montesquieu quis evitar foi constitucionalizada no Brasil. "
                "Pancronia: o debate sobre o Poder Moderador ressurge toda vez que "
                "o STF age como árbitro entre os demais poderes."
            )
        },
        {
            "nome": "Código Criminal de 1830",
            "ano": 1830,
            "destaque": "Primeiro código penal do Brasil independente",
            "descricao": (
                "Influenciado pelo Código Penal francês (1810) e pela filosofia penal "
                "de Beccaria (1738–1794) — humanização das penas, legalidade, proporcionalidade. "
                "Contemporâneo da consolidação do direito penal moderno europeu. "
                "Pancronia: os princípios de Beccaria de 1764 estão na CF/88 art. 5º, XXXIX "
                "(nullum crimen sine lege) e no debate atual sobre responsabilidade penal por IA."
            )
        },
        {
            "nome": "Código de Processo Criminal de 1832",
            "ano": 1832,
            "destaque": "Júri popular; habeas corpus como remédio processual",
            "descricao": (
                "Introduziu o júri popular e o habeas corpus como garantias processuais — "
                "influência do modelo inglês (Habeas Corpus Act, 1679). "
                "O habeas corpus de 1832 é o antepassado do habeas data da CF/88 (art. 5º, LXXII) "
                "e do direito de acesso da LGPD — pancronia de quase dois séculos."
            )
        },
        {
            "nome": "Código Comercial de 1850 (Lei 556)",
            "ano": 1850,
            "destaque": "Segundo ano do reinado de Pedro II — mesmo ano da Lei de Terras",
            "descricao": (
                "O ano de 1850 é o mais denso do Brasil Império em termos legislativos: "
                "Lei Eusébio de Queirós (abolição do tráfico), Lei de Terras, Código Comercial. "
                "Três leis que estruturaram a economia e a sociedade brasileiras por décadas. "
                "Direito comparado glocal (global + local, Robertson, 1990s): "
                "inspirado no Code de Commerce francês (1807) — o Brasil copiou o modelo "
                "napoleônico 43 anos depois, enquanto a Alemanha ainda não tinha unificado "
                "seu código comercial (HGB virá em 1897)."
            )
        },
        {
            "nome": "Lei de Terras de 1850 (Lei 601)",
            "ano": 1850,
            "destaque": "Estrutura fundiária com efeitos até 2026",
            "descricao": (
                "Proibiu a aquisição de terras devolutas por outro meio que não a compra — "
                "impossibilitou que escravizados libertos e imigrantes pobres adquirissem terra. "
                "Criou o modelo fundiário concentrado que persiste no Brasil. "
                "Pancronia exemplar: norma de 1850 em diálogo com conflitos agrários de 2026 — "
                "a estrutura de propriedade que a Lei de Terras criou ainda é debatida "
                "no STF e no Congresso. O direito digital de acesso e inclusão (CF/88 art. 5º, XXXIII) "
                "é a versão contemporânea do mesmo debate: quem tem acesso e quem é excluído."
            )
        }
    ]
}
