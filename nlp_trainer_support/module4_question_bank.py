from __future__ import annotations


MODULE_TITLE = "De verborgen wereld van metaforen"


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


MODULE4_STRUCTURE = [
    {
        "topic": "Metaforen",
        "subheading_distractors": ["Het metamodel", "Taal en neurologie"],
        "concepts": [
            {
                "concept": "Soorten",
                "distractors": ["Nominalisaties", "Constructivisme"],
                "terms": [
                    {
                        "term": "Homomorfisch",
                        "questions": [
                            (
                                "Wat is een homomorfische metafoor?",
                                "Een homomorfische metafoor is een metafoor waarin slechts een deel van de structuur van de ene situatie overeenkomt met de andere situatie.",
                            ),
                            (
                                "Waarom heet deze metafoor homomorfisch?",
                                "Omdat er sprake is van een gedeeltelijke overeenkomst in vorm of structuur, maar niet van een volledige parallel.",
                            ),
                            (
                                "Wat is het nut van een homomorfische metafoor?",
                                "Het nut is dat je een idee of ervaring begrijpelijk maakt door een gedeeltelijk vergelijkbare situatie te gebruiken.",
                            ),
                            (
                                "Wanneer gebruik je een homomorfische metafoor?",
                                "Je gebruikt deze wanneer een volledige één-op-één vergelijking niet nodig is, maar een gedeeltelijke overeenkomst genoeg is om inzicht te geven.",
                            ),
                        ],
                    },
                    {
                        "term": "Isomorfisch",
                        "questions": [
                            (
                                "Wat is een isomorfische metafoor?",
                                "Een isomorfische metafoor is een metafoor waarin de structuur van het verhaal of beeld sterk overeenkomt met de structuur van de situatie waarop het betrekking heeft.",
                            ),
                            (
                                "Waarom is een isomorfische metafoor krachtig?",
                                "Omdat de onderliggende structuur vrijwel gelijk is, waardoor de boodschap diep en herkenbaar kan binnenkomen.",
                            ),
                            (
                                "Wat is het verschil tussen homomorfisch en isomorfisch?",
                                "Bij homomorfisch is er een gedeeltelijke overeenkomst, terwijl bij isomorfisch de structuur veel vollediger overeenkomt.",
                            ),
                            (
                                "Wanneer is een isomorfische metafoor bruikbaar?",
                                "Wanneer je een ervaring of probleem indirect wilt spiegelen op een manier die sterk aansluit bij iemands situatie.",
                            ),
                        ],
                    },
                    {
                        "term": "Cultureel",
                        "questions": [
                            (
                                "Wat is een culturele metafoor?",
                                "Een culturele metafoor is een metafoor die betekenis ontleent aan gedeelde culturele beelden, verhalen, symbolen of gebruiken.",
                            ),
                            (
                                "Waarom werken culturele metaforen vaak snel?",
                                "Omdat mensen binnen dezelfde cultuur de onderliggende verwijzing vaak direct herkennen en begrijpen.",
                            ),
                            (
                                "Wat is een risico van culturele metaforen?",
                                "Dat ze minder goed werken of verkeerd begrepen worden door mensen met een andere culturele achtergrond.",
                            ),
                            (
                                "Waarom is context belangrijk bij culturele metaforen?",
                                "Omdat de betekenis afhankelijk is van gedeelde kennis, normen en symbolen binnen een bepaalde groep.",
                            ),
                        ],
                    },
                    {
                        "term": "Universeel",
                        "questions": [
                            (
                                "Wat is een universele metafoor?",
                                "Een universele metafoor is een metafoor die aansluit bij ervaringen of beelden die voor vrijwel alle mensen herkenbaar zijn.",
                            ),
                            (
                                "Waarom zijn universele metaforen breed toepasbaar?",
                                "Omdat ze gebaseerd zijn op algemene menselijke ervaringen, zoals groei, reis, licht, donker, strijd of verandering.",
                            ),
                            (
                                "Wat maakt een metafoor universeel?",
                                "Dat de kernbetekenis los van cultuur, leeftijd of achtergrond begrijpelijk blijft.",
                            ),
                            (
                                "Wanneer is een universele metafoor extra nuttig?",
                                "Wanneer je een boodschap wilt overbrengen aan een breed publiek of in een context met verschillende achtergronden.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Functie",
                "distractors": ["Reflectie en communicatie", "Ethiek en verantwoordelijkheid"],
                "terms": [
                    {
                        "term": "Indirecte communicatie",
                        "questions": [
                            (
                                "Wat is de functie van metaforen in indirecte communicatie?",
                                "Metaforen maken het mogelijk om een boodschap indirect over te brengen zonder deze letterlijk uit te spreken.",
                            ),
                            (
                                "Waarom kan indirecte communicatie effectief zijn?",
                                "Omdat iemand minder snel in weerstand schiet wanneer een boodschap niet rechtstreeks confronterend wordt gebracht.",
                            ),
                            (
                                "Hoe helpen metaforen om weerstand te verminderen?",
                                "Ze verschuiven de aandacht van het directe probleem naar een verhaal of beeld, waardoor de boodschap veiliger ontvangen kan worden.",
                            ),
                            (
                                "Wanneer is indirecte communicatie met metaforen nuttig?",
                                "Vooral wanneer een onderwerp gevoelig ligt of wanneer directe taal te hard, te abstract of te bedreigend zou zijn.",
                            ),
                        ],
                    },
                    {
                        "term": "Verandering",
                        "questions": [
                            (
                                "Hoe kunnen metaforen verandering ondersteunen?",
                                "Metaforen kunnen een nieuw perspectief openen, waardoor iemand een situatie anders gaat zien en anders kan beleven.",
                            ),
                            (
                                "Waarom zijn metaforen geschikt voor veranderingsprocessen?",
                                "Omdat ze niet alleen informatie geven, maar ook gevoel, betekenis en innerlijke beweging oproepen.",
                            ),
                            (
                                "Hoe draagt een metafoor bij aan herinterpretatie?",
                                "Door een ervaring in een ander kader te plaatsen, zodat nieuwe keuzes of betekenissen mogelijk worden.",
                            ),
                            (
                                "Waarom is dit relevant binnen NLP?",
                                "Omdat NLP veel werkt met betekenisverandering, perspectiefwisseling en het herstructureren van subjectieve ervaring.",
                            ),
                        ],
                    },
                    {
                        "term": "Betekenis",
                        "questions": [
                            (
                                "Welke rol speelt betekenis in metaforen?",
                                "Metaforen geven betekenis aan ervaringen door ze te koppelen aan een beeld, verhaal of vergelijking.",
                            ),
                            (
                                "Waarom is betekenisgeving zo belangrijk bij metaforen?",
                                "Omdat de kracht van een metafoor niet alleen in het beeld zit, maar vooral in wat dat beeld voor iemand betekent.",
                            ),
                            (
                                "Hoe kan een metafoor de betekenis van een situatie veranderen?",
                                "Door dezelfde ervaring in een nieuw kader te plaatsen, waardoor iemand er anders over gaat denken en voelen.",
                            ),
                            (
                                "Waarom verschilt de betekenis van een metafoor per persoon?",
                                "Omdat iedereen metaforen begrijpt vanuit zijn eigen ervaringen, overtuigingen en wereldmodel.",
                            ),
                        ],
                    },
                    {
                        "term": "Verbeelding",
                        "questions": [
                            (
                                "Waarom is verbeelding belangrijk bij metaforen?",
                                "Omdat metaforen innerlijke beelden oproepen en daarmee direct de verbeeldingskracht aanspreken.",
                            ),
                            (
                                "Hoe helpt verbeelding bij het begrijpen van een metafoor?",
                                "Verbeelding maakt het mogelijk om een abstract idee concreet en beleefbaar te maken in het innerlijk van de luisteraar.",
                            ),
                            (
                                "Waarom kan verbeelding emotionele impact versterken?",
                                "Omdat beelden en symbolen vaak directer binnenkomen dan droge, letterlijke uitleg.",
                            ),
                            (
                                "Wat is de relatie tussen verbeelding en verandering?",
                                "Verbeelding maakt nieuwe innerlijke ervaringen mogelijk, en dat kan bijdragen aan een andere betekenis, een ander gevoel en ander gedrag.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
]


def _topic_summary(concepts: list[dict]) -> str:
    return "Onderwerpen in dit leerpaddeel: " + ", ".join(concept["concept"] for concept in concepts) + "."


def _concept_summary(terms: list[dict]) -> str:
    return ", ".join(term["term"] for term in terms) + "."


def build_module4_topics() -> list[dict]:
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
        for topic in MODULE4_STRUCTURE
    ]


MODULE4_TOPIC_BLUEPRINT = build_module4_topics()


def build_module4_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE4_STRUCTURE]
    heading_options = topic_names + [
        "De kunst van magische taalpatronen",
        "Wereldmodellen van NLP",
    ]
    exercises = [
        _build_multi_select(
            title="De verborgen wereld van de metaforen - hoofdstukkoppen",
            topic_title=MODULE4_STRUCTURE[0]["topic"],
            concept_title=MODULE4_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk De verborgen wereld van de metaforen?",
            question="Selecteer de koppen die bij het hoofdstuk De verborgen wereld van de metaforen horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE4_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"De verborgen wereld van de metaforen - {topic['topic']} subkoppen",
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
                    title=f"De verborgen wereld van de metaforen - {concept['concept']} termen",
                    topic_title=topic["topic"],
                    concept_title=concept["concept"],
                    prompt=f"Welke termen vallen onder de subkop {concept['concept']}?",
                    question=f"Selecteer de termen die horen bij de subkop {concept['concept']}.",
                    option_labels=term_names + concept.get("distractors", []),
                    correct_labels=term_names,
                )
            )

            for term in concept["terms"]:
                for question_index, (question, model_answer) in enumerate(term["questions"], start=1):
                    exercises.append(
                        _build_study_card(
                            title=(
                                f"De verborgen wereld van de metaforen - {concept['concept']} - {term['term']} - vraag {question_index}"
                            ),
                            topic_title=topic["topic"],
                            concept_title=concept["concept"],
                            prompt=question,
                            question=question,
                            model_answer=model_answer,
                        )
                    )

    return exercises