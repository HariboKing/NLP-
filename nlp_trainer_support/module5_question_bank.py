from __future__ import annotations


MODULE_TITLE = "De transformatie van droom naar outcome"


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


MODULE5_STRUCTURE = [
    {
        "topic": "Doelstellingenproces",
        "subheading_distractors": ["Metaforen", "Het metamodel"],
        "concepts": [
            {
                "concept": "Stappen",
                "distractors": ["Constructivisme", "Nominalisaties"],
                "terms": [
                    {
                        "term": "Ken je doel",
                        "questions": [
                            (
                                "Wat betekent 'ken je doel'?",
                                "Dat je helder moet weten wat je wilt bereiken en een duidelijk beeld moet hebben van het gerealiseerde einddoel.",
                            ),
                            (
                                "Waarom is een duidelijk doel belangrijk?",
                                "Omdat je zonder duidelijke bestemming geen gerichte actie kunt ondernemen.",
                            ),
                            (
                                "Hoe kun je je doel sterker formuleren?",
                                "Door je doel te visualiseren en jezelf voor te stellen hoe het voelt wanneer het al bereikt is.",
                            ),
                            (
                                "Wat is het verschil tussen een wens en een doel?",
                                "Een wens is vaak nog algemeen, terwijl een doel richting, vorm en concreet eindresultaat heeft.",
                            ),
                        ],
                    },
                    {
                        "term": "Neem actie",
                        "questions": [
                            (
                                "Waarom is actie nodig in het doelstellingenproces?",
                                "Omdat een doel pas werkelijkheid wordt wanneer je stappen onderneemt die je dichter bij het gewenste resultaat brengen.",
                            ),
                            (
                                "Wat betekent 'neem actie' concreet?",
                                "Dat je doet wat nodig is om je doel te bereiken, bijvoorbeeld nieuwe vaardigheden leren, relaties opbouwen of gedrag aanpassen.",
                            ),
                            (
                                "Waarom is alleen willen niet genoeg?",
                                "Omdat intentie zonder gedrag geen resultaat oplevert.",
                            ),
                            (
                                "Wat vraagt effectief handelen volgens NLP?",
                                "Dat je niet alleen begint, maar ook consequent blijft handelen in de richting van je outcome.",
                            ),
                        ],
                    },
                    {
                        "term": "Check resultaat",
                        "questions": [
                            (
                                "Wat betekent 'check resultaat'?",
                                "Dat je je voortgang volgt en beoordeelt of wat je doet je ook werkelijk dichter bij je doel brengt.",
                            ),
                            (
                                "Waarom moet je je resultaat meten?",
                                "Omdat feedback zichtbaar maakt wat werkt en wat niet werkt, zodat je kunt verbeteren.",
                            ),
                            (
                                "Wat is de rol van feedback in dit proces?",
                                "Feedback toetst de uitkomst aan de doelstelling. Als de resultaten afwijken, gebruik je die informatie om iets te veranderen.",
                            ),
                            (
                                "Wanneer weet je dat je goed bezig bent?",
                                "Wanneer je resultaten in lijn liggen met het doel dat je vooraf hebt geformuleerd.",
                            ),
                        ],
                    },
                    {
                        "term": "Wees flexibel",
                        "questions": [
                            (
                                "Waarom is flexibiliteit belangrijk bij doelen bereiken?",
                                "Omdat niet elke eerste aanpak werkt. Als iets niet werkt, moet je je benadering aanpassen zonder het doel los te laten.",
                            ),
                            (
                                "Wat betekent flexibiliteit in NLP?",
                                "Dat je bereid bent andere manieren te proberen om hetzelfde gewenste resultaat te bereiken.",
                            ),
                            (
                                "Wanneer moet je flexibel zijn?",
                                "Op het moment dat je merkt dat je huidige aanpak niet het gewenste resultaat oplevert.",
                            ),
                            (
                                "Wat blijft gelijk als je flexibel bent?",
                                "Het doel blijft gelijk, maar het proces of de route ernaartoe mag veranderen.",
                            ),
                        ],
                    },
                    {
                        "term": "Beloon jezelf",
                        "questions": [
                            (
                                "Waarom hoort belonen bij het doelstellingenproces?",
                                "Omdat het belangrijk is om het behaalde resultaat bewust te beleven en ervan te genieten.",
                            ),
                            (
                                "Wat betekent 'beloon jezelf voor de resultaten'?",
                                "Dat je stilstaat bij wat je hebt bereikt, trots bent op je prestaties en het succes ook werkelijk ervaart.",
                            ),
                            (
                                "Waarom is genieten van het resultaat belangrijk?",
                                "Omdat het doelstellingenproces niet alleen om presteren gaat, maar ook om het beleven van de opbrengst van je inspanningen.",
                            ),
                            (
                                "Wat versterkt een beloning na het behalen van een doel?",
                                "Het gevoel van succes, voldoening en de bereidheid om opnieuw doelgericht te handelen.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Outcome frame",
        "subheading_distractors": ["Algemene semantiek", "Filosofie en NLP"],
        "concepts": [
            {
                "concept": "Vormvoorwaarden",
                "distractors": ["Universal quantifiers", "Referentiële index"],
                "terms": [
                    {
                        "term": "Positief formuleren",
                        "questions": [
                            (
                                "Wat betekent positief formuleren?",
                                "Dat je formuleert wat je wél wilt bereiken, in plaats van wat je wilt vermijden.",
                            ),
                            (
                                "Waarom moet een outcome positief geformuleerd zijn?",
                                "Omdat een positieve formulering meer richting, motivatie en een duidelijker beeld van de gewenste toekomst geeft.",
                            ),
                            (
                                "Hoe herken je een negatieve formulering?",
                                "Aan taal die draait om wat je niet wilt, zoals 'ik wil niet meer gestrest zijn'.",
                            ),
                            (
                                "Waarom werken negaties minder goed in een outcome?",
                                "Omdat ze minder richting geven dan taal die concreet benoemt wat het gewenste resultaat is.",
                            ),
                        ],
                    },
                    {
                        "term": "Eigen controle",
                        "questions": [
                            (
                                "Wat betekent 'binnen eigen controle'?",
                                "Dat het succes van de outcome afhankelijk is van jouw eigen handelen en niet van factoren buiten jou.",
                            ),
                            (
                                "Waarom moet een outcome binnen eigen controle liggen?",
                                "Omdat dat eigenaarschap en verantwoordelijkheid vergroot, en daarmee ook de kans op succes.",
                            ),
                            (
                                "Wat is een voorbeeld van een doel buiten eigen controle?",
                                "Een doel dat volledig afhangt van de beslissing of het gedrag van anderen.",
                            ),
                            (
                                "Wat is een beter alternatief?",
                                "Een doel formuleren dat draait om jouw eigen acties, inzet of ontwikkeling.",
                            ),
                        ],
                    },
                    {
                        "term": "Zintuiglijk specifiek",
                        "questions": [
                            (
                                "Wat betekent 'zintuiglijk specifiek'?",
                                "Dat je je outcome zo formuleert dat duidelijk is wat je zult zien, horen, voelen, ruiken of proeven wanneer het doel bereikt is.",
                            ),
                            (
                                "Waarom moet een outcome zintuiglijk specifiek zijn?",
                                "Omdat het doel dan concreet en meetbaar wordt, zodat je vooruitgang kunt herkennen en bijsturen.",
                            ),
                            (
                                "Wat is het voordeel van zintuiglijk specifieke taal?",
                                "Dat communicatie levendiger en begrijpelijker wordt en dat het gewenste resultaat concreter wordt voorgesteld.",
                            ),
                            (
                                "Hoe toets je of een doel zintuiglijk specifiek genoeg is?",
                                "Door te vragen: hoe weet je dat je het hebt, en wat neem je dan precies waar?",
                            ),
                        ],
                    },
                    {
                        "term": "Context",
                        "questions": [
                            (
                                "Wat betekent context binnen een outcome?",
                                "Dat duidelijk is waar, wanneer en met wie het doel bereikt of zichtbaar moet zijn.",
                            ),
                            (
                                "Waarom is context belangrijk?",
                                "Omdat een doel pas echt werkbaar wordt als je weet in welke situatie het geldt.",
                            ),
                            (
                                "Hoe helpt context bij doelbereik?",
                                "Door het mogelijk te maken realistische plannen te maken en obstakels eerder te voorzien.",
                            ),
                            (
                                "Wanneer is een outcome contextloos?",
                                "Wanneer onduidelijk blijft in welke omgeving, op welk moment of met welke mensen het resultaat zichtbaar moet zijn.",
                            ),
                        ],
                    },
                    {
                        "term": "Ecologie",
                        "questions": [
                            (
                                "Wat betekent ecologie in NLP?",
                                "Dat je kijkt naar de nevengevolgen van het behalen van je doel en of het resultaat past binnen je leven en omgeving.",
                            ),
                            (
                                "Waarom is ecologie belangrijk bij een outcome?",
                                "Omdat een outcome niet alleen haalbaar moet zijn, maar ook passend voor jezelf, je waarden en je omgeving.",
                            ),
                            (
                                "Welke vraag hoort bij ecologie?",
                                "Bijvoorbeeld: hoe zal dit je leven, werk, familie of vrienden beïnvloeden?",
                            ),
                            (
                                "Wat onderzoekt ecologie nog meer?",
                                "Of er positieve bijproducten verloren gaan of dat er een tweede winst zit in het huidige probleem of de huidige situatie.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Van droom naar resultaat",
        "subheading_distractors": ["Taal en neurologie", "Complexe equivalentie"],
        "concepts": [
            {
                "concept": "Beslisvragen",
                "distractors": ["Nominalisaties", "Kritisch reflecteren"],
                "terms": [
                    {
                        "term": "Richting",
                        "questions": [
                            (
                                "Waarom is richting een belangrijke beslisvraag?",
                                "Omdat richting bepaalt naar welke gewenste toekomst je werkelijk toe wilt bewegen.",
                            ),
                            (
                                "Wat betekent richting in dit proces?",
                                "Dat je kiest welke kant je op wilt in plaats van vaag te blijven hopen op verandering.",
                            ),
                            (
                                "Wat gebeurt er als je geen richting kiest?",
                                "Dan ontbreekt focus en wordt het moeilijk om passende stappen te nemen.",
                            ),
                            (
                                "Welke bekende illustratie hoort hierbij?",
                                "Het idee dat als het niet uitmaakt waar je heen wilt, het ook niet uitmaakt welke kant je opgaat.",
                            ),
                        ],
                    },
                    {
                        "term": "Eindresultaat",
                        "questions": [
                            (
                                "Waarom moet je het eindresultaat kennen?",
                                "Omdat een doel pas kracht krijgt wanneer je weet hoe het gerealiseerde resultaat eruitziet.",
                            ),
                            (
                                "Wat is een eindresultaat?",
                                "De gewenste toestand die je wilt creëren en waaraan je kunt merken dat je doel bereikt is.",
                            ),
                            (
                                "Hoe maak je een eindresultaat sterker?",
                                "Door het aantrekkelijk, concreet en zintuiglijk voor te stellen alsof het al in de toekomst aanwezig is.",
                            ),
                            (
                                "Waarom is een eindresultaat meer dan alleen een idee?",
                                "Omdat het dient als toetssteen voor gedrag, feedback en bijsturing.",
                            ),
                        ],
                    },
                    {
                        "term": "Haalbaarheid",
                        "questions": [
                            (
                                "Waarom is haalbaarheid een beslisvraag?",
                                "Omdat niet elke wens automatisch een werkbare outcome is; het doel moet ook realistisch en bereikbaar zijn.",
                            ),
                            (
                                "Hoe toets je haalbaarheid?",
                                "Door te onderzoeken of het doel realistisch is en welke hulpmiddelen, mensen of andere middelen nodig zijn.",
                            ),
                            (
                                "Welke rol spelen hulpbronnen bij haalbaarheid?",
                                "Hulpbronnen maken duidelijk of je beschikt over wat nodig is om het doel werkelijk te realiseren.",
                            ),
                            (
                                "Wanneer is een outcome onvoldoende haalbaar?",
                                "Wanneer hij buiten je controle ligt, niet realistisch is, of niet ondersteund wordt door beschikbare middelen en acties.",
                            ),
                        ],
                    },
                    {
                        "term": "Keuze",
                        "questions": [
                            (
                                "Waarom is keuze belangrijk in de stap van droom naar resultaat?",
                                "Omdat resultaat vraagt om bewuste selectie: welke wens maak je concreet, welke route kies je, en welke actie brengt je dichter bij het doel?",
                            ),
                            (
                                "Wat voor keuze maak je bij outcomes?",
                                "Je kiest welke wensen realistisch zijn, welke prioriteit krijgen en welke je werkelijk wilt realiseren.",
                            ),
                            (
                                "Waarom is keuze gekoppeld aan verantwoordelijkheid?",
                                "Omdat een outcome binnen eigen controle ligt en daardoor vraagt om eigen initiatief en onderhoud door het individu zelf.",
                            ),
                            (
                                "Hoe helpt keuze om van droom naar resultaat te gaan?",
                                "Door vaag verlangen om te zetten in een concrete richting, een gekozen eindresultaat en doelgerichte actie.",
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


def build_module5_topics() -> list[dict]:
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
        for topic in MODULE5_STRUCTURE
    ]


MODULE5_TOPIC_BLUEPRINT = build_module5_topics()


def build_module5_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE5_STRUCTURE]
    heading_options = topic_names + [
        "De verborgen wereld van metaforen",
        "De kunst van magische taalpatronen",
    ]
    exercises = [
        _build_multi_select(
            title="De transformatie van droom naar outcome - hoofdstukkoppen",
            topic_title=MODULE5_STRUCTURE[0]["topic"],
            concept_title=MODULE5_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk De transformatie van droom naar outcome?",
            question="Selecteer de koppen die bij het hoofdstuk De transformatie van droom naar outcome horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE5_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"De transformatie van droom naar outcome - {topic['topic']} subkoppen",
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
                    title=f"De transformatie van droom naar outcome - {concept['concept']} termen",
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
                                "De transformatie van droom naar outcome - "
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