from __future__ import annotations


MODULE_TITLE = "Interventies"


def _option_entries(labels: list[str]) -> list[dict[str, str]]:
    return [{"value": chr(97 + index), "label": label} for index, label in enumerate(labels)]


def _build_multi_select(
    *,
    title: str,
    topic_title: str,
    concept_title: str,
    prompt: str,
    question: str,
    option_labels: list[str],
    correct_labels: list[str],
    instructions: str = "Selecteer alle juiste onderdelen.",
    difficulty: str = "intro",
) -> dict:
    options = _option_entries(option_labels)
    correct_values = [option["value"] for option in options if option["label"] in correct_labels]
    return {
        "title": title,
        "exercise_type": "multi_select",
        "mode_support": "learn,exam",
        "difficulty": difficulty,
        "module_title": MODULE_TITLE,
        "topic_title": topic_title,
        "concept_title": concept_title,
        "instructions": instructions,
        "prompt": prompt,
        "content": {
            "question": question,
            "options": options,
            "model_answer": "Juiste onderdelen: " + ", ".join(correct_labels) + ".",
        },
        "scoring": {"correct_options": correct_values},
        "max_score": 100,
        "requires_manual_review": False,
    }


def _build_study_card(
    *,
    title: str,
    topic_title: str,
    concept_title: str,
    prompt: str,
    question: str,
    model_answer: str,
    difficulty: str = "core",
) -> dict:
    return {
        "title": title,
        "exercise_type": "study_card",
        "mode_support": "learn",
        "difficulty": difficulty,
        "module_title": MODULE_TITLE,
        "topic_title": topic_title,
        "concept_title": concept_title,
        "instructions": "Beantwoord de vraag in je eigen woorden en vergelijk daarna met het modelantwoord.",
        "prompt": prompt,
        "content": {
            "question": question,
            "placeholder": "Schrijf hier je antwoord...",
            "model_answer": model_answer,
        },
        "scoring": {},
        "max_score": 100,
        "requires_manual_review": False,
    }


MODULE12_STRUCTURE = [
    {
        "topic": "Verandermodel van NLP",
        "subheading_distractors": ["Strategieën", "Ankeren"],
        "concepts": [
            {
                "concept": "Fasen",
                "distractors": ["Constructivisme", "Nominalisaties"],
                "terms": [
                    {
                        "term": "Analyse",
                        "questions": [
                            (
                                "Wat betekent analyse binnen het veranderproces van NLP?",
                                "Analyse betekent dat eerst onderzocht wordt wat de huidige situatie is, wat het probleem precies inhoudt en hoe de bestaande ervaring of het gedrag is opgebouwd.",
                            ),
                            (
                                "Waarom is analyse de eerste fase?",
                                "Omdat gerichte verandering pas mogelijk is wanneer duidelijk is wat er precies speelt en welke patronen daarin een rol spelen.",
                            ),
                            (
                                "Wat wordt er in de analysefase in kaart gebracht?",
                                "De beginsituatie, de structuur van de ervaring, het doel van verandering en de factoren die het probleem of patroon in stand houden.",
                            ),
                            (
                                "Waarom is analyse belangrijk voor effectieve interventie?",
                                "Omdat een interventie beter werkt wanneer die aansluit op de werkelijke oorzaak, structuur en context van het probleem.",
                            ),
                        ],
                    },
                    {
                        "term": "Hulpbronnen",
                        "questions": [
                            (
                                "Wat zijn hulpbronnen in het NLP-verandermodel?",
                                "Hulpbronnen zijn innerlijke of uiterlijke middelen die iemand nodig heeft om tot verandering te komen, zoals gevoelens, overtuigingen, vaardigheden, herinneringen of steun uit de omgeving.",
                            ),
                            (
                                "Waarom zijn hulpbronnen belangrijk?",
                                "Omdat verandering makkelijker en duurzamer wordt wanneer iemand toegang heeft tot de juiste mentale, emotionele of gedragsmatige ondersteuning.",
                            ),
                            (
                                "Welke vormen kunnen hulpbronnen aannemen?",
                                "Bijvoorbeeld zelfvertrouwen, rust, focus, moed, flexibiliteit, positieve ervaringen of steun van anderen.",
                            ),
                            (
                                "Wat gebeurt er als hulpbronnen ontbreken?",
                                "Dan wordt verandering moeilijker, omdat iemand onvoldoende innerlijke of uiterlijke basis ervaart om anders te reageren.",
                            ),
                        ],
                    },
                    {
                        "term": "Interventie",
                        "questions": [
                            (
                                "Wat is een interventie binnen NLP?",
                                "Een interventie is een doelgerichte techniek of handeling die bedoeld is om een verandering in beleving, betekenis, gedrag of toestand op gang te brengen.",
                            ),
                            (
                                "Waarom komt interventie pas na analyse en hulpbronnen?",
                                "Omdat eerst duidelijk moet zijn wat er speelt en welke ondersteuning nodig is voordat een techniek effectief kan worden ingezet.",
                            ),
                            (
                                "Waarop richt een interventie zich meestal?",
                                "Op de structuur van subjectieve ervaring, zoals betekenisgeving, emoties, interne representaties, overtuigingen of gedragspatronen.",
                            ),
                            (
                                "Wat maakt een interventie effectief?",
                                "Dat ze goed aansluit op het doel, de context, de persoon en de onderliggende structuur van het probleem.",
                            ),
                        ],
                    },
                    {
                        "term": "Verandering",
                        "questions": [
                            (
                                "Wat betekent verandering in het NLP-verandermodel?",
                                "Verandering betekent dat er een verschuiving optreedt in beleving, gedrag, betekenis, emotie of reactiepatroon.",
                            ),
                            (
                                "Wanneer is er echt sprake van verandering?",
                                "Wanneer iemand niet alleen iets begrijpt, maar ook anders ervaart, anders reageert of andere keuzes maakt in relevante situaties.",
                            ),
                            (
                                "Waarom is verandering meer dan inzicht alleen?",
                                "Omdat inzicht pas waarde krijgt als het zich vertaalt in een andere innerlijke ervaring of een ander gedragspatroon.",
                            ),
                            (
                                "Wat is het doel van deze fase?",
                                "Dat het nieuwe patroon of de nieuwe ervaring daadwerkelijk beschikbaar en bruikbaar wordt in het dagelijks leven.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Belangrijke interventies",
        "subheading_distractors": ["Emoties en toestanden", "Feedback"],
        "concepts": [
            {
                "concept": "Technieken",
                "distractors": ["Ecologie", "Universal quantifiers"],
                "terms": [
                    {
                        "term": "Transfer of a resource",
                        "questions": [
                            (
                                "Wat is transfer of a resource?",
                                "Transfer of a resource is een techniek waarbij een hulpbron uit een situatie waarin die al aanwezig is wordt overgebracht naar een andere situatie waarin die hulpbron nodig is.",
                            ),
                            (
                                "Waarom is deze techniek nuttig?",
                                "Omdat iemand zo toegang krijgt tot gevoelens of kwaliteiten die al bestaan, maar nog niet beschikbaar zijn in de probleemcontext.",
                            ),
                            (
                                "Welke hulpbronnen kunnen worden overgebracht?",
                                "Bijvoorbeeld rust, zelfvertrouwen, kracht, helderheid, moed of concentratie.",
                            ),
                            (
                                "Wat is het doel van transfer of a resource?",
                                "Dat iemand in een moeilijke situatie kan beschikken over een meer helpende toestand of kwaliteit.",
                            ),
                        ],
                    },
                    {
                        "term": "Neuro-logische niveaus",
                        "questions": [
                            (
                                "Wat zijn neuro-logische niveaus?",
                                "Neuro-logische niveaus zijn verschillende lagen waarop menselijke ervaring en verandering kunnen worden bekeken, zoals omgeving, gedrag, vaardigheden, overtuigingen, identiteit en missie of zingeving.",
                            ),
                            (
                                "Waarom zijn neuro-logische niveaus belangrijk?",
                                "Omdat ze helpen om te bepalen op welk niveau een probleem speelt en op welk niveau verandering nodig is.",
                            ),
                            (
                                "Wat is het nut van denken in niveaus?",
                                "Het maakt zichtbaar dat niet elk probleem op hetzelfde niveau opgelost hoeft te worden als waar het zich uit.",
                            ),
                            (
                                "Waarom zijn deze niveaus relevant voor interventies?",
                                "Omdat een interventie vaak effectiever is wanneer die wordt ingezet op het juiste niveau van ervaring of betekenis.",
                            ),
                        ],
                    },
                    {
                        "term": "Uitlijnen van logische niveaus",
                        "questions": [
                            (
                                "Wat betekent het uitlijnen van logische niveaus?",
                                "Het betekent dat de verschillende niveaus van ervaring beter op elkaar afgestemd worden, zodat er minder innerlijk conflict is.",
                            ),
                            (
                                "Waarom is uitlijning belangrijk?",
                                "Omdat spanning of blokkade vaak ontstaat wanneer gedrag, overtuigingen, identiteit en doelen niet goed met elkaar overeenkomen.",
                            ),
                            (
                                "Wat gebeurt er als niveaus niet zijn uitgelijnd?",
                                "Dan kan iemand tegenstrijdigheid ervaren, zoals iets willen op gedragsniveau maar zichzelf op identiteitsniveau tegenhouden.",
                            ),
                            (
                                "Wat is het doel van deze interventie?",
                                "Meer congruentie, duidelijkheid en innerlijke samenhang.",
                            ),
                        ],
                    },
                    {
                        "term": "Fast phobia cure",
                        "questions": [
                            (
                                "Wat is fast phobia cure?",
                                "Fast phobia cure is een NLP-techniek die bedoeld is om de emotionele intensiteit van een fobische of traumatische reactie snel te verminderen.",
                            ),
                            (
                                "Waarop is deze techniek gebaseerd?",
                                "Op dissociatie, herstructurering van de innerlijke ervaring en het veranderen van de manier waarop een herinnering wordt beleefd.",
                            ),
                            (
                                "Waarom werkt afstand hierin vaak helpend?",
                                "Omdat de emotionele lading meestal afneemt wanneer iemand niet volledig geassocieerd in de ervaring blijft.",
                            ),
                            (
                                "Wat is het doel van fast phobia cure?",
                                "Dat iemand op een rustiger en minder automatisch angstige manier op de trigger of herinnering kan reageren.",
                            ),
                        ],
                    },
                    {
                        "term": "Spatial reframe",
                        "questions": [
                            (
                                "Wat is spatial reframe?",
                                "Spatial reframe is een techniek waarbij fysieke ruimte wordt gebruikt om verschillende perspectieven, betekenissen of delen van een ervaring zichtbaar en voelbaar te maken.",
                            ),
                            (
                                "Waarom is ruimte hierbij belangrijk?",
                                "Omdat ruimtelijke positionering helpt om ervaring letterlijk anders te ordenen en daardoor nieuwe inzichten of betekenissen mogelijk maakt.",
                            ),
                            (
                                "Wat kan spatial reframe opleveren?",
                                "Meer afstand, nieuw perspectief, betere afweging of een andere beleving van het probleem.",
                            ),
                            (
                                "Wat is het doel van deze techniek?",
                                "Dat iemand via ruimtelijk werken tot een andere interpretatie of keuze komt.",
                            ),
                        ],
                    },
                    {
                        "term": "Swish pattern",
                        "questions": [
                            (
                                "Wat is het swish pattern?",
                                "Het swish pattern is een techniek waarbij een ongewenste interne voorstelling wordt vervangen door een aantrekkelijker, krachtiger of gewenster beeld van jezelf of de situatie.",
                            ),
                            (
                                "Waarom is deze techniek effectief?",
                                "Omdat ze snel invloed kan uitoefenen op automatische associaties en gedragsneigingen.",
                            ),
                            (
                                "Wat verandert er bij een swish?",
                                "De koppeling tussen een trigger en de oude reactie wordt onderbroken en vervangen door een andere innerlijke richting.",
                            ),
                            (
                                "Wat is het doel van het swish pattern?",
                                "Dat iemand spontaner beweegt richting gewenst gedrag in plaats van richting het oude patroon.",
                            ),
                        ],
                    },
                    {
                        "term": "Collapsing anchors",
                        "questions": [
                            (
                                "Wat zijn collapsing anchors?",
                                "Collapsing anchors is een techniek waarbij een ongewenste toestand en een krachtige hulpbrontoestand tegelijk worden geactiveerd, zodat de oude lading kan veranderen of oplossen.",
                            ),
                            (
                                "Waarom werkt deze techniek met ankers?",
                                "Omdat ankers specifieke toestanden kunnen oproepen, en het gelijktijdig activeren van tegengestelde toestanden een verschuiving kan veroorzaken.",
                            ),
                            (
                                "Wanneer is collapsing anchors nuttig?",
                                "Wanneer een ongewenste emotionele reactie verminderd moet worden door er een sterkere, helpende toestand tegenover te zetten.",
                            ),
                            (
                                "Wat is het doel van collapsing anchors?",
                                "Het verzwakken van een oud probleemanker en het versterken van een meer gewenste innerlijke toestand.",
                            ),
                        ],
                    },
                    {
                        "term": "Herkaderen",
                        "questions": [
                            (
                                "Wat is herkaderen?",
                                "Herkaderen is het veranderen van de betekenis van een ervaring of gedrag door die in een ander kader of perspectief te plaatsen.",
                            ),
                            (
                                "Waarom is herkaderen krachtig?",
                                "Omdat dezelfde situatie anders kan voelen en ander gedrag kan oproepen wanneer de betekenis verandert.",
                            ),
                            (
                                "Wat verandert er precies bij herkaderen?",
                                "Niet noodzakelijk de feiten, maar wel de interpretatie en de emotionele of gedragsmatige uitwerking ervan.",
                            ),
                            (
                                "Wat is het doel van herkaderen?",
                                "Meer keuzevrijheid, minder automatische beperking en een functionelere manier van kijken naar de situatie.",
                            ),
                        ],
                    },
                    {
                        "term": "Tijdlijnen",
                        "questions": [
                            (
                                "Wat zijn tijdlijnen in NLP?",
                                "Tijdlijnen zijn de innerlijke manier waarop mensen hun verleden, heden en toekomst organiseren en beleven.",
                            ),
                            (
                                "Waarom zijn tijdlijnen relevant voor interventies?",
                                "Omdat ervaringen uit verleden en toekomst invloed hebben op gedrag, emotie en betekenis in het heden.",
                            ),
                            (
                                "Wat kun je doen met tijdlijnen?",
                                "Je kunt gebeurtenissen herordenen, emotionele lading veranderen, toekomstbeelden versterken of oude ervaringen anders integreren.",
                            ),
                            (
                                "Wat is het doel van werken met tijdlijnen?",
                                "Dat iemand vrijer en bewuster omgaat met verleden, heden en toekomst, en daardoor anders kan kiezen en reageren.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
]


def _topic_summary(concepts: list[dict]) -> str:
    return "Onderwerpen in dit leerpaddeel: " + ", ".join(
        concept["concept"] for concept in concepts
    ) + "."


def _concept_summary(terms: list[dict]) -> str:
    return ", ".join(term["term"] for term in terms) + "."


def build_module12_topics() -> list[dict]:
    return [
        {
            "title": topic["topic"],
            "summary": _topic_summary(topic["concepts"]),
            "concepts": [
                {
                    "title": concept["concept"],
                    "summary": _concept_summary(concept["terms"]),
                    "tags": [term["term"].lower() for term in concept["terms"]],
                }
                for concept in topic["concepts"]
            ],
        }
        for topic in MODULE12_STRUCTURE
    ]


MODULE12_TOPIC_BLUEPRINT = build_module12_topics()


def build_module12_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE12_STRUCTURE]
    heading_options = topic_names + [
        "Ankeren",
        "Strategieën",
    ]
    exercises = [
        _build_multi_select(
            title="Interventies - hoofdstukkoppen",
            topic_title=MODULE12_STRUCTURE[0]["topic"],
            concept_title=MODULE12_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk Interventies?",
            question="Selecteer de koppen die bij het hoofdstuk Interventies horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE12_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"Interventies - {topic['topic']} subkoppen",
                topic_title=topic["topic"],
                concept_title=topic["concepts"][0]["concept"],
                prompt=topic.get("subheading_prompt", "Welke subkoppen vallen onder deze kop?"),
                question=topic.get("subheading_prompt", "Welke subkoppen vallen onder deze kop?"),
                option_labels=concept_names + topic.get("subheading_distractors", []),
                correct_labels=concept_names,
            )
        )

        for concept in topic["concepts"]:
            term_names = [term["term"] for term in concept["terms"]]
            exercises.append(
                _build_multi_select(
                    title=f"Interventies - {concept['concept']} termen",
                    topic_title=topic["topic"],
                    concept_title=concept["concept"],
                    prompt=f"Welke termen vallen onder de subkop {concept['concept']}?",
                    question=f"Selecteer de termen die horen bij de subkop {concept['concept']}.",
                    option_labels=term_names + concept.get("distractors", []),
                    correct_labels=term_names,
                )
            )

            for term in concept["terms"]:
                for question_index, (question, model_answer) in enumerate(
                    term["questions"], start=1
                ):
                    exercises.append(
                        _build_study_card(
                            title=(
                                "Interventies - "
                                f"{concept['concept']} - {term['term']} - vraag {question_index}"
                            ),
                            topic_title=topic["topic"],
                            concept_title=concept["concept"],
                            prompt=question,
                            question=question,
                            model_answer=model_answer,
                        )
                    )

    return exercises