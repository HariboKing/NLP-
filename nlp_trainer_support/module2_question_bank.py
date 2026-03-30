from __future__ import annotations


MODULE_TITLE = "Wereldmodellen van NLP"


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


MODULE2_STRUCTURE = [
    {
        "topic": "Het G6 model/de G4 theorie",
        "subheading_distractors": ["XXXX", "XXXX"],
        "concepts": [
            {
                "concept": "Oorsprong en ontwikkeling van het model",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Aaron T. Beck",
                        "questions": [
                            (
                                "Wie was Aaron T. Beck?",
                                "Antwoord op wie Aaron T. Beck is.",
                            ),
                            (
                                "Welke bijdrage leverde Beck aan de cognitieve gedragstherapie?",
                                "Antwoord op hoe Beck een bijdrage leverde aan de ontwikkeling van cognitieve gedragstherapie.",
                            ),
                            (
                                "Wat stelde Beck over de relatie tussen gedachten, emoties en gedrag?",
                                "Antwoord op de vraag.",
                            ),
                            (
                                "Waarom is Beck relevant binnen het hoofdstuk over wereldmodellen?",
                                "Antwoord op de vraag.",
                            ),
                        ],
                    },
                    {
                        "term": "Albert Ellis",
                        "questions": [
                            (
                                "Wie was Albert Ellis?",
                                "Antwoord op de vraag wie Albert Ellis is.",
                            ),
                            (
                                "Welke benadering ontwikkelde Ellis?",
                                "Antwoord op welke benadering Ellis ontwikkelde.",
                            ),
                            (
                                "Wat stelde Ellis over emoties en de manier waarop mensen denken over gebeurtenissen?",
                                "Antwoord wat Ellis stelde over de manier waarop mensen nadachten over gebeurtenissen.",
                            ),
                        ],
                    },
                    {
                        "term": "REBT",
                        "questions": [
                            (
                                "Waar staat REBT voor?",
                                "Rational Emotive Behaviour Therapy.",
                            ),
                            (
                                "Op welk idee is REBT gebaseerd?",
                                "Antwoord waar REBT op is gebaseerd.",
                            ),
                            (
                                "Welke rol spelen irrationele overtuigingen binnen REBT?",
                                "Irrationele overtuigingen spelen volgens REBT een centrale rol in het ontstaan van emotionele problemen.",
                            ),
                            (
                                "Hoe probeert REBT mensen te helpen hun denken te veranderen?",
                                "REBT helpt mensen door irrationele gedachten te herkennen, uit te dagen en te vervangen door rationelere alternatieven.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "De 4G theorie",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Gebeurtenis",
                        "questions": [
                            (
                                "Wat wordt binnen de 4G-theorie bedoeld met een gebeurtenis?",
                                "Binnen de 4G-theorie is een gebeurtenis de concrete situatie of prikkel die plaatsvindt.",
                            ),
                            (
                                "Waarom leidt een gebeurtenis niet automatisch tot een emotie?",
                                "Tussen gebeurtenis en emotie zitten nog andere schakels, zoals gedachte of overtuiging.",
                            ),
                            (
                                "Welke rol speelt de gebeurtenis als startpunt in het model?",
                                "De gebeurtenis vormt het startpunt van de cyclus. Zonder gebeurtenis is er niets om een gedachte of geloof over te vormen.",
                            ),
                            (
                                "Waarom is het belangrijk om gebeurtenis en interpretatie van elkaar te onderscheiden?",
                                "Omdat niet de gebeurtenis zelf, maar de interpretatie ervan bepaalt wat iemand voelt en doet.",
                            ),
                        ],
                    },
                    {
                        "term": "Geloof/gedachte",
                        "questions": [
                            (
                                "Wat wordt bedoeld met geloof of gedachte binnen de 4G-theorie?",
                                "Een geloof of gedachte is de betekenis of interpretatie die iemand aan een gebeurtenis geeft.",
                            ),
                            (
                                "Hoe beïnvloedt een overtuiging de betekenis die iemand aan een gebeurtenis geeft?",
                                "Een overtuiging kleurt hoe iemand een gebeurtenis begrijpt en beoordeelt.",
                            ),
                            (
                                "Waarom zijn juist gedachten en overtuigingen bepalend voor de uitkomst van het model?",
                                "Omdat gedachten en overtuigingen bepalen welk gevoel als volgende stap in de cyclus ontstaat.",
                            ),
                            (
                                "Hoe kunnen vervormde of irrationele gedachten problemen versterken?",
                                "Omdat zij negatieve of problematische gevoelens versterken en daardoor ook onhandig gedrag kunnen uitlokken.",
                            ),
                        ],
                    },
                    {
                        "term": "Gevoel/emotie",
                        "questions": [
                            (
                                "Hoe ontstaan emoties volgens de 4G-theorie?",
                                "Emoties ontstaan uit de betekenis die iemand via gedachten of overtuigingen aan een gebeurtenis geeft.",
                            ),
                            (
                                "Waarom zijn emoties volgens dit model niet direct het gevolg van de gebeurtenis zelf?",
                                "Omdat emoties altijd mede gevormd worden door gedachten of geloof over die gebeurtenis.",
                            ),
                            (
                                "Welke relatie bestaat er tussen overtuiging en emotionele reactie?",
                                "De overtuiging bepaalt in sterke mate welke emotionele reactie op een gebeurtenis ontstaat.",
                            ),
                            (
                                "Hoe kan verandering van denken leiden tot verandering van gevoel?",
                                "Omdat andere gedachten meestal ook andere emoties oproepen.",
                            ),
                        ],
                    },
                    {
                        "term": "Gedrag",
                        "questions": [
                            (
                                "Welke plaats neemt gedrag in binnen de 4G-theorie?",
                                "Gedrag is de laatste schakel voordat weer een nieuwe gebeurtenis of reactie ontstaat.",
                            ),
                            (
                                "Hoe vloeit gedrag voort uit gedachten en emoties?",
                                "We denken iets over een situatie, voelen daar iets bij, en op basis daarvan gaan we handelen.",
                            ),
                            (
                                "Waarom is gedrag zichtbaar bewijs van het onderliggende wereldmodel?",
                                "Omdat gedrag laat zien hoe iemand gebeurtenissen interpreteert en welke overtuigingen daaronder liggen.",
                            ),
                            (
                                "Hoe kan ander denken uiteindelijk leiden tot ander gedrag?",
                                "Andere gedachten leiden vaak tot andere gevoelens, en die zorgen vervolgens voor ander gedrag.",
                            ),
                        ],
                    },
                    {
                        "term": "Irrationele overtuigingen",
                        "questions": [
                            (
                                "Wat zijn irrationele overtuigingen?",
                                "Irrationele overtuigingen zijn onrealistische, starre of onlogische gedachten die problemen in stand kunnen houden.",
                            ),
                            (
                                "Waarom kunnen irrationele overtuigingen leiden tot emotionele en gedragsproblemen?",
                                "Omdat zij negatieve gevoelens versterken en gedrag uitlokken dat niet helpend is.",
                            ),
                            (
                                "Hoe kun je irrationele overtuigingen herkennen binnen de 4G-theorie?",
                                "Je kunt ze herkennen door te onderzoeken welke gedachten tussen gebeurtenis en emotie zitten.",
                            ),
                            (
                                "Waarom is het uitdagen van deze overtuigingen belangrijk?",
                                "Omdat verandering van die overtuigingen kan leiden tot gezondere gevoelens en effectiever gedrag.",
                            ),
                        ],
                    },
                    {
                        "term": "Verandering van denken",
                        "questions": [
                            (
                                "Waarom ligt verandering in dit model vooral op het niveau van denken en overtuigen?",
                                "Omdat dit na de gebeurtenis de eerste schakel is waarop bewust invloed kan worden uitgeoefend.",
                            ),
                            (
                                "Hoe helpt het onderzoeken van gedachten bij gedragsverandering?",
                                "Als je weet welke gedachten irrationeel zijn, kun je gericht werken aan alternatieve gedachten.",
                            ),
                            (
                                "Waarom is een realistischer gedachte vaak functioneler dan een irrationele gedachte?",
                                "Omdat realistischere gedachten vaker leiden tot gevoelens en gedrag die beter werken.",
                            ),
                            (
                                "Hoe sluit dit aan op het NLP-idee van betekenisgeving?",
                                "Het sluit aan omdat NLP ook uitgaat van het idee dat betekenisgeving bepaalt hoe iemand iets ervaart en erop reageert.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Het structureel differentiaal",
        "subheading_distractors": ["XXXX", "XXXX"],
        "concepts": [
            {
                "concept": "Alfred Korzybski",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Algemene semantiek",
                        "questions": [
                            (
                                "Wie was Alfred Korzybski?",
                                "Antwoord op de vraag wie Alfred Korzybski was.",
                            ),
                            (
                                "Wat onderzoekt de theorie van algemene semantiek?",
                                "Antwoord op wat algemene semantiek onderzoekt.",
                            ),
                            (
                                "Waarom is Korzybski belangrijk voor het begrijpen van wereldmodellen?",
                                "Antwoord op waarom Korzybski belangrijk is voor wereldmodellen.",
                            ),
                            (
                                "Hoe verbindt zijn werk taal, denken en ervaring?",
                                "Antwoord op hoe zijn werk taal, denken en ervaring met elkaar verbindt.",
                            ),
                        ],
                    },
                    {
                        "term": "De kaart is niet het gebied",
                        "questions": [
                            (
                                "Wat betekent de uitspraak 'de kaart is niet het gebied'?",
                                "De uitspraak betekent dat onze voorstelling van de werkelijkheid niet hetzelfde is als de werkelijkheid zelf.",
                            ),
                            (
                                "Waarom zijn woorden en symbolen slechts representaties van de werkelijkheid?",
                                "Woorden en symbolen verwijzen naar de werkelijkheid, maar zijn die werkelijkheid niet zelf.",
                            ),
                            (
                                "Hoe helpt deze uitspraak om onderscheid te maken tussen ervaring en interpretatie?",
                                "Deze uitspraak helpt om directe ervaring los te zien van de betekenis of interpretatie die eraan gegeven wordt.",
                            ),
                            (
                                "Waarom is dit een kernidee binnen NLP?",
                                "Omdat NLP uitgaat van subjectieve wereldmodellen in plaats van objectieve werkelijkheid.",
                            ),
                        ],
                    },
                    {
                        "term": "Werkelijkheid versus representatie",
                        "questions": [
                            (
                                "Wat is volgens Korzybski het verschil tussen de werkelijkheid en onze beschrijving daarvan?",
                                "De werkelijkheid is wat er feitelijk is, terwijl onze beschrijving daarvan een vereenvoudigde representatie is.",
                            ),
                            (
                                "Waarom verwarren mensen representaties vaak met de werkelijkheid zelf?",
                                "Omdat mensen geneigd zijn hun taal, beelden en betekenissen voor waar aan te nemen.",
                            ),
                            (
                                "Hoe beïnvloedt dat misverstanden en verkeerde conclusies?",
                                "Het zorgt ervoor dat mensen reageren op hun interpretatie in plaats van op wat er feitelijk gebeurt.",
                            ),
                            (
                                "Waarom is dit onderscheid essentieel voor communicatie?",
                                "Omdat heldere communicatie vraagt om besef dat iedereen vanuit een eigen representatie spreekt.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Algemene semantiek",
        "subheading_distractors": ["XXXX", "XXXX"],
        "concepts": [
            {
                "concept": "Kern van algemene semantiek",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Taal",
                        "questions": [
                            (
                                "Welke rol speelt taal volgens de algemene semantiek?",
                                "Taal speelt een centrale rol in hoe mensen hun ervaringen ordenen en communiceren.",
                            ),
                            (
                                "Waarom structureert taal onze ervaringen?",
                                "Omdat taal bepaalt hoe we onderscheid maken, labelen en betekenis toekennen.",
                            ),
                            (
                                "Waarom zijn woorden niet hetzelfde als de dingen waarnaar ze verwijzen?",
                                "Omdat woorden symbolen zijn en niet de objecten of ervaringen zelf.",
                            ),
                            (
                                "Hoe beïnvloedt taal de manier waarop we de wereld begrijpen?",
                                "Taal stuurt aandacht, interpretatie en de vorm van ons wereldmodel.",
                            ),
                        ],
                    },
                    {
                        "term": "Denken",
                        "questions": [
                            (
                                "Hoe hangt denken samen met taal volgens Korzybski?",
                                "Denken en taal zijn nauw verbonden, omdat taal de structuur van ons denken mede vormgeeft.",
                            ),
                            (
                                "Waarom weerspiegelt de structuur van taal de structuur van perceptie en denken?",
                                "Omdat mensen hun waarneming en interpretatie in taal omzetten volgens herkenbare patronen.",
                            ),
                            (
                                "Hoe kunnen onbewuste denkgewoonten onze communicatie beïnvloeden?",
                                "Onbewuste denkgewoonten sturen woordkeuze, betekenisgeving en reacties zonder dat we dat direct merken.",
                            ),
                            (
                                "Waarom is reflectie op het eigen denken belangrijk?",
                                "Omdat je zo bewuster wordt van je aannames en nauwkeuriger leert communiceren.",
                            ),
                        ],
                    },
                    {
                        "term": "Ervaring",
                        "questions": [
                            (
                                "Waarom staat ervaring centraal in de algemene semantiek?",
                                "Omdat ervaring de basis is waarop mensen betekenis, taal en oordelen bouwen.",
                            ),
                            (
                                "Hoe verschilt ervaring van de woorden die we eraan geven?",
                                "Ervaring is direct en zintuiglijk, terwijl woorden slechts beschrijvingen of symbolen ervan zijn.",
                            ),
                            (
                                "Waarom leidt dit onderscheid tot meer nauwkeurigheid in communicatie?",
                                "Omdat je dan minder snel je beschrijving verwart met de werkelijkheid zelf.",
                            ),
                            (
                                "Hoe helpt dit om misverstanden te voorkomen?",
                                "Het helpt mensen om zorgvuldiger te formuleren en open te blijven voor andere interpretaties.",
                            ),
                        ],
                    },
                    {
                        "term": "Structureren van ervaring",
                        "questions": [
                            (
                                "Hoe gebruiken mensen taal om hun ervaringen te structureren?",
                                "Mensen geven met taal vorm aan wat ze waarnemen, onthouden en begrijpen.",
                            ),
                            (
                                "Waarom leidt deze structurering tot niveaus van betekenis en begrip?",
                                "Omdat elke stap van ervaring naar taal en oordeel een extra laag van abstractie toevoegt.",
                            ),
                            (
                                "Hoe beïnvloedt dit onze interpretaties en oordelen?",
                                "Het zorgt ervoor dat interpretaties vaak gebaseerd zijn op bewerkte in plaats van directe ervaring.",
                            ),
                            (
                                "Waarom is bewustwording van die structuur nuttig?",
                                "Omdat het helpt om nauwkeuriger te denken, communiceren en waarnemen.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Reflectie en communicatie",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Kritisch reflecteren",
                        "questions": [
                            (
                                "Waarom moedigt de manual kritisch reflecteren op taal en denken aan?",
                                "Omdat kritisch reflecteren helpt om aannames, vertekeningen en onduidelijkheden te herkennen.",
                            ),
                            (
                                "Hoe helpt kritisch reflecteren om eigen aannames te herkennen?",
                                "Door stil te staan bij de woorden, betekenissen en conclusies die je automatisch trekt.",
                            ),
                            (
                                "Waarom is dat belangrijk voor helderder communiceren?",
                                "Omdat je preciezer leert formuleren en minder snel praat vanuit onbewuste oordelen.",
                            ),
                            (
                                "Hoe draagt dit bij aan betere besluitvorming?",
                                "Omdat betere besluitvorming gebaseerd is op nauwkeuriger waarnemen en denken.",
                            ),
                        ],
                    },
                    {
                        "term": "Communicatie verbeteren",
                        "questions": [
                            (
                                "Hoe helpt algemene semantiek om communicatie te verbeteren?",
                                "Algemene semantiek helpt om nauwkeuriger en bewuster om te gaan met taal en betekenis.",
                            ),
                            (
                                "Waarom leidt nauwkeuriger taalgebruik tot minder misverstanden?",
                                "Omdat minder onduidelijke of absolute formuleringen leiden tot meer gedeeld begrip.",
                            ),
                            (
                                "Hoe beïnvloedt bewust taalgebruik de kwaliteit van interactie?",
                                "Bewust taalgebruik maakt gesprekken helderder, respectvoller en effectiever.",
                            ),
                            (
                                "Waarom is dit relevant binnen NLP?",
                                "Omdat NLP sterk werkt met taal, betekenis en subjectieve ervaring.",
                            ),
                        ],
                    },
                    {
                        "term": "Openere en inclusievere maatschappij",
                        "questions": [
                            (
                                "Waarom verbindt de manual algemene semantiek met een opener en inclusievere maatschappij?",
                                "Omdat bewuster omgaan met taal en betekenis ruimte maakt voor meer begrip tussen mensen.",
                            ),
                            (
                                "Hoe kan bewustzijn van taal bijdragen aan meer begrip voor verschillen?",
                                "Het helpt om minder snel vanuit eigen aannames te reageren op anderen.",
                            ),
                            (
                                "Waarom helpt dit om minder snel te veroordelen?",
                                "Omdat je leert zien dat jouw beschrijving of oordeel niet gelijk is aan de volledige werkelijkheid.",
                            ),
                            (
                                "Welke rol speelt dit in sociale interactie?",
                                "Het bevordert respect, nuance en betere afstemming tussen mensen.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Korzybski citaten en hun betekenis",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "De kaart is niet het gebied",
                        "questions": [
                            (
                                "Wat leert dit citaat over representatie en werkelijkheid?",
                                "Het leert dat onze voorstelling van de werkelijkheid niet hetzelfde is als de werkelijkheid zelf.",
                            ),
                            (
                                "Waarom is dit citaat zo fundamenteel voor NLP?",
                                "Omdat NLP uitgaat van persoonlijke kaarten of wereldmodellen in plaats van objectieve waarheid.",
                            ),
                            (
                                "Hoe helpt dit om subjectieve ervaring beter te begrijpen?",
                                "Het maakt duidelijk dat mensen reageren op hun eigen interpretatie van de werkelijkheid.",
                            ),
                            (
                                "Waarom vraagt dit om bescheidenheid in oordelen?",
                                "Omdat je nooit over de volledige werkelijkheid beschikt, maar slechts over jouw representatie ervan.",
                            ),
                        ],
                    },
                    {
                        "term": "Niet de dingen zelf, maar onze ideeën erover",
                        "questions": [
                            (
                                "Wat betekent Korzybski's uitspraak dat niet de dingen zelf ons van streek maken, maar onze ideeën daarover?",
                                "Dat onze reactie niet direct voortkomt uit de gebeurtenis, maar uit de betekenis die wij eraan geven.",
                            ),
                            (
                                "Hoe benadrukt dit de rol van interpretatie?",
                                "Het laat zien dat interpretatie de brug vormt tussen ervaring en emotionele reactie.",
                            ),
                            (
                                "Waarom sluit dit aan op het idee van wereldmodellen?",
                                "Omdat wereldmodellen bepalen hoe iemand gebeurtenissen interpreteert.",
                            ),
                            (
                                "Hoe kan dit inzicht helpen bij verandering?",
                                "Door interpretaties te onderzoeken en te veranderen, kunnen ook emoties en gedrag veranderen.",
                            ),
                        ],
                    },
                    {
                        "term": "Onderscheidingen en verschillen",
                        "questions": [
                            (
                                "Wat bedoelt Korzybski met de uitspraak dat de wereld uit onderscheidingen en verschillen bestaat?",
                                "Dat nauwkeurig waarnemen draait om verschillen zien in plaats van alles over één kam scheren.",
                            ),
                            (
                                "Waarom waarschuwt dit tegen valse generalisaties?",
                                "Omdat generalisaties unieke eigenschappen en nuances uitwissen.",
                            ),
                            (
                                "Hoe helpt dit om preciezer waar te nemen?",
                                "Door aandacht te hebben voor details en concrete verschillen in ervaring of gedrag.",
                            ),
                            (
                                "Waarom is dit relevant voor communicatie?",
                                "Omdat preciezer waarnemen en formuleren leidt tot helderdere communicatie.",
                            ),
                        ],
                    },
                    {
                        "term": "Woorden zijn symbolen",
                        "questions": [
                            (
                                "Waarom noemt Korzybski woorden symbolen van de wereld en niet de wereld zelf?",
                                "Omdat woorden alleen verwijzen naar de wereld, maar die niet letterlijk bevatten of vervangen.",
                            ),
                            (
                                "Hoe voorkomt dit dat taal absoluut wordt genomen?",
                                "Het herinnert eraan dat taal altijd een vereenvoudigde weergave is.",
                            ),
                            (
                                "Waarom is dit onderscheid belangrijk in gesprekken?",
                                "Omdat het helpt om open te blijven voor nuance, context en alternatieve betekenissen.",
                            ),
                            (
                                "Hoe ondersteunt dit het ontwikkelen van flexibelere wereldmodellen?",
                                "Omdat je minder vast komt te zitten in absolute formuleringen en meer ruimte krijgt voor andere perspectieven.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Filosofie en NLP",
        "subheading_distractors": ["XXXX", "XXXX"],
        "concepts": [
            {
                "concept": "Taal en betekenis",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Taal vormt realiteit",
                        "questions": [
                            (
                                "Waarom speelt taal zowel in NLP als in filosofie een cruciale rol?",
                                "Omdat taal een hoofdrol speelt in hoe mensen hun werkelijkheid begrijpen, ordenen en communiceren.",
                            ),
                            (
                                "Hoe scheppen woorden volgens de manual de wereld zoals wij die begrijpen?",
                                "Woorden geven vorm aan betekenis en sturen hoe ervaringen geïnterpreteerd worden.",
                            ),
                            (
                                "Waarom beïnvloedt taal onze percepties en overtuigingen?",
                                "Omdat de taal die we gebruiken bepaalt welke aspecten we benadrukken of negeren.",
                            ),
                            (
                                "Hoe sluit dit aan op het thema wereldmodellen?",
                                "Wereldmodellen worden mede opgebouwd uit taal, betekenissen en interpretaties.",
                            ),
                        ],
                    },
                    {
                        "term": "Wittgenstein",
                        "questions": [
                            (
                                "Welke rol speelt Wittgenstein in dit onderdeel van de manual?",
                                "Wittgenstein wordt genoemd als filosoof die benadrukte dat betekenis voortkomt uit taalgebruik in context.",
                            ),
                            (
                                "Wat wordt bedoeld met zijn idee dat de betekenis van woorden in hun gebruik ligt?",
                                "Dat woorden geen vaste betekenis hebben los van de situatie waarin ze gebruikt worden.",
                            ),
                            (
                                "Waarom sluit dit aan bij NLP?",
                                "Omdat NLP ook kijkt naar hoe taal in concrete communicatie betekenis krijgt en effect heeft.",
                            ),
                            (
                                "Hoe helpt deze gedachte om taal contextueel te benaderen?",
                                "Het maakt duidelijk dat woorden pas begrepen kunnen worden binnen hun gebruik en situatie.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Bewustzijn en ervaring",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Bewustzijn",
                        "questions": [
                            (
                                "Hoe beschouwt NLP bewustzijn volgens de manual?",
                                "NLP beschouwt bewustzijn als iets wat invloed heeft op ervaring en gedrag en dat ontwikkeld kan worden.",
                            ),
                            (
                                "Waarom wordt bewustzijn beschreven als iets dat getraind en geprogrammeerd kan worden?",
                                "Omdat NLP ervan uitgaat dat mentale processen beïnvloed en herstructureerd kunnen worden.",
                            ),
                            (
                                "Hoe verschilt deze benadering van een puur filosofische analyse van bewustzijn?",
                                "De NLP-benadering is praktischer en gericht op verandering, terwijl filosofie vaker beschouwend is.",
                            ),
                            (
                                "Waarom is dit relevant voor verandering?",
                                "Omdat verandering begint bij bewustwording van hoe ervaring wordt opgebouwd.",
                            ),
                        ],
                    },
                    {
                        "term": "Husserl/fenomenologie",
                        "questions": [
                            (
                                "Waarom wordt Edmund Husserl in dit deel genoemd?",
                                "Omdat Husserl als grondlegger van de fenomenologie de directe ervaring centraal stelde.",
                            ),
                            (
                                "Hoe sluit fenomenologie aan op het bestuderen van ervaring?",
                                "Fenomenologie onderzoekt hoe verschijnselen beleefd worden vanuit de eerste persoon.",
                            ),
                            (
                                "Wat is het verschil tussen filosofisch begrijpen van ervaring en NLP-technieken om ervaring te veranderen?",
                                "Filosofie beschrijft en onderzoekt ervaring, terwijl NLP vooral gericht is op beïnvloeden en herstructureren.",
                            ),
                            (
                                "Waarom versterken deze invalshoeken elkaar?",
                                "Omdat ze allebei subjectieve ervaring serieus nemen, maar vanuit een ander doel.",
                            ),
                        ],
                    },
                    {
                        "term": "Herstructureren van ervaring",
                        "questions": [
                            (
                                "Hoe helpt NLP mensen om bewustzijn en ervaring te herstructureren?",
                                "Door technieken aan te bieden waarmee betekenis, focus en beleving veranderd kunnen worden.",
                            ),
                            (
                                "Waarom is dit volgens de manual praktisch toepasbaar?",
                                "Omdat het direct gebruikt kan worden in communicatie, coaching en persoonlijke ontwikkeling.",
                            ),
                            (
                                "Hoe verschilt een bewuste interventie van alleen theoretisch inzicht?",
                                "Een interventie verandert daadwerkelijk de ervaring, terwijl inzicht alleen begrip geeft.",
                            ),
                            (
                                "Waarom is deze koppeling belangrijk binnen hoofdstuk 2?",
                                "Omdat wereldmodellen pas echt relevant worden wanneer ze ook beïnvloed en veranderd kunnen worden.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Constructie van realiteit",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Kaart van de werkelijkheid",
                        "questions": [
                            (
                                "Hoe gebruikt NLP de metafoor van de kaart om menselijke perceptie uit te leggen?",
                                "NLP gebruikt de kaartmetafoor om te laten zien dat mensen de werkelijkheid via een eigen model ervaren.",
                            ),
                            (
                                "Waarom creëert ieder individu een eigen kaart van de werkelijkheid?",
                                "Omdat ervaringen, overtuigingen, waarden en filters per persoon verschillen.",
                            ),
                            (
                                "Waarom is die kaart geen objectieve representatie van de echte wereld?",
                                "Omdat een kaart altijd een selectie en interpretatie is van wat werkelijk bestaat.",
                            ),
                            (
                                "Hoe helpt dit begrip om wereldmodellen te begrijpen?",
                                "Het maakt duidelijk dat wereldmodellen persoonlijke constructies zijn waarmee mensen betekenis geven.",
                            ),
                        ],
                    },
                    {
                        "term": "Constructivisme",
                        "questions": [
                            (
                                "Wat is de relatie tussen NLP en constructivisme volgens de manual?",
                                "Beide gaan ervan uit dat mensen hun werkelijkheid mede zelf construeren.",
                            ),
                            (
                                "Waarom stelt constructivisme dat kennis van de realiteit altijd gekleurd is door mentale en culturele kaders?",
                                "Omdat waarneming en interpretatie nooit losstaan van eerdere ervaringen en context.",
                            ),
                            (
                                "Hoe ondersteunt dit de NLP-visie op subjectieve ervaring?",
                                "Het bevestigt dat mensen reageren op hun eigen constructie van de werkelijkheid.",
                            ),
                            (
                                "Waarom is dit belangrijk voor communicatie en verandering?",
                                "Omdat verandering mogelijk wordt zodra iemand zijn constructie anders leert organiseren.",
                            ),
                        ],
                    },
                    {
                        "term": "Subjectieve interpretatie",
                        "questions": [
                            (
                                "Waarom zijn onze kaarten subjectieve interpretaties en geen absolute waarheden?",
                                "Omdat ze gevormd worden door persoonlijke filters, ervaringen en overtuigingen.",
                            ),
                            (
                                "Hoe beïnvloeden overtuigingen, ervaringen en waarden die interpretaties?",
                                "Zij bepalen wat iemand opmerkt, hoe iets wordt begrepen en welke betekenis eraan wordt toegekend.",
                            ),
                            (
                                "Waarom leidt dit tot verschillende wereldmodellen tussen mensen?",
                                "Omdat niemand exact dezelfde achtergrond, filters en interpretatiekaders heeft.",
                            ),
                            (
                                "Hoe helpt dit om conflicten en misverstanden te begrijpen?",
                                "Het maakt duidelijk dat mensen vaak botsen vanuit verschillende interpretaties van dezelfde situatie.",
                            ),
                        ],
                    },
                    {
                        "term": "Postmodernisme",
                        "questions": [
                            (
                                "Waarom wordt postmodernisme in de manual genoemd?",
                                "Omdat postmodernisme de nadruk legt op perspectief, interpretatie en het ontbreken van één absolute waarheid.",
                            ),
                            (
                                "Hoe sluit de gedachte dat objectieve waarheid moeilijk grijpbaar is aan op NLP?",
                                "Omdat NLP werkt met subjectieve modellen van de werkelijkheid in plaats van één objectieve versie.",
                            ),
                            (
                                "Waarom benadrukt dit het belang van perspectief?",
                                "Omdat elk perspectief een andere toegang geeft tot betekenis en ervaring.",
                            ),
                            (
                                "Hoe ondersteunt dit het idee dat realiteit mede geconstrueerd wordt?",
                                "Het laat zien dat mensen via taal en interpretatie actief vorm geven aan hun beleving van de werkelijkheid.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Ethiek en verantwoordelijkheid",
                "distractors": ["XXXX", "XXXX"],
                "terms": [
                    {
                        "term": "Persoonlijke verantwoordelijkheid",
                        "questions": [
                            (
                                "Welke ethische vraag roept NLP op rond persoonlijke verantwoordelijkheid?",
                                "De ethische vraag is in hoeverre mensen verantwoordelijkheid dragen voor hun interpretaties, reacties en keuzes.",
                            ),
                            (
                                "Waarom benadrukt de manual dat individuen verantwoordelijkheid dragen voor hun reacties en emoties?",
                                "Omdat reacties en emoties mede voortkomen uit de betekenis die iemand zelf aan ervaringen geeft.",
                            ),
                            (
                                "Hoe sluit dit aan op het thema betekenisgeving?",
                                "Betekenisgeving vormt de schakel tussen gebeurtenis en reactie, en daar ligt persoonlijke invloed.",
                            ),
                            (
                                "Waarom is dit belangrijk voor persoonlijke ontwikkeling?",
                                "Omdat groei begint waar iemand verantwoordelijkheid neemt voor eigen ervaring en gedrag.",
                            ),
                        ],
                    },
                    {
                        "term": "Jean-Paul Sartre",
                        "questions": [
                            (
                                "Waarom wordt Sartre in dit hoofdstuk genoemd?",
                                "Sartre wordt genoemd vanwege zijn nadruk op vrijheid, keuze en verantwoordelijkheid.",
                            ),
                            (
                                "Wat stelde Sartre over vrijheid en verantwoordelijkheid?",
                                "Dat mensen vrij zijn om te kiezen en daarom ook verantwoordelijkheid dragen voor die keuzes.",
                            ),
                            (
                                "Hoe sluit dit aan op de ethische dimensie van NLP?",
                                "Omdat NLP mensen uitnodigt om bewust keuzes te maken in hun denken, voelen en handelen.",
                            ),
                            (
                                "Waarom is de koppeling met existentialisme relevant?",
                                "Omdat existentialisme net als NLP aandacht geeft aan keuzevrijheid, betekenis en persoonlijke verantwoordelijkheid.",
                            ),
                        ],
                    },
                    {
                        "term": "Controle over eigen ervaring",
                        "questions": [
                            (
                                "Hoe moedigt NLP mensen aan om controle te nemen over hun eigen ervaringen?",
                                "Door hen bewust te maken van hun wereldmodel en mogelijkheden om betekenis en reactie te veranderen.",
                            ),
                            (
                                "Waarom is dit meer dan alleen positief denken?",
                                "Omdat het gaat om actief onderzoeken, herstructureren en beïnvloeden van ervaring.",
                            ),
                            (
                                "Hoe verbindt dit keuzevrijheid met verantwoordelijkheid?",
                                "Hoe meer keuze iemand heeft, hoe meer verantwoordelijkheid hij ook draagt voor wat hij ermee doet.",
                            ),
                            (
                                "Waarom is dit een belangrijk filosofisch raakvlak?",
                                "Omdat het de brug vormt tussen praktische verandering en vragen over vrijheid, ethiek en mensbeeld.",
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


def build_module2_topics() -> list[dict]:
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
        for topic in MODULE2_STRUCTURE
    ]


MODULE2_TOPIC_BLUEPRINT = build_module2_topics()


def build_module2_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE2_STRUCTURE]
    heading_options = topic_names + [
        "De kunst van magische taalpatronen",
        "Fundamenten van NLP",
    ]
    exercises = [
        _build_multi_select(
            title="Wereldmodellen van NLP - hoofdstukkoppen",
            topic_title=MODULE2_STRUCTURE[0]["topic"],
            concept_title=MODULE2_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder hoofdstuk 2 Wereldmodellen van NLP?",
            question="Selecteer de koppen die bij hoofdstuk 2 Wereldmodellen van NLP horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE2_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"Wereldmodellen van NLP - {topic['topic']} subkoppen",
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
                    title=f"Wereldmodellen van NLP - {concept['concept']} termen",
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
                                f"Wereldmodellen van NLP - {concept['concept']} - {term['term']} - vraag {question_index}"
                            ),
                            topic_title=topic["topic"],
                            concept_title=concept["concept"],
                            prompt=question,
                            question=question,
                            model_answer=model_answer,
                        )
                    )

    return exercises
