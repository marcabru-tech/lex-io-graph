"""
Camada multissemiótica do Lex-IO-Graph.
Citações literárias, obras de arte e glossário jurídico.

Fundamento metodológico: dialogismo e polifonia bakhtinianos
(Bakhtin, 1895–1975) — múltiplas vozes coexistindo em tensão
produtiva. A literatura universal como instrumento de fundamentação
jurídica — tradição dos grandes doutrinadores brasileiros.
"""

# ---- Citações literárias ----
CITACOES = [
    {
        "id": "kafka_processo",
        "autor": "Franz Kafka",
        "datas": "1883–1924",
        "obra": "O Processo (Der Proceß), 1925 (póstumo)",
        "citacao_original": "Jemand musste Josef K. verleumdet haben, denn ohne dass er etwas Böses getan hätte, wurde er eines Morgens verhaftet.",
        "idioma_original": "Alemão",
        "traducao": "Alguém havia caluniado Josef K., pois sem ter feito nada de mal, ele foi preso numa manhã.",
        "contexto_juridico": "A opacidade do sistema normativo — o indivíduo submetido a um processo cujas regras não conhece e cuja autoridade não pode questionar. Metáfora da responsabilidade de plataformas sem transparência algorítmica.",
        "uso_jurisprudencia": "Citado em votos do STF sobre devido processo legal e transparência — Min. Gilmar Mendes utiliza O Processo para ilustrar a arbitrariedade sem contraditório",
        "normas_relacionadas": ["marco_civil", "stf_tema987", "pl_ia"],
        "tema": "devido processo legal, transparência algorítmica, opacidade normativa"
    },
    {
        "id": "dostoievski_crime",
        "autor": "Fiódor Dostoiévski",
        "datas": "1821–1881",
        "obra": "Crime e Castigo (Prestupleniye i Nakazaniye), 1866",
        "citacao_original": "Боль и страдание всегда обязательны для широкого сознания и глубокого сердца.",
        "idioma_original": "Russo",
        "traducao": "A dor e o sofrimento são sempre inevitáveis para uma consciência ampla e um coração profundo.",
        "contexto_juridico": "A tensão entre culpa subjetiva e responsabilidade objetiva — central na virada paradigmática do CC/2025 (resgate de Pontes de Miranda). A responsabilidade civil não como punição mas como prevenção.",
        "uso_jurisprudencia": "Dostoiévski é citado em votos sobre dosimetria da pena e ressocialização — STJ REsp sobre proporcionalidade da sanção digital",
        "normas_relacionadas": ["pl_cc_digital", "lgpd"],
        "tema": "responsabilidade civil, culpa, prevenção de danos"
    },
    {
        "id": "shakespeare_mercador",
        "autor": "William Shakespeare",
        "datas": "1564–1616",
        "obra": "O Mercador de Veneza (The Merchant of Venice), c.1596–1598",
        "citacao_original": "The quality of mercy is not strained; it droppeth as the gentle rain from heaven upon the place beneath.",
        "idioma_original": "Inglês",
        "traducao": "A qualidade da misericórdia não é forçada; cai como a suave chuva do céu sobre o lugar abaixo.",
        "contexto_juridico": "Portia defende que a letra da lei (Shylock e a libra de carne) sem equidade é injustiça. Precursor da distinção entre legalidade e legitimidade — antinomia entre norma positiva e princípio de justiça. O Mercador de Veneza é Kafka avant la lettre: a lei como instrumento de crueldade.",
        "uso_jurisprudencia": "Citado por Rui Barbosa em defesas no Supremo — a equidade como instrumento hermenêutico. Min. Marco Aurélio citou Shakespeare em voto sobre proporcionalidade",
        "normas_relacionadas": ["cf88", "stf_tema987"],
        "tema": "equidade, legalidade vs. legitimidade, hermenêutica, proporcionalidade"
    },
    {
        "id": "machado_memorias",
        "autor": "Machado de Assis",
        "datas": "1839–1908",
        "obra": "Memórias Póstumas de Brás Cubas, 1881",
        "citacao_original": "Ao vencedor, as batatas.",
        "idioma_original": "Português",
        "traducao": "Ao vencedor, as batatas. (ironia sobre a lógica do poder e da lei)",
        "contexto_juridico": "A crítica machadiana ao positivismo jurídico formal — a lei que serve ao vencedor, não à justiça. O Brasil oitocentista de Machado é o mesmo que produziu o Código Comercial de 1850 e a Lei de Terras de 1850 — legislação que favoreceu estruturalmente as elites. Pancronia: a crítica de 1881 ilumina o debate atual sobre acesso à justiça digital.",
        "uso_jurisprudencia": "Machado de Assis é a referência literária mais citada na jurisprudência brasileira — STJ e STF utilizam seus personagens para ilustrar hipocrisia normativa e formalismo vazio",
        "normas_relacionadas": ["cf88", "lgpd"],
        "tema": "acesso à justiça, formalismo jurídico, crítica ao positivismo, pancronia"
    },
    {
        "id": "goethe_fausto",
        "autor": "Johann Wolfgang von Goethe",
        "datas": "1749–1832",
        "obra": "Fausto (Faust), Parte I: 1808 / Parte II: 1832",
        "citacao_original": "Im Anfang war die Tat.",
        "idioma_original": "Alemão",
        "traducao": "No princípio era a Ação. (Fausto reinterpretando João 1:1 — 'No princípio era o Verbo')",
        "contexto_juridico": "O pacto fáustico como metáfora do contrato de adesão digital — o usuário que aceita termos sem ler troca sua privacidade (alma) por serviços (conhecimento/poder). Pacta sunt servanda vs. autonomia da vontade informada. Citado na doutrina de contratos eletrônicos.",
        "uso_jurisprudencia": "Savigny (1779–1861) era contemporâneo de Goethe — o Volksgeist (espírito do povo) de Savigny dialoga com o individualismo fáustico. Citado em votos sobre autonomia contratual e consentimento livre e informado (LGPD art. 7º)",
        "normas_relacionadas": ["lgpd", "marco_civil"],
        "tema": "contrato, consentimento, autonomia da vontade, privacidade"
    },
    {
        "id": "jorge_amado_capitaes",
        "autor": "Jorge Amado",
        "datas": "1912–2001",
        "obra": "Capitães da Areia, 1937",
        "citacao_original": "A cidade da Bahia tem mistérios que nem os seus habitantes conhecem.",
        "idioma_original": "Português",
        "traducao": "A cidade da Bahia tem mistérios que nem os seus habitantes conhecem.",
        "contexto_juridico": "Capitães da Areia narra crianças abandonadas à margem da lei — precursor literário da doutrina da proteção integral do ECA (1990). A obra foi censurada pelo Estado Novo (1937) — ironia: o Estado que censurou é o mesmo que deveria proteger. Dialoga com o ECA Digital sobre proteção de menores em ambientes opacos (plataformas digitais = a cidade com mistérios que nem os habitantes conhecem).",
        "uso_jurisprudencia": "Jorge Amado é citado em votos do STJ sobre direitos de crianças em situação de vulnerabilidade — a ficção como documento histórico do fracasso da proteção estatal",
        "normas_relacionadas": ["eca", "eca_digital"],
        "tema": "proteção integral de menores, vulnerabilidade digital, censura, acesso à justiça"
    },
    {
        "id": "machado_alienista",
        "autor": "Machado de Assis",
        "datas": "1839–1908",
        "obra": "O Alienista, 1882 (in: Papéis Avulsos)",
        "citacao_original": "O Dr. Bacamarte examinou a questão sob todos os lados, meditou, orou; e ao cabo de três semanas declarou que ia meter a vila inteira no hospício.",
        "idioma_original": "Português",
        "traducao": "O Dr. Bacamarte examinou a questão sob todos os lados, meditou, orou; e ao cabo de três semanas declarou que ia meter a vila inteira no hospício.",
        "contexto_juridico": "A antinomia bacamartiana — o sistema normativo que muda os critérios retroativamente, internando quem antes era são. Bacamarte é simultaneamente legislador, juiz e executor: a concentração de poder que Montesquieu (1689–1755) quis evitar com a separação dos três poderes. No fim, interna a si mesmo — a norma que se volta contra seu criador. Metáfora da crise do art. 19 do Marco Civil: o Estado que criou a regra (exigência de ordem judicial) e doze anos depois a declara insuficiente via STF e decretos, gerando insegurança jurídica total. Machado antecipou em 1882 o que Fuller (1902–1978) teorizaria em 1964: a lei que muda seus critérios continuamente viola a moralidade interna do direito.",
        "uso_jurisprudencia": "O Alienista é a obra de Machado de Assis mais citada em votos sobre insegurança jurídica e arbitrariedade normativa — STJ e STF utilizam Bacamarte para ilustrar sistemas que perdem a capacidade de distinguir normalidade de patologia. Min. Luis Felipe Salomão citou O Alienista em voto sobre responsabilidade civil por dano institucional.",
        "normas_relacionadas": ["marco_civil", "stf_tema987", "decreto_12975_2026", "cf88"],
        "tema": "insegurança jurídica, separação de poderes, antinomia institucional, moralidade interna do direito"
    },
    {
        "id": "graciliano_relatorios",
        "autor": "Graciliano Ramos",
        "datas": "1892–1953",
        "obra": "Relatórios ao Governador do Estado de Alagoas (1929, 1930) — atos administrativos oficiais da Prefeitura de Palmeira dos Índios, Alagoas. Republicados in: O Prefeito Escritor (Editora Record, 2024)",
        "citacao_original": "Os mortos esperarão mais algum tempo. São os munícipes que não reclamam.",
        "idioma_original": "Português",
        "traducao": "Sobre a impossibilidade orçamentária de construir o cemitério naquele exercício fiscal — os vivos têm prioridade.",
        "contexto_juridico": (
            "Graciliano Ramos foi prefeito de Palmeira dos Índios, Alagoas, de janeiro de 1928 a abril de 1930. "
            "Seus relatórios de gestão ao governador Álvaro Paes — publicados no Diário Oficial do Estado — "
            "são documentos administrativos oficiais, atos jurídicos no sentido pleno, redigidos com a economia "
            "verbal e a precisão que marcaria Vidas Secas (1938). Não é literatura sobre direito — é um literato "
            "produzindo direito. A distinção é ontológica. "
            "É o caso mais antigo documentado de accountability municipal com linguagem clara no Brasil: "
            "em 1929, sem Lei de Responsabilidade Fiscal (LC 101/2000), sem CGU (criada em 2001), "
            "sem Portal da Transparência, Graciliano prestou contas com mais clareza e precisão "
            "do que a maioria dos gestores públicos obrigados por lei a fazê-lo hoje. "
            "Primeiro ato de gestão: 'estabelecer alguma ordem na administração' — vetou apadrinhamentos, "
            "demitiu cobradores irregulares, construiu escolas, abriu estradas. "
            "A receita municipal cresceu 41% em 1929 com supressão de taxas, não criação de novas. "
            "O governador ficou tão impressionado que o convidou para diretor da Instrução Pública de Alagoas. "
            "Pancronia: o princípio da publicidade administrativa (CF/88 art. 37), a LAI (Lei 12.527/2011) "
            "e o debate contemporâneo sobre linguagem clara na LGPD, no ECA Digital e nos termos de uso "
            "das plataformas têm aqui seu antecedente literário e administrativo mais preciso."
        ),
        "uso_jurisprudencia": (
            "Em março de 1936, Graciliano foi preso sem acusação formal pelo governo Vargas — "
            "sob o estado de guerra declarado após a Intentona Comunista de novembro de 1935 "
            "(Lei de Segurança Nacional, Decreto 38/1935). O Estado Novo seria decretado apenas "
            "em novembro de 1937, mas a lógica autoritária já operava sem due process desde 1935. "
            "Ficou detido 10 meses sem processo, sem habeas corpus, sem contraditório. "
            "O mesmo Estado que havia reconhecido e promovido sua excelência administrativa "
            "o encarcerou pela mesma estrutura que O Alienista diagnosticou em 1882 e que "
            "a dissertação de Sandoval Gonçalves dos Santos analisou em 1982: "
            "o sistema que pune sem explicar, que julga sem fundamentar. "
            "A experiência da prisão resultou em Memórias do Cárcere (1953, póstumo). "
            "O arco pancrônico fecha: 1928 (prefeito que presta contas com clareza) → "
            "1936 (preso sem acusação) → 1982 (dissertação sobre o mito da intimidação) → "
            "2026 (debate sobre transparência algorítmica e due process digital)."
        ),
        "normas_relacionadas": ["cf88", "lgpd", "marco_civil", "decreto_12975_2026"],
        "tema": "publicidade administrativa, linguagem clara, accountability, due process, pancronia, Estado de exceção"
    },
    {
        "id": "kafka_colonia",
        "autor": "Franz Kafka",
        "datas": "1883–1924",
        "obra": "Na Colônia Penal (In der Strafkolonie), 1919",
        "citacao_original": "Die Schuld ist immer zweifellos.",
        "idioma_original": "Alemão",
        "traducao": "A culpa é sempre indiscutível.",
        "contexto_juridico": "A máquina que inscreve a sentença no corpo do condenado sem que ele saiba qual é seu crime — metáfora da opacidade algorítmica: sistemas de IA que decidem sobre crédito, emprego, liberdade condicional sem explicabilidade. Antecipa o direito à explicação do PL 2.338/2023 (Marco Legal da IA) e do GDPR (art. 22).",
        "uso_jurisprudencia": "Citado em artigos doutrinários sobre responsabilidade por decisões automatizadas — o dever de explicabilidade como antídoto kafkiano",
        "normas_relacionadas": ["pl_ia", "lgpd"],
        "tema": "decisões automatizadas, explicabilidade da IA, responsabilidade algorítmica"
    }
]

# ---- Obras de arte (domínio público via Wikimedia Commons) ----
OBRAS_ARTE = [
    {
        "id": "rafael_justica",
        "titulo": "A Justiça (Iustitia)",
        "autor": "Rafael Sanzio (Raffaello Sanzio da Urbino)",
        "datas_autor": "1483–1520",
        "ano": "1509–1511",
        "tecnica": "Afresco",
        "localizacao": "Stanza della Segnatura, Museus do Vaticano, Roma",
        "url_wikimedia": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Raphael_-_Jurisprudence.jpg/800px-Raphael_-_Jurisprudence.jpg",
        "descricao": "A Jurisprudência como uma das quatro virtudes cardeais — ao lado da Teologia, Filosofia e Poesia. Rafael representa a Justiça como mulher coroada segurando espada e balança — ícone que atravessa 500 anos e ainda simboliza o Judiciário brasileiro.",
        "conexao_juridica": "O afresco foi encomendado pelo Papa Júlio II para a biblioteca papal — o mesmo espaço onde Graciano formalizou o Corpus Iuris Canonici (1140). Arte e direito como sistemas semióticos irmãos desde a Renascença.",
        "normas_relacionadas": ["cf88", "stf_tema987"]
    },
    {
        "id": "david_juramento",
        "titulo": "O Juramento dos Horácios (Le Serment des Horaces)",
        "autor": "Jacques-Louis David",
        "datas_autor": "1748–1825",
        "ano": "1784",
        "tecnica": "Óleo sobre tela",
        "localizacao": "Musée du Louvre, Paris",
        "url_wikimedia": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Jacques-Louis_David_-_Oath_of_the_Horatii_-_WGA06081.jpg/800px-Jacques-Louis_David_-_Oath_of_the_Horatii_-_WGA06081.jpg",
        "descricao": "Três irmãos juram sobre espadas defender Roma — o pacto como fundamento da ordem jurídica. David pintou esta obra no mesmo período em que Montesquieu era absorvido pelas constituições americanas (1787) e francesa (1791). Pacta sunt servanda como ato fundador da república.",
        "conexao_juridica": "O juramento como ato jurídico performativo — Austin (1911–1960) e a teoria dos atos de fala: o juramento não descreve, cria a obrigação. Dialoga com o art. 5º da CF/88 — direitos fundamentais como pacto social.",
        "normas_relacionadas": ["cf88"]
    },
    {
        "id": "debret_justica_brasil",
        "titulo": "Distribuição de Justiça no Brasil",
        "autor": "Jean-Baptiste Debret",
        "datas_autor": "1768–1848",
        "ano": "c.1820–1831",
        "tecnica": "Aquarela",
        "localizacao": "Voyage pittoresque et historique au Brésil (1834–1839)",
        "url_wikimedia": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Debret-Audience_d%27un_juge_de_paix.jpg/800px-Debret-Audience_d%27un_juge_de_paix.jpg",
        "descricao": "Debret documentou o sistema jurídico colonial brasileiro — juízes de paz, escravizados, a justiça como poder dos senhores. Pancronia em ação: a obra de 1820 dialoga com o debate atual sobre acesso à justiça digital e desigualdade algorítmica.",
        "conexao_juridica": "O Brasil Império de Debret é o mesmo que produziu o Código Criminal de 1830, o Código Comercial de 1850 e a Lei de Terras de 1850 — legislação que estruturou a desigualdade que persiste no ordenamento digital de 2026.",
        "normas_relacionadas": ["cf88", "eca"]
    },
    {
        "id": "cranach_justica",
        "titulo": "Alegoria da Justiça (Justitia)",
        "autor": "Lucas Cranach, o Velho",
        "datas_autor": "1472–1553",
        "ano": "c.1537",
        "tecnica": "Óleo sobre madeira",
        "localizacao": "Gemäldegalerie, Berlim",
        "url_wikimedia": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Lucas_Cranach_d.%C3%84._-_Justice_%28Justitia%29_-_Google_Art_Project.jpg/600px-Lucas_Cranach_d.%C3%84._-_Justice_%28Justitia%29_-_Google_Art_Project.jpg",
        "descricao": "Justitia como mulher vendada segurando balança e espada — a iconografia da justiça cega que atravessa o direito ocidental. Cranach era contemporâneo de Lutero e do início da Reforma Protestante — período em que o direito canônico começava a ceder ao direito secular.",
        "conexao_juridica": "A venda nos olhos da Justiça: isonomia formal vs. equidade substantiva. O debate atual sobre viés algorítmico nos sistemas de IA é a versão digital desta tensão — a máquina que julga 'com olhos vendados' reproduz os vieses de quem a treinou.",
        "normas_relacionadas": ["pl_ia", "lgpd", "cf88"]
    }
]

# ---- Glossário jurídico ----
GLOSSARIO = [
    {
        "termo": "Antinomia",
        "latim": "Antinomia (do grego: anti = contra + nomos = lei)",
        "definicao": "Conflito entre duas normas jurídicas de mesmo ordenamento cuja aplicação simultânea é impossível ou gera resultado contraditório. Bobbio (1909–2004) sistematizou três critérios de resolução: lex superior (hierarquia), lex posterior (temporalidade), lex specialis (especialidade).",
        "corrente": "Positivismo jurídico analítico (Bobbio)",
        "exemplo_brasil": "PL 4/2025 (Livro VI CC Digital) × LGPD — antinomia apontada pela ANPD (Autoridade Nacional de Proteção de Dados): mesma matéria regulada por dois diplomas com critérios distintos"
    },
    {
        "termo": "Hermenêutica jurídica",
        "latim": "Hermeneutica iuris (do grego: hermeneúein = interpretar, de Hermes, mensageiro dos deuses)",
        "definicao": "Teoria e método de interpretação das normas jurídicas. Principais correntes: histórica (Savigny, 1779–1861), teleológica (Ihering, 1818–1892), filosófica (Gadamer, 1900–2002), integridade (Dworkin, 1931–2013). No Brasil: Carlos Maximiliano (1873–1960) sintetizou os métodos gramatical, lógico, histórico, sistemático e teleológico.",
        "corrente": "Transversal — fundamento de toda interpretação normativa",
        "exemplo_brasil": "O STF interpreta a CF/88 via mutação constitucional — método gadameriano de fusão de horizontes entre o texto de 1988 e os contextos de 2026"
    },
    {
        "termo": "Hierarquia normativa",
        "latim": "Hierarchia normativa (do grego: hierarchia = governo sagrado, depois: ordem de precedência)",
        "definicao": "Estrutura vertical do ordenamento jurídico — cada norma extrai sua validade de uma norma superior, culminando na Constituição (Kelsen, 1881–1973). No Brasil: CF/88 > Emendas Constitucionais > Leis Complementares > Leis Ordinárias > Decretos > Normas Regulamentares.",
        "corrente": "Positivismo normativista (Kelsen)",
        "exemplo_brasil": "O STF declara inconstitucional norma que viola a CF/88 — exercício da hierarquia normativa kelseniana"
    },
    {
        "termo": "Pancronia",
        "latim": "Panchronia (do grego: pan = todo + chronos = tempo)",
        "definicao": "Metodologia que acessa o arco histórico completo simultaneamente — nem sincrônica (corte temporal fixo) nem diacrônica (evolução linear). No Lex-IO-Graph: o ordenamento jurídico brasileiro como campo de camadas coexistentes, do Código Comercial de 1850 ao Decreto 12.975/2026.",
        "corrente": "Fundamento metodológico do Lex-IO-Graph — dialogismo e polifonia bakhtinianos (Bakhtin, 1895–1975)",
        "exemplo_brasil": "Lei de Terras de 1850 (Brasil Império) em diálogo com conflitos fundiários de 2026 — pancronia exemplar"
    },
    {
        "termo": "Devido processo legal",
        "latim": "Due process of law / Per legem terrae (pela lei da terra — Magna Carta, 1215)",
        "definicao": "Garantia de que ninguém será privado de liberdade ou propriedade sem processo que respeite contraditório, ampla defesa e juiz natural. CF/88 art. 5º, LIV. No ambiente digital: o debate sobre notice-and-takedown sem ordem judicial (pós-Tema 987) tensiona o devido processo das plataformas.",
        "corrente": "Direito constitucional processual — convergência common law e civil law",
        "exemplo_brasil": "STF Tema 987: o art. 19 do Marco Civil exigia ordem judicial — a inconstitucionalidade parcial cria dever de remoção sem essa garantia, gerando tensão com o devido processo das plataformas"
    },
    {
        "termo": "Lex specialis",
        "latim": "Lex specialis derogat generali (a lei especial derroga a geral)",
        "definicao": "Critério de resolução de antinomia por especialidade — quando duas normas de mesmo grau e mesma época regulam o mesmo fato, a mais específica prevalece. Terceiro critério de Bobbio, o mais complexo: exige identificação precisa do âmbito de aplicação.",
        "corrente": "Positivismo jurídico analítico (Bobbio, 1909–2004)",
        "exemplo_brasil": "LGPD (Lei Geral de Proteção de Dados Pessoais — Lei 13.709/2018) como lex specialis em relação ao PL 4/2025 (Código Civil Digital) — alerta da ANPD sobre sobreposição normativa"
    },
    {
        "termo": "Mutação constitucional",
        "latim": "Mutatio constitutionalis",
        "definicao": "Alteração informal do sentido da Constituição por via interpretativa, sem mudança do texto. O texto permanece o mesmo; o significado muda por força de nova interpretação do STF. Gadamer (1900–2002): fusão de horizontes entre o texto histórico e o contexto presente.",
        "corrente": "Hermenêutica constitucional / Teoria da Constituição",
        "exemplo_brasil": "CF/88 art. 5º, XII (sigilo de dados) interpretado pelo STF como incluindo dados pessoais digitais — mutação constitucional que precedeu a EC 115/2022 (direito fundamental à proteção de dados)"
    },
    {
        "termo": "Repercussão geral",
        "latim": "Transcendentia causae (transcendência da causa)",
        "definicao": "Requisito de admissibilidade do Recurso Extraordinário ao STF — a questão constitucional deve transcender os interesses das partes e ter relevância para toda a sociedade. EC 45/2004. Aprovada: o STF julga e a decisão vincula todos os tribunais (stare decisis à brasileira).",
        "corrente": "Direito processual constitucional",
        "exemplo_brasil": "Tema 987 (RE 1.037.396) — repercussão geral reconhecida: a responsabilidade de plataformas por conteúdo de terceiros transcende o caso e afeta toda a internet brasileira"
    },
    {
        "termo": "Glocal",
        "latim": "Neologismo: global + local (Roland Robertson, sociólogo escocês, 1992)",
        "definicao": "Dinâmica pela qual fenômenos globais se manifestam com características locais e vice-versa. No direito: normas internacionais (GDPR, EU AI Act) que impactam o ordenamento brasileiro e normas brasileiras (LGPD, Marco Civil) com efeito extraterritorial.",
        "corrente": "Sociologia jurídica / Direito internacional comparado",
        "exemplo_brasil": "LGPD e GDPR: empresas brasileiras com usuários europeus sujeitas a ambas simultaneamente — o glocal como realidade normativa cotidiana"
    },
    {
        "termo": "Titular de dados",
        "latim": "Dominus datorum (senhor dos dados — adaptação moderna)",
        "definicao": "Pessoa natural a quem se referem os dados pessoais objeto de tratamento (LGPD art. 5º, V). O titular tem direitos de acesso, retificação, portabilidade, eliminação e revogação do consentimento — base do paradigma de autodeterminação informativa.",
        "corrente": "Direito fundamental à proteção de dados (EC 115/2022)",
        "exemplo_brasil": "LGPD art. 18 — rol de direitos do titular. ECA Digital (Lei 15.211/2025) amplia: para menores, o titular é representado pelo responsável legal com consentimento qualificado"
    }
]
