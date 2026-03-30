from __future__ import annotations


MODULE_TITLE = "Ankeren"


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


MODULE11_STRUCTURE = [
    {
        "topic": "Conditionering en associatie",
        "subheading_distractors": ["Strategieën", "Emoties en toestanden"],
        "concepts": [
            {
                "concept": "Invloeden",
                "distractors": ["Nominalisaties", "Constructivisme"],
                "terms": [
                    {
                        "term": "Pavlov",
                        "questions": [
                            (
                                "Wie was Pavlov?",
                                "Ivan Pavlov was een Russische fysioloog en psycholoog die beroemd werd door zijn onderzoek naar klassieke conditionering.",
                            ),
                            (
                                "Waar draaide Pavlovs onderzoek om?",
                                "Zijn onderzoek liet zien hoe een neutrale stimulus, zoals een bel, gekoppeld kan worden aan een onvoorwaardelijke stimulus, zoals voedsel, totdat die neutrale stimulus zelfstandig een geconditioneerde respons oproept.",
                            ),
                            (
                                "Wat toonde het beroemde experiment met de hond aan?",
                                "Dat de hond uiteindelijk al ging kwijlen bij het horen van de bel, ook zonder voedsel. Daarmee werd zichtbaar hoe associaties tussen stimulus en respons worden aangeleerd.",
                            ),
                            (
                                "Waarom is Pavlov belangrijk voor ankeren?",
                                "Omdat ankeren in NLP voortbouwt op het idee dat een specifieke stimulus later opnieuw een bepaalde reactie of stemming kan oproepen.",
                            ),
                        ],
                    },
                    {
                        "term": "Skinner",
                        "questions": [
                            (
                                "Wie was Skinner?",
                                "Burrhus Frederic Skinner was een Amerikaanse psycholoog die bekend werd door zijn werk op het gebied van behaviorisme en operante conditionering.",
                            ),
                            (
                                "Wat is operante conditionering volgens Skinner?",
                                "Operante conditionering houdt in dat gedrag wordt versterkt of verzwakt door de consequenties die erop volgen, zoals beloning of straf.",
                            ),
                            (
                                "Wat liet de Skinner-box zien?",
                                "Dat dieren een specifieke handeling leren uitvoeren om een beloning te krijgen, waarmee de principes van gedragsversterking zichtbaar werden gemaakt.",
                            ),
                            (
                                "Waarom is Skinner relevant in dit hoofdstuk?",
                                "Omdat zijn werk laat zien hoe gedrag gevormd en herhaald wordt door consequenties, wat aansluit bij leren, conditionering en gedragsverandering.",
                            ),
                        ],
                    },
                    {
                        "term": "Watson",
                        "questions": [
                            (
                                "Wie was John B. Watson?",
                                "John B. Watson was een Amerikaanse psycholoog die bekend werd door zijn werk rond klassieke conditionering en het Little Albert-experiment.",
                            ),
                            (
                                "Wat onderzocht Watson met Little Albert?",
                                "Hij onderzocht of het mogelijk was om bij een jong kind een angstreactie of fobie te conditioneren door een neutrale stimulus te koppelen aan een hard, schrikachtig geluid.",
                            ),
                            (
                                "Wat liet het experiment zien?",
                                "Dat angstresponsen aangeleerd kunnen worden en gekoppeld kunnen raken aan specifieke stimuli.",
                            ),
                            (
                                "Waarom is Watson van belang voor ankeren?",
                                "Omdat zijn werk laat zien hoe sterke emotionele reacties aan een prikkel gekoppeld kunnen worden, wat nauw aansluit bij het principe van ankers en triggers.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Ankeren",
                "distractors": ["Ecologie", "Universal quantifiers"],
                "terms": [
                    {
                        "term": "Stimulus-respons",
                        "questions": [
                            (
                                "Wat betekent stimulus-respons in ankeren?",
                                "Het betekent dat een specifieke prikkel een bepaalde reactie oproept. In ankeren wordt een stimulus gekoppeld aan een emotionele staat of stemming.",
                            ),
                            (
                                "Welke vormen kan zo'n stimulus hebben?",
                                'Dat kan bijvoorbeeld een woord, beeld, aanraking of ander zintuiglijk signaal zijn.',
                            ),
                            (
                                "Waarom is stimulus-respons belangrijk voor ankeren?",
                                "Omdat het de basis vormt van hoe een anker werkt: een prikkel wordt verbonden met een gewenste of ongewenste reactie en kan die later opnieuw oproepen.",
                            ),
                            (
                                "Wat bepaalt mede de kracht van de respons?",
                                "De intensiteit van de ervaring, de timing van het anker, de precisie van de stimulus en de herhaling ervan.",
                            ),
                        ],
                    },
                    {
                        "term": "Conditionering",
                        "questions": [
                            (
                                "Wat is conditionering in de context van ankeren?",
                                "Conditionering is het proces waarbij een stimulus verbonden raakt met een bepaalde reactie, zodat die reactie later opnieuw kan worden opgeroepen.",
                            ),
                            (
                                "Moet conditionering altijd lang duren?",
                                "Nee. Ankers hoeven niet altijd over een lange periode geconditioneerd te worden; een enkele intense leerervaring kan al voldoende zijn.",
                            ),
                            (
                                "Welke rol speelt herhaling?",
                                "Herhaling kan een anker versterken en de koppeling tussen stimulus en stemming nauwkeuriger en sneller oproepbaar maken.",
                            ),
                            (
                                "Waarom is conditionering relevant voor NLP?",
                                "Omdat NLP ervan uitgaat dat ook interne ervaringen, zoals beelden, gevoelens en innerlijke dialoog, als responsen kunnen functioneren en dus geankerd kunnen worden.",
                            ),
                        ],
                    },
                    {
                        "term": "Contextverandering",
                        "questions": [
                            (
                                "Wat betekent contextverandering bij ankeren?",
                                "Het betekent dat een hulpbron, stemming of reactie uit de ene context beschikbaar gemaakt wordt in een andere context waarin die nuttig is.",
                            ),
                            (
                                "Waarom is contextverandering belangrijk?",
                                "Omdat ankeren pas echt waarde krijgt wanneer een gewenste toestand ook in nieuwe of moeilijke situaties opgeroepen kan worden.",
                            ),
                            (
                                "Hoe gebeurt contextverandering praktisch?",
                                "Door eerst een hulpbron of sterke toestand op te roepen, die te ankeren, en het anker daarna te activeren in een andere, problematische situatie.",
                            ),
                            (
                                "Wat is het doel van contextverandering?",
                                "Dat iemand in een nieuwe context anders kan reageren dan voorheen, met meer keuzevrijheid en meer passende emoties of gedragingen.",
                            ),
                        ],
                    },
                    {
                        "term": "Trigger",
                        "questions": [
                            (
                                "Wat is een trigger?",
                                "Een trigger is een spontane stimulus die, zodra die wordt waargenomen, automatisch een respons in gang zet.",
                            ),
                            (
                                "Welke vormen kan een trigger aannemen?",
                                "Triggers kunnen woorden, geluiden of non-verbale signalen zijn die meestal onbewust gedragspatronen activeren.",
                            ),
                            (
                                "Waarom zijn triggers belangrijk binnen ankeren?",
                                "Omdat een anker feitelijk werkt als een trigger: een specifieke stimulus roept later automatisch een bepaalde toestand of reactie op.",
                            ),
                            (
                                "Hoe hangen triggers samen met fobieën of verslavingen?",
                                "Veel verslavingen worden in stand gehouden door triggers en fobische reacties starten vaak met een externe trigger die daarna automatisch een heftige emotionele respons activeert.",
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


def build_module11_topics() -> list[dict]:
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
        for topic in MODULE11_STRUCTURE
    ]


MODULE11_TOPIC_BLUEPRINT = build_module11_topics()


def build_module11_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE11_STRUCTURE]
    heading_options = topic_names + [
        "NLP technieken",
        "Strategieën",
    ]
    exercises = [
        _build_multi_select(
            title="Ankeren - hoofdstukkoppen",
            topic_title=MODULE11_STRUCTURE[0]["topic"],
            concept_title=MODULE11_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk Ankeren?",
            question="Selecteer de koppen die bij het hoofdstuk Ankeren horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE11_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"Ankeren - {topic['topic']} subkoppen",
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
                    title=f"Ankeren - {concept['concept']} termen",
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
                                "Ankeren - "
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