from __future__ import annotations


MODULE_TITLE = "NLP en spiritualiteit"


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


MODULE13_STRUCTURE = [
    {
        "topic": "Spiritueel NLP",
        "subheading_distractors": ["Interventies", "Ankeren"],
        "concepts": [
            {
                "concept": "Principes",
                "distractors": ["Ecologie", "Nominalisaties"],
                "terms": [
                    {
                        "term": "Woordgebruik",
                        "questions": [
                            (
                                "Waarom is woordgebruik belangrijk binnen spiritueel NLP?",
                                "Omdat woorden niet neutraal zijn. Ze beïnvloeden hoe iemand betekenis geeft aan ervaringen, zichzelf ziet en met anderen omgaat.",
                            ),
                            (
                                "Hoe kan woordgebruik iemands innerlijke wereld beïnvloeden?",
                                "Woorden sturen aandacht, gevoel en interpretatie. Daardoor kunnen ze iemand versterken of juist beperken.",
                            ),
                            (
                                "Waarom vraagt spiritueel NLP om bewust taalgebruik?",
                                "Omdat bewuste taal helpt om zorgvuldiger, respectvoller en helderder om te gaan met jezelf en anderen.",
                            ),
                            (
                                "Wat is het doel van zorgvuldig woordgebruik?",
                                "Dat communicatie meer in lijn komt met bewustzijn, verantwoordelijkheid en innerlijke rust.",
                            ),
                        ],
                    },
                    {
                        "term": "Eigenwaarde",
                        "questions": [
                            (
                                "Wat betekent eigenwaarde binnen spiritueel NLP?",
                                "Eigenwaarde is het gevoel dat je jezelf als waardevol en betekenisvol kunt ervaren, los van voortdurende goedkeuring van buitenaf.",
                            ),
                            (
                                "Waarom is eigenwaarde belangrijk?",
                                "Omdat een stabiele eigenwaarde helpt om minder afhankelijk te zijn van oordeel, afwijzing of externe bevestiging.",
                            ),
                            (
                                "Hoe hangt eigenwaarde samen met persoonlijke groei?",
                                "Wie zichzelf meer waardeert, durft eerlijker te kijken naar gedrag, verantwoordelijkheid te nemen en zich verder te ontwikkelen.",
                            ),
                            (
                                "Wat is het effect van gezonde eigenwaarde op communicatie?",
                                "Dat iemand vaak rustiger, minder defensief en duidelijker in contact met anderen staat.",
                            ),
                        ],
                    },
                    {
                        "term": "Niets persoonlijk nemen",
                        "questions": [
                            (
                                "Wat betekent het principe 'niets persoonlijk nemen'?",
                                "Het betekent dat je reacties, woorden of gedrag van anderen niet automatisch opvat als een directe uitspraak over jouw waarde als persoon.",
                            ),
                            (
                                "Waarom is dit principe belangrijk?",
                                "Omdat het helpt om minder snel gekwetst, defensief of emotioneel meegesleept te worden door wat anderen doen of zeggen.",
                            ),
                            (
                                "Wat verandert er wanneer je minder persoonlijk neemt?",
                                "Je krijgt meer innerlijke rust, meer afstand en meer ruimte om bewuster te reageren.",
                            ),
                            (
                                "Betekent 'niets persoonlijk nemen' dat niets je meer raakt?",
                                "Nee. Het betekent niet dat je gevoelloos wordt, maar dat je minder snel alles koppelt aan je identiteit of eigenwaarde.",
                            ),
                        ],
                    },
                    {
                        "term": "Aannames vermijden",
                        "questions": [
                            (
                                "Wat betekent het om aannames te vermijden?",
                                "Dat je niet te snel invult wat iets betekent, wat iemand bedoelt of wat waar zou zijn zonder dat eerst zorgvuldig te onderzoeken.",
                            ),
                            (
                                "Waarom is dit belangrijk binnen spiritueel NLP?",
                                "Omdat aannames vaak leiden tot misverstanden, onrust, verkeerde conclusies en onnodig lijden.",
                            ),
                            (
                                "Wat is het effect van minder aannames maken?",
                                "Dat je helderder kijkt, preciezer communiceert en meer open blijft voor wat werkelijk aan de hand is.",
                            ),
                            (
                                "Hoe kun je aannames vermijden in de praktijk?",
                                "Door vragen te stellen, concreet waar te nemen en betekenis niet te snel als feit te behandelen.",
                            ),
                        ],
                    },
                    {
                        "term": "Altijd je best doen",
                        "questions": [
                            (
                                "Wat betekent het principe 'altijd je best doen'?",
                                "Het betekent dat je handelt vanuit oprechte inzet, binnen de mogelijkheden en omstandigheden van dat moment.",
                            ),
                            (
                                "Waarom is dit principe waardevol?",
                                "Omdat het helpt om verantwoordelijkheid te nemen zonder jezelf voortdurend te veroordelen op basis van perfectie.",
                            ),
                            (
                                "Betekent 'je best doen' altijd hetzelfde niveau presteren?",
                                "Nee. Je best doen kan per moment verschillen, afhankelijk van energie, context, draagkracht en omstandigheden.",
                            ),
                            (
                                "Wat is het effect van dit principe op innerlijke houding?",
                                "Dat het meer rust, eerlijkheid en zelfacceptatie kan brengen, terwijl je toch gericht blijft op groei en zorgvuldigheid.",
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


def build_module13_topics() -> list[dict]:
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
        for topic in MODULE13_STRUCTURE
    ]


MODULE13_TOPIC_BLUEPRINT = build_module13_topics()


def build_module13_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE13_STRUCTURE]
    heading_options = topic_names + [
        "Interventies",
        "Ankeren",
    ]
    exercises = [
        _build_multi_select(
            title="NLP en spiritualiteit - hoofdstukkoppen",
            topic_title=MODULE13_STRUCTURE[0]["topic"],
            concept_title=MODULE13_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk NLP en spiritualiteit?",
            question="Selecteer de koppen die bij het hoofdstuk NLP en spiritualiteit horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE13_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"NLP en spiritualiteit - {topic['topic']} subkoppen",
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
                    title=f"NLP en spiritualiteit - {concept['concept']} termen",
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
                                "NLP en spiritualiteit - "
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