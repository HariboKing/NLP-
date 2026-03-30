from __future__ import annotations


MODULE_TITLE = "De kracht van excellente communicatie"


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


MODULE7_STRUCTURE = [
    {
        "topic": "Excellente communicatie",
        "subheading_distractors": ["Veiligheid en groei", "Outcome frame"],
        "concepts": [
            {
                "concept": "Basis",
                "distractors": ["Ecologie", "Nominalisaties"],
                "terms": [
                    {
                        "term": "Doel",
                        "questions": [
                            (
                                "Waarom is doel belangrijk binnen excellente communicatie?",
                                "Omdat communicatie effectiever wordt wanneer je weet wat je wilt bereiken. Een duidelijk doel geeft richting aan wat je zegt en hoe je het zegt.",
                            ),
                            (
                                "Wat gebeurt er als communicatie geen duidelijk doel heeft?",
                                "Dan wordt communicatie sneller vaag, reactief of onsamenhangend, waardoor de kans groter wordt dat de boodschap zijn effect mist.",
                            ),
                            (
                                "Hoe beïnvloedt een doel de kwaliteit van een gesprek?",
                                "Het helpt je om keuzes te maken in toon, woorden en aanpak, zodat je communicatie beter aansluit bij het gewenste resultaat.",
                            ),
                            (
                                "Is het doel van communicatie hetzelfde als de bedoeling van de spreker?",
                                "Niet helemaal. De bedoeling is wat je wilt overbrengen, maar het communicatiedoel gaat ook over het effect dat je wilt bereiken bij de ander.",
                            ),
                        ],
                    },
                    {
                        "term": "Waarnemingsvermogen",
                        "questions": [
                            (
                                "Wat betekent waarnemingsvermogen binnen excellente communicatie?",
                                "Het betekent dat je goed kunt opmerken wat er bij de ander gebeurt, zowel verbaal als non-verbaal.",
                            ),
                            (
                                "Waarom is waarnemingsvermogen belangrijk?",
                                "Omdat je alleen goed kunt afstemmen als je nauwkeurig ziet, hoort en merkt hoe de ander reageert.",
                            ),
                            (
                                "Wat helpt je om je waarnemingsvermogen te vergroten?",
                                "Goed observeren, letten op kleine signalen, luisteren naar woordkeuze en aandacht hebben voor lichaamstaal en toon.",
                            ),
                            (
                                "Hoe hangt waarnemingsvermogen samen met feedback?",
                                "Hoe beter je waarneemt, hoe beter je kunt herkennen of je boodschap aankomt en of je je aanpak moet aanpassen.",
                            ),
                        ],
                    },
                    {
                        "term": "Flexibiliteit",
                        "questions": [
                            (
                                "Waarom is flexibiliteit een basisvoorwaarde van excellente communicatie?",
                                "Omdat niet elke manier van communiceren bij elke persoon of situatie werkt. Flexibiliteit maakt aanpassing mogelijk.",
                            ),
                            (
                                "Wat betekent flexibiliteit in communicatie?",
                                "Dat je kunt schakelen in stijl, taalgebruik, tempo of aanpak om beter aan te sluiten bij de ander en bij het doel.",
                            ),
                            (
                                "Wat gebeurt er als iemand niet flexibel communiceert?",
                                "Dan blijft iemand vasthouden aan één manier van communiceren, ook als die niet werkt, waardoor weerstand of misverstanden kunnen ontstaan.",
                            ),
                            (
                                "Waarom hangt flexibiliteit samen met invloed?",
                                "Omdat degene met de meeste keuzemogelijkheden in gedrag en communicatie zich het best kan aanpassen aan de situatie.",
                            ),
                        ],
                    },
                    {
                        "term": "Communicatievaardigheden",
                        "questions": [
                            (
                                "Wat zijn communicatievaardigheden?",
                                "Dat zijn de vaardigheden die iemand gebruikt om helder, effectief en afgestemd te communiceren met anderen.",
                            ),
                            (
                                "Welke communicatievaardigheden zijn hier belangrijk?",
                                "Bijvoorbeeld luisteren, afstemmen, samenvatten, feedback geven, vragen stellen en non-verbaal bewust communiceren.",
                            ),
                            (
                                "Waarom zijn communicatievaardigheden trainbaar?",
                                "Omdat communicatie uit concrete gedragingen bestaat die je kunt observeren, oefenen en verbeteren.",
                            ),
                            (
                                "Waarom zijn communicatievaardigheden essentieel voor excellente communicatie?",
                                "Omdat ze bepalen hoe goed iemand contact maakt, betekenis overbrengt en invloed uitoefent in interactie.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Rapport",
        "subheading_distractors": ["Zelfonderzoek", "Metaforen"],
        "concepts": [
            {
                "concept": "Proces",
                "distractors": ["Constructivisme", "Verbeelding"],
                "terms": [
                    {
                        "term": "Pacing",
                        "questions": [
                            (
                                "Wat is pacing?",
                                "Pacing is het afstemmen op de ander door aan te sluiten bij diens gedrag, taal, tempo, houding of beleving.",
                            ),
                            (
                                "Waarom is pacing belangrijk voor rapport?",
                                "Omdat pacing helpt om herkenning, vertrouwen en verbinding op te bouwen.",
                            ),
                            (
                                "Wat is het doel van pacing?",
                                "Het doel is om eerst contact en afstemming te creëren voordat je iemand probeert mee te nemen in een andere richting.",
                            ),
                            (
                                "Is pacing hetzelfde als nadoen?",
                                "Nee. Pacing gaat niet om mechanisch kopiëren, maar om functioneel en respectvol aansluiten bij de ander.",
                            ),
                        ],
                    },
                    {
                        "term": "Testen",
                        "questions": [
                            (
                                "Waarom hoort testen bij rapport?",
                                "Omdat je wilt weten of de afstemming die je denkt te hebben ook werkelijk aanwezig is.",
                            ),
                            (
                                "Wat betekent testen in dit proces?",
                                "Dat je kleine veranderingen inzet om te zien of de ander mee beweegt, zodat je kunt beoordelen of er echt rapport is.",
                            ),
                            (
                                "Waarom is testen nuttig na pacing?",
                                "Omdat pacing pas waarde heeft als je kunt vaststellen dat de verbinding sterk genoeg is geworden.",
                            ),
                            (
                                "Wat leert testen je over de interactie?",
                                "Of de ander je volgt, of er voldoende contact is, en of je klaar bent om verder te gaan naar leading.",
                            ),
                        ],
                    },
                    {
                        "term": "Leading",
                        "questions": [
                            (
                                "Wat is leading?",
                                "Leading is het begeleiden van de ander nadat er rapport is ontstaan, zodat je richting kunt geven aan het gesprek of het proces.",
                            ),
                            (
                                "Waarom komt leading pas na pacing?",
                                "Omdat invloed pas echt werkt wanneer er eerst voldoende afstemming en verbinding is opgebouwd.",
                            ),
                            (
                                "Wat is het risico van te vroeg leading geven?",
                                "Dat de ander niet meegaat, weerstand voelt of afhaakt omdat er nog geen rapport is.",
                            ),
                            (
                                "Wat laat succesvolle leading zien?",
                                "Dat het contact sterk genoeg is om de ander mee te nemen in een nieuwe richting of gewenste verandering.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Luisteren en afstemmen",
        "subheading_distractors": ["Doelstellingenproces", "Algemene semantiek"],
        "concepts": [
            {
                "concept": "Vaardigheden",
                "distractors": ["Ecologie", "Universal quantifiers"],
                "terms": [
                    {
                        "term": "Backtrack match",
                        "questions": [
                            (
                                "Wat is backtrack match?",
                                "Backtrack match is het teruggeven van de woorden of kernformuleringen van de ander op een manier die nauw aansluit bij diens taalgebruik.",
                            ),
                            (
                                "Waarom is backtrack match effectief?",
                                "Omdat het de ander het gevoel geeft echt gehoord en begrepen te worden.",
                            ),
                            (
                                "Wat is het verschil tussen backtrack match en gewoon herhalen?",
                                "Bij backtrack match geef je selectief en functioneel terug wat belangrijk is, zodat begrip en rapport toenemen.",
                            ),
                            (
                                "Wanneer gebruik je backtrack match?",
                                "Vooral wanneer je begrip wilt verdiepen, rapport wilt versterken of wilt controleren of je de ander goed hebt begrepen.",
                            ),
                        ],
                    },
                    {
                        "term": "Backtrack mismatch",
                        "questions": [
                            (
                                "Wat is backtrack mismatch?",
                                "Backtrack mismatch is het bewust niet volledig aansluiten bij de formulering van de ander, zodat je verschil, nuance of een andere invalshoek zichtbaar maakt.",
                            ),
                            (
                                "Waarom kan backtrack mismatch nuttig zijn?",
                                "Omdat het kan helpen om patronen te doorbreken, aannames te bevragen of iemand uit een star taalframe te halen.",
                            ),
                            (
                                "Wanneer kan backtrack mismatch riskant zijn?",
                                "Wanneer er nog onvoldoende rapport is, kan het als tegendraads of corrigerend worden ervaren.",
                            ),
                            (
                                "Wat vraagt effectief gebruik van backtrack mismatch?",
                                "Goede timing, voldoende rapport en een duidelijk doel.",
                            ),
                        ],
                    },
                    {
                        "term": "Vakjargon eliciteren",
                        "questions": [
                            (
                                "Wat betekent vakjargon eliciteren?",
                                "Dat je specifieke woorden, termen en betekenissen uitvraagt die voor de ander belangrijk zijn binnen zijn of haar vakgebied of belevingswereld.",
                            ),
                            (
                                "Waarom is dit belangrijk in communicatie?",
                                "Omdat woorden voor verschillende mensen iets anders kunnen betekenen, zeker in specialistische contexten.",
                            ),
                            (
                                "Wat levert vakjargon eliciteren op?",
                                "Meer precisie, minder misverstanden en betere afstemming op de taalwereld van de ander.",
                            ),
                            (
                                "Hoe doe je dit goed?",
                                "Door nieuwsgierig en concreet te vragen wat iemand precies bedoelt met een bepaalde term of uitdrukking.",
                            ),
                        ],
                    },
                    {
                        "term": "Samenvatten",
                        "questions": [
                            (
                                "Waarom is samenvatten een belangrijke luistervaardigheid?",
                                "Omdat samenvatten helpt om de kern van wat gezegd is helder te maken en te controleren of je de ander goed hebt begrepen.",
                            ),
                            (
                                "Wat is het effect van goed samenvatten?",
                                "Het geeft structuur, bevestigt begrip en helpt de ander om overzicht te houden in het gesprek.",
                            ),
                            (
                                "Wat maakt een samenvatting goed?",
                                "Dat de essentie behouden blijft, de formulering helder is en de ander zich erin herkent.",
                            ),
                            (
                                "Wanneer is samenvatten extra nuttig?",
                                "Bij complexe gesprekken, emotionele gesprekken of wanneer er veel informatie is uitgewisseld.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Feedback",
        "subheading_distractors": ["Filosofie en NLP", "Satir-condities"],
        "concepts": [
            {
                "concept": "Vormen",
                "distractors": ["Constructivisme", "Koppelingen"],
                "terms": [
                    {
                        "term": "Zelfonthulling",
                        "questions": [
                            (
                                "Wat is zelfonthulling in feedback?",
                                "Zelfonthulling is het delen van je eigen ervaring, gevoel of reactie in contact met de ander.",
                            ),
                            (
                                "Waarom is zelfonthulling waardevol?",
                                "Omdat het feedback persoonlijk, eerlijk en relationeel maakt zonder direct over de ander te oordelen.",
                            ),
                            (
                                "Wat is het verschil tussen zelfonthulling en beschuldigen?",
                                "Zelfonthulling gaat over jouw ervaring, terwijl beschuldigen de ander vastzet als oorzaak of probleem.",
                            ),
                            (
                                "Wanneer werkt zelfonthulling goed?",
                                "Wanneer het open, concreet en respectvol wordt gebruikt.",
                            ),
                        ],
                    },
                    {
                        "term": "Confrontatie",
                        "questions": [
                            (
                                "Wat is confrontatie als vorm van feedback?",
                                "Confrontatie is het benoemen van verschil, spanning, incongruentie of vermijding op een manier die iemand uitnodigt tot bewustwording.",
                            ),
                            (
                                "Waarom kan confrontatie waardevol zijn?",
                                "Omdat het helpt om patronen zichtbaar te maken die anders verborgen of onbesproken blijven.",
                            ),
                            (
                                "Wanneer wordt confrontatie onveilig?",
                                "Wanneer het te hard, beschuldigend of zonder voldoende rapport wordt gebracht.",
                            ),
                            (
                                "Wat maakt confrontatie effectief?",
                                "Dat ze helder, respectvol, doelgericht en afgestemd op de ander is.",
                            ),
                        ],
                    },
                    {
                        "term": "Wederkerige feedback",
                        "questions": [
                            (
                                "Wat is wederkerige feedback?",
                                "Wederkerige feedback is feedback die over en weer gegeven wordt, zodat beide partijen kunnen leren van de interactie.",
                            ),
                            (
                                "Waarom is wederkerigheid belangrijk?",
                                "Omdat het de relatie gelijkwaardiger maakt en voorkomt dat feedback alleen van één kant komt.",
                            ),
                            (
                                "Wat levert wederkerige feedback op?",
                                "Meer openheid, meer wederzijds begrip en een grotere kans op gezamenlijke groei.",
                            ),
                            (
                                "Hoe ondersteunt wederkerige feedback zelfbewustzijn?",
                                "Omdat beide partijen inzicht krijgen in hun eigen invloed op het contact.",
                            ),
                        ],
                    },
                    {
                        "term": "Ik-statements",
                        "questions": [
                            (
                                "Wat zijn ik-statements?",
                                "Ik-statements zijn uitspraken waarin je spreekt vanuit jezelf, bijvoorbeeld over wat je merkt, voelt of nodig hebt.",
                            ),
                            (
                                "Waarom zijn ik-statements belangrijk in feedback?",
                                "Omdat ze minder snel beschuldigend overkomen en de kans op defensieve reacties verkleinen.",
                            ),
                            (
                                "Wat is een voordeel van ik-statements?",
                                "Ze maken de feedback persoonlijk en helder, zonder de ander direct als probleem neer te zetten.",
                            ),
                            (
                                "Hoe ziet een goed ik-statement eruit?",
                                "Het benoemt concreet wat jij ervaart of waarneemt, zonder interpretaties of aanvallen op de persoon.",
                            ),
                        ],
                    },
                    {
                        "term": "Zintuiglijk taalgebruik",
                        "questions": [
                            (
                                "Wat betekent zintuiglijk taalgebruik in feedback?",
                                "Dat je feedback geeft op basis van wat je concreet hebt gezien, gehoord of waargenomen, in plaats van op basis van vage interpretaties.",
                            ),
                            (
                                "Waarom is zintuiglijk taalgebruik belangrijk?",
                                "Omdat het feedback concreter, toetsbaarder en minder aanvallend maakt.",
                            ),
                            (
                                "Wat is het verschil tussen interpretatie en zintuiglijke beschrijving?",
                                "Een interpretatie voegt betekenis toe, terwijl een zintuiglijke beschrijving blijft bij waarneembaar gedrag.",
                            ),
                            (
                                "Waarom helpt zintuiglijk taalgebruik bij heldere communicatie?",
                                "Omdat het de kans verkleint dat de ander moet reageren op een oordeel in plaats van op feitelijke observatie.",
                            ),
                        ],
                    },
                    {
                        "term": "Gedrag vs persoon",
                        "questions": [
                            (
                                "Waarom is het onderscheid tussen gedrag en persoon belangrijk?",
                                "Omdat feedback gericht moet zijn op wat iemand doet, niet op wie iemand is.",
                            ),
                            (
                                "Wat is het risico als je persoon en gedrag vermengt?",
                                "Dan voelt feedback sneller als aanval op identiteit, wat weerstand en schaamte kan oproepen.",
                            ),
                            (
                                "Hoe geef je feedback op gedrag in plaats van op de persoon?",
                                "Door concreet te benoemen welk gedrag je hebt waargenomen en wat het effect daarvan was.",
                            ),
                            (
                                "Waarom is dit onderscheid essentieel voor groei?",
                                "Omdat gedrag veranderbaar is, terwijl een aanval op de persoon eerder verlammend dan leerzaam werkt.",
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


def build_module7_topics() -> list[dict]:
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
        for topic in MODULE7_STRUCTURE
    ]


MODULE7_TOPIC_BLUEPRINT = build_module7_topics()


def build_module7_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE7_STRUCTURE]
    heading_options = topic_names + [
        "De ontdekking van het zelf",
        "De transformatie van droom naar outcome",
    ]
    exercises = [
        _build_multi_select(
            title="De kracht van excellente communicatie - hoofdstukkoppen",
            topic_title=MODULE7_STRUCTURE[0]["topic"],
            concept_title=MODULE7_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk De kracht van excellente communicatie?",
            question="Selecteer de koppen die bij het hoofdstuk De kracht van excellente communicatie horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE7_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"De kracht van excellente communicatie - {topic['topic']} subkoppen",
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
                    title=f"De kracht van excellente communicatie - {concept['concept']} termen",
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
                                "De kracht van excellente communicatie - "
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