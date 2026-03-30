from __future__ import annotations


MODULE_TITLE = "NLP technieken"


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


MODULE9_STRUCTURE = [
    {
        "topic": "Technieken",
        "subheading_distractors": ["Feedback", "Outcome frame"],
        "concepts": [
            {
                "concept": "Perceptuele posities",
                "distractors": ["Nominalisaties", "Constructivisme"],
                "terms": [
                    {
                        "term": "Eerste positie",
                        "questions": [
                            (
                                "Wat is de eerste positie?",
                                "De eerste positie is de beleving vanuit jezelf. Je kijkt, voelt en denkt vanuit je eigen perspectief en eigen ervaring.",
                            ),
                            (
                                "Waarom is de eerste positie belangrijk?",
                                "Omdat deze positie contact geeft met je eigen gevoelens, behoeften, gedachten en grenzen.",
                            ),
                            (
                                "Wat is een voordeel van de eerste positie?",
                                "Dat je duidelijker ervaart wat iets persoonlijk voor jou betekent.",
                            ),
                            (
                                "Wat is een risico van te veel eerste positie?",
                                "Dat je zo sterk in je eigen ervaring zit dat je minder goed ziet wat er bij de ander gebeurt.",
                            ),
                        ],
                    },
                    {
                        "term": "Tweede positie",
                        "questions": [
                            (
                                "Wat is de tweede positie?",
                                "De tweede positie is het innemen van het perspectief van de ander. Je probeert de situatie te ervaren alsof je de ander bent.",
                            ),
                            (
                                "Waarom is de tweede positie belangrijk?",
                                "Omdat deze positie empathie, begrip en afstemming bevordert.",
                            ),
                            (
                                "Wat leer je in de tweede positie?",
                                "Je leert hoe de ander mogelijk denkt, voelt en de situatie beleeft.",
                            ),
                            (
                                "Wat is een risico van te veel tweede positie?",
                                "Dat je te veel opgaat in de ander en het contact met je eigen grenzen of perspectief verliest.",
                            ),
                        ],
                    },
                    {
                        "term": "Derde positie",
                        "questions": [
                            (
                                "Wat is de derde positie?",
                                "De derde positie is de observerende positie. Je kijkt als het ware van buitenaf naar de interactie tussen jezelf en de ander.",
                            ),
                            (
                                "Waarom is de derde positie belangrijk?",
                                "Omdat deze positie overzicht, afstand en objectiever inzicht geeft in wat er gebeurt.",
                            ),
                            (
                                "Wat is het voordeel van de derde positie?",
                                "Dat je patronen, interacties en verhoudingen beter kunt zien zonder direct in de emotie te zitten.",
                            ),
                            (
                                "Wat helpt de derde positie te ontwikkelen?",
                                "Het helpt om rustiger te analyseren, bewuster te kiezen en minder automatisch te reageren.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Associatie en dissociatie",
                "distractors": ["Ecologie", "Universal quantifiers"],
                "terms": [
                    {
                        "term": "In ervaring stappen",
                        "questions": [
                            (
                                "Wat betekent in ervaring stappen?",
                                "In ervaring stappen betekent dat je geassocieerd bent: je beleeft een herinnering of situatie alsof je er weer middenin zit.",
                            ),
                            (
                                "Wat kenmerkt een geassocieerde ervaring?",
                                "Dat je de ervaring vanuit je eigen ogen beleeft en de gevoelens direct opnieuw kunt voelen.",
                            ),
                            (
                                "Waarom is associatie belangrijk?",
                                "Omdat het helpt om ervaringen intens te voelen, hulpbronnen op te roepen en contact te maken met emotionele betekenis.",
                            ),
                            (
                                "Wat is een risico van sterke associatie?",
                                "Dat overweldigende gevoelens opnieuw te sterk worden ervaren.",
                            ),
                        ],
                    },
                    {
                        "term": "Afstand nemen",
                        "questions": [
                            (
                                "Wat betekent afstand nemen?",
                                "Afstand nemen betekent dat je dissocieert: je kijkt als het ware van buitenaf naar een ervaring in plaats van die volledig opnieuw te beleven.",
                            ),
                            (
                                "Waarom is dissociatie nuttig?",
                                "Omdat het helpt om rustiger, objectiever en met meer overzicht naar een ervaring te kijken.",
                            ),
                            (
                                "Wanneer is afstand nemen handig?",
                                "Vooral bij heftige, beladen of stressvolle ervaringen waarbij te veel emotionele betrokkenheid onhandig is.",
                            ),
                            (
                                "Wat is het effect van dissociatie?",
                                "Dat de emotionele intensiteit vaak afneemt en reflectie gemakkelijker wordt.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Eye Accessing Cues",
                "distractors": ["Kritisch reflecteren", "Verbeelding"],
                "terms": [
                    {
                        "term": "Oogbewegingen",
                        "questions": [
                            (
                                "Wat zijn eye accessing cues?",
                                "Eye accessing cues zijn oogbewegingen die binnen NLP worden gezien als aanwijzingen voor hoe iemand op dat moment informatie intern verwerkt.",
                            ),
                            (
                                "Waarom zijn oogbewegingen relevant?",
                                "Omdat ze een aanwijzing kunnen geven of iemand beelden opbouwt, geluiden oproept of gevoelens ervaart.",
                            ),
                            (
                                "Wat kun je met oogbewegingen observeren?",
                                "Welke representatiesystemen iemand mogelijk gebruikt tijdens denken, herinneren of construeren.",
                            ),
                            (
                                "Waarom moet je voorzichtig zijn met interpretatie van oogbewegingen?",
                                "Omdat oogbewegingen aanwijzingen zijn en geen absoluut bewijs; context en individu blijven belangrijk.",
                            ),
                        ],
                    },
                    {
                        "term": "Visuele constructie",
                        "questions": [
                            (
                                "Wat is visuele constructie?",
                                "Visuele constructie is het innerlijk opbouwen van beelden die niet letterlijk worden herinnerd, maar worden samengesteld of bedacht.",
                            ),
                            (
                                "Wanneer gebruikt iemand visuele constructie?",
                                "Wanneer iemand zich iets voorstelt, visualiseert of een nieuw beeld mentaal creëert.",
                            ),
                            (
                                "Waarom is visuele constructie belangrijk binnen NLP?",
                                "Omdat innerlijke beelden invloed hebben op beleving, verwachting en gedrag.",
                            ),
                            (
                                "Hoe verschilt visuele constructie van visuele herinnering?",
                                "Bij constructie wordt een beeld samengesteld, terwijl bij herinnering een bestaand beeld wordt teruggehaald.",
                            ),
                        ],
                    },
                    {
                        "term": "Auditieve toegang",
                        "questions": [
                            (
                                "Wat is auditieve toegang?",
                                "Auditieve toegang is het innerlijk oproepen of verwerken van geluiden, woorden, stemmen of andere auditieve informatie.",
                            ),
                            (
                                "Wanneer is auditieve toegang actief?",
                                "Wanneer iemand luistert naar innerlijke dialoog, een stem herinnert of geluiden mentaal oproept.",
                            ),
                            (
                                "Waarom is auditieve toegang relevant?",
                                "Omdat auditieve verwerking invloed heeft op betekenisgeving, herinnering en communicatie.",
                            ),
                            (
                                "Hoe herken je auditieve toegang in taal?",
                                "Vaak aan auditieve woorden zoals horen, zeggen, klinken, luisteren of bespreken.",
                            ),
                        ],
                    },
                    {
                        "term": "Kinesthetische toegang",
                        "questions": [
                            (
                                "Wat is kinesthetische toegang?",
                                "Kinesthetische toegang is het innerlijk oproepen of ervaren van gevoelens, lichamelijke sensaties en emotionele beleving.",
                            ),
                            (
                                "Waarom is kinesthetische toegang belangrijk?",
                                "Omdat gevoelens en lichaamssensaties een grote rol spelen in de manier waarop mensen ervaringen betekenis geven.",
                            ),
                            (
                                "Wanneer gebruikt iemand kinesthetische toegang?",
                                "Wanneer iemand zich afstemt op gevoel, spanning, aanraking, emotie of lichamelijke reactie.",
                            ),
                            (
                                "Hoe kan kinesthetische toegang zichtbaar worden in communicatie?",
                                "Vaak via woorden die verwijzen naar voelen, aanraken, zwaar, licht, spanning of rust.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Submodaliteiten",
                "distractors": ["Zelfonderzoek", "Satir-condities"],
                "terms": [
                    {
                        "term": "Contrastanalyse",
                        "questions": [
                            (
                                "Wat is contrastanalyse?",
                                "Contrastanalyse is het vergelijken van twee innerlijke ervaringen om te ontdekken welke submodaliteiten verschillen.",
                            ),
                            (
                                "Waarom is contrastanalyse belangrijk?",
                                "Omdat het zichtbaar maakt welke specifieke verschillen verantwoordelijk kunnen zijn voor een verschil in beleving.",
                            ),
                            (
                                "Wat vergelijk je bij contrastanalyse?",
                                "Bijvoorbeeld een prettige en een onprettige ervaring, of een gemotiveerde en een ongemotiveerde toestand.",
                            ),
                            (
                                "Wat levert contrastanalyse op?",
                                "Inzicht in welke interne kenmerken aangepast kunnen worden om de ervaring te beïnvloeden.",
                            ),
                        ],
                    },
                    {
                        "term": "Drivers",
                        "questions": [
                            (
                                "Wat zijn drivers binnen submodaliteiten?",
                                "Drivers zijn de submodaliteiten die de sterkste invloed hebben op hoe een ervaring wordt beleefd.",
                            ),
                            (
                                "Waarom zijn drivers belangrijk?",
                                "Omdat juist die elementen vaak de grootste verandering veroorzaken als je ze aanpast.",
                            ),
                            (
                                "Hoe ontdek je drivers?",
                                "Door systematisch te onderzoeken welke verandering in een beeld, geluid of gevoel de meeste impact heeft.",
                            ),
                            (
                                "Wat is het voordeel van het kennen van drivers?",
                                "Dat je gerichter en efficiënter invloed kunt uitoefenen op beleving en toestand.",
                            ),
                        ],
                    },
                    {
                        "term": "Bouwstenen van perceptie",
                        "questions": [
                            (
                                "Wat wordt bedoeld met bouwstenen van perceptie?",
                                "Daarmee worden de kleinere onderdelen bedoeld waaruit innerlijke ervaring is opgebouwd, zoals grootte, helderheid, afstand, toon, volume of intensiteit.",
                            ),
                            (
                                "Waarom zijn submodaliteiten bouwstenen van perceptie?",
                                "Omdat ze bepalen hoe een ervaring intern is samengesteld en dus hoe die ervaring gevoeld en begrepen wordt.",
                            ),
                            (
                                "Waarom is dit belangrijk binnen NLP?",
                                "Omdat verandering in deze bouwstenen vaak leidt tot verandering in de totale ervaring.",
                            ),
                            (
                                "Wat is het voordeel van werken met bouwstenen van perceptie?",
                                "Dat je subjectieve ervaring heel precies kunt onderzoeken en gericht kunt beïnvloeden.",
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


def build_module9_topics() -> list[dict]:
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
        for topic in MODULE9_STRUCTURE
    ]


MODULE9_TOPIC_BLUEPRINT = build_module9_topics()


def build_module9_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE9_STRUCTURE]
    heading_options = topic_names + [
        "Over emoties en states (toestanden)",
        "De kracht van excellente communicatie",
    ]
    exercises = [
        _build_multi_select(
            title="NLP technieken - hoofdstukkoppen",
            topic_title=MODULE9_STRUCTURE[0]["topic"],
            concept_title=MODULE9_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk NLP technieken?",
            question="Selecteer de koppen die bij het hoofdstuk NLP technieken horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE9_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"NLP technieken - {topic['topic']} subkoppen",
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
                    title=f"NLP technieken - {concept['concept']} termen",
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
                                "NLP technieken - "
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