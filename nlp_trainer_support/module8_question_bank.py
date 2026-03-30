from __future__ import annotations


MODULE_TITLE = "Emoties en states"


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


MODULE8_STRUCTURE = [
    {
        "topic": "Emoties en toestanden",
        "subheading_distractors": ["Feedback", "Outcome frame"],
        "concepts": [
            {
                "concept": "Kern",
                "distractors": ["Constructivisme", "Nominalisaties"],
                "terms": [
                    {
                        "term": "State",
                        "questions": [
                            (
                                "Wat wordt bedoeld met een state?",
                                "Een state is de totale innerlijke toestand waarin iemand zich op een bepaald moment bevindt. Die toestand bestaat uit gevoelens, gedachten, lichamelijke spanning, focus en energie.",
                            ),
                            (
                                "Waarom is een state belangrijk?",
                                "Omdat een state sterk beïnvloedt hoe iemand denkt, voelt, waarneemt en handelt. Dezelfde situatie kan heel anders worden beleefd vanuit een andere state.",
                            ),
                            (
                                "Is een state blijvend of veranderlijk?",
                                "Een state is veranderlijk. Mensen kunnen van toestand wisselen door ervaringen, gedachten, taal, lichaamshouding of externe prikkels.",
                            ),
                            (
                                "Hoe hangt een state samen met gedrag?",
                                "Gedrag komt vaak voort uit de state waarin iemand zich bevindt. Een krachtige of rustige state leidt vaak tot ander gedrag dan een angstige of gespannen state.",
                            ),
                        ],
                    },
                    {
                        "term": "Emotionele schakeling",
                        "questions": [
                            (
                                "Wat is emotionele schakeling?",
                                "Emotionele schakeling is het proces waarbij iemand van de ene emotionele toestand naar de andere overgaat.",
                            ),
                            (
                                "Waarom is emotionele schakeling relevant?",
                                "Omdat mensen niet vastzitten in één emotie. Ze kunnen leren herkennen hoe emoties veranderen en hoe ze daar invloed op kunnen uitoefenen.",
                            ),
                            (
                                "Waardoor kan emotionele schakeling ontstaan?",
                                "Door gedachten, herinneringen, taal, lichamelijke veranderingen, prikkels uit de omgeving of contact met andere mensen.",
                            ),
                            (
                                "Wat is het nut van inzicht in emotionele schakeling?",
                                "Het helpt om beter te begrijpen hoe emoties ontstaan, hoe ze veranderen en hoe je sneller kunt schakelen naar een meer helpende toestand.",
                            ),
                        ],
                    },
                    {
                        "term": "Invloed",
                        "questions": [
                            (
                                "Wat betekent invloed in dit hoofdstuk?",
                                "Invloed betekent dat emoties en states niet alleen vanzelf ontstaan, maar ook beïnvloed kunnen worden.",
                            ),
                            (
                                "Waarop hebben emoties en states invloed?",
                                "Op waarneming, denken, communicatie, gedrag, keuzes en prestaties.",
                            ),
                            (
                                "Waarop kun je zelf invloed uitoefenen bij states?",
                                "Op je focus, taalgebruik, lichaamshouding, ademhaling, betekenisgeving en de manier waarop je met situaties omgaat.",
                            ),
                            (
                                "Waarom is invloed een belangrijk begrip binnen NLP?",
                                "Omdat NLP ervan uitgaat dat innerlijke ervaring veranderbaar is en dat mensen meer keuzemogelijkheden krijgen wanneer ze invloed leren uitoefenen op hun toestand.",
                            ),
                        ],
                    },
                    {
                        "term": "Regulatie",
                        "questions": [
                            (
                                "Wat is regulatie?",
                                "Regulatie is het vermogen om emoties en states bewust te sturen, te beïnvloeden of te stabiliseren.",
                            ),
                            (
                                "Waarom is regulatie belangrijk?",
                                "Omdat het helpt om niet volledig door emoties overspoeld te raken, maar bewustere keuzes te maken in hoe je reageert.",
                            ),
                            (
                                "Wat valt onder emotionele regulatie?",
                                "Bijvoorbeeld het herkennen van je toestand, het bijsturen van je focus, het veranderen van betekenis, het inzetten van ademhaling of het opwekken van een meer helpende state.",
                            ),
                            (
                                "Wat levert goede regulatie op?",
                                "Meer stabiliteit, meer keuzevrijheid, betere communicatie en effectiever gedrag in lastige of belangrijke situaties.",
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


def build_module8_topics() -> list[dict]:
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
        for topic in MODULE8_STRUCTURE
    ]


MODULE8_TOPIC_BLUEPRINT = build_module8_topics()


def build_module8_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE8_STRUCTURE]
    heading_options = topic_names + [
        "De kracht van excellente communicatie",
        "De ontdekking van het zelf",
    ]
    exercises = [
        _build_multi_select(
            title="Over emoties en states (toestanden) - hoofdstukkoppen",
            topic_title=MODULE8_STRUCTURE[0]["topic"],
            concept_title=MODULE8_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk Over emoties en states (toestanden)?",
            question="Selecteer de koppen die bij het hoofdstuk Over emoties en states (toestanden) horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE8_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"Over emoties en states (toestanden) - {topic['topic']} subkoppen",
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
                    title=f"Over emoties en states (toestanden) - {concept['concept']} termen",
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
                                "Over emoties en states (toestanden) - "
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