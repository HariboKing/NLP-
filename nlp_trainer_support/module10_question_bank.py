from __future__ import annotations


MODULE_TITLE = "Strategieën ontcijferen"


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


MODULE10_STRUCTURE = [
    {
        "topic": "Strategieën",
        "subheading_distractors": ["Emoties en toestanden", "Feedback"],
        "concepts": [
            {
                "concept": "Basis",
                "distractors": ["Nominalisaties", "Constructivisme"],
                "terms": [
                    {
                        "term": "Zintuiglijke sequenties",
                        "questions": [
                            (
                                "Wat zijn zintuiglijke sequenties?",
                                "Zintuiglijke sequenties zijn de volgordes waarin iemand intern beelden, geluiden, gevoelens en andere representaties doorloopt tijdens denken en handelen.",
                            ),
                            (
                                "Waarom zijn zintuiglijke sequenties belangrijk?",
                                "Omdat ze laten zien hoe een bepaalde uitkomst stap voor stap intern wordt opgebouwd.",
                            ),
                            (
                                "Wat kun je leren uit zintuiglijke sequenties?",
                                "Je kunt ontdekken hoe iemand tot een keuze, gevoel of gedrag komt.",
                            ),
                            (
                                "Waarom zijn zintuiglijke sequenties relevant binnen NLP?",
                                "Omdat NLP ervan uitgaat dat subjectieve ervaring een structuur heeft en dat die structuur onderzocht en veranderd kan worden.",
                            ),
                        ],
                    },
                    {
                        "term": "TOTE-model",
                        "questions": [
                            (
                                "Waar staat TOTE voor?",
                                "TOTE staat voor Test, Operate, Test, Exit.",
                            ),
                            (
                                "Wat beschrijft het TOTE-model?",
                                "Het beschrijft hoe gedrag en strategie verlopen via een cyclisch proces van toetsen, handelen, opnieuw toetsen en stoppen wanneer het doel is bereikt.",
                            ),
                            (
                                "Waarom is het TOTE-model belangrijk?",
                                "Omdat het laat zien dat gedrag niet willekeurig is, maar gericht verloopt via feedback en bijsturing.",
                            ),
                            (
                                "Wat is het voordeel van denken in TOTE?",
                                "Dat je beter begrijpt hoe mensen acties aanpassen totdat een gewenst resultaat bereikt is.",
                            ),
                        ],
                    },
                    {
                        "term": "Gedragsstrategie",
                        "questions": [
                            (
                                "Wat is een gedragsstrategie?",
                                "Een gedragsstrategie is het interne en externe stappenplan waarmee iemand een bepaald gedrag of resultaat tot stand brengt.",
                            ),
                            (
                                "Waarom is een gedragsstrategie belangrijk?",
                                "Omdat het verklaart hoe iemand consequent tot een bepaalde reactie of uitkomst komt.",
                            ),
                            (
                                "Wat kun je met inzicht in gedragsstrategieën?",
                                "Je kunt succesvolle strategieën herkennen, modelleren, verbeteren of vervangen.",
                            ),
                            (
                                "Hoe hangt gedragsstrategie samen met verandering?",
                                "Wanneer je de strategie kent, kun je gericht ingrijpen in de stappen die tot het gedrag leiden.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Elicitatie",
                "distractors": ["Ecologie", "Universal quantifiers"],
                "terms": [
                    {
                        "term": "Strategie-eliciteren",
                        "questions": [
                            (
                                "Wat betekent strategie-eliciteren?",
                                "Strategie-eliciteren betekent dat je onderzoekt welke interne stappen iemand gebruikt om tot een bepaald gedrag of resultaat te komen.",
                            ),
                            (
                                "Waarom is strategie-eliciteren nuttig?",
                                "Omdat het zichtbaar maakt hoe iemand denkt, voelt en intern schakelt tijdens een proces.",
                            ),
                            (
                                "Wat probeer je met eliciteren te achterhalen?",
                                "De volgorde van representaties, beslissende schakels en terugkerende patronen in iemands strategie.",
                            ),
                            (
                                "Waarom past eliciteren goed binnen NLP?",
                                "Omdat NLP gericht is op het blootleggen van de structuur van subjectieve ervaring.",
                            ),
                        ],
                    },
                    {
                        "term": "Sequentie vinden",
                        "questions": [
                            (
                                "Wat betekent het om een sequentie te vinden?",
                                "Het betekent dat je de juiste volgorde van interne en externe stappen in een strategie ontdekt.",
                            ),
                            (
                                "Waarom is de volgorde belangrijk?",
                                "Omdat de kracht van een strategie vaak zit in de precieze opeenvolging van de stappen.",
                            ),
                            (
                                "Wat gebeurt er als de sequentie onduidelijk blijft?",
                                "Dan wordt het moeilijk om de strategie goed te begrijpen, te herhalen of te veranderen.",
                            ),
                            (
                                "Wat levert het vinden van de sequentie op?",
                                "Een beter inzicht in hoe een bepaald gedrag tot stand komt en waar verandering mogelijk is.",
                            ),
                        ],
                    },
                    {
                        "term": "Notatie",
                        "questions": [
                            (
                                "Wat is notatie bij strategieën?",
                                "Notatie is de manier waarop een strategie gestructureerd wordt opgeschreven met symbolen of aanduidingen voor interne stappen.",
                            ),
                            (
                                "Waarom is notatie nuttig?",
                                "Omdat notatie helpt om een strategie overzichtelijk, analyseerbaar en overdraagbaar te maken.",
                            ),
                            (
                                "Wat leg je vast in een notatie?",
                                "De volgorde van representatiesystemen, beslismomenten en eventuele terugkoppelingen in de strategie.",
                            ),
                            (
                                "Waarom helpt notatie bij verandering?",
                                "Omdat je pas gericht kunt aanpassen wat eerst helder in kaart is gebracht.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Toepassing",
                "distractors": ["Zelfonderzoek", "Rapport"],
                "terms": [
                    {
                        "term": "Ontdekken",
                        "questions": [
                            (
                                "Wat betekent ontdekken in het werken met strategieën?",
                                "Ontdekken betekent dat je een bestaande strategie zichtbaar maakt en leert begrijpen.",
                            ),
                            (
                                "Waarom is ontdekken de eerste stap?",
                                "Omdat je een strategie pas kunt beïnvloeden wanneer je weet hoe die werkt.",
                            ),
                            (
                                "Wat ontdek je precies?",
                                "Je ontdekt welke interne stappen, volgordes en schakelingen bijdragen aan een bepaald gedrag of resultaat.",
                            ),
                            (
                                "Waarom is ontdekken belangrijk voor bewuste keuzes?",
                                "Omdat onbewuste patronen pas veranderd kunnen worden als ze eerst bewust worden gemaakt.",
                            ),
                        ],
                    },
                    {
                        "term": "Gebruiken",
                        "questions": [
                            (
                                "Wat betekent gebruiken in dit onderdeel?",
                                "Gebruiken betekent dat je een eenmaal herkende strategie doelgericht inzet in een situatie waarin die nuttig is.",
                            ),
                            (
                                "Waarom is het gebruiken van strategieën waardevol?",
                                "Omdat effectieve strategieën herhaalbaar worden en daardoor bewuster inzetbaar zijn.",
                            ),
                            (
                                "Wat kun je gebruiken uit een strategie?",
                                "Je kunt de volgorde, de interne schakels of de beslissende elementen gebruiken om prestaties of gedrag te ondersteunen.",
                            ),
                            (
                                "Wanneer is bewust gebruiken belangrijk?",
                                "Wanneer je niet toevallig, maar doelgericht invloed wilt uitoefenen op denken en handelen.",
                            ),
                        ],
                    },
                    {
                        "term": "Veranderen",
                        "questions": [
                            (
                                "Wat betekent het om een strategie te veranderen?",
                                "Dat je onderdelen van de strategie aanpast zodat er een andere ervaring, keuze of gedragsuitkomst ontstaat.",
                            ),
                            (
                                "Waarom zou je een strategie willen veranderen?",
                                "Omdat sommige strategieën onhandig, beperkend of ineffectief zijn.",
                            ),
                            (
                                "Wat kun je veranderen in een strategie?",
                                "Bijvoorbeeld de volgorde van stappen, de inhoud van representaties of de schakel die een beslissing triggert.",
                            ),
                            (
                                "Wat is het doel van strategieverandering?",
                                "Meer keuzevrijheid, effectiever gedrag en een beter passend resultaat.",
                            ),
                        ],
                    },
                    {
                        "term": "Installeren",
                        "questions": [
                            (
                                "Wat betekent installeren in het werken met strategieën?",
                                "Installeren betekent dat een nieuwe of aangepaste strategie wordt ingebouwd zodat deze beschikbaar wordt in toekomstige situaties.",
                            ),
                            (
                                "Waarom is installeren belangrijk?",
                                "Omdat inzicht of verandering pas echt waarde krijgt wanneer het ook duurzaam toepasbaar wordt.",
                            ),
                            (
                                "Wat wordt er eigenlijk geïnstalleerd?",
                                "Een nieuwe volgorde van denken, voelen en reageren die een gewenste uitkomst ondersteunt.",
                            ),
                            (
                                "Wat is het verschil tussen veranderen en installeren?",
                                "Veranderen gaat over het aanpassen van de strategie; installeren gaat over het verankeren en beschikbaar maken van die nieuwe strategie.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Voorbeelden",
                "distractors": ["Constructivisme", "Koppelingen"],
                "terms": [
                    {
                        "term": "Stressmanagement",
                        "questions": [
                            (
                                "Waarom is stressmanagement een voorbeeld van strategiewerk?",
                                "Omdat stress vaak samenhangt met een terugkerende interne strategie van denken, voelen en reageren.",
                            ),
                            (
                                "Wat kun je ontdekken in een stressstrategie?",
                                "Welke beelden, gedachten, gevoelens en interne schakelingen stress versterken of juist verminderen.",
                            ),
                            (
                                "Hoe helpt strategie-inzicht bij stressmanagement?",
                                "Het maakt zichtbaar waar je kunt ingrijpen om sneller naar een meer helpende toestand te schakelen.",
                            ),
                            (
                                "Wat is het doel van stressmanagement binnen NLP?",
                                "Niet alleen stress begrijpen, maar ook de interne strategie zo beïnvloeden dat iemand meer rust en keuzevrijheid krijgt.",
                            ),
                        ],
                    },
                    {
                        "term": "Motivatie",
                        "questions": [
                            (
                                "Waarom is motivatie een voorbeeld van een strategie?",
                                "Omdat motivatie vaak niet toevallig ontstaat, maar voortkomt uit een herkenbare interne volgorde van beelden, betekenissen en gevoelens.",
                            ),
                            (
                                "Wat kun je onderzoeken bij motivatie?",
                                "Welke representaties, woorden en gevoelens ervoor zorgen dat iemand in beweging komt of juist afhaakt.",
                            ),
                            (
                                "Hoe helpt een strategiebenadering bij motivatie?",
                                "Door inzicht te geven in hoe motivatie wordt opgebouwd en welke schakels versterkt kunnen worden.",
                            ),
                            (
                                "Wat is het voordeel van motivatie als strategie zien?",
                                "Dat motivatie niet alleen als karaktereigenschap wordt gezien, maar als iets dat onderzocht en beïnvloed kan worden.",
                            ),
                        ],
                    },
                    {
                        "term": "Besluitvorming",
                        "questions": [
                            (
                                "Waarom is besluitvorming een strategie?",
                                "Omdat beslissingen vaak voortkomen uit een vaste interne volgorde van afwegen, voorstellen, voelen en kiezen.",
                            ),
                            (
                                "Wat kun je ontdekken in een besluitvormingsstrategie?",
                                "Welke stappen iemand doorloopt voordat er een keuze wordt gemaakt.",
                            ),
                            (
                                "Hoe kan strategie-inzicht besluitvorming verbeteren?",
                                "Door zichtbaar te maken welke stappen helpend zijn en welke juist verwarring, uitstel of twijfel veroorzaken.",
                            ),
                            (
                                "Wat is het doel van werken met besluitvormingsstrategieën?",
                                "Bewustere keuzes maken en effectiever leren omgaan met innerlijke afwegingen.",
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


def build_module10_topics() -> list[dict]:
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
        for topic in MODULE10_STRUCTURE
    ]


MODULE10_TOPIC_BLUEPRINT = build_module10_topics()


def build_module10_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE10_STRUCTURE]
    heading_options = topic_names + [
        "NLP technieken",
        "Over emoties en states (toestanden)",
    ]
    exercises = [
        _build_multi_select(
            title="Strategieën ontcijferen: het pad naar bewuste keuzes en verandering - hoofdstukkoppen",
            topic_title=MODULE10_STRUCTURE[0]["topic"],
            concept_title=MODULE10_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk Strategieën ontcijferen: het pad naar bewuste keuzes en verandering?",
            question="Selecteer de koppen die bij het hoofdstuk Strategieën ontcijferen: het pad naar bewuste keuzes en verandering horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE10_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"Strategieën ontcijferen: het pad naar bewuste keuzes en verandering - {topic['topic']} subkoppen",
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
                    title=f"Strategieën ontcijferen: het pad naar bewuste keuzes en verandering - {concept['concept']} termen",
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
                                "Strategieën ontcijferen: het pad naar bewuste keuzes en verandering - "
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