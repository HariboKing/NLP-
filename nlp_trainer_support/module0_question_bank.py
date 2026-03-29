from __future__ import annotations


MODULE_TITLE = "De geschiedenis van NLP"


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


MODULE0_HEADING_EXERCISES = [
    _build_multi_select(
        title="Module 0 - hoofdstukkoppen",
        topic_title="Pre-NLP",
        concept_title="",
        prompt="Welke koppen vallen onder hoofdstuk 0?",
        question="Selecteer de koppen die bij hoofdstuk 0 horen.",
        option_labels=[
            "Pre-NLP",
            "Grondleggers van NLP",
            "Fundamenten van NLP",
            "Metamodel",
        ],
        correct_labels=["Pre-NLP", "Grondleggers van NLP"],
    ),
    _build_multi_select(
        title="Module 0 - Pre-NLP subkoppen",
        topic_title="Pre-NLP",
        concept_title="Virginia Satir",
        prompt="Welke subkoppen vallen onder de kop Pre-NLP?",
        question="Selecteer de subkoppen binnen Pre-NLP.",
        option_labels=[
            "Virginia Satir",
            "Milton Erickson",
            "Fritz Perls",
            "Richard Bandler",
        ],
        correct_labels=["Virginia Satir", "Milton Erickson", "Fritz Perls"],
    ),
    _build_multi_select(
        title="Module 0 - Grondleggers van NLP subkoppen",
        topic_title="Grondleggers van NLP",
        concept_title="Frank Pucelik",
        prompt="Welke subkoppen vallen onder de kop Grondleggers van NLP?",
        question="Selecteer de subkoppen binnen Grondleggers van NLP.",
        option_labels=[
            "Frank Pucelik",
            "Richard Bandler",
            "John Grinder",
            "Virginia Satir",
        ],
        correct_labels=["Frank Pucelik", "Richard Bandler", "John Grinder"],
    ),
]


MODULE0_PERSON_DATA = [
    {
        "topic": "Pre-NLP",
        "concept": "Virginia Satir",
        "distractors": ["Hypnotherapie", "Taalstructuren"],
        "terms": [
            {
                "term": "Gezinstherapie",
                "questions": [
                    (
                        "Wie was Virginia Satir binnen de gezinstherapie?",
                        "Virginia Satir was een pionier in de gezinstherapie die families zag als systemen waarin communicatie, emoties en relaties elkaar wederzijds beinvloeden.",
                    ),
                    (
                        "Wat maakte haar benadering innovatief en holistisch?",
                        "Haar benadering was innovatief omdat zij niet alleen naar losse klachten keek, maar naar het geheel van interacties, rollen, emoties en hulpbronnen binnen het familiesysteem.",
                    ),
                    (
                        "Waarom wordt haar werk gezien als een belangrijke voorloper van NLP?",
                        "Haar werk geldt als voorloper van NLP omdat zij communicatiepatronen, verandering en de structuur van subjectieve ervaring observeerde en praktisch toepaste.",
                    ),
                ],
            },
            {
                "term": "Communicatiecategorieen",
                "questions": [
                    (
                        "Welke vijf communicatiecategorieen beschreef Virginia Satir?",
                        "De vijf communicatiecategorieen zijn Placater, Blamer, Superreasonable, Irrelevant en Congruent.",
                    ),
                    (
                        "Wat zegt elke categorie over de manier waarop iemand communiceert?",
                        "Elke categorie laat zien hoe iemand onder druk contact maakt: sussen, beschuldigen, rationaliseren, afleiden of congruent en authentiek reageren.",
                    ),
                    (
                        "Hoe helpen deze categorieen om interacties tussen mensen beter te begrijpen?",
                        "Ze maken zichtbaar welke stressreacties en contactpatronen spelen, waardoor misverstanden, spanning en dynamiek in relaties beter te begrijpen worden.",
                    ),
                ],
            },
            {
                "term": "Communicatie en relaties",
                "questions": [
                    (
                        "Waarop lag Satirs focus in haar werk met individuen en groepen?",
                        "Satirs focus lag op communicatiepatronen, zelfbeeld, contact en de kwaliteit van relaties binnen gezinnen en groepen.",
                    ),
                    (
                        "Hoe hangen communicatie en relaties volgens Satir met elkaar samen?",
                        "Volgens Satir vormen communicatie en relaties elkaar wederzijds: de manier waarop mensen spreken, luisteren en reageren bepaalt de kwaliteit van het contact.",
                    ),
                    (
                        "Welke invloed hebben gezins- en interpersoonlijke relaties op emoties en gedrag?",
                        "Relaties beinvloeden hoe mensen zich voelen, zichzelf zien en reageren; terugkerende interactiepatronen kleuren emoties, overtuigingen en gedrag.",
                    ),
                ],
            },
            {
                "term": "Familiestamboom",
                "questions": [
                    (
                        "Wat is de familiestamboom-oefening van Virginia Satir?",
                        "De familiestamboom-oefening brengt familieleden, generaties, relaties en terugkerende patronen systematisch in kaart.",
                    ),
                    (
                        "Met welk doel onderzocht zij familiegeschiedenis?",
                        "Zij onderzocht familiegeschiedenis om zichtbaar te maken hoe rollen, loyaliteiten, regels en eerdere ervaringen het huidige functioneren beinvloeden.",
                    ),
                    (
                        "Welk inzicht kan deze oefening geven in patronen van gedrag en emoties?",
                        "De oefening kan laten zien welke gedragspatronen, emoties, overtuigingen en relationele dynamieken zich door de familie heen herhalen.",
                    ),
                ],
            },
        ],
    },
    {
        "topic": "Pre-NLP",
        "concept": "Milton Erickson",
        "distractors": ["Gestalttherapie", "Co-grondlegger"],
        "terms": [
            {
                "term": "Hypnotherapie",
                "questions": [
                    (
                        "Wie was Milton Erickson en waarom wordt hij gezien als de vader van de moderne hypnotherapie?",
                        "Milton Erickson was psychiater en hypnotherapeut en wordt gezien als vader van de moderne hypnotherapie omdat hij hypnose flexibel, creatief en therapeutisch toepaste.",
                    ),
                    (
                        "Waarin verschilde zijn benadering van traditionele hypnose?",
                        "Hij werkte minder directief en sloot juist aan bij de unieke taal, ervaring en hulpbronnen van de client in plaats van een standaard script te volgen.",
                    ),
                    (
                        "Waarom werd zijn manier van werken zo invloedrijk?",
                        "Zijn werkwijze werd invloedrijk omdat zij praktisch werkte, minder weerstand opriep en ruimte liet voor verandering vanuit de eigen belevingswereld van de client.",
                    ),
                ],
            },
            {
                "term": "Indirecte suggestie",
                "questions": [
                    (
                        "Wat wordt bedoeld met indirecte suggesties in Ericksons werkwijze?",
                        "Indirecte suggesties zijn uitnodigende en niet-frontale taalpatronen waarmee verandering wordt gesuggereerd zonder directe opdracht.",
                    ),
                    (
                        "Waarom gebruikte Erickson liever indirecte dan directe suggesties?",
                        "Hij gebruikte indirecte suggesties omdat die minder weerstand oproepen en beter aansluiten bij onbewuste verwerking en eigen keuzevrijheid.",
                    ),
                    (
                        "Hoe konden indirecte suggesties verandering op gang brengen?",
                        "Ze activeerden verbeelding, nieuwe interpretaties en innerlijke zoekprocessen waardoor verandering van binnenuit kon ontstaan.",
                    ),
                ],
            },
            {
                "term": "Metaforen en verhalen",
                "questions": [
                    (
                        "Hoe gebruikte Erickson metaforen en verhalen in therapie?",
                        "Erickson gebruikte metaforen en verhalen om onbewuste leerprocessen te activeren en weerstand op een elegante manier te omzeilen.",
                    ),
                    (
                        "Waarom zijn verhalen effectief bij het stimuleren van de verbeeldingskracht van een client?",
                        "Verhalen zijn effectief omdat ze identificatie, beelden, emoties en innerlijke representaties oproepen zonder dat de client zich direct aangevallen voelt.",
                    ),
                    (
                        "Welke rol speelden metaforen in het vinden van nieuwe manieren van denken?",
                        "Metaforen boden alternatieve kaders en nieuwe betekenissen waardoor de client andere perspectieven en oplossingen kon ontdekken.",
                    ),
                ],
            },
            {
                "term": "Taalgebruik",
                "questions": [
                    (
                        "Waarom stond Erickson bekend als meester in taalgebruik en communicatie?",
                        "Hij stond bekend als meester in taalgebruik omdat hij uitzonderlijk precies luisterde en taal subtiel inzette om aandacht, betekenis en ervaring te sturen.",
                    ),
                    (
                        "Hoe gebruikte hij subtiele nuances in de taal van zijn clienten?",
                        "Hij pikte nuances, woordkeus en patronen van clienten op en gebruikte die als ingang voor interventie en verandering.",
                    ),
                    (
                        "Welke invloed had dit taalgebruik later op NLP?",
                        "Dit taalgebruik had grote invloed op NLP, onder meer via het Milton-model en het bredere denken over taalpatronen en therapeutische communicatie.",
                    ),
                ],
            },
        ],
    },
    {
        "topic": "Pre-NLP",
        "concept": "Fritz Perls",
        "distractors": ["Hypnotherapie", "Modelleren"],
        "terms": [
            {
                "term": "Gestalttherapie",
                "questions": [
                    (
                        "Wie was Fritz Perls en wat is zijn rol binnen de Gestalttherapie?",
                        "Fritz Perls was de grondlegger van de Gestalttherapie en ontwikkelde een ervaringsgerichte benadering rond contact, bewustzijn en verantwoordelijkheid.",
                    ),
                    (
                        "Wat maakt Gestalttherapie tot een holistische benadering?",
                        "Gestalttherapie is holistisch omdat denken, voelen, lichaam, gedrag en omgeving als een samenhangend geheel worden benaderd.",
                    ),
                    (
                        "Waarom is Perls belangrijk voor de ontwikkeling van NLP?",
                        "Perls is belangrijk voor NLP omdat zijn werk het belang van directe ervaring, waarneming, contact en verandering in het moment heeft versterkt.",
                    ),
                ],
            },
            {
                "term": "Hier-en-nu",
                "questions": [
                    (
                        "Waarom legt Gestalttherapie nadruk op het huidige moment?",
                        "Gestalttherapie legt nadruk op het huidige moment omdat verandering plaatsvindt in de actuele ervaring en niet alleen in analyse achteraf.",
                    ),
                    (
                        "Wat betekent aandacht voor de relatie tussen individu en omgeving?",
                        "Dat betekent kijken hoe iemand hier en nu contact maakt met de omgeving en welke patronen daarin zichtbaar worden.",
                    ),
                    (
                        "Hoe helpt werken in het hier-en-nu bij verandering?",
                        "Werken in het hier-en-nu maakt patronen direct ervaarbaar en daardoor concreet veranderbaar.",
                    ),
                ],
            },
            {
                "term": "Zelfbewustzijn",
                "questions": [
                    (
                        "Waarom is zelfbewustzijn een kernpunt in het werk van Perls?",
                        "Zelfbewustzijn is een kernpunt omdat bewuste waarneming van gevoelens, impulsen en gedrag nodig is om keuzevrijheid te ontwikkelen.",
                    ),
                    (
                        "Hoe draagt meer zelfbewustzijn bij aan persoonlijke groei?",
                        "Meer zelfbewustzijn helpt iemand automatische patronen te herkennen en bewustere keuzes te maken, wat groei mogelijk maakt.",
                    ),
                    (
                        "Welke relatie is er tussen bewustzijn, gedrag en contact met de omgeving?",
                        "Bewustzijn verbindt innerlijke ervaring met gedrag en bepaalt hoe iemand in contact treedt met de omgeving.",
                    ),
                ],
            },
            {
                "term": "Verantwoordelijkheid",
                "questions": [
                    (
                        "Waarom vond Perls verantwoordelijkheid nemen voor eigen acties belangrijk?",
                        "Perls vond dit belangrijk omdat groei begint wanneer iemand eigenaarschap neemt over gevoelens, keuzes en gedrag.",
                    ),
                    (
                        "Hoe hangt verantwoordelijkheid samen met gezonde relaties?",
                        "Verantwoordelijkheid ondersteunt gezonde relaties doordat projectie en slachtofferschap afnemen en contact eerlijker en directer wordt.",
                    ),
                    (
                        "Wat verandert er wanneer iemand meer verantwoordelijkheid neemt voor de eigen ervaring?",
                        "Iemand krijgt meer invloed op de eigen ervaring, maakt bewustere keuzes en kan effectiever veranderen.",
                    ),
                ],
            },
        ],
    },
    {
        "topic": "Grondleggers van NLP",
        "concept": "Frank Pucelik",
        "distractors": ["Hypnotherapie", "Zelfbewustzijn"],
        "terms": [
            {
                "term": "Co-grondlegger",
                "questions": [
                    (
                        "Wie is Frank Pucelik en waarom wordt hij een grondlegger van NLP genoemd?",
                        "Frank Pucelik is een van de vroege mede-ontwikkelaars van NLP en wordt daarom een grondlegger genoemd.",
                    ),
                    (
                        "Met wie ontwikkelde hij het NLP-model?",
                        "Hij werkte samen met Richard Bandler en John Grinder aan de vroege ontwikkeling van NLP.",
                    ),
                    (
                        "Welke professionele achtergrond nam hij mee in de ontwikkeling van NLP?",
                        "Hij bracht ervaring mee uit therapie, veranderwerk, groepsprocessen en menselijke communicatie.",
                    ),
                ],
            },
            {
                "term": "NLP-model",
                "questions": [
                    (
                        "Waarop is het NLP-model volgens Pucelik gebaseerd?",
                        "Volgens Pucelik is het NLP-model gebaseerd op hoe mensen hun subjectieve ervaring structureren via neurologie, taal en gedrag.",
                    ),
                    (
                        "Hoe spelen taal, communicatie en gedrag hierin samen?",
                        "Taal, communicatie en gedrag grijpen in elkaar omdat woorden betekenis sturen, betekenis gedrag beinvloedt en gedrag weer communicatie vormt.",
                    ),
                    (
                        "Wat bedoelt het model met het veranderen van subjectieve ervaring?",
                        "Daarmee wordt bedoeld dat je patronen van waarnemen, betekenisgeven en reageren kunt herstructureren zodat de innerlijke ervaring verandert.",
                    ),
                ],
            },
            {
                "term": "Menselijke ervaring",
                "questions": [
                    (
                        "Welke nadruk legde Pucelik op menselijke ervaring in zijn werk?",
                        "Hij legde nadruk op hoe mensen hun innerlijke ervaring opbouwen en hoe die ervaring gedrag en keuzes stuurt.",
                    ),
                    (
                        "Hoe vormen taal en communicatie volgens hem onze innerlijke wereld?",
                        "Taal en communicatie vormen onze innerlijke wereld doordat ze bepalen hoe we gebeurtenissen interpreteren en betekenis geven.",
                    ),
                    (
                        "Waarom is dit belangrijk voor persoonlijke ontwikkeling?",
                        "Dit is belangrijk omdat duurzame ontwikkeling begint bij het veranderen van de manier waarop iemand ervaring structureert en begrijpt.",
                    ),
                ],
            },
            {
                "term": "Beperkende overtuigingen en potentieel",
                "questions": [
                    (
                        "Waarop richtte Pucelik zich bij het veranderen van beperkende overtuigingen?",
                        "Hij richtte zich op het herkennen en veranderen van overtuigingen die gedrag, keuzes en persoonlijke mogelijkheden beperken.",
                    ),
                    (
                        "Hoe helpt dit mensen hun potentieel te maximaliseren?",
                        "Door beperkende overtuigingen te veranderen ontstaat meer toegang tot hulpbronnen, keuzevrijheid en gedrag dat beter past bij doelen en potentieel.",
                    ),
                    (
                        "In welke contexten paste hij NLP toe via trainingen en workshops?",
                        "Hij paste NLP toe in trainingen, workshops, coaching en andere ontwikkelcontexten gericht op groei en effectievere communicatie.",
                    ),
                ],
            },
        ],
    },
    {
        "topic": "Grondleggers van NLP",
        "concept": "Richard Bandler",
        "distractors": ["Familiestamboom", "Gestalttherapie"],
        "terms": [
            {
                "term": "Co-creator",
                "questions": [
                    (
                        "Wie is Richard Bandler binnen NLP?",
                        "Richard Bandler is een van de centrale co-creators van NLP.",
                    ),
                    (
                        "Hoe kwam hij samen te werken met John Grinder?",
                        "Hij kwam met John Grinder samen vanuit een gedeelde interesse in taal, therapie en het modelleren van excellente prestaties.",
                    ),
                    (
                        "Waarom geldt hij als een centrale figuur in de ontstaansgeschiedenis van NLP?",
                        "Hij geldt als sleutelpersoon omdat hij actief meebouwde aan de eerste modellen, technieken en trainingen van NLP.",
                    ),
                ],
            },
            {
                "term": "Modelleren van therapeuten",
                "questions": [
                    (
                        "Welke succesvolle therapeuten modelleerden Bandler en Grinder?",
                        "Zij modelleerden onder anderen Virginia Satir, Milton Erickson en Fritz Perls.",
                    ),
                    (
                        "Wat probeerden zij uit deze therapeuten af te leiden?",
                        "Zij probeerden de patronen, taalstructuren en interventies te achterhalen die deze therapeuten effectief maakten.",
                    ),
                    (
                        "Hoe leidde dit modelleren tot de ontwikkeling van NLP?",
                        "Het modelleren leidde tot NLP doordat impliciete successtrategien overdraagbaar en trainbaar werden gemaakt.",
                    ),
                ],
            },
            {
                "term": "Taal, denken en gedrag",
                "questions": [
                    (
                        "Welke samenhang zag Bandler tussen taal, denken en gedrag?",
                        "Bandler zag taal, denken en gedrag als direct met elkaar verbonden onderdelen van menselijke ervaring.",
                    ),
                    (
                        "Waarom is deze samenhang fundamenteel voor NLP?",
                        "Deze samenhang is fundamenteel omdat verandering vaak begint bij hoe ervaring wordt gecodeerd, benoemd en vervolgens uitgevoerd in gedrag.",
                    ),
                    (
                        "Hoe helpt dit inzicht bij verandering en communicatie?",
                        "Het helpt omdat je via taal en representatie invloed kunt uitoefenen op gedrag, beleving en de kwaliteit van communicatie.",
                    ),
                ],
            },
            {
                "term": "Persoonlijke ontwikkeling",
                "questions": [
                    (
                        "Hoe droeg Bandler bij aan persoonlijke ontwikkeling buiten de theorie?",
                        "Bandler droeg bij door technieken en trainingsvormen te ontwikkelen die mensen praktisch helpen veranderen.",
                    ),
                    (
                        "Welke rol speelden seminars en trainingen daarin?",
                        "Seminars en trainingen maakten zijn werk schaalbaar en direct toepasbaar voor veel deelnemers.",
                    ),
                    (
                        "Op welke manier hebben mensen door zijn werk hun leven positief veranderd?",
                        "Via zijn werk veranderden mensen vaak overtuigingen, communicatie, zelfbeeld en gedragsstrategien op een praktische manier.",
                    ),
                ],
            },
        ],
    },
    {
        "topic": "Grondleggers van NLP",
        "concept": "John Grinder",
        "distractors": ["Indirecte suggestie", "Communicatiecategorieen"],
        "terms": [
            {
                "term": "Linguistiek",
                "questions": [
                    (
                        "Wie is John Grinder en wat is zijn taalkundige achtergrond?",
                        "John Grinder is linguist van oorsprong en bracht een sterke taalkundige basis in in NLP.",
                    ),
                    (
                        "Hoe beinvloedde linguistiek zijn bijdrage aan NLP?",
                        "Zijn achtergrond beinvloedde NLP doordat hij scherp keek naar structuur, grammatica, betekenis en patroonvorming in taal.",
                    ),
                    (
                        "Waarom is taal zo belangrijk in zijn visie op menselijk gedrag?",
                        "Taal is belangrijk omdat menselijk gedrag mede wordt gestuurd door hoe ervaringen linguistisch worden geordend en betekenis krijgen.",
                    ),
                ],
            },
            {
                "term": "Modelleren",
                "questions": [
                    (
                        "Met wie werkte Grinder aan de ontwikkeling van NLP?",
                        "Grinder werkte samen met Richard Bandler aan de ontwikkeling van NLP.",
                    ),
                    (
                        "Welke therapeuten werden door hem en zijn collega's bestudeerd?",
                        "Zij bestudeerden onder anderen Virginia Satir, Milton Erickson en Fritz Perls.",
                    ),
                    (
                        "Wat leverde dit modelleren op voor NLP?",
                        "Het modelleren leverde overdraagbare patronen, taalmodellen en interventies op die het fundament van NLP vormden.",
                    ),
                ],
            },
            {
                "term": "Taalstructuren",
                "questions": [
                    (
                        "Welke rol speelden taalstructuren in Grinders werk?",
                        "Taalstructuren stonden centraal omdat ze zichtbaar maken hoe mensen ervaring coderen, generaliseren en vervormen.",
                    ),
                    (
                        "Hoe pasten Bandler en Grinder ideeen uit de taalkunde toe in NLP?",
                        "Zij pasten taalkundige inzichten toe in modellen zoals het metamodel om taalpatronen beter te analyseren en te benutten.",
                    ),
                    (
                        "Waarom zijn taalstructuren belangrijk voor effectieve communicatie?",
                        "Taalstructuren zijn belangrijk omdat effectieve communicatie afhangt van precisie, betekenis en het doorzien van patronen in taalgebruik.",
                    ),
                ],
            },
            {
                "term": "Communicatiepatronen",
                "questions": [
                    (
                        "Wat onderzocht Grinder in de communicatiepatronen van succesvolle therapeuten?",
                        "Grinder onderzocht welke taal- en interactiepatronen succesvolle therapeuten consequent gebruikten.",
                    ),
                    (
                        "Hoe verbond hij taalpatronen aan therapeutisch succes?",
                        "Hij verbond taalpatronen aan succes doordat bepaalde formuleringen direct effect hadden op contact, betekenis en verandering.",
                    ),
                    (
                        "Hoe werd die kennis vertaald naar trainingen in communicatie, management en leiderschap?",
                        "Die kennis werd vertaald naar trainingen waarin taalpatronen en communicatievaardigheden doelgericht werden toegepast in coaching, management en leiderschap.",
                    ),
                ],
            },
        ],
    },
]


def build_module0_exercises() -> list[dict]:
    exercises = list(MODULE0_HEADING_EXERCISES)

    for person in MODULE0_PERSON_DATA:
        correct_terms = [term["term"] for term in person["terms"]]
        exercises.append(
            _build_multi_select(
                title=f"Module 0 - {person['concept']} - termen",
                topic_title=person["topic"],
                concept_title=person["concept"],
                prompt=f"Welke termen vallen onder de subkop {person['concept']}?",
                question=f"Selecteer de termen die bij {person['concept']} horen.",
                option_labels=correct_terms + person["distractors"],
                correct_labels=correct_terms,
                difficulty="intro",
            )
        )

        for term in person["terms"]:
            for index, (question, answer) in enumerate(term["questions"], start=1):
                exercises.append(
                    _build_study_card(
                        title=f"Module 0 - {person['concept']} - {term['term']} - vraag {index}",
                        topic_title=person["topic"],
                        concept_title=person["concept"],
                        prompt=f"{person['concept']} - {term['term']}",
                        question=question,
                        model_answer=answer,
                    )
                )

    return exercises
