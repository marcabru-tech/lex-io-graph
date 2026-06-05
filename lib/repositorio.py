"""
Repositório de conhecimento do Lex-IO-Graph.
Dados doutrinários, latinos, históricos e de direito comparado glocal.
"""

# ---- Autores do inventário doutrinário ----
AUTORES = {
    "kelsen": {
        "nome": "Hans Kelsen",
        "datas": "1881–1973",
        "nacionalidade": "Austro-americano",
        "obra_principal": "Teoria Pura do Direito (Reine Rechtslehre), 1934",
        "contribuicao": "Hierarquia normativa — a Constituição como norma fundamental (Grundnorm) que confere validade a todo o ordenamento. Criador do Tribunal Constitucional austríaco (1920).",
        "corrente": "Positivismo jurídico normativista",
        "relevancia_brasil": "Fundamento do controle de constitucionalidade concentrado (STF) e da hierarquia CF/88 → leis → decretos"
    },
    "bobbio": {
        "nome": "Norberto Bobbio",
        "datas": "1909–2004",
        "nacionalidade": "Italiano",
        "obra_principal": "Teoria do Ordenamento Jurídico (Teoria dell'ordinamento giuridico), 1960",
        "contribuicao": "Sistematização das antinomias jurídicas e seus critérios de resolução: lex superior, lex posterior, lex specialis. O ordenamento como sistema coerente, pleno e fechado.",
        "corrente": "Positivismo jurídico analítico",
        "relevancia_brasil": "Critérios de resolução de antinomias aplicados pelo STJ e STF — especialmente lex specialis (LGPD vs. PL 4/2025)"
    },
    "canaris": {
        "nome": "Claus-Wilhelm Canaris",
        "datas": "1937–2021",
        "nacionalidade": "Alemão",
        "obra_principal": "Pensamento Sistemático e Conceito de Sistema na Ciência do Direito (Systemdenken), 1969",
        "contribuicao": "Teoria da complementaridade normativa — normas que se reforçam mutuamente formam sistema coerente. Distinção entre lacunas autênticas e inautênticas.",
        "corrente": "Jurisprudência dos conceitos / Hermenêutica sistemática",
        "relevancia_brasil": "Fundamenta a interpretação sistemática do ordenamento digital brasileiro — LGPD + Marco Civil + ECA Digital como sistema coerente"
    },
    "montesquieu": {
        "nome": "Charles-Louis de Secondat, Barão de Montesquieu",
        "datas": "1689–1755",
        "nacionalidade": "Francês",
        "obra_principal": "Do Espírito das Leis (De l'Esprit des Lois), 1748",
        "contribuicao": "Primeira sistematização da separação dos três poderes (executivo, legislativo, judiciário) como garantia das liberdades individuais. Antecedentes: Aristóteles (Política, séc. IV a.C.) e Locke (Segundo Tratado, 1689).",
        "corrente": "Iluminismo jurídico-político",
        "relevancia_brasil": "CF/88 art. 2º — separação dos poderes tensionada pelo Tema 987 STF e pelos Decretos 12.975 e 12.976/2026"
    },
    "carlos_maximiliano": {
        "nome": "Carlos Maximiliano Pereira dos Santos",
        "datas": "1873–1960",
        "nacionalidade": "Brasileiro",
        "obra_principal": "Hermenêutica e Aplicação do Direito, 1924",
        "contribuicao": "Obra fundadora da hermenêutica jurídica brasileira. Síntese dos métodos: gramatical, lógico, histórico, sistemático e teleológico. Ainda referência obrigatória no STJ.",
        "corrente": "Hermenêutica jurídica clássica brasileira",
        "relevancia_brasil": "Referência direta em votos do STJ e STF — método de interpretação das normas digitais brasileiras"
    },
    "pontes_miranda": {
        "nome": "Francisco Cavalcanti Pontes de Miranda",
        "datas": "1892–1979",
        "nacionalidade": "Brasileiro",
        "obra_principal": "Tratado de Direito Privado (58 volumes), 1954–1969",
        "contribuicao": "Distinção tripartite: fato jurídico / ato jurídico / ato ilícito. Separação entre responsabilidade civil e ilicitude — superação do paradigma patrimonialista reparatório em favor do preventivo.",
        "corrente": "Pandectismo brasileiro / Teoria geral do direito privado",
        "relevancia_brasil": "Resgatado na reforma do CC (Código Civil — Lei 10.406/2002) em 2025 — virada paradigmática do patrimonialismo para a prevenção"
    },
    "savigny": {
        "nome": "Friedrich Carl von Savigny",
        "datas": "1779–1861",
        "nacionalidade": "Alemão",
        "obra_principal": "Sistema do Direito Romano Atual (System des heutigen römischen Rechts), 1840",
        "contribuicao": "Hermenêutica histórica — a lei deve ser interpretada pela intenção original do legislador e pelo espírito do povo (Volksgeist). Fundador da Escola Histórica do Direito.",
        "corrente": "Escola Histórica do Direito",
        "relevancia_brasil": "Influência no CC/1916 de Clóvis Beviláqua — interpretação originalista ainda presente na jurisprudência conservadora"
    },
    "ihering": {
        "nome": "Rudolf von Ihering",
        "datas": "1818–1892",
        "nacionalidade": "Alemão",
        "obra_principal": "O Fim no Direito (Der Zweck im Recht), 1877",
        "contribuicao": "Hermenêutica teleológica — a lei serve a fins sociais, não à intenção histórica. 'O fim é o criador de todo o direito.' Superação de Savigny.",
        "corrente": "Jurisprudência dos interesses / Hermenêutica teleológica",
        "relevancia_brasil": "Influência no CC/2002 (função social do contrato e da propriedade) e na interpretação teleológica da LGPD e do ECA Digital"
    },
    "gadamer": {
        "nome": "Hans-Georg Gadamer",
        "datas": "1900–2002",
        "nacionalidade": "Alemão",
        "obra_principal": "Verdade e Método (Wahrheit und Methode), 1960",
        "contribuicao": "Hermenêutica filosófica — fusão de horizontes: intérprete e texto se transformam mutuamente no ato de interpretação. O 'círculo hermenêutico' como método.",
        "corrente": "Hermenêutica filosófica / Fenomenologia",
        "relevancia_brasil": "Fundamenta as mutações constitucionais do STF — a CF/88 interpretada à luz de contextos históricos novos (tecnologia, IA, dados)"
    },
    "dworkin": {
        "nome": "Ronald Dworkin",
        "datas": "1931–2013",
        "nacionalidade": "Americano",
        "obra_principal": "O Império do Direito (Law's Empire), 1986",
        "contribuicao": "Teoria da integridade — o direito como romance em cadeia: cada decisão judicial continua a narrativa anterior, mantendo coerência de princípios. Distinção entre regras e princípios.",
        "corrente": "Pós-positivismo / Teoria dos princípios",
        "relevancia_brasil": "Influência direta na jurisprudência do STF — decisões como o Tema 987 como continuidade interpretativa dos direitos fundamentais, não ruptura"
    },
    "bakhtin": {
        "nome": "Mikhail Bakhtin",
        "datas": "1895–1975",
        "nacionalidade": "Russo",
        "obra_principal": "Problemas da Poética de Dostoiévski, 1929 / A Estética da Criação Verbal, 1979",
        "contribuicao": "Dialogismo e polifonia — múltiplas vozes que coexistem em tensão produtiva sem fusão em voz única autoritária. O romance polifônico como modelo epistemológico.",
        "corrente": "Teoria literária / Filosofia da linguagem",
        "relevancia_brasil": "Fundamento metodológico do Lex-IO-Graph — o ordenamento jurídico brasileiro como sistema polifônico: legislador, juiz, doutrinador, costume coexistindo em dialogismo pancrônico"
    }
}

# ---- Brocardos latinos ----
BROCARDOS = [
    {
        "original": "Lex superior derogat inferiori",
        "traducao_literal": "A lei superior derroga a inferior",
        "traducao_juridica": "Critério de resolução de antinomia por hierarquia normativa — norma de grau superior prevalece sobre a inferior",
        "contexto_romano": "Brocardo da teoria geral do direito — sistematizado por Kelsen (1881–1973) na hierarquia normativa",
        "uso_brasil": "Aplicado pelo STF (Supremo Tribunal Federal) no controle de constitucionalidade — CF/88 prevalece sobre leis ordinárias",
        "relacao_norma": "cf88"
    },
    {
        "original": "Lex posterior derogat priori",
        "traducao_literal": "A lei posterior derroga a anterior",
        "traducao_juridica": "Critério de resolução de antinomia por temporalidade — norma mais recente prevalece sobre a mais antiga de mesmo grau",
        "contexto_romano": "Brocardo romano clássico — um dos três critérios de Bobbio (1909–2004) para resolução de antinomias",
        "uso_brasil": "Aplicado na relação entre o CC/2002 e o Código Comercial de 1850 — o posterior absorveu o anterior",
        "relacao_norma": "lgpd"
    },
    {
        "original": "Lex specialis derogat generali",
        "traducao_literal": "A lei especial derroga a geral",
        "traducao_juridica": "Critério de resolução de antinomia por especialidade — norma específica prevalece sobre a geral",
        "contexto_romano": "Terceiro critério de Bobbio — o mais complexo, pois exige identificação do âmbito de aplicação de cada norma",
        "uso_brasil": "LGPD como lex specialis em relação ao PL 4/2025 (Livro VI CC Digital) — alerta da ANPD (Autoridade Nacional de Proteção de Dados)",
        "relacao_norma": "pl_cc_digital"
    },
    {
        "original": "Pacta sunt servanda",
        "traducao_literal": "Os pactos devem ser cumpridos",
        "traducao_juridica": "Princípio da força obrigatória dos contratos — base do direito contratual brasileiro (CC/2002 art. 421)",
        "contexto_romano": "Direito romano clássico — base do ius gentium (direito das gentes). Ulpiano (170–228 d.C.)",
        "uso_brasil": "Aplicado nos contratos de uso de plataformas digitais — termos de serviço como contratos de adesão sujeitos ao CDC (Código de Defesa do Consumidor)",
        "relacao_norma": "marco_civil"
    },
    {
        "original": "Alterum non laedere",
        "traducao_literal": "Não causar dano a outrem",
        "traducao_juridica": "Um dos três preceitos do direito de Ulpiano — base da responsabilidade civil extracontratual",
        "contexto_romano": "Ulpiano (170–228 d.C.) — Digesto de Justiniano (533 d.C.): 'Iuris praecepta sunt haec: honeste vivere, alterum non laedere, suum cuique tribuere'",
        "uso_brasil": "Fundamenta a responsabilidade por danos em ambiente digital — LGPD, Marco Civil e ECA Digital",
        "relacao_norma": "lgpd"
    },
    {
        "original": "In dubio pro infante",
        "traducao_literal": "Na dúvida, a favor da criança",
        "traducao_juridica": "Princípio da proteção integral — em qualquer interpretação que envolva menores, prevalece o interesse superior da criança",
        "contexto_romano": "Adaptação do brocardo romano ao direito da criança — incorporado à doutrina brasileira via Convenção da ONU sobre os Direitos da Criança (1989)",
        "uso_brasil": "ECA (Lei 8.069/1990) art. 3º e ECA Digital (Lei 15.211/2025) — fundamenta proibição de dark patterns direcionados a menores",
        "relacao_norma": "eca_digital"
    },
    {
        "original": "Nemo plus iuris ad alium transferre potest quam ipse habet",
        "traducao_literal": "Ninguém pode transferir a outrem mais direitos do que ele próprio tem",
        "traducao_juridica": "Princípio da nemo dat — limitação da transmissão de direitos sobre dados pessoais",
        "contexto_romano": "Ulpiano — Digesto 50.17.54. Base do direito real romano",
        "uso_brasil": "Aplicado no tratamento de dados pessoais — o controlador não pode transferir dados além do consentimento obtido do titular",
        "relacao_norma": "lgpd"
    },
    {
        "original": "Ubi jus ibi remedium",
        "traducao_literal": "Onde há direito, há remédio",
        "traducao_juridica": "Onde há violação de direito fundamental, deve haver tutela jurisdicional efetiva",
        "contexto_romano": "Brocardo do common law inglês (ubi jus ibi remedium) incorporado à tradição romano-germânica — base do direito de ação",
        "uso_brasil": "Fundamenta a intervenção do STF no Tema 987 — ante a omissão do legislativo, o judiciário provê o remédio constitucional",
        "relacao_norma": "stf_tema987"
    },
    {
        "original": "Habeas data",
        "traducao_literal": "Que tenha os dados",
        "traducao_juridica": "Ação constitucional para acesso e retificação de dados pessoais em registros públicos ou de caráter público",
        "contexto_romano": "Adaptação do habeas corpus (séc. XIII, Magna Carta inglesa) ao direito de informação — criado pela CF/88 art. 5º, LXXII",
        "uso_brasil": "Remédio constitucional brasileiro — precursor do direito de acesso e retificação da LGPD",
        "relacao_norma": "lgpd"
    }
]

# ---- Tradição jurídica comparada glocal ----
TRADICOES_JURIDICAS = {
    "romano_germanica": {
        "nome": "Tradição Romano-Germânica (Civil Law)",
        "paises": ["Brasil", "França", "Alemanha", "Itália", "Portugal", "Espanha", "Argentina"],
        "caracteristicas": "Direito codificado, primazia da lei escrita, papel secundário da jurisprudência (não vinculante formalmente), influência do direito romano via Corpus Iuris Civilis de Justiniano (533 d.C.) e do direito canônico medieval",
        "brasil": "Brasil herdou via Portugal — Ordenações Filipinas (1603) → CC/1916 (influência do BGB alemão, 1896) → CC/2002",
        "codigos_referencia": "BGB — Bürgerliches Gesetzbuch (Código Civil alemão, 1896); Code Civil (França, 1804 — Código Napoleônico); Codice Civile (Itália, 1942)"
    },
    "common_law": {
        "nome": "Tradição Anglo-Saxônica (Common Law)",
        "paises": ["Reino Unido", "Estados Unidos", "Canadá", "Austrália", "Índia"],
        "caracteristicas": "Primazia dos precedentes judiciais (stare decisis), direito construído caso a caso, ausência de codificação geral, flexibilidade interpretativa maior",
        "brasil": "Influência crescente via súmulas vinculantes do STF (EC 45/2004) e precedentes do CPC/2015 — aproximação híbrida com o common law",
        "codigos_referencia": "Magna Carta (1215); Habeas Corpus Act (1679); Bill of Rights (1689); US Constitution (1787)"
    },
    "judaico": {
        "nome": "Direito Judaico (Halachá)",
        "paises": ["Israel (sistema híbrido)", "comunidades judaicas globalmente"],
        "caracteristicas": (
            "Fontes: Torah, Talmude (Mishná + Guemará), responsa rabínica (teshuvot). "
            "3.000 anos de jurisprudência contínua — o sistema jurídico com registro "
            "ininterrupto mais antigo do mundo. Metodologia talmúdica: argumento e "
            "contra-argumento registrados simultaneamente — minoria preservada junto "
            "com maioria. Forma de polifonia bakhtiniana avant la lettre (Bakhtin, 1895–1975). "
            "Israel: sistema híbrido — Estado secular com tribunais rabínicos (Batei Din) "
            "com jurisdição exclusiva sobre casamento e divórcio de judeus."
        ),
        "brasil": (
            "Sem aplicação direta. Relevante para direito comparado glocal "
            "(global + local, Robertson, 1990s) e para o inventário pancrônico: "
            "a Halachá influenciou o direito canônico medieval e, via este, "
            "o direito civil europeu e brasileiro. O conceito de Tikkun Olam "
            "(reparação do mundo) dialoga com a virada preventiva do CC/2025 "
            "(resgate de Pontes de Miranda)."
        ),
        "codigos_referencia": (
            "Torah (séc. XIII–V a.C.); Mishná (200 d.C.); "
            "Talmude de Jerusalém (séc. IV d.C.); "
            "Talmude da Babilônia (séc. VI d.C.); "
            "Mishné Torá — Maimônides (1180 d.C.); "
            "Shulchan Aruch — Josef Karo (1565 d.C.)"
        )
    },
    "islamico": {
        "nome": "Direito Islâmico (Sharia)",
        "paises": ["Irã", "Arábia Saudita", "Paquistão (misto)", "Malásia (misto)"],
        "caracteristicas": "Fontes: Corão, Sunna, Ijma (consenso dos sábios), Qiyas (analogia jurídica). Hermenêutica própria: Usul al-Fiqh (fundamentos da jurisprudência islâmica). Não separa direito de religião — legitimidade normativa deriva de Deus",
        "brasil": "Sem aplicação direta — relevante para direito comparado e para análise glocal (global + local, Robertson, 1990s) do crescimento do islamismo na Europa e seus impactos no pluralismo jurídico",
        "codigos_referencia": "Corão (séc. VII d.C.); Hadith; Fiqh (jurisprudência islâmica clássica)"
    },
    "canonico": {
        "nome": "Direito Canônico Católico",
        "paises": ["Vaticano (Estado independente)", "aplicável a 1,3 bilhão de católicos globalmente"],
        "caracteristicas": "Corpus Iuris Canonici (séc. XII — Graciano). Código de Direito Canônico atual (1983). Distinção foro interno (consciência) / foro externo (atos jurídicos da Igreja). Influência histórica decisiva no direito civil europeu e brasileiro",
        "brasil": "Influência via Portugal — casamento canônico teve efeitos civis até 1916. Encíclica Magnifica Humanitas (Leão XIV, 25/05/2026) como vetor ético sobre IA com impacto no PL 2.338/2023",
        "codigos_referencia": "Decreto de Graciano (1140); Corpus Iuris Canonici (1582); Código de Direito Canônico (1983)"
    }
}

# ---- Encíclica Magnifica Humanitas ----
MAGNIFICA_HUMANITAS = {
    "titulo": "Magnifica Humanitas",
    "autor": "Papa Leão XIV (Robert Francis Prevost, 1955–)",
    "data": "25 de maio de 2026",
    "local": "Sala Nova do Sínodo, Vaticano",
    "tema_central": "Custódia da pessoa humana na era da Inteligência Artificial (IA)",
    "tese_principal": (
        "A IA precisa ser desarmada, livre das lógicas que a transformam em "
        "instrumento de dominação, exclusão ou morte. A tecnologia não é neutra — "
        "pode proteger ou ameaçar a dignidade humana. A escolha não é entre aceitar "
        "ou rejeitar a IA, mas entre usos que prejudicam ou protegem a dignidade humana."
    ),
    "capitulos": [
        "Cap. I — Doutrina Social da Igreja (DSI) e IA: teologia da comunhão na história",
        "Cap. II — Reconhecimento dos direitos das minorias, especialmente mulheres",
        "Cap. III — Cinco princípios da DSC: bem comum, solidariedade, subsidiariedade, participação, destinação universal dos bens",
        "Cap. IV — Ecologia da comunicação baseada na verdade; transparência nos algoritmos de seleção de conteúdo",
        "Cap. V — IA em conflitos armados: rejeição da automação de decisões sobre vida humana"
    ],
    "continuidade_historica": (
        "Leão XIII / Rerum Novarum (1891) → questão social da Revolução Industrial "
        "→ direitos trabalhistas → CLT brasileira (1943) → NR-1 com riscos psicossociais "
        "de IA (2026) → Leão XIV / Magnifica Humanitas (2026) → questão social da IA. "
        "Arco de 135 anos de magistério social católico sobre tecnologia e trabalho."
    ),
    "convergencia_maio_2026": (
        "Na semana de 21–27 de maio de 2026, três instâncias independentes convergiram "
        "no mesmo campo normativo: (1) Executivo brasileiro — Decretos 12.975 e 12.976/2026 "
        "sobre responsabilidade de plataformas; (2) Vaticano — Magnifica Humanitas sobre "
        "dignidade humana e IA; (3) Congresso — 24+ PDLs para derrubar os decretos. "
        "Momento civilizatório singular documentado."
    ),
    "presenca_anthropic": (
        "O evento de lançamento contou com a presença de Chris Olah, cofundador da Anthropic "
        "— criadora do Claude. Sinal do reconhecimento do Vaticano de que as empresas de IA "
        "são interlocutores normativos relevantes no debate sobre dignidade humana."
    ),
    "impacto_brasil": [
        "PL 2.338/2023 (Marco Legal da IA): reforço ético ao princípio da dignidade humana",
        "NR-1: convergência sobre riscos psicossociais de IA no trabalho",
        "Decretos 12.975 e 12.976/2026: convergência sobre responsabilidade de plataformas",
        "CF/88 art. 1º, III: dignidade humana como fundamento normativo supremo"
    ]
}
