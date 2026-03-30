from __future__ import annotations


MODULE_TITLE = "De ontdekking van het zelf"


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


MODULE6_STRUCTURE = [
    {
        "topic": "Zelfonderzoek",
        "subheading_distractors": ["Outcome frame", "Metaforen"],
        "concepts": [
            {
                "concept": "Thema's",
                "distractors": ["Ecologie", "Universal quantifiers"],
                "terms": [
                    {
                        "term": "Identiteit",
                        "questions": [
                            (
                                "Wat wordt binnen dit hoofdstuk bedoeld met identiteit?",
                                "Identiteit verwijst naar het bewuste zelfconcept: het idee dat je hebt over wie je bent. Het gaat om je basale besef van jezelf en de manier waarop je jezelf definieert.",
                            ),
                            (
                                "Waarom hoort identiteit bij de ontdekking van het zelf?",
                                "Omdat zelfonderzoek begint bij de vraag wie je bent. Pas wanneer je zicht krijgt op je identiteit, kun je begrijpen hoe je denkt, voelt en handelt.",
                            ),
                            (
                                "Is identiteit volgens deze benadering vast of veranderlijk?",
                                "Identiteit is niet volledig vast. Het bewuste zelfconcept kan veranderen door nieuwe ervaringen, nieuwe informatie, relaties met anderen en invloeden uit de omgeving.",
                            ),
                            (
                                "Welke vraag hoort bij het identiteitsniveau?",
                                "De centrale vraag op dit niveau is: wie ben ik? Op het niveau van identiteit draait het om het meest basale besef van wie je bent.",
                            ),
                        ],
                    },
                    {
                        "term": "Zelfbeeld",
                        "questions": [
                            (
                                "Wat is zelfbeeld?",
                                "Zelfbeeld is de manier waarop je jezelf ziet en omschrijft. Het is nauw verbonden met je zelfconcept en bepaalt mede hoe je jezelf ervaart in het contact met anderen.",
                            ),
                            (
                                "Waaruit wordt een zelfbeeld opgebouwd?",
                                "Het zelfbeeld wordt opgebouwd uit ervaringen, herinneringen, emoties en perspectieven die je in de loop van je leven verzamelt.",
                            ),
                            (
                                "Hoe beïnvloedt zelfbeeld gedrag?",
                                "Je zelfbeeld beïnvloedt hoe je jezelf ziet en daardoor ook hoe je je gedraagt in sociale situaties. Wat je over jezelf gelooft, werkt door in je houding, keuzes en reacties.",
                            ),
                            (
                                "Waarom is het belangrijk te weten dat zelfbeeld kan veranderen?",
                                "Omdat dit ruimte geeft voor groei. Als je zelfbeeld niet vaststaat, kun je opener worden voor nieuwe ervaringen en je minder vastzetten in oude ideeën over jezelf.",
                            ),
                        ],
                    },
                    {
                        "term": "Zelfbewustzijn",
                        "questions": [
                            (
                                "Wat is zelfbewustzijn?",
                                "Zelfbewustzijn is het vermogen om je bewust te zijn van je eigen gedachten, gevoelens, overtuigingen en gedrag. Het gaat om zicht krijgen op hoe jij functioneert.",
                            ),
                            (
                                "Waarom is zelfbewustzijn belangrijk?",
                                "Omdat het helpt om blinde vlekken te ontdekken, je gedrag beter af te stemmen op de werkelijkheid en gerichter te groeien in je persoonlijke ontwikkeling.",
                            ),
                            (
                                "Welke rol speelt feedback bij zelfbewustzijn?",
                                "Feedback is essentieel voor zelfbewustzijn, omdat je daarmee ziet wat je zelf niet direct waarneemt. Feedback helpt je om je acties en reacties bij te sturen en je vrije ruimte te vergroten.",
                            ),
                            (
                                "Hoe helpt het Johari- of feedbackvenster bij zelfbewustzijn?",
                                "Het model laat zien dat er delen van jezelf zijn die open, blind, verborgen of onbekend zijn. Door feedback en openheid wordt de vrije ruimte groter, en daarmee ook je zelfbewustzijn.",
                            ),
                        ],
                    },
                    {
                        "term": "Persoonlijke veiligheid",
                        "questions": [
                            (
                                "Waarom is persoonlijke veiligheid belangrijk in zelfonderzoek?",
                                "Omdat groei, zelfexpressie en eerlijke communicatie alleen echt mogelijk worden wanneer iemand zich veilig voelt. Zonder veiligheid ontstaat eerder verdediging dan ontwikkeling.",
                            ),
                            (
                                "Wat bedoelde Satir met veiligheid?",
                                "Satir zag veiligheid als een fundamentele bouwsteen voor openheid, eigenwaarde, gezonde relaties en persoonlijke groei. Een veilige omgeving maakt het mogelijk om gevoelens en behoeften te delen zonder angst voor afwijzing of kritiek.",
                            ),
                            (
                                "Wat gebeurt er als persoonlijke veiligheid ontbreekt?",
                                "Bij een gebrek aan veiligheid ontstaan eerder defensieve houdingen en ineffectieve communicatiestijlen. Mensen beschermen zich dan in plaats van zich open te stellen.",
                            ),
                            (
                                "Welke soorten veiligheid onderscheidt Satir?",
                                "Satir noemt onder meer fysieke, emotionele, relationele, psychologische en sociale veiligheid. Daarnaast benadrukt zij ook interne veiligheid vanuit zelfwaardering en zelfacceptatie.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Satir-condities",
        "subheading_distractors": ["Algemene semantiek", "Van droom naar resultaat"],
        "concepts": [
            {
                "concept": "Veiligheid en groei",
                "distractors": ["Nominalisaties", "Constructivisme"],
                "terms": [
                    {
                        "term": "Vertrouwen",
                        "questions": [
                            (
                                "Waarom is vertrouwen een voorwaarde voor veiligheid en groei?",
                                "Omdat iemand zich pas werkelijk kan openen wanneer er vertrouwen is in de persoon met wie hij of zij samenwerkt. Zonder vertrouwen blijft er afstand en terughoudendheid bestaan.",
                            ),
                            (
                                "Wat maakt vertrouwen zo belangrijk in begeleiding of therapie?",
                                "Vertrouwen zorgt ervoor dat iemand gevoelens, behoeften en kwetsbaarheid durft te tonen. Dat is nodig voor echte verandering en groei.",
                            ),
                            (
                                "Wat ontstaat er door vertrouwen?",
                                "Door vertrouwen ontstaat ruimte voor openheid, eerlijkheid en samenwerking. Daardoor kunnen mensen zich veiliger voelen en sterker ontwikkelen.",
                            ),
                            (
                                "Hoe hangt vertrouwen samen met eigenwaarde?",
                                "Wanneer iemand zich veilig en vertrouwd voelt, wordt het makkelijker om zichzelf te laten zien. Dat ondersteunt het versterken van self-esteem of eigenwaarde.",
                            ),
                        ],
                    },
                    {
                        "term": "Veilige plek",
                        "questions": [
                            (
                                "Wat betekent een veilige plek binnen Satirs visie?",
                                "Een veilige plek betekent dat iemand ervaart dat de omgeving fysiek en emotioneel veilig is. Het is een plaats waar je jezelf kunt uiten zonder angst voor aanval, afwijzing of kritiek.",
                            ),
                            (
                                "Waarom is een veilige plek belangrijk?",
                                "Omdat veiligheid de basis vormt voor zelfexpressie, groei en effectieve communicatie. Zonder veilige plek zullen mensen zich eerder afsluiten of verdedigen.",
                            ),
                            (
                                "Gaat een veilige plek alleen over fysieke veiligheid?",
                                "Nee. Het gaat niet alleen om fysieke veiligheid, maar ook om emotionele, psychologische en relationele veiligheid. Pas samen vormen die een echt veilige plek.",
                            ),
                            (
                                "Wat maakt een plek veilig genoeg voor groei?",
                                "Dat iemand daar open mag zijn over gevoelens en behoeften, dat er respect is, en dat er geen voortdurende dreiging van oordeel of afwijzing wordt ervaren.",
                            ),
                        ],
                    },
                    {
                        "term": "Vangnet",
                        "questions": [
                            (
                                "Wat wordt bedoeld met een vangnet?",
                                "Een vangnet is het gevoel dat er ondersteuning beschikbaar is wanneer dat nodig is. Het betekent dat je niet volledig alleen staat als iets moeilijk wordt of misgaat.",
                            ),
                            (
                                "Waarom draagt een vangnet bij aan veiligheid?",
                                "Omdat het rust geeft te weten dat er hulp, steun of terugvalmogelijkheid is. Daardoor durven mensen eerder stappen te zetten richting groei en verandering.",
                            ),
                            (
                                "Hoe werkt een vangnet in persoonlijke ontwikkeling?",
                                "Een vangnet vermindert de angst om te falen of te vallen. Daardoor ontstaat meer moed om te oefenen, te leren en buiten oude patronen te treden.",
                            ),
                            (
                                "Wat is het verschil tussen steun en afhankelijkheid bij een vangnet?",
                                "Een vangnet betekent niet dat iemand alles voor je oplost, maar dat er een veilige basis is van waaruit jij zelf stappen kunt zetten. Het ondersteunt zelfstandigheid, in plaats van die weg te nemen.",
                            ),
                        ],
                    },
                    {
                        "term": "De wereld aankunnen",
                        "questions": [
                            (
                                "Wat betekent 'de wereld aankunnen' binnen Satir-condities?",
                                "Het betekent dat iemand zich sterk genoeg voelt om het leven en de buitenwereld tegemoet te treden, zonder te hoeven schamen voor wie hij is of wat hij heeft gedaan.",
                            ),
                            (
                                "Waarom hangt dit samen met veiligheid?",
                                "Omdat echte veiligheid niet alleen van buiten komt, maar ook van binnen. Wie innerlijke veiligheid en zelfacceptatie ontwikkelt, voelt zich steviger tegenover de wereld.",
                            ),
                            (
                                "Welke innerlijke kwaliteiten ondersteunen het aankunnen van de wereld?",
                                "Zelfacceptatie, zelfwaardering en het gevoel dat je jezelf niet hoeft te verbergen of te verloochenen. Dat vormt een basis van interne veiligheid.",
                            ),
                            (
                                "Hoe draagt 'de wereld aankunnen' bij aan groei?",
                                "Wanneer iemand niet langer vooral bezig is met schaamte of zelfbescherming, ontstaat ruimte om authentiek te leven, keuzes te maken en zich verder te ontwikkelen.",
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


def build_module6_topics() -> list[dict]:
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
        for topic in MODULE6_STRUCTURE
    ]


MODULE6_TOPIC_BLUEPRINT = build_module6_topics()


def build_module6_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE6_STRUCTURE]
    heading_options = topic_names + [
        "De transformatie van droom naar outcome",
        "De verborgen wereld van metaforen",
    ]
    exercises = [
        _build_multi_select(
            title="De ontdekking van het zelf - hoofdstukkoppen",
            topic_title=MODULE6_STRUCTURE[0]["topic"],
            concept_title=MODULE6_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk De ontdekking van het zelf?",
            question="Selecteer de koppen die bij het hoofdstuk De ontdekking van het zelf horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE6_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"De ontdekking van het zelf - {topic['topic']} subkoppen",
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
                    title=f"De ontdekking van het zelf - {concept['concept']} termen",
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
                                "De ontdekking van het zelf - "
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
