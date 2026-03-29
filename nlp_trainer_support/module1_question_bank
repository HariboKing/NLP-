from __future__ import annotations


MODULE_TITLE = "Fundamenten van NLP"


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


MODULE1_STRUCTURE = [
    {
        "topic": "Wat is NLP / NLP staat voor / Over NLP",
        "subheading_distractors": ["Rob Kamps", "Spelend leren"],
        "concepts": [
            {
                "concept": "Wat is NLP",
                "distractors": ["NLP als attitude", "Rob Kamps"],
                "terms": [
                    {
                        "term": "Definitie van NLP",
                        "questions": [
                            (
                                "Wat is Neuro-Linguistisch Programmeren volgens de manual?",
                                "Volgens de manual is NLP een benadering die onderzoekt hoe mensen via neurologie, taal en patronen hun ervaring structureren en veranderen.",
                            ),
                            (
                                "Op welke gebieden richt NLP zich: communicatie, emoties, gedachten of gedrag?",
                                "NLP richt zich op al deze gebieden, omdat communicatie, emoties, gedachten en gedrag elkaar voortdurend beinvloeden.",
                            ),
                            (
                                "Wat wil NLP bij mensen begrijpen en verbeteren?",
                                "NLP wil begrijpen hoe mensen denken, voelen, betekenis geven en handelen, zodat die processen doelgerichter en effectiever kunnen worden verbeterd.",
                            ),
                            (
                                "Waarom wordt NLP beschreven als een benadering van communicatie en persoonlijke ontwikkeling?",
                                "Omdat NLP zowel gaat over hoe mensen met zichzelf en anderen communiceren als over hoe zij hun gedrag, resultaten en groei kunnen verbeteren.",
                            ),
                        ],
                    },
                    {
                        "term": "Ontstaan van NLP",
                        "questions": [
                            ("In welke periode is NLP ontstaan?", "NLP is ontstaan in de jaren zeventig van de twintigste eeuw."),
                            (
                                "Welke drie grondleggers worden in de manual genoemd bij het ontstaan van NLP?",
                                "De manual noemt Frank Pucelik, Richard Bandler en John Grinder.",
                            ),
                            (
                                "Welke succesvolle therapeuten werden bestudeerd bij de ontwikkeling van NLP?",
                                "Bij de ontwikkeling van NLP werden onder anderen Virginia Satir, Milton Erickson en Fritz Perls bestudeerd.",
                            ),
                            (
                                "Welke vraag lag aan de basis van het modelleren van deze therapeuten?",
                                "De kernvraag was welke specifieke patronen en vaardigheden deze therapeuten zo effectief maakten en hoe die overdraagbaar konden worden gemaakt.",
                            ),
                            (
                                "Waarom waren de grondleggers niet tevreden met bestaande psychotherapiemethoden?",
                                "Omdat veel bestaande methoden volgens hen te weinig concreet, overdraagbaar en praktisch leerbaar waren voor anderen.",
                            ),
                        ],
                    },
                    {
                        "term": "Modelleren",
                        "questions": [
                            (
                                "Wat betekent modelleren binnen NLP?",
                                "Modelleren betekent dat je de structuur van excellent gedrag onderzoekt, expliciet maakt en overdraagbaar maakt.",
                            ),
                            (
                                "Waarom is modelleren een kernprincipe van NLP?",
                                "Omdat NLP ervan uitgaat dat succespatronen leerbaar worden zodra je hun onderliggende structuur zichtbaar maakt.",
                            ),
                            (
                                "Wat probeerden Pucelik, Bandler en Grinder uit het gedrag van succesvolle therapeuten af te leiden?",
                                "Zij probeerden de taalpatronen, denkwijzen, waarnemingsstrategien en interventies te achterhalen die tot uitzonderlijke resultaten leidden.",
                            ),
                            (
                                "Waarom moest wat zij vonden overdraagbaar en leerbaar zijn voor anderen?",
                                "Omdat het doel van NLP niet alleen begrijpen is, maar ook dat anderen dezelfde effectieve patronen kunnen leren toepassen.",
                            ),
                        ],
                    },
                    {
                        "term": "Structuur van subjectieve ervaring",
                        "questions": [
                            (
                                "Wat bedoelt de manual met de structuur van subjectieve ervaring?",
                                "Daarmee bedoelt de manual de manier waarop iemand innerlijke ervaring opbouwt via waarneming, betekenis, taal en interne representatie.",
                            ),
                            (
                                "Waarom gaat het in NLP niet alleen om wat iemand meemaakt, maar vooral om wat iemand ermee doet?",
                                "Omdat niet de gebeurtenis zelf maar de interne verwerking en betekenisgeving bepalen hoe iemand zich voelt en handelt.",
                            ),
                            (
                                "Hoe beinvloedt betekenisgeving gedrag en resultaat?",
                                "Betekenisgeving stuurt emoties, verwachtingen, keuzes en daardoor ook gedrag en uiteindelijke resultaten.",
                            ),
                            (
                                "Waarom ligt hier volgens de manual de kern van het succes van NLP?",
                                "Omdat juist het veranderen van deze structuur mensen nieuwe keuzes, andere ervaringen en betere resultaten geeft.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "NLP staat voor",
                "distractors": ["NLP als methodologie", "Rob Kamps"],
                "terms": [
                    {
                        "term": "Neuro",
                        "questions": [
                            (
                                "Waar verwijst het onderdeel neuro naar binnen NLP?",
                                "Neuro verwijst naar het zenuwstelsel en de manier waarop ervaring via zintuigen en neurologische processen wordt verwerkt.",
                            ),
                            (
                                "Welke rol spelen zintuiglijke processen in het ontstaan van gedrag?",
                                "Zintuiglijke processen leveren de ruwe input waarmee mensen hun ervaring opbouwen en waaruit gedrag voortkomt.",
                            ),
                            (
                                "Waarom is waarneming essentieel binnen NLP?",
                                "Omdat waarneming het startpunt is van betekenisgeving, emotie en reactie.",
                            ),
                            (
                                "Hoe hangt neuro samen met ervaren en reageren?",
                                "Wat mensen neurologisch registreren en coderen bepaalt hoe zij iets ervaren en hoe zij vervolgens reageren.",
                            ),
                        ],
                    },
                    {
                        "term": "Linguistisch",
                        "questions": [
                            (
                                "Waar verwijst het onderdeel linguistisch naar binnen NLP?",
                                "Linguistisch verwijst naar taal, symbolen en de manier waarop mensen ervaring benoemen en ordenen.",
                            ),
                            (
                                "Hoe gebruiken mensen taal om gedachten en gedrag te ordenen?",
                                "Mensen gebruiken taal om ervaringen te categoriseren, betekenis te geven en richting te geven aan hun denken en handelen.",
                            ),
                            (
                                "Waarom heeft taal zoveel invloed op betekenis, emoties en gedrag?",
                                "Omdat taal niet alleen beschrijft, maar ook focus legt, interpretatie stuurt en emotionele reacties kan versterken of veranderen.",
                            ),
                            (
                                "Hoe helpt taal ons om te communiceren met anderen?",
                                "Taal maakt het mogelijk om innerlijke ervaring te delen, af te stemmen en gezamenlijk betekenis te vormen.",
                            ),
                        ],
                    },
                    {
                        "term": "Programmeren",
                        "questions": [
                            (
                                "Waar verwijst het onderdeel programmeren naar binnen NLP?",
                                "Programmeren verwijst naar de patronen en strategieen waarmee mensen denken, voelen en handelen organiseren.",
                            ),
                            (
                                "Hoe structureren en organiseren mensen hun ideeen en gedragingen?",
                                "Zij doen dat via terugkerende interne strategieen, overtuigingen, taalpatronen en gewoonten.",
                            ),
                            (
                                "Waarom is programmeren belangrijk voor het bereiken van doelen?",
                                "Omdat doelgericht gedrag makkelijker verandert wanneer de onderliggende patronen bewust worden gemaakt en opnieuw ingericht kunnen worden.",
                            ),
                            (
                                "Hoe hangt programmeren samen met het veranderen van patronen?",
                                "Wie patronen kan herkennen en herstructureren, kan gedrag en resultaten gerichter veranderen.",
                            ),
                        ],
                    },
                    {
                        "term": "Van wens naar resultaat",
                        "questions": [
                            (
                                "Welke drie stappen laat het schema van wens naar resultaat zien?",
                                "Het schema laat zien dat een wens via gedrag en actie wordt omgezet in een concreet resultaat.",
                            ),
                            (
                                "Hoe hangen intentie, gedrag en resultaat met elkaar samen?",
                                "Intentie geeft richting, gedrag maakt uitvoering mogelijk en resultaat laat zien wat de werkelijke uitkomst van dat gedrag is.",
                            ),
                            (
                                "Waarom is een duidelijk doel nodig voordat verandering mogelijk wordt?",
                                "Omdat zonder duidelijk doel gedrag versnipperd raakt en niet goed op resultaat gestuurd kan worden.",
                            ),
                            (
                                "Wat zegt dit schema over verantwoordelijkheid voor uitkomsten?",
                                "Dat mensen verantwoordelijkheid dragen voor het afstemmen van hun gedrag op het resultaat dat zij werkelijk willen bereiken.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Over NLP",
                "distractors": ["NLP anno nu", "Rob Kamps"],
                "terms": [
                    {
                        "term": "NLP als attitude",
                        "questions": [
                            (
                                "Waarom beschrijft Frank Pucelik NLP als een attitude?",
                                "Omdat NLP volgens hem niet alleen uit technieken bestaat, maar ook uit een manier van kijken, leren en communiceren.",
                            ),
                            (
                                "Welke rol spelen nieuwsgierigheid en avontuurlijkheid in die attitude?",
                                "Nieuwsgierigheid en avontuurlijkheid stimuleren open onderzoek, experimenteren en het zoeken naar nieuwe mogelijkheden.",
                            ),
                            (
                                "Waarom hoort leren en ontdekken wezenlijk bij NLP?",
                                "Omdat NLP vertrekt vanuit de gedachte dat ervaring onderzocht, gemodelleerd en verfijnd kan worden.",
                            ),
                            (
                                "Hoe beinvloedt deze houding de manier waarop iemand naar communicatie kijkt?",
                                "Je kijkt dan minder oordelend en meer onderzoekend naar wat werkt, wat niet werkt en wat veranderd kan worden.",
                            ),
                        ],
                    },
                    {
                        "term": "NLP als methodologie",
                        "questions": [
                            (
                                "Waarom wordt NLP ook een methodologie genoemd?",
                                "Omdat NLP een systematische manier biedt om patronen in gedrag en ervaring te onderzoeken, te modelleren en te veranderen.",
                            ),
                            (
                                "Welke aanname over gedrag ligt aan deze methodologie ten grondslag?",
                                "De aanname dat gedrag structuur heeft en dat die structuur herkenbaar en veranderbaar is.",
                            ),
                            (
                                "Hoe maakt deze methodologie modelleren, leren en veranderen mogelijk?",
                                "Door succesvolle patronen op te sporen, te beschrijven en vertaalbaar te maken naar concrete stappen voor anderen.",
                            ),
                            (
                                "Waarom is structuur daarin belangrijk?",
                                "Omdat zonder structuur succes vaag blijft en dus niet betrouwbaar overdraagbaar of herhaalbaar wordt.",
                            ),
                        ],
                    },
                    {
                        "term": "NLP als technologie",
                        "questions": [
                            (
                                "Waarom wordt NLP in de manual een innovatieve technologie genoemd?",
                                "Omdat NLP praktische methoden biedt om informatie, perceptie en gedrag doelgericht te organiseren en te veranderen.",
                            ),
                            (
                                "Wat kunnen beoefenaars met informatie en perceptie doen volgens deze beschrijving?",
                                "Zij kunnen informatie en perceptie benutten om bewust invloed uit te oefenen op ervaring, communicatie en gedrag.",
                            ),
                            (
                                "Hoe helpt deze technologie mensen resultaten te bereiken?",
                                "Door bruikbare strategieen te bieden waarmee mensen effectiever kunnen leren, communiceren en veranderen.",
                            ),
                            (
                                "Wat zegt deze formulering over praktische toepasbaarheid?",
                                "Dat NLP niet alleen theoretisch is, maar vooral bedoeld is om zichtbaar resultaat in de praktijk op te leveren.",
                            ),
                        ],
                    },
                    {
                        "term": "NLP als holistisch communicatie-instrument",
                        "questions": [
                            (
                                "Waarom wordt NLP een holistisch instrument voor communicatie genoemd?",
                                "Omdat NLP communicatie ziet als een samenspel van taal, gedrag, emotie, context en non-verbale signalen.",
                            ),
                            (
                                "Wat betekent de uitspraak dat communicatie niet je intentie is, maar het resultaat dat je bereikt?",
                                "Dat de werkelijke betekenis van communicatie blijkt uit de respons die je oproept, niet alleen uit wat je bedoelde.",
                            ),
                            (
                                "Hoe verandert dat de manier waarop je naar gesprekken kijkt?",
                                "Je gaat sterker letten op effect, afstemming en terugkoppeling in plaats van alleen op je eigen bedoeling.",
                            ),
                            (
                                "Waarom vraagt dit om verantwoordelijkheid van de communicator?",
                                "Omdat jij je communicatie moet aanpassen wanneer de respons niet overeenkomt met het gewenste effect.",
                            ),
                        ],
                    },
                    {
                        "term": "Toepassingsgebieden van NLP",
                        "questions": [
                            (
                                "In welke contexten wordt NLP volgens de manual gebruikt?",
                                "NLP wordt gebruikt in onder meer coaching, therapie, onderwijs, communicatie, management, sales en persoonlijke ontwikkeling.",
                            ),
                            (
                                "Waarom is NLP niet beperkt tot therapie alleen?",
                                "Omdat het zich richt op algemene patronen van menselijk functioneren en daardoor in veel contexten toepasbaar is.",
                            ),
                            (
                                "Welke persoonlijke en professionele doelen kunnen met NLP worden ondersteund?",
                                "Bijvoorbeeld betere communicatie, meer zelfinzicht, gedragsverandering, leiderschap, leren en resultaatgericht handelen.",
                            ),
                            (
                                "Waarom wordt NLP context-onafhankelijk genoemd?",
                                "Omdat de onderliggende principes over waarneming, taal en gedrag in uiteenlopende situaties bruikbaar zijn.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Trainers en positionering van NLP",
        "subheading_distractors": ["NLP staat voor", "De tweede wet van George Miller"],
        "concepts": [
            {
                "concept": "Rob Kamps",
                "distractors": ["NLP anno nu", "Spelend leren"],
                "terms": [
                    {
                        "term": "Opleiding en ervaring",
                        "questions": [
                            (
                                "Wie is Rob Kamps binnen BPD?",
                                "Binnen BPD wordt Rob Kamps neergezet als een ervaren trainer die een centrale rol speelt in het verzorgen van de NLP-opleidingen.",
                            ),
                            (
                                "Hoe lang geeft hij al trainingen volgens de manual?",
                                "Volgens de manual geeft hij al vele jaren trainingen en bouwde hij daarin een brede praktijkervaring op.",
                            ),
                            (
                                "In welke vakgebieden is hij actief geweest?",
                                "Hij is actief geweest in verschillende ontwikkel- en communicatiegerichte vakgebieden zoals training, coaching en begeleiding.",
                            ),
                            (
                                "Waarom is zijn achtergrond relevant voor de training?",
                                "Omdat zijn brede praktijkervaring de training concreet, geloofwaardig en toepasbaar maakt voor deelnemers.",
                            ),
                        ],
                    },
                    {
                        "term": "NLP-certificeringen",
                        "questions": [
                            (
                                "Door welke bekende namen en organisaties is Rob Kamps gecertificeerd?",
                                "De manual koppelt Rob Kamps aan certificeringen via bekende namen en erkende organisaties binnen het NLP-veld.",
                            ),
                            (
                                "Welke rechten kreeg hij hierdoor binnen NLP-opleidingen?",
                                "Hierdoor kreeg hij het recht om op erkend niveau NLP-trainingen en certificeringstrajecten te verzorgen.",
                            ),
                            (
                                "Waarom versterken deze certificeringen zijn positie als trainer?",
                                "Omdat ze laten zien dat zijn trainerschap niet alleen op ervaring maar ook op formele erkenning is gebaseerd.",
                            ),
                            (
                                "Hoe verbindt de manual zijn certificeringen aan zijn expertise?",
                                "De manual gebruikt die certificeringen als onderbouwing van zijn deskundigheid en zijn plek als senior trainer.",
                            ),
                        ],
                    },
                    {
                        "term": "Trainingsstijl",
                        "questions": [
                            (
                                "Hoe wordt de trainingsstijl van Rob Kamps omschreven?",
                                "Zijn trainingsstijl wordt omschreven als direct, levendig, persoonlijk en sterk ervaringsgericht.",
                            ),
                            (
                                "Waarom zijn persoonlijke voorbeelden belangrijk in zijn manier van trainen?",
                                "Omdat persoonlijke voorbeelden theorie tastbaar maken en deelnemers helpen de stof te koppelen aan echte situaties.",
                            ),
                            (
                                "Hoe dragen humor en controversiele benadering bij aan zijn reputatie?",
                                "Humor en een prikkelende stijl maken zijn trainingen memorabel en dagen deelnemers uit om scherper na te denken.",
                            ),
                            (
                                "Waarom wordt zijn stijl als levend en inspirerend beschreven?",
                                "Omdat hij theorie actief tot leven brengt en deelnemers energie geeft om ermee te oefenen en te experimenteren.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Caroline Kamps",
                "distractors": ["Rob Kamps", "Meta"],
                "terms": [
                    {
                        "term": "Wetenschappelijke achtergrond",
                        "questions": [
                            (
                                "Welke universitaire vakgebieden worden bij Caroline Kamps genoemd?",
                                "Bij Caroline Kamps worden onder meer linguistics, psychology en cognitive neuroscience genoemd.",
                            ),
                            (
                                "Waarom is haar combinatie van linguistics, psychology en cognitive neuroscience relevant voor NLP?",
                                "Omdat deze combinatie taal, gedrag, cognitie en waarneming samenbrengt, precies de gebieden waarop NLP zich richt.",
                            ),
                            (
                                "Hoe verrijkt deze achtergrond volgens de manual haar trainerschap?",
                                "Die achtergrond verdiept haar trainerschap doordat zij theorie, wetenschap en praktische toepassing goed kan verbinden.",
                            ),
                            (
                                "Waarom wordt zij gepresenteerd als brug tussen wetenschap en toepasbare kennis?",
                                "Omdat zij academische kennis vertaalt naar praktische inzichten die direct bruikbaar zijn in training en communicatie.",
                            ),
                        ],
                    },
                    {
                        "term": "Profiling en aanvullende specialisaties",
                        "questions": [
                            (
                                "Welke bijzondere expertise heeft Caroline op het gebied van profiling?",
                                "De manual presenteert haar als iemand met specialistische kennis van profiling en het herkennen van subtiele gedrags- en communicatiesignalen.",
                            ),
                            (
                                "Waarom wordt dit als onderscheidend benoemd?",
                                "Omdat deze expertise haar helpt om dieper waar te nemen dan alleen de zichtbare inhoud van wat iemand zegt.",
                            ),
                            (
                                "Hoe helpt dit haar om onder de oppervlakte waar te nemen wat er bij mensen gebeurt?",
                                "Het helpt haar patronen in taal, gedrag, emotie en non-verbaal gedrag sneller en nauwkeuriger te herkennen.",
                            ),
                            (
                                "Welke relatie heeft dit met communicatie en gedragsanalyse?",
                                "Profiling versterkt juist het analyseren van hoe mensen communiceren en welk gedrag daarbij zichtbaar wordt.",
                            ),
                        ],
                    },
                    {
                        "term": "NLP-certificeringen en trainerschap",
                        "questions": [
                            (
                                "Welke NLP-certificeringen van Caroline worden genoemd?",
                                "De manual noemt haar internationale NLP-certificeringen als onderbouwing van haar trainerschap.",
                            ),
                            (
                                "Door wie is zij getraind en gecertificeerd?",
                                "Volgens de manual is zij op hoog niveau getraind en gecertificeerd door erkende namen binnen het internationale NLP-veld.",
                            ),
                            (
                                "Waarom is haar positie als jonge internationaal gecertificeerde trainer relevant?",
                                "Omdat het laat zien dat zij moderne wetenschappelijke bagage combineert met formeel erkende NLP-kwaliteit.",
                            ),
                            (
                                "Hoe wordt haar rol binnen de training samengevat?",
                                "Zij wordt samengevat als een trainer die wetenschappelijke diepgang, observatievermogen en praktische toepasbaarheid samenbrengt.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "NLP anno nu",
                "distractors": ["Kalibreren", "NLP als technologie"],
                "terms": [
                    {
                        "term": "Ontwikkeling van NLP",
                        "questions": [
                            (
                                "Hoe heeft NLP zich volgens de manual ontwikkeld sinds de introductie?",
                                "Volgens de manual heeft NLP zich ontwikkeld van een vernieuwende therapeutische benadering naar een breder toepasbare discipline voor menselijk functioneren.",
                            ),
                            (
                                "Waarom wordt gesproken over een transformatie richting de 21ste eeuw?",
                                "Omdat NLP niet is blijven steken in de oorsprong, maar zich heeft verbreed naar moderne toepassingen en contexten.",
                            ),
                            (
                                "Welke verbreding in toepassingen wordt genoemd?",
                                "De manual noemt verbreding naar onder meer onderwijs, coaching, leiderschap, communicatie en persoonlijke ontwikkeling.",
                            ),
                            (
                                "Waarom wordt NLP beschreven als technologie van menselijk functioneren?",
                                "Omdat het draait om praktische inzichten in hoe mensen waarnemen, betekenis geven, communiceren en veranderen.",
                            ),
                        ],
                    },
                    {
                        "term": "Eenzijdig beeld van NLP",
                        "questions": [
                            (
                                "Welk eenzijdig beeld van NLP bekritiseert de manual?",
                                "De manual bekritiseert het idee dat NLP slechts uit slimme trucs, snelle verkooptechnieken of oppervlakkige show bestaat.",
                            ),
                            (
                                "Waarom worden clowneske vertolkers en slimme trucs genoemd?",
                                "Omdat zulke voorbeelden volgens de manual een karikatuur maken van een veel rijker en serieuzer vakgebied.",
                            ),
                            (
                                "Wat doet dit volgens de manual met het publieke beeld van NLP?",
                                "Het versmalt en vervormt het publieke beeld, waardoor de diepgang en werkelijke breedte van NLP minder zichtbaar wordt.",
                            ),
                            (
                                "Waarom is dit volgens de tekst te beperkt voor de rijkdom van het vakgebied?",
                                "Omdat NLP veel verder gaat dan trucs en juist gaat over diepere structuren van ervaring, communicatie en verandering.",
                            ),
                        ],
                    },
                    {
                        "term": "Brede toepasbaarheid",
                        "questions": [
                            (
                                "Waarom wordt NLP context-onafhankelijk genoemd?",
                                "Omdat de kernprincipes van NLP in veel verschillende domeinen en situaties toepasbaar zijn.",
                            ),
                            (
                                "Wat betekent het dat NLP zich bezighoudt met het hoe in plaats van alleen de inhoud?",
                                "Dat NLP vooral kijkt naar de structuur en het proces achter ervaring en gedrag, niet alleen naar het onderwerp zelf.",
                            ),
                            (
                                "In welke domeinen heeft NLP zich volgens de manual bewezen?",
                                "Volgens de manual heeft NLP zich bewezen in bijvoorbeeld communicatie, management, coaching, onderwijs en therapie.",
                            ),
                            (
                                "Waarom maakt dit NLP breed inzetbaar?",
                                "Omdat wie het proces begrijpt, dezelfde principes in veel contexten kan toepassen.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Het NLP Speelveld",
        "subheading_distractors": ["Rob Kamps", "NLP anno nu"],
        "concepts": [
            {
                "concept": "Spelend leren",
                "distractors": ["Kalibreren", "Uniek wereldmodel"],
                "terms": [
                    {
                        "term": "Oefenomgeving",
                        "questions": [
                            (
                                "Waarom noemt de manual NLP-training spelend leren?",
                                "Omdat leren in NLP sterk ervaringsgericht is en deelnemers in een veilige setting oefenen, experimenteren en ontdekken.",
                            ),
                            (
                                "Wat betekent het dat de trainingsruimte een speelomgeving is?",
                                "Dat de ruimte bedoeld is om te proberen, te oefenen en te leren zonder dat fouten meteen als mislukking worden gezien.",
                            ),
                            (
                                "Waarom kan er volgens deze benadering niets mislukken?",
                                "Omdat elke uitkomst informatie geeft over wat wel of niet werkt en dus bruikbaar is als feedback.",
                            ),
                            (
                                "Hoe wordt leren gekoppeld aan ervaring en interventie?",
                                "Leren ontstaat doordat deelnemers technieken direct ervaren, toepassen, observeren en daarop bijsturen.",
                            ),
                        ],
                    },
                    {
                        "term": "Feedback",
                        "questions": [
                            (
                                "Welke rol speelt feedback in het NLP-speelveld?",
                                "Feedback laat zien wat het effect van gedrag en interventies werkelijk is en vormt daarmee de motor van leren.",
                            ),
                            (
                                "Hoe worden resultaten getoetst aan een doelstelling?",
                                "Door te kijken of het waargenomen effect overeenkomt met het gewenste resultaat of de beoogde verandering.",
                            ),
                            (
                                "Wat gebeurt er wanneer resultaten afwijken van het doel?",
                                "Dan wordt het gedrag of de interventie aangepast op basis van de verkregen feedback.",
                            ),
                            (
                                "Waarom past feedback bij de gedachte dat je altijd een resultaat hebt?",
                                "Omdat elk resultaat, ook een onverwacht resultaat, bruikbare informatie geeft voor de volgende stap.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Rollen in de oefening",
                "distractors": ["Rapport", "Praktische toepasbaarheid"],
                "terms": [
                    {
                        "term": "Subject",
                        "questions": [
                            (
                                "Wat is de rol van het subject binnen een NLP-oefening?",
                                "Het subject is degene die de oefening ervaart en bij wie de verandering of interventie direct wordt onderzocht.",
                            ),
                            (
                                "Waarom is veranderingservaring in positie A de belangrijkste?",
                                "Omdat de innerlijke ervaring van het subject laat zien of de interventie werkelijk effect heeft op de persoon om wie het gaat.",
                            ),
                            (
                                "Waarom moet je een techniek eerst zelf ervaren om die congruent toe te passen?",
                                "Omdat eigen ervaring begrip, geloofwaardigheid en gevoeligheid vergroot wanneer je de techniek later bij anderen toepast.",
                            ),
                            (
                                "Wat leert het subject over huidig gedrag en doelen?",
                                "Het subject ontdekt hoe het huidige patroon werkt, wat het doel is en welke verandering werkelijk helpend voelt.",
                            ),
                        ],
                    },
                    {
                        "term": "Programmer",
                        "questions": [
                            (
                                "Wat is de rol van de programmer binnen een NLP-oefening?",
                                "De programmer begeleidt de oefening en past de interventie of techniek bewust en doelgericht toe.",
                            ),
                            (
                                "Welke vaardigheden oefent de programmer?",
                                "De programmer oefent onder meer afstemmen, vragen stellen, taalgebruik, waarnemen en procesbegeleiding.",
                            ),
                            (
                                "Waarom is kalibreren belangrijk in deze rol?",
                                "Omdat de programmer alleen goed kan bijsturen wanneer subtiele veranderingen bij het subject worden waargenomen.",
                            ),
                            (
                                "Hoe verschilt de rol van programmer van die van subject?",
                                "Het subject ondergaat de ervaring, terwijl de programmer verantwoordelijk is voor begeleiding en processturing.",
                            ),
                        ],
                    },
                    {
                        "term": "Meta",
                        "questions": [
                            (
                                "Wat is de rol van de meta binnen een oefening?",
                                "De meta observeert het proces van buitenaf en helpt om de kwaliteit, ecologie en structuur van de oefening te bewaken.",
                            ),
                            (
                                "Waarom is de meta een coachende en niet-beoordelende rol?",
                                "Omdat de meta bedoeld is om het leerproces te ondersteunen en niet om deelnemers af te rekenen op fouten.",
                            ),
                            (
                                "Hoe helpt de meta wanneer de programmer vastloopt?",
                                "De meta kan teruggeven wat zichtbaar is, suggesties doen en helpen om het proces weer helder en veilig te maken.",
                            ),
                            (
                                "Welke metaverantwoordelijkheid draagt de meta voor het proces?",
                                "De meta bewaakt onder meer rapport, ecologie, duidelijkheid van stappen en de veiligheid van alle betrokkenen.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Basisregels in oefeningen",
                "distractors": ["Meta-programma's", "Caroline Kamps"],
                "terms": [
                    {
                        "term": "Rapport",
                        "questions": [
                            (
                                "Waarom is de programmer verantwoordelijk voor het behoud van rapport?",
                                "Omdat zonder rapport de samenwerking en daarmee de effectiviteit van de oefening direct afneemt.",
                            ),
                            (
                                "Wat moet er gebeuren bij rapportbreuk?",
                                "Bij rapportbreuk moet eerst opnieuw afstemming en verbinding worden hersteld voordat de oefening doorgaat.",
                            ),
                            (
                                "Waarom gaat rapport voor de rest van het proces?",
                                "Omdat zonder voldoende contact en veiligheid de rest van de interventie weinig betekenisvol of zelfs contraproductief kan worden.",
                            ),
                            (
                                "Hoe beinvloedt rapport de effectiviteit van de oefening?",
                                "Goede afstemming vergroot vertrouwen, ontvankelijkheid en de kans dat verandering daadwerkelijk wordt ervaren.",
                            ),
                        ],
                    },
                    {
                        "term": "Kalibreren",
                        "questions": [
                            (
                                "Waarom moeten programmer en meta het subject kalibreren?",
                                "Omdat zij alleen met nauwkeurige observatie kunnen zien wat de huidige toestand is en welke veranderingen optreden.",
                            ),
                            (
                                "Wat betekent zintuiglijk specifiek werken in deze context?",
                                "Dat je observeert wat concreet waarneembaar is in gedrag, stem, ademhaling, houding en mimiek, zonder interpretaties toe te voegen.",
                            ),
                            (
                                "Waarom moeten huidige en gewenste toestand in kaart worden gebracht?",
                                "Omdat je anders niet helder kunt beoordelen of de oefening iemand werkelijk richting het gewenste resultaat beweegt.",
                            ),
                            (
                                "Welke rol spelen non-verbale signalen hierin?",
                                "Non-verbale signalen geven vaak de meest directe informatie over state, congruentie en verandering in het proces.",
                            ),
                        ],
                    },
                    {
                        "term": "Ecologie",
                        "questions": [
                            (
                                "Wat wordt bedoeld met ecologie binnen een oefening?",
                                "Ecologie betekent dat je onderzoekt of een gewenste verandering ook op de langere termijn en in bredere contexten gezond en passend is.",
                            ),
                            (
                                "Waarom moeten nevengevolgen van succes worden meegenomen?",
                                "Omdat een verandering die een doel dient toch ongewenste gevolgen kan hebben voor andere delen van iemands leven.",
                            ),
                            (
                                "Welke risico's ontstaan als ecologie wordt vergeten?",
                                "Dan kan een ogenschijnlijk goede interventie later spanning, verlies of nieuwe problemen veroorzaken.",
                            ),
                            (
                                "Waarom bewaakt de meta dit onderdeel van het proces?",
                                "Omdat de meta overzicht houdt en daardoor makkelijker kan zien of belangrijke contextfactoren of neveneffecten over het hoofd worden gezien.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Fundament 1: De wetten van Miller",
        "subheading_distractors": ["NLP anno nu", "Rollen in de oefening"],
        "concepts": [
            {
                "concept": "De eerste wet van George Miller",
                "distractors": ["Praktische toepasbaarheid", "Empathische communicatie"],
                "terms": [
                    {
                        "term": "Magical Number Seven",
                        "questions": [
                            (
                                "Wat houdt de eerste wet van George Miller in?",
                                "De eerste wet stelt dat het korte termijn geheugen maar een beperkt aantal eenheden tegelijk kan vasthouden, vaak rond zeven plus of min twee.",
                            ),
                            (
                                "Wat zegt deze wet over de capaciteit van het korte termijn geheugen?",
                                "Dat die capaciteit beperkt is en daardoor vraagt om slimme ordening van informatie.",
                            ),
                            (
                                "Waarom is deze wet belangrijk voor informatieverwerking?",
                                "Omdat zij verklaart waarom te veel losse informatie snel onoverzichtelijk wordt en moeilijker blijft hangen.",
                            ),
                            (
                                "Hoe werkt deze wet door in onderwijs, communicatie of marketing?",
                                "Ze laat zien dat informatie beter werkt wanneer die overzichtelijk, geclusterd en behapbaar wordt aangeboden.",
                            ),
                        ],
                    },
                    {
                        "term": "Chunking",
                        "questions": [
                            (
                                "Welke relatie legt de manual tussen Miller en chunking?",
                                "De manual koppelt chunking aan Millers wet omdat groeperen helpt om meer informatie binnen de beperkte geheugencapaciteit hanteerbaar te maken.",
                            ),
                            (
                                "Waarom helpt groeperen van informatie bij onthouden?",
                                "Omdat losse elementen dan als betekenisvolle gehelen worden opgeslagen in plaats van als losse flarden.",
                            ),
                            (
                                "Hoe draagt chunking bij aan beter verwerken van informatie?",
                                "Chunking vermindert complexiteit en maakt informatie sneller begrijpelijk, vergelijkbaar en toepasbaar.",
                            ),
                            (
                                "Waarom is dit relevant binnen NLP?",
                                "Omdat NLP veel werkt met het structureren en herstructureren van ervaring, taal en informatie.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "De tweede wet van George Miller",
                "distractors": ["Chunking", "Rapport"],
                "terms": [
                    {
                        "term": "Waarheidsaanname",
                        "questions": [
                            (
                                "Wat bedoelt George Miller met de aanname dat je eerst moet aannemen dat iets waar is?",
                                "Hij bedoelt dat je eerst probeert te begrijpen vanuit welk kader iets voor de ander waar of logisch is, voordat je het afwijst.",
                            ),
                            (
                                "Waarom helpt deze houding om communicatie beter te begrijpen?",
                                "Omdat je daardoor opener luistert en sneller ontdekt welke betekenis, ervaring of intentie achter iemands woorden zit.",
                            ),
                            (
                                "Wat is het verschil tussen onmiddellijk tegenspreken en eerst onderzoeken waar iets waar van is?",
                                "Tegenspreken sluit begrip vaak af, terwijl onderzoeken juist ruimte maakt voor inzicht, nuance en contact.",
                            ),
                            (
                                "Waarom vraagt deze aanname om openheid?",
                                "Omdat je je eigen oordeel tijdelijk parkeert om werkelijk perspectief van de ander te kunnen verkennen.",
                            ),
                        ],
                    },
                    {
                        "term": "Empathische communicatie",
                        "questions": [
                            (
                                "Waarom past de tweede wet van Miller bij empathisch luisteren?",
                                "Omdat empathisch luisteren begint met het serieus nemen van hoe de ander zijn werkelijkheid ervaart.",
                            ),
                            (
                                "Hoe helpt deze benadering om de wereld door de ogen van de spreker te zien?",
                                "Ze nodigt uit om mee te bewegen met de logica, emotie en betekenisstructuur van de spreker.",
                            ),
                            (
                                "Welke rol spelen emoties, overtuigingen en perspectieven hierin?",
                                "Die vormen het kader waardoor iets voor iemand waar, vanzelfsprekend of belangrijk voelt.",
                            ),
                            (
                                "Waarom is dit nuttig bij meningsverschillen en misverstanden?",
                                "Omdat je eerst begrip opbouwt, waardoor correctie of verdieping later veel effectiever en respectvoller wordt.",
                            ),
                        ],
                    },
                    {
                        "term": "Praktische toepasbaarheid",
                        "questions": [
                            (
                                "Hoe kan de waarheidsaanname helpen in discussies of conflicten?",
                                "Ze helpt om escalatie te verminderen door eerst te zoeken naar het perspectief en de bedoeling achter iemands standpunt.",
                            ),
                            (
                                "Waarom is deze benadering ook bruikbaar in therapie of counseling?",
                                "Omdat mensen zich veiliger en beter begrepen voelen wanneer hun werkelijkheid eerst serieus wordt genomen.",
                            ),
                            (
                                "Hoe draagt dit bij aan een veilige omgeving?",
                                "Het vermindert oordeel en vergroot ruimte voor eerlijk contact en onderzoek.",
                            ),
                            (
                                "Waarom noemt de manual dit een oefening in communicatie en menselijkheid?",
                                "Omdat deze houding zowel communicatieve vaardigheid als respect en menselijke openheid vraagt.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Fundament 2: Nine Major Beliefs",
        "subheading_distractors": ["Spelend leren", "Wetenschappelijke achtergrond"],
        "concepts": [
            {
                "concept": "Overzicht van de Nine Major Beliefs",
                "distractors": ["Uniek wereldmodel", "Chunking"],
                "terms": [
                    {
                        "term": "De kaart is niet het gebied",
                        "questions": [
                            (
                                "Wat betekent de uitspraak de kaart is niet het gebied?",
                                "Dat iemands innerlijke representatie van de werkelijkheid nooit gelijk is aan de werkelijkheid zelf.",
                            ),
                            (
                                "Waarom is onze kaart geen objectieve werkelijkheid?",
                                "Omdat waarneming altijd gefilterd, geinterpreteerd en persoonlijk gekleurd wordt.",
                            ),
                            (
                                "Hoe hangt dit samen met wereldmodel, perceptie en representatie?",
                                "Ons wereldmodel ontstaat uit perceptie en representatie en vormt zo de kaart waarmee wij de wereld begrijpen.",
                            ),
                            (
                                "Waarom leidt een verandering van perspectief tot meer keuzemogelijkheden?",
                                "Omdat een bredere of andere kaart meer betekenissen en handelingsopties zichtbaar maakt.",
                            ),
                        ],
                    },
                    {
                        "term": "Respect / positieve intentie",
                        "questions": [
                            (
                                "Wat betekent respect binnen de Nine Major Beliefs?",
                                "Respect betekent dat je het wereldmodel en de ervaring van de ander serieus neemt, ook als je die niet deelt.",
                            ),
                            (
                                "Wat wordt bedoeld met de positieve intentie achter gedrag?",
                                "Dat gedrag, hoe onhandig ook, vaak een poging is om iets positiefs te bereiken of te beschermen.",
                            ),
                            (
                                "Waarom is respect voor de kaart van de ander zo belangrijk?",
                                "Omdat echt begrip en effectieve communicatie pas ontstaan wanneer de ander zich gezien voelt in zijn eigen model.",
                            ),
                            (
                                "Hoe helpt dit om gedrag anders te begrijpen?",
                                "Het maakt zichtbaar dat achter gedrag vaak een begrijpelijke behoefte of intentie schuilgaat.",
                            ),
                        ],
                    },
                    {
                        "term": "Schoonheid zit in verschillen",
                        "questions": [
                            ("Waarom zijn verschillen volgens deze belief waardevol?", "Omdat verschillen nieuwe informatie, perspectieven en leerervaringen opleveren."),
                            (
                                "Hoe kun je van de kaart van een ander leren?",
                                "Door nieuwsgierig te onderzoeken hoe de ander waarneemt, betekenis geeft en keuzes maakt.",
                            ),
                            (
                                "Waarom deelt niemand ooit precies dezelfde ervaring?",
                                "Omdat ieders waarneming, geschiedenis en filters uniek zijn.",
                            ),
                            (
                                "Hoe verrijkt dit je eigen wereldmodel?",
                                "Door verschillen toe te laten, vergroot je je eigen flexibiliteit en begrip van mogelijkheden.",
                            ),
                        ],
                    },
                    {
                        "term": "Communicatie is beinvloeding",
                        "questions": [
                            (
                                "Wat bedoelt de manual met communicatie is beinvloeding?",
                                "Dat elke vorm van communicatie effect heeft op jezelf en op anderen, bewust of onbewust.",
                            ),
                            (
                                "Waarom is niet-communiceren volgens deze belief onmogelijk?",
                                "Omdat ook zwijgen, lichaamstaal en afwezigheid altijd iets communiceren.",
                            ),
                            (
                                "Hoe beinvloeden mensen elkaar bewust en onbewust?",
                                "Via woorden, toon, timing, context, houding en allerlei subtiele signalen.",
                            ),
                            (
                                "Wat betekent dit voor verantwoordelijkheid in contact?",
                                "Dat je verantwoordelijkheid draagt voor het effect dat jouw communicatie heeft.",
                            ),
                        ],
                    },
                    {
                        "term": "Weerstand is kracht",
                        "questions": [
                            (
                                "Wat zegt weerstand over de communicatie van de zender?",
                                "Weerstand zegt vaak dat de gekozen communicatie of aanpak nog niet goed aansluit bij de ander.",
                            ),
                            (
                                "Waarom wordt weerstand gekoppeld aan inflexibiliteit van de communicator?",
                                "Omdat star vasthouden aan een aanpak vaak meer zegt over gebrek aan keuzevrijheid bij de communicator dan over onwil van de ander.",
                            ),
                            (
                                "Wat betekent kracht hier: macht of keuzemogelijkheden?",
                                "Kracht verwijst hier vooral naar keuzemogelijkheden en flexibiliteit, niet naar dominantie.",
                            ),
                            (
                                "Hoe kan weerstand juist informatie opleveren?",
                                "Weerstand laat zien waar afstemming ontbreekt en geeft dus richting voor een betere volgende interventie.",
                            ),
                        ],
                    },
                    {
                        "term": "50/50-regel",
                        "questions": [
                            (
                                "Wat houdt de 50/50-regel in?",
                                "De regel benadrukt dat non-verbale communicatie minstens zo bepalend is als verbale inhoud.",
                            ),
                            (
                                "Waarom is non-verbale communicatie minimaal zo belangrijk als woorden?",
                                "Omdat houding, mimiek, stem en timing vaak sterker laten zien wat iemand werkelijk ervaart of bedoelt.",
                            ),
                            (
                                "Welke non-verbale signalen noemt de manual?",
                                "Onder andere lichaamshouding, gezichtsuitdrukking, gebaren, ademhaling, oogcontact en stemgebruik.",
                            ),
                            (
                                "Waarom wordt dit als vuistregel gebruikt?",
                                "Omdat het helpt om communicatie niet te beperken tot woorden alleen, maar breder en realistischer te observeren.",
                            ),
                        ],
                    },
                    {
                        "term": "Vertrouw je onbewuste",
                        "questions": [
                            (
                                "Waarom noemt de manual het onderbewuste je rijkste bron van levenservaring?",
                                "Omdat het onbewuste een enorme hoeveelheid ervaringen, patronen en hulpbronnen bevat die niet steeds bewust toegankelijk zijn.",
                            ),
                            (
                                "Welke informatie ligt in het onderbewuste opgeslagen?",
                                "Herinneringen, associaties, emoties, automatische patronen en veel impliciete kennis.",
                            ),
                            (
                                "Op welke manieren spreekt het onderbewuste met je?",
                                "Via gevoelens, intuities, lichamelijke signalen, beelden, dromen en spontane ingevingen.",
                            ),
                            (
                                "Waarom is vertrouwen op het onbewuste belangrijk binnen NLP?",
                                "Omdat veel verandering en creativiteit juist ontstaan wanneer je toegang krijgt tot die diepere hulpbronnen.",
                            ),
                        ],
                    },
                    {
                        "term": "Het recht om te leren",
                        "questions": [
                            (
                                "Waarom bestaat er volgens deze belief geen falen, alleen informatie?",
                                "Omdat elk resultaat feedback geeft over wat werkt en wat nog bijstelling vraagt.",
                            ),
                            (
                                "Wat gebeurt er als je mislukkingen als feedback gaat zien?",
                                "Dan worden tegenslagen leerkansen in plaats van vaste oordelen over jezelf.",
                            ),
                            (
                                "Waarom zijn etiketten als falen destructief?",
                                "Omdat ze ontwikkeling blokkeren en mensen laten stoppen met onderzoeken en bijsturen.",
                            ),
                            (
                                "Hoe ondersteunt dit persoonlijke ontwikkeling?",
                                "Het vergroot veerkracht, experimenteerbereidheid en de wil om te blijven leren.",
                            ),
                        ],
                    },
                    {
                        "term": "Jij bent de belangrijkste persoon in je leven",
                        "questions": [
                            (
                                "Wat betekent deze belief precies?",
                                "Dat jij verantwoordelijkheid draagt voor je eigen welzijn, keuzes en ontwikkeling.",
                            ),
                            (
                                "Waarom ben jij volgens de manual het centrum van je eigen ervaringen?",
                                "Omdat jij degene bent die jouw ervaring beleeft, interpreteert en ermee leert omgaan.",
                            ),
                            (
                                "Hoe gebruikt de manual het voorbeeld van het zuurstofmasker?",
                                "Om te laten zien dat je eerst voor je eigen basis moet zorgen voordat je duurzaam voor anderen kunt zorgen.",
                            ),
                            (
                                "Waarom is zelfzorg geen egoisme binnen deze visie?",
                                "Omdat gezonde zelfzorg juist de voorwaarde is om aanwezig, stabiel en behulpzaam voor anderen te kunnen zijn.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Over aannamen, vooronderstellingen en overtuigingen",
        "subheading_distractors": ["Caroline Kamps", "Auditief"],
        "concepts": [
            {
                "concept": "Soorten aannamen binnen NLP",
                "distractors": ["Koppeling major beliefs en basisaannamen", "Rapport"],
                "terms": [
                    {
                        "term": "Basisaannamen",
                        "questions": [
                            (
                                "Wat zijn basisaannamen binnen NLP?",
                                "Basisaannamen zijn fundamentele uitgangspunten die richting geven aan hoe NLP naar menselijk gedrag en verandering kijkt.",
                            ),
                            (
                                "Waarom vormen zij de basis van NLP-technieken?",
                                "Omdat technieken betekenis en richting krijgen vanuit de onderliggende aannamen over menselijk functioneren.",
                            ),
                            (
                                "Welke voorbeelden van basisaannamen worden genoemd?",
                                "Voorbeelden zijn dat de kaart niet het gebied is, falen niet bestaat en dat mensen hulpbronnen en keuzemogelijkheden hebben.",
                            ),
                            (
                                "Hoe sturen deze aannamen denken en handelen?",
                                "Ze bepalen welke vragen je stelt, hoe je gedrag interpreteert en welke veranderstrategieen je kiest.",
                            ),
                        ],
                    },
                    {
                        "term": "Vooronderstellingen",
                        "questions": [
                            (
                                "Wat zijn vooronderstellingen in communicatie?",
                                "Vooronderstellingen zijn impliciete aannamen die in taal en communicatie besloten liggen zonder expliciet te worden uitgesproken.",
                            ),
                            (
                                "Waarom zijn vooronderstellingen nuttig om bedoelingen te begrijpen?",
                                "Omdat ze laten zien welke onuitgesproken kaders en verwachtingen onder iemands woorden liggen.",
                            ),
                            (
                                "Welke voorbeelden van vooronderstellingen noemt de manual?",
                                "Bijvoorbeeld aannamen over tijd, oorzaak, intentie, identiteit of wat al als waar wordt verondersteld.",
                            ),
                            (
                                "Hoe beinvloeden ze communicatie zonder expliciet uitgesproken te worden?",
                                "Ze sturen de betekenis van een boodschap doordat de luisteraar onbewust een bepaald kader overneemt.",
                            ),
                        ],
                    },
                    {
                        "term": "Meta-programma's",
                        "questions": [
                            (
                                "Wat zijn meta-programma's volgens de manual?",
                                "Meta-programma's zijn terugkerende voorkeurspatronen in aandacht, motivatie en informatieverwerking.",
                            ),
                            (
                                "Waarom geven meta-programma's inzicht in gedrag en communicatie?",
                                "Omdat ze laten zien hoe iemand keuzes maakt, informatie filtert en reageert op situaties.",
                            ),
                            (
                                "Welke voorbeelden worden genoemd?",
                                "Denk aan voorkeuren zoals naar iets toe of ergens van weg, details of grote lijn, en overeenkomsten of verschillen.",
                            ),
                            (
                                "Hoe helpen meta-programma's om effectiever af te stemmen op anderen?",
                                "Ze helpen omdat je je communicatie beter kunt laten aansluiten op iemands natuurlijke verwerkingsstijl.",
                            ),
                        ],
                    },
                    {
                        "term": "Identiteitsaannamen",
                        "questions": [
                            (
                                "Wat zijn identiteitsaannamen?",
                                "Identiteitsaannamen zijn overtuigingen die iemand heeft over wie hij is of denkt te zijn.",
                            ),
                            (
                                "Hoe beinvloeden zulke aannamen gedrag en emoties?",
                                "Ze kleuren wat iemand mogelijk acht, hoe hij zich voelt en welk gedrag logisch of passend lijkt.",
                            ),
                            (
                                "Welke voorbeelden geeft de manual van identiteitsaannamen?",
                                "Voorbeelden zijn uitspraken als ik ben nu eenmaal zo, ik ben geen leider of ik ben iemand die altijd moet zorgen.",
                            ),
                            (
                                "Waarom zijn deze belangrijk voor verandering?",
                                "Omdat diepere verandering vaak pas mogelijk wordt wanneer beperkende aannamen over identiteit worden onderzocht en herzien.",
                            ),
                        ],
                    },
                    {
                        "term": "Overtuigingen",
                        "questions": [
                            (
                                "Waarom zijn overtuigingen volgens NLP fundamentele drijfveren achter gedrag?",
                                "Omdat overtuigingen bepalen wat iemand voor waar, mogelijk en belangrijk houdt en daarop zijn gedrag afstemt.",
                            ),
                            (
                                "Hoe beinvloeden overtuigingen onze perceptie van de wereld?",
                                "Ze sturen waar we op letten, hoe we gebeurtenissen interpreteren en wat we verwachten.",
                            ),
                            (
                                "Uit welke drie componenten is een overtuiging opgebouwd?",
                                "Een overtuiging is opgebouwd uit representatie, betekenis en de emotionele lading die daaraan gekoppeld is.",
                            ),
                            (
                                "Hoe kan verandering van representatie, betekenis en emotie een overtuiging veranderen?",
                                "Door alle drie te verschuiven verandert de beleving van waarheid en daarmee ook de kracht van de overtuiging.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Basisaannamen van klassiek NLP",
                "distractors": ["Respect / positieve intentie", "Oefenomgeving"],
                "terms": [
                    {
                        "term": "Uniek wereldmodel",
                        "questions": [
                            (
                                "Waarom heeft ieder individu een uniek wereldmodel?",
                                "Omdat iedereen een eigen geschiedenis, filters, ervaringen en betekeniskaders heeft.",
                            ),
                            (
                                "Hoe ontstaan misverstanden door botsende wereldmodellen?",
                                "Misverstanden ontstaan wanneer mensen hun eigen kaart als vanzelfsprekend zien en die van de ander onvoldoende onderzoeken.",
                            ),
                            (
                                "Waarom helpt deze aanname bij empathie en begrip?",
                                "Omdat je dan erkent dat de ander vanuit een ander, maar voor hem logisch, perspectief kijkt.",
                            ),
                            (
                                "Wat verandert er wanneer je jouw perspectief niet meer als de enige juiste ziet?",
                                "Je wordt flexibeler, nieuwsgieriger en beter in afstemmen en leren.",
                            ),
                        ],
                    },
                    {
                        "term": "Proces belangrijker dan inhoud",
                        "questions": [
                            (
                                "Wat betekent het dat het proces belangrijker is dan de inhoud?",
                                "Dat de manier waarop iemand iets beleeft en structureert vaak belangrijker is dan het exacte onderwerp waarover het gaat.",
                            ),
                            (
                                "Waarom is verandering van het ervaringsproces vaak waardevoller dan verandering van de inhoud?",
                                "Omdat hetzelfde onderwerp heel anders wordt ervaren zodra het onderliggende proces van waarnemen en betekenisgeven verandert.",
                            ),
                            (
                                "Hoe sluit dit aan op de kaart is niet het gebied?",
                                "Het benadrukt dat niet de objectieve inhoud maar de persoonlijke kaart en het verwerkingsproces doorslaggevend zijn.",
                            ),
                            (
                                "Wat betekent dit praktisch in coaching of therapie?",
                                "Dat je niet alleen over problemen praat, maar vooral onderzoekt hoe iemand ze intern opbouwt en in stand houdt.",
                            ),
                        ],
                    },
                    {
                        "term": "Betekenisgeving",
                        "questions": [
                            (
                                "Wat betekent de aanname dat niets betekenis heeft behalve de betekenis die jij eraan geeft?",
                                "Dat gebeurtenissen op zichzelf niet automatisch vastliggende betekenis hebben; mensen geven die betekenis actief zelf.",
                            ),
                            (
                                "Hoe creeren mensen daarmee hun eigen werkelijkheid?",
                                "Door hun interpretaties, taal en emotionele koppelingen krijgt ervaring een persoonlijke realiteit.",
                            ),
                            (
                                "Waarom geeft dit invloed op ervaring en gedrag?",
                                "Omdat veranderde betekenis vaak direct leidt tot andere emoties, reacties en keuzes.",
                            ),
                            (
                                "Hoe kan verandering van betekenis leiden tot verandering van realiteit?",
                                "Wanneer iemand anders interpreteert, verandert de ervaren werkelijkheid en daarmee het gedrag dat daaruit voortkomt.",
                            ),
                        ],
                    },
                    {
                        "term": "Respons op communicatie",
                        "questions": [
                            (
                                "Wat betekent de basisaanname dat de betekenis van je communicatie de respons is die je krijgt?",
                                "Dat het effect van je boodschap uiteindelijk wordt bepaald door hoe de ander reageert, niet door jouw bedoeling alleen.",
                            ),
                            (
                                "Hoe helpt dit bij verantwoordelijkheid nemen voor je communicatie?",
                                "Je leert kijken naar effect en je aanpak bij te stellen wanneer de boodschap anders landt dan bedoeld.",
                            ),
                            (
                                "Waarom wordt weerstand hier gekoppeld aan de communicator?",
                                "Omdat weerstand kan aangeven dat de communicator nog niet flexibel genoeg heeft afgestemd.",
                            ),
                            (
                                "Hoe kun je hiermee effectiever leren communiceren?",
                                "Door respons als feedback te gebruiken en je stijl, woorden of tempo bewuster aan te passen.",
                            ),
                        ],
                    },
                    {
                        "term": "Falen bestaat niet",
                        "questions": [
                            (
                                "Wat verandert er als je falen als resultaat of informatie gaat zien?",
                                "Dan wordt een tegenvallende uitkomst een bron van leren in plaats van een eindpunt.",
                            ),
                            (
                                "Waarom is dat werkbaarder dan het label falen?",
                                "Omdat het ruimte laat voor bijsturen, experimenteren en blijven ontwikkelen.",
                            ),
                            (
                                "Hoe ondersteunt dit leren en ontwikkelen?",
                                "Het vermindert verlamming en vergroot de bereidheid om te oefenen en feedback te benutten.",
                            ),
                            (
                                "Wat vraagt deze aanname van je houding naar jezelf?",
                                "Een mildere, onderzoekende en groeigerichte houding in plaats van zelfveroordeling.",
                            ),
                        ],
                    },
                    {
                        "term": "Hulpbronnen",
                        "questions": [
                            (
                                "Wat bedoelt de manual met hulpbronnen?",
                                "Hulpbronnen zijn innerlijke en uiterlijke bronnen zoals vaardigheden, ervaringen, overtuigingen, states en steun die iemand kan inzetten.",
                            ),
                            (
                                "Waarom hebben mensen volgens NLP de hulpbronnen om hun doel te bereiken?",
                                "Omdat veel mogelijkheden al aanwezig zijn of ontwikkeld kunnen worden wanneer iemand toegang krijgt tot passende states en strategieen.",
                            ),
                            (
                                "Hoe kunnen hulpbronnen van anderen worden overgenomen of gemodelleerd?",
                                "Door succesvolle patronen van anderen te observeren, te begrijpen en in eigen gedrag te integreren.",
                            ),
                            (
                                "Wat zegt dit over verantwoordelijkheid en potentieel?",
                                "Dat mensen meer potentieel hebben dan zij vaak denken en daar actief verantwoordelijkheid voor kunnen nemen.",
                            ),
                        ],
                    },
                    {
                        "term": "Positieve intentie",
                        "questions": [
                            (
                                "Waarom ligt er aan de basis van elk gedrag een positieve intentie?",
                                "Omdat gedrag vaak een poging is om iets waardevols te bereiken of iets te beschermen, ook als de vorm onhandig is.",
                            ),
                            (
                                "Wat is het verschil tussen destructief gedrag en de intentie daarachter?",
                                "Het gedrag kan schadelijk zijn, terwijl de onderliggende intentie juist veiligheid, erkenning of controle probeert te realiseren.",
                            ),
                            (
                                "Waarom helpt dit onderscheid bij verandering?",
                                "Omdat je de intentie kunt behouden maar een beter, effectiever gedragspatroon kunt ontwikkelen.",
                            ),
                            (
                                "Hoe ondersteunt deze aanname respect voor de ander?",
                                "Ze nodigt uit om voorbij het zichtbare gedrag te kijken naar de menselijke behoefte eronder.",
                            ),
                        ],
                    },
                    {
                        "term": "Meerdere keuzes",
                        "questions": [
                            (
                                "Waarom zijn er volgens NLP altijd meerdere keuzes mogelijk?",
                                "Omdat een situatie vanuit meerdere perspectieven kan worden benaderd en gedrag zelden echt maar een mogelijkheid kent.",
                            ),
                            (
                                "Hoe vergroot perspectiefwisseling je keuzemogelijkheden?",
                                "Een ander perspectief laat andere betekenissen, strategieen en acties zien.",
                            ),
                            (
                                "Waarom is keuze verbonden aan groei en ontwikkeling?",
                                "Omdat meer keuzes leiden tot meer flexibiliteit en dus tot meer invloed op ervaring en resultaat.",
                            ),
                            (
                                "Hoe helpt dit wanneer iemand zich vast voelt zitten?",
                                "Het doorbreekt het idee dat er geen uitweg is en opent ruimte voor nieuwe mogelijkheden.",
                            ),
                        ],
                    },
                    {
                        "term": "Ervaring heeft structuur",
                        "questions": [
                            (
                                "Wat betekent het dat ervaring structuur heeft?",
                                "Dat ervaring volgens NLP niet willekeurig is, maar opgebouwd wordt uit herkenbare patronen van representatie, taal en betekenis.",
                            ),
                            (
                                "Waarom kun je een ervaring veranderen als je de structuur ervan kent?",
                                "Omdat je dan weet aan welke bouwstenen je kunt sleutelen om de beleving te veranderen.",
                            ),
                            (
                                "Hoe hangt dit samen met subjectieve ervaring?",
                                "Subjectieve ervaring ontstaat juist uit die persoonlijke structuur van waarnemen en betekenisgeven.",
                            ),
                            (
                                "Waarom is dit een kernidee van NLP?",
                                "Omdat het verklaart waarom verandering systematisch en leerbaar kan worden gemaakt.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Koppeling major beliefs en basisaannamen",
                "distractors": ["Rapport", "Wet van benodigde variatie"],
                "terms": [
                    {
                        "term": "Filosofisch fundament en praktische toepassing",
                        "questions": [
                            (
                                "Wat is het verschil tussen de Nine Major Beliefs en de basisaannamen?",
                                "De major beliefs vormen de bredere filosofische houding, terwijl de basisaannamen die houding concreter en praktischer maken in toepassing.",
                            ),
                            (
                                "Waarom worden de major beliefs als fundament beschreven?",
                                "Omdat zij het bredere mensbeeld en de waarden van NLP verwoorden.",
                            ),
                            (
                                "Hoe maken de basisaannamen dat fundament praktisch toepasbaar?",
                                "Zij vertalen de filosofie naar werkbare uitgangspunten voor communicatie, coaching en verandering.",
                            ),
                            (
                                "Waarom vullen beide sets principes elkaar aan?",
                                "Omdat het ene richting en betekenis geeft, terwijl het andere helpt om die richting concreet in gedrag en interventie om te zetten.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Fundament 3: Zintuigen",
        "subheading_distractors": ["NLP anno nu", "Benodigde variatie"],
        "concepts": [
            {
                "concept": "Modaliteiten",
                "distractors": ["Perceptie en illusie", "Rapport"],
                "terms": [
                    {
                        "term": "Zintuigen als modaliteiten",
                        "questions": [
                            (
                                "Waarom worden zintuigen in NLP modaliteiten genoemd?",
                                "Omdat zij de verschillende kanalen vormen waarlangs mensen ervaring waarnemen, representeren en structureren.",
                            ),
                            (
                                "Welke primaire modaliteiten noemt de manual?",
                                "De manual noemt visueel, auditief, kinesthetisch, digitaal en daarnaast geur en smaak als aanvullende zintuiglijke modaliteiten.",
                            ),
                            (
                                "Hoe helpen modaliteiten om menselijke ervaring te begrijpen?",
                                "Ze laten zien via welk zintuiglijk kanaal iemand informatie opneemt, opslaat en betekenis geeft.",
                            ),
                            (
                                "Waarom zijn modaliteiten belangrijk voor communicatie?",
                                "Omdat communicatie effectiever wordt wanneer je aansluit bij hoe iemand ervaring intern organiseert.",
                            ),
                        ],
                    },
                    {
                        "term": "Primair representatiesysteem",
                        "questions": [
                            (
                                "Wat is een primair representatiesysteem?",
                                "Dat is het zintuiglijke kanaal dat iemand relatief vaak gebruikt om informatie te verwerken en te beschrijven.",
                            ),
                            (
                                "Hoe kun je herkennen welk zintuig iemand primair gebruikt?",
                                "Door te letten op woordkeuze, tempo, focus, oogbewegingen en de manier waarop iemand ervaring beschrijft.",
                            ),
                            (
                                "Welke rol speelt taalgebruik daarbij?",
                                "Taalgebruik verraadt vaak welke predikaten en zintuiglijke voorkeuren iemand het meest vanzelfsprekend inzet.",
                            ),
                            (
                                "Waarom helpt dit om communicatie effectiever te maken?",
                                "Omdat je beter kunt afstemmen op iemands innerlijke belevingswereld en daardoor sneller rapport opbouwt.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Visueel",
                "distractors": ["Auditieve voorkeur", "Digitale predikaten"],
                "terms": [
                    {
                        "term": "Visuele voorkeur",
                        "questions": [
                            (
                                "Hoe denkt iemand met een visuele voorkeur volgens de manual?",
                                "Iemand met een visuele voorkeur denkt vaak in beelden, overzicht en ruimtelijke indrukken.",
                            ),
                            (
                                "Hoe spreekt iemand met een visuele voorkeur vaak?",
                                "Vaak sneller en met woorden die verwijzen naar zien, helderheid, beeld en perspectief.",
                            ),
                            (
                                "Hoe leert iemand met een visuele voorkeur het best?",
                                "Door beelden, schema's, demonstraties en een duidelijk overzicht van het grotere geheel.",
                            ),
                            (
                                "Wat is de valkuil van een sterk visuele voorkeur?",
                                "Dat iemand te veel op plaatjes en indrukken leunt en minder contact houdt met gevoel, nuance of feitelijke stap-voor-stapverwerking.",
                            ),
                        ],
                    },
                    {
                        "term": "Visuele predikaten",
                        "questions": [
                            (
                                "Wat zijn visuele predikaten?",
                                "Dat zijn woorden en uitdrukkingen die verwijzen naar zien, beeld, licht, scherpte en perspectief.",
                            ),
                            (
                                "Waarom helpt het om visuele predikaten te herkennen in taal?",
                                "Omdat je daardoor ziet hoe iemand intern informatie codeert en waarop je communicatief kunt aansluiten.",
                            ),
                            (
                                "Wat betekent het om predikaten te matchen?",
                                "Dat je in jouw taalgebruik aansluit bij het dominante zintuiglijke kanaal van de ander.",
                            ),
                            (
                                "Hoe draagt dit bij aan begrip en rapport?",
                                "Het vergroot herkenning en maakt het voor de ander makkelijker om jouw boodschap te volgen en te vertrouwen.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Kinesthetisch",
                "distractors": ["Visuele predikaten", "Olfactorisch"],
                "terms": [
                    {
                        "term": "Kinesthetische voorkeur",
                        "questions": [
                            (
                                "Hoe denkt iemand met een kinesthetische voorkeur?",
                                "Zo iemand denkt sterk vanuit gevoel, lichamelijke ervaring, beweging en innerlijke sensaties.",
                            ),
                            (
                                "Hoe leert iemand met een kinesthetische voorkeur het best?",
                                "Door te doen, te ervaren, te voelen en informatie te koppelen aan concrete lichamelijke of emotionele beleving.",
                            ),
                            (
                                "Waarom krijgt informatie pas betekenis wanneer het lichamelijk gevoeld wordt?",
                                "Omdat de innerlijke overtuiging en het begrip voor deze voorkeur vaak pas echt landen via gevoelservaring.",
                            ),
                            (
                                "Wat zijn de valkuilen van een sterk kinesthetische voorkeur?",
                                "Dat iemand trager verwerkt, sneller blijft hangen in gevoel of moeite heeft om afstand te nemen en te structureren.",
                            ),
                        ],
                    },
                    {
                        "term": "Kinesthetische predikaten",
                        "questions": [
                            (
                                "Wat zijn kinesthetische predikaten?",
                                "Dat zijn woorden die verwijzen naar voelen, aanraken, druk, beweging, grip en lichamelijke sensaties.",
                            ),
                            (
                                "Waarom verwijzen deze woorden vaak naar lichamelijke ervaring?",
                                "Omdat kinesthetische taal direct gekoppeld is aan hoe iets in het lichaam of gevoel wordt beleefd.",
                            ),
                            (
                                "Hoe kun je aan taal herkennen dat iemand kinesthetisch communiceert?",
                                "Door woorden te horen als voelen, raken, zwaar, licht, warm, vastpakken of in beweging komen.",
                            ),
                            (
                                "Waarom helpt dit bij afstemmen?",
                                "Omdat je dan taal kunt gebruiken die voor de ander natuurlijk en invoelbaar klinkt.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Digitaal",
                "distractors": ["Visueel", "Rapport via modaliteiten"],
                "terms": [
                    {
                        "term": "Digitaal als verwerkingssysteem",
                        "questions": [
                            (
                                "Waarom is digitaal volgens de manual geen echt zintuig maar wel een belangrijk verwerkingssysteem?",
                                "Omdat digitaal niet direct zintuiglijk waarneemt, maar vooral logisch, talig en analytisch verwerkt wat via andere kanalen binnenkomt.",
                            ),
                            (
                                "Hoe denkt iemand met een digitale voorkeur?",
                                "Zo iemand denkt vaak in analyse, structuur, feiten, definities en logische samenhang.",
                            ),
                            (
                                "Waarom staat informatie en structuur bij deze voorkeur centraal?",
                                "Omdat betekenis vooral ontstaat via ordening, begrip, onderscheid en heldere conceptuele kaders.",
                            ),
                            (
                                "Wat is de valkuil van een sterk digitale voorkeur?",
                                "Dat iemand te veel afstand neemt van directe ervaring en gevoel en daardoor abstract, droog of los van beleving communiceert.",
                            ),
                        ],
                    },
                    {
                        "term": "Digitale predikaten",
                        "questions": [
                            (
                                "Waaraan herken je digitale predikaten?",
                                "Aan woorden die verwijzen naar logica, analyse, begrijpen, structuur, informatie en conclusies.",
                            ),
                            (
                                "Waarom zijn deze vaak feitelijk, abstract en afstandelijk?",
                                "Omdat digitale taal vooral conceptueel ordent in plaats van zintuiglijk ervaarbaar beschrijft.",
                            ),
                            (
                                "Hoe verschilt digitale taal van zintuiglijk rijke taal?",
                                "Digitale taal beschrijft vaker analyse en interpretatie, terwijl zintuiglijke taal concreter voelbaar of voorstelbaar is.",
                            ),
                            (
                                "Wat zegt digitale taal over de manier waarop iemand informatie verwerkt?",
                                "Dat die persoon vaak via denken, structureren en verklaren betekenis opbouwt.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Auditief",
                "distractors": ["Kinesthetisch", "Falen bestaat niet"],
                "terms": [
                    {
                        "term": "Auditieve voorkeur",
                        "questions": [
                            (
                                "Hoe denkt iemand met een auditieve voorkeur?",
                                "Iemand met een auditieve voorkeur denkt vaak in woorden, ritme, klank, gesprekken en innerlijke dialoog.",
                            ),
                            (
                                "Hoe spreekt iemand met een auditieve voorkeur vaak?",
                                "Vaak in zorgvuldig geformuleerde taal met nadruk op klank, toon, logische volgorde en verbale precisie.",
                            ),
                            (
                                "Hoe leert iemand met een auditieve voorkeur het best?",
                                "Door uitleg te horen, hardop te bespreken, te luisteren en informatie verbaal te herhalen.",
                            ),
                            (
                                "Wat zijn mogelijke valkuilen van deze voorkeur?",
                                "Dat iemand kan blijven hangen in praten of analyseren via woorden zonder genoeg visueel of gevoelsmatig contact.",
                            ),
                        ],
                    },
                    {
                        "term": "Auditieve predikaten",
                        "questions": [
                            (
                                "Wat zijn auditieve predikaten?",
                                "Dat zijn woorden die verwijzen naar horen, klinken, zeggen, stem, toon en ritme.",
                            ),
                            (
                                "Hoe kun je auditieve voorkeur herkennen in woordgebruik?",
                                "Door uitdrukkingen te horen als dat klinkt goed, ik hoor wat je zegt of dat resoneert niet voor mij.",
                            ),
                            (
                                "Waarom helpt het herkennen van deze woorden bij communicatie?",
                                "Omdat je daardoor sneller merkt welk kanaal voor de ander vertrouwd en overtuigend voelt.",
                            ),
                            (
                                "Hoe draagt auditieve afstemming bij aan rapport?",
                                "Auditieve afstemming versterkt herkenning en maakt je communicatie vloeiender en beter invoelbaar voor de ander.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Geur en smaak",
                "distractors": ["Visuele voorkeur", "Meta-programma's"],
                "terms": [
                    {
                        "term": "Olfactorisch",
                        "questions": [
                            (
                                "Wat is het olfactorische zintuig?",
                                "Het olfactorische zintuig is het reukzintuig, waarmee mensen geuren waarnemen.",
                            ),
                            (
                                "Waarom is geur sterk gekoppeld aan emotie en herinnering?",
                                "Omdat geur direct en krachtig verbonden is met geheugenstructuren en emotionele associaties.",
                            ),
                            (
                                "Waarom speelt reuk een rol in veiligheid en waarschuwing?",
                                "Geur helpt mensen snel signalen op te merken die met gevaar, bederf of juist vertrouwdheid te maken hebben.",
                            ),
                            (
                                "Waarom krijgt dit zintuig in communicatie minder nadruk in NLP?",
                                "Omdat het minder vaak expliciet in taal voorkomt dan zien, horen of voelen, al kan het wel sterk doorwerken in ervaring.",
                            ),
                        ],
                    },
                    {
                        "term": "Gustatorisch",
                        "questions": [
                            (
                                "Wat is het gustatorische zintuig?",
                                "Dat is het smaakzintuig, waarmee mensen smaken ervaren.",
                            ),
                            (
                                "Welke smaken worden genoemd als basisvoorbeelden?",
                                "Basisvoorbeelden zijn onder meer zoet, zuur, zout en bitter.",
                            ),
                            (
                                "Waarom is smaak gekoppeld aan emotie en herinnering?",
                                "Omdat smaakervaringen vaak sterk verbonden raken met herinneringen, voorkeuren en emotionele beleving.",
                            ),
                            (
                                "Waarom staat dit zintuig in NLP meer op de achtergrond?",
                                "Omdat smaak in communicatie meestal minder direct een rol speelt dan visuele, auditieve en kinesthetische kanalen.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Zintuigen en functionaliteit / perceptie",
                "distractors": ["Spelend leren", "NLP als technologie"],
                "terms": [
                    {
                        "term": "Rapport via modaliteiten",
                        "questions": [
                            (
                                "Waarom helpt afstemmen op iemands dominante modaliteit bij het opbouwen van rapport?",
                                "Omdat de ander zich sneller begrepen voelt wanneer jij taal en voorbeelden gebruikt die passen bij zijn voorkeurskanaal.",
                            ),
                            (
                                "Hoe maakt schakelen tussen modaliteiten communicatie effectiever?",
                                "Je kunt iemand helpen informatie beter te verwerken door bewust via meerdere zintuiglijke ingangen aan te sluiten of te verbreden.",
                            ),
                            (
                                "Waarom vergroot dit begrip bij de ontvanger?",
                                "Omdat de boodschap toegankelijker wordt wanneer die aansluit op de manier waarop de ontvanger betekenis opbouwt.",
                            ),
                            (
                                "Hoe maakt dit je flexibeler als communicator?",
                                "Je beschikt dan over meer manieren om contact te maken, uit te leggen en iemand mee te nemen in verandering.",
                            ),
                        ],
                    },
                    {
                        "term": "Rijkere innerlijke wereld",
                        "questions": [
                            (
                                "Waarom geeft toegang tot meerdere modaliteiten een rijkere innerlijke wereld?",
                                "Omdat ervaring dan niet via een smal kanaal verloopt, maar voller, genuanceerder en creatiever beleefd kan worden.",
                            ),
                            (
                                "Hoe vergroot dit verbeelding en zelfreflectie?",
                                "Meer modaliteiten geven meer invalshoeken om ervaringen te onderzoeken, voor te stellen en te begrijpen.",
                            ),
                            (
                                "Waarom verdiept dit emotionele ervaring?",
                                "Omdat emotie rijker wordt beleefd wanneer beeld, geluid, gevoel en betekenis elkaar versterken.",
                            ),
                            (
                                "Hoe helpt dit bij persoonlijke ontwikkeling?",
                                "Het maakt mensen flexibeler in waarnemen, betekenis geven en kiezen hoe ze met ervaring omgaan.",
                            ),
                        ],
                    },
                    {
                        "term": "Perceptie en illusie",
                        "questions": [
                            (
                                "Wat laten optische illusies zien over menselijke perceptie?",
                                "Dat perceptie geen directe kopie van de werkelijkheid is, maar een actieve interpretatie door het brein.",
                            ),
                            (
                                "Waarom is perceptie geen passieve registratie van de werkelijkheid?",
                                "Omdat aandacht, verwachting, context en eerdere ervaring bepalen wat iemand meent waar te nemen.",
                            ),
                            (
                                "Hoe ondersteunt dit het NLP-uitgangspunt over subjectieve ervaring?",
                                "Het laat zien dat mensen hun eigen werkelijkheid construeren in plaats van die simpelweg objectief op te nemen.",
                            ),
                            (
                                "Wat leert dit over de relatie tussen waarneming en interpretatie?",
                                "Dat waarneming en interpretatie onafscheidelijk zijn en samen bepalen hoe ervaring wordt beleefd.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Fundament 4: Wet van Cybernetica",
        "subheading_distractors": ["Auditief", "NLP anno nu"],
        "concepts": [
            {
                "concept": "Benodigde variatie",
                "distractors": ["Rapport", "Toepassing binnen NLP"],
                "terms": [
                    {
                        "term": "Wet van benodigde variatie",
                        "questions": [
                            (
                                "Wat stelt de wet van cybernetica of benodigde variatie volgens de manual?",
                                "De wet stelt dat het systeem of element met de meeste relevante gedragskeuzes de meeste invloed op het geheel heeft.",
                            ),
                            (
                                "Waarom heeft het systeem met de meeste keuze de meeste mogelijkheden?",
                                "Omdat meer variatie meer manieren geeft om passend te reageren op veranderingen en verstoringen.",
                            ),
                            (
                                "Hoe hangt flexibiliteit samen met beheersing van een context?",
                                "Wie flexibeler kan schakelen, kan beter afstemmen en daardoor effectiever invloed uitoefenen op de situatie.",
                            ),
                            (
                                "Waarom is variatie belangrijk voor aanpassing en veerkracht?",
                                "Omdat star gedrag sneller vastloopt, terwijl variatie ruimte geeft om je aan te passen en te herstellen.",
                            ),
                        ],
                    },
                    {
                        "term": "Macht en systeemverstoring",
                        "questions": [
                            (
                                "Wat gebeurt er volgens Frank Pucelik wanneer een element het systeem overheerst door macht?",
                                "Dan raakt het systeem uit balans, omdat andere delen minder ruimte hebben om flexibel mee te bewegen en bij te sturen.",
                            ),
                            (
                                "Waarom kan dat een systeem ontwrichten of lamleggen?",
                                "Omdat overmatige macht keuzevrijheid en terugkoppeling vermindert, waardoor het systeem minder adaptief wordt.",
                            ),
                            (
                                "Wat zegt dit over gezonde dynamiek in systemen?",
                                "Dat gezonde systemen ruimte nodig hebben voor wederzijdse invloed, variatie en responsiviteit.",
                            ),
                            (
                                "Waarom is dit relevant voor communicatie en organisaties?",
                                "Omdat ook teams en relaties beter functioneren wanneer er voldoende flexibiliteit, feedback en keuzeruimte aanwezig zijn.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Toepassingen van cybernetica in NLP en daarbuiten",
                "distractors": ["Wetenschappelijke achtergrond", "Spelend leren"],
                "terms": [
                    {
                        "term": "Toepassingen in praktijkvelden",
                        "questions": [
                            (
                                "In welke domeinen noemt de manual voorbeelden van de wet van cybernetica?",
                                "De manual noemt onder meer management, onderwijs, gezondheidszorg, coaching, relaties en persoonlijke ontwikkeling.",
                            ),
                            (
                                "Waarom helpt benodigde variatie in management, onderwijs en gezondheidszorg?",
                                "Omdat professionals in die velden effectiever worden wanneer zij flexibel kunnen inspelen op verschillende mensen en omstandigheden.",
                            ),
                            (
                                "Hoe ondersteunt variatie betere respons op veranderende omstandigheden?",
                                "Meer variatie maakt het mogelijk om sneller en passender te reageren wanneer de context verandert.",
                            ),
                            (
                                "Waarom is dit ook relevant in relaties, coaching en persoonlijke ontwikkeling?",
                                "Omdat ook daar meer keuzevrijheid en gedragsflexibiliteit leiden tot betere afstemming en groei.",
                            ),
                        ],
                    },
                    {
                        "term": "Toepassing binnen NLP",
                        "questions": [
                            (
                                "Waarom moet een NLP-practitioner flexibel zijn in interventies?",
                                "Omdat geen enkele interventie in elke situatie hetzelfde werkt en effectieve begeleiding vraagt om kunnen variëren.",
                            ),
                            (
                                "Hoe helpt variatie in taal, metaforen en interventies bij verandering?",
                                "Variatie vergroot de kans dat een boodschap of interventie aansluit bij het wereldmodel en de behoefte van de ander.",
                            ),
                            (
                                "Waarom vergroot meer keuze de controle over een situatie?",
                                "Omdat meer keuzemogelijkheden je minder afhankelijk maken van een enkele aanpak die misschien niet werkt.",
                            ),
                            (
                                "Hoe verbindt dit de wet van cybernetica met gedragsverandering?",
                                "Gedragsverandering wordt sterker wanneer iemand nieuwe opties ontwikkelt en daardoor flexibeler kan reageren.",
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


def build_module1_topics() -> list[dict]:
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
        for topic in MODULE1_STRUCTURE
    ]


MODULE1_TOPIC_BLUEPRINT = build_module1_topics()


def build_module1_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE1_STRUCTURE]
    heading_options = topic_names + [
        "Wereldmodellen van NLP",
        "De kunst van magische taalpatronen",
    ]
    exercises = [
        _build_multi_select(
            title="Fundamenten van NLP - hoofdstukkoppen",
            topic_title=MODULE1_STRUCTURE[0]["topic"],
            concept_title=MODULE1_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder hoofdstuk 1 Fundamenten van NLP?",
            question="Selecteer de koppen die bij hoofdstuk 1 Fundamenten van NLP horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE1_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"Fundamenten van NLP - {topic['topic']} subkoppen",
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
                    title=f"Fundamenten van NLP - {concept['concept']} termen",
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
                                f"Fundamenten van NLP - {concept['concept']} - {term['term']} - vraag {question_index}"
                            ),
                            topic_title=topic["topic"],
                            concept_title=concept["concept"],
                            prompt=question,
                            question=question,
                            model_answer=model_answer,
                        )
                    )

    return exercises
