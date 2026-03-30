from __future__ import annotations


MODULE_TITLE = "De kunst van magische taalpatronen"


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


MODULE3_STRUCTURE = [
    {
        "topic": "Taal en neurologie",
        "subheading_distractors": ["Het structureel differentiaal", "Filosofie en NLP"],
        "concepts": [
            {
                "concept": "Taalverwerking",
                "distractors": ["Constructivisme", "Nominalisaties"],
                "terms": [
                    {
                        "term": "Taalgeneratie",
                        "questions": [
                            (
                                "Wat is taalgeneratie?",
                                "Taalgeneratie is het proces waarbij gedachten worden omgezet in woorden en zinnen.",
                            ),
                            (
                                "Welke functie heeft taalgeneratie binnen communicatie?",
                                "Taalgeneratie maakt het mogelijk om innerlijke ervaring uit te drukken en betekenis met anderen te delen.",
                            ),
                            (
                                "Waarom is taalgeneratie belangrijk binnen NLP?",
                                "Omdat NLP uitgaat van het idee dat woorden invloed hebben op interpretatie, emotie en gedrag.",
                            ),
                            (
                                "Wat gebeurt er eerst: taal of betekenis?",
                                "Binnen dit hoofdstuk zijn taal en betekenis nauw verweven: woorden geven vorm aan betekenis en betekenis beïnvloedt vervolgens gevoel en gedrag.",
                            ),
                        ],
                    },
                    {
                        "term": "Taalbegrip",
                        "questions": [
                            (
                                "Wat is taalbegrip?",
                                "Taalbegrip is het proces waarbij iemand woorden, zinnen en boodschappen interpreteert en er betekenis aan geeft.",
                            ),
                            (
                                "Waarom is taalbegrip meer dan alleen woorden horen?",
                                "Omdat begrip niet alleen afhangt van woorden, maar ook van de betekenis, overtuigingen en interpretaties die iemand eraan koppelt.",
                            ),
                            (
                                "Hoe hangt taalbegrip samen met wereldmodellen?",
                                "Mensen begrijpen taal vanuit hun eigen wereldmodel, waardoor dezelfde woorden verschillende betekenissen kunnen oproepen.",
                            ),
                            (
                                "Waarom kan taalbegrip tot misverstanden leiden?",
                                "Omdat mensen vaak reageren op hun eigen interpretatie van woorden en niet op een objectieve werkelijkheid.",
                            ),
                        ],
                    },
                    {
                        "term": "Interne dialoog",
                        "questions": [
                            (
                                "Wat is interne dialoog?",
                                "Interne dialoog is de taal die iemand in zichzelf gebruikt om ervaringen te duiden, situaties te beoordelen en zichzelf aan te sturen.",
                            ),
                            (
                                "Waarom is interne dialoog belangrijk?",
                                "Omdat de woorden die iemand in het eigen hoofd gebruikt invloed hebben op interpretatie, overtuigingen, emoties en gedrag.",
                            ),
                            (
                                "Hoe beïnvloedt interne dialoog gevoel?",
                                "De betekenis van woorden bepaalt eerst emoties en daarna gedrag. Interne dialoog beïnvloedt dus rechtstreeks hoe iemand zich voelt.",
                            ),
                            (
                                "Waarom is bewustwording van interne dialoog nuttig?",
                                "Omdat iemand pas taalpatronen kan veranderen als die eerst herkend worden.",
                            ),
                        ],
                    },
                    {
                        "term": "Beslissingen",
                        "questions": [
                            (
                                "Welke rol speelt taal bij beslissingen?",
                                "Taal beïnvloedt hoe iemand situaties interpreteert, en die interpretatie stuurt vervolgens emoties, overtuigingen en keuzes.",
                            ),
                            (
                                "Waarom zijn beslissingen niet volledig objectief?",
                                "Omdat beslissingen voortkomen uit een persoonlijk wereldmodel, opgebouwd uit zintuiglijke indrukken, generalisaties en betekenissen.",
                            ),
                            (
                                "Hoe kan andere taal tot andere beslissingen leiden?",
                                "Andere taal kan een andere betekenis geven aan dezelfde ervaring, waardoor ook gevoelens, gedrag en keuzes veranderen.",
                            ),
                            (
                                "Waarom is dit relevant binnen NLP?",
                                "Omdat NLP werkt met het veranderen van taal- en denkpatronen om andere uitkomsten mogelijk te maken.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Negatieven en taal",
                "distractors": ["Kritisch reflecteren", "Universal quantifiers"],
                "terms": [
                    {
                        "term": "Interne representatie",
                        "questions": [
                            (
                                "Wat is een interne representatie?",
                                "Een interne representatie is de innerlijke voorstelling die iemand maakt van een ervaring, bijvoorbeeld in beelden, geluiden of gevoelens.",
                            ),
                            (
                                "Waarom is interne representatie belangrijk bij taal?",
                                "Omdat woorden innerlijke beelden en betekenissen oproepen, en die innerlijke voorstellingen beïnvloeden hoe iemand iets ervaart.",
                            ),
                            (
                                "Hoe hangt interne representatie samen met overtuigingen?",
                                "Overtuigingen worden mede opgebouwd uit de interne representatie, de betekenis die eraan wordt gegeven en de emotionele reactie die daarop volgt.",
                            ),
                            (
                                "Waarom zijn negaties hier relevant?",
                                "Omdat taal vaak eerst een voorstelling oproept van datgene wat genoemd wordt, waardoor ook een ontkenning nog steeds een specifieke interne representatie activeert.",
                            ),
                        ],
                    },
                    {
                        "term": "Focus",
                        "questions": [
                            (
                                "Wat doet taal met focus?",
                                "Taal stuurt de aandacht van iemand naar bepaalde elementen van een ervaring, en laat andere elementen juist naar de achtergrond verdwijnen.",
                            ),
                            (
                                "Waarom is focus belangrijk binnen communicatie?",
                                "Omdat waar de aandacht op gericht wordt mede bepaalt welke betekenis iemand aan een situatie geeft.",
                            ),
                            (
                                "Hoe hangen focus en deletie samen?",
                                "Deletie is het weglaten van informatie. Daardoor komt de aandacht automatisch op een beperkt deel van de ervaring te liggen.",
                            ),
                            (
                                "Waarom kan taal iemand eenzijdig laten kijken?",
                                "Omdat woorden kunnen zorgen voor selectieve aandacht, waardoor iemand vooral één betekenis of één aspect van de situatie ziet.",
                            ),
                        ],
                    },
                    {
                        "term": "Suggestie",
                        "questions": [
                            (
                                "Wat is suggestie in taal?",
                                "Suggestie is taalgebruik dat impliciet richting geeft aan wat iemand denkt, voelt of verwacht, zonder dat dit altijd expliciet wordt benoemd.",
                            ),
                            (
                                "Waarom heeft suggestie invloed?",
                                "Omdat woorden betekenis, verwachting en interne beelden oproepen, en daarmee de ervaring van de luisteraar sturen.",
                            ),
                            (
                                "Hoe hangt suggestie samen met focus?",
                                "Suggestie richt de aandacht op een bepaalde interpretatie of uitkomst, waardoor andere mogelijkheden minder zichtbaar worden.",
                            ),
                            (
                                "Waarom moet je zorgvuldig omgaan met suggestieve taal?",
                                "Omdat taal invloed heeft op overtuigingen, emoties en gedrag, en dus ook manipulatief of onethisch kan worden ingezet.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Complexe equivalentie",
        "subheading_distractors": ["Algemene semantiek", "Ethiek en verantwoordelijkheid"],
        "concepts": [
            {
                "concept": "Betekenisgeving",
                "distractors": ["Deleties", "Taalgeneratie"],
                "terms": [
                    {
                        "term": "Koppelingen",
                        "questions": [
                            (
                                "Wat is een koppeling binnen complexe equivalentie?",
                                "Een koppeling is een verbinding waarbij iemand twee zaken aan elkaar gelijk of direct verbonden maakt, alsof het één en hetzelfde betekent.",
                            ),
                            (
                                "Hoe ziet een complexe equivalentie er taalkundig uit?",
                                "Vaak als een impliciete of expliciete structuur van X = Y, bijvoorbeeld: 'Als ik kritiek krijg, betekent dat dat ik faal.'",
                            ),
                            (
                                "Waarom zijn zulke koppelingen belangrijk?",
                                "Omdat ze sterke invloed hebben op emoties, overtuigingen en gedrag.",
                            ),
                            (
                                "Wat is het doel van het onderzoeken van koppelingen?",
                                "Het doel is zichtbaar maken welke betekenis iemand geeft, zodat die koppeling eventueel functioneler gemaakt kan worden.",
                            ),
                        ],
                    },
                    {
                        "term": "Logica",
                        "questions": [
                            (
                                "Welke rol speelt logica bij complexe equivalenties?",
                                "Logica bepaalt of de koppeling tussen twee zaken redelijk, onderbouwd en geldig is, of dat iemand te snel iets gelijkstelt.",
                            ),
                            (
                                "Waarom kan de logica in een complexe equivalentie problematisch zijn?",
                                "Omdat iemand een verband kan aannemen zonder voldoende bewijs, waardoor een onjuiste overtuiging ontstaat.",
                            ),
                            (
                                "Hoe herken je zwakke logica in taal?",
                                "Door te letten op uitspraken waarin een gebeurtenis direct wordt vertaald naar een betekenis, identiteit of conclusie.",
                            ),
                            (
                                "Waarom is logisch onderzoeken nuttig?",
                                "Omdat het helpt om automatische betekeniskoppelingen te toetsen in plaats van ze zomaar als waar aan te nemen.",
                            ),
                        ],
                    },
                    {
                        "term": "Overtuigingen",
                        "questions": [
                            (
                                "Hoe hangen complexe equivalenties samen met overtuigingen?",
                                "Complexe equivalenties kunnen bouwstenen zijn van overtuigingen, doordat iemand vaste betekenissen koppelt aan ervaringen.",
                            ),
                            (
                                "Waarom kunnen overtuigingen door complexe equivalenties versterkt worden?",
                                "Omdat terugkerende koppelingen tussen gebeurtenis en betekenis uiteindelijk als vanzelfsprekend of waar gaan voelen.",
                            ),
                            (
                                "Hoe kun je een beperkende overtuiging onderzoeken?",
                                "Door na te gaan welke koppeling eronder ligt en te vragen hoe iemand precies van feit naar betekenis gaat.",
                            ),
                            (
                                "Waarom is dit relevant binnen NLP?",
                                "Omdat NLP werkt met het zichtbaar maken en veranderen van de structuur achter overtuigingen en ervaringen.",
                            ),
                        ],
                    },
                    {
                        "term": "Verdiepingen",
                        "questions": [
                            (
                                "Wat wordt hier bedoeld met verdiepingen?",
                                "Verdiepingen zijn lagen van betekenis onder een uitspraak, waarbij je niet alleen de woorden bekijkt maar ook de onderliggende aannames en waarden.",
                            ),
                            (
                                "Waarom is verdieping belangrijk bij complexe equivalenties?",
                                "Omdat achter een ogenschijnlijk simpele uitspraak vaak een diepere overtuiging of waarde schuilgaat.",
                            ),
                            (
                                "Hoe kom je tot verdieping in een gesprek?",
                                "Door door te vragen naar wat iets betekent, waarop de koppeling gebaseerd is en wat eronder ligt.",
                            ),
                            (
                                "Wat levert die verdieping op?",
                                "Meer inzicht in hoe iemand betekenis geeft en waar verandering of herinterpretatie mogelijk is.",
                            ),
                        ],
                    },
                    {
                        "term": "Cartesian logics",
                        "questions": [
                            (
                                "Wat is het doel van cartesian logics in deze context?",
                                "Cartesian logics helpen om aannames, gevolgtrekkingen en overtuigingen systematisch te onderzoeken en op logische gaten te testen.",
                            ),
                            (
                                "Waarom past cartesian logics bij complexe equivalenties?",
                                "Omdat complexe equivalenties vaak op impliciete logica rusten, en cartesian logics helpen om die logica expliciet te maken.",
                            ),
                            (
                                "Wat toets je met cartesian logics?",
                                "Je toetst of een overtuiging klopt, wat waar zou zijn als het wel klopt, en wat waar zou zijn als het niet klopt.",
                            ),
                            (
                                "Waarom is dat nuttig?",
                                "Omdat het starre betekeniskoppelingen kan losmaken en ruimte geeft voor alternatieve interpretaties.",
                            ),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "topic": "Het metamodel",
        "subheading_distractors": ["Constructie van realiteit", "Bewustzijn en ervaring"],
        "concepts": [
            {
                "concept": "Doel",
                "distractors": ["Kritisch reflecteren", "Werkelijkheid versus representatie"],
                "terms": [
                    {
                        "term": "Verhelderen",
                        "questions": [
                            (
                                "Wat is het doel van verhelderen in het metamodel?",
                                "Verhelderen betekent dat vage of onduidelijke taal concreter gemaakt wordt, zodat beter zichtbaar wordt wat iemand precies bedoelt.",
                            ),
                            (
                                "Waarom is verhelderen belangrijk?",
                                "Omdat mensen vaak spreken vanuit aannames, weglatingen of vervormingen, waardoor betekenis onduidelijk blijft.",
                            ),
                            (
                                "Hoe verhelder je een uitspraak?",
                                "Door door te vragen naar wie, wat, waar, wanneer, hoe en waaraan iemand dat precies merkt.",
                            ),
                            (
                                "Wat levert verhelderen op?",
                                "Meer precisie, minder misverstanden en een beter zicht op het wereldmodel van de spreker.",
                            ),
                        ],
                    },
                    {
                        "term": "Specificeren",
                        "questions": [
                            (
                                "Wat betekent specificeren in het metamodel?",
                                "Specificeren betekent dat algemene of vage uitspraken teruggebracht worden naar concrete informatie.",
                            ),
                            (
                                "Waarom is specificeren nodig?",
                                "Omdat taal vaak informatie weglaat of te algemeen maakt, waardoor niet duidelijk is wat feitelijk bedoeld wordt.",
                            ),
                            (
                                "Welke vraag helpt bij specificeren?",
                                "Bijvoorbeeld: 'Wie precies?', 'Wanneer precies?', 'Hoe vaak precies?' of 'Wat bedoel je precies?'",
                            ),
                            (
                                "Wat is het effect van specificeren?",
                                "Het maakt uitspraken toetsbaar, concreet en bruikbaar voor verdere interventie.",
                            ),
                        ],
                    },
                    {
                        "term": "Uitdagen",
                        "questions": [
                            (
                                "Wat betekent uitdagen in het metamodel?",
                                "Uitdagen betekent dat je de taalstructuur van een uitspraak onderzoekt op aannames, vervormingen of generalisaties.",
                            ),
                            (
                                "Waarom wordt taal uitgedaagd?",
                                "Om te toetsen of de gevolgtrekking klopt en of de spreker niet gevangen zit in een beperkt of vervormd wereldmodel.",
                            ),
                            (
                                "Wanneer is uitdagen behulpzaam?",
                                "Wanneer iemand spreekt in absolute, vage of starre termen die beperkend werken.",
                            ),
                            (
                                "Wat is het doel van uitdagen?",
                                "Meer keuzevrijheid, nauwkeuriger betekenis en een opener manier van kijken naar ervaring.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Functies",
                "distractors": ["Postmodernisme", "Structureren van ervaring"],
                "terms": [
                    {
                        "term": "Vragen",
                        "questions": [
                            (
                                "Waarom werkt het metamodel met vragen?",
                                "Omdat vragen helpen om ontbrekende informatie terug te halen en onduidelijke taal te verduidelijken.",
                            ),
                            (
                                "Wat doen metamodelvragen met een uitspraak?",
                                "Ze maken zichtbaar welke aannames, deleties, generalisaties of vervormingen in de uitspraak zitten.",
                            ),
                            (
                                "Waarom zijn vragen krachtiger dan alleen uitleg geven?",
                                "Omdat de spreker zelf actief betekenis moet onderzoeken en formuleren.",
                            ),
                            (
                                "Wat is een voorbeeld van een metamodelvraag?",
                                "Bijvoorbeeld: 'Wie precies?', 'Hoe weet je dat?', 'Altijd?', of 'Hoe gebeurt dat precies?'",
                            ),
                        ],
                    },
                    {
                        "term": "Prioriteiten",
                        "questions": [
                            (
                                "Wat is de functie van prioriteiten binnen het metamodel?",
                                "Prioriteiten helpen bepalen welke uitspraak, welk patroon of welke betekenis het meest belangrijk is om eerst te onderzoeken.",
                            ),
                            (
                                "Waarom kun je niet alles tegelijk uitvragen?",
                                "Omdat te veel vragen tegelijk onoverzichtelijk wordt en rapport of helderheid kan verstoren.",
                            ),
                            (
                                "Waar let je op bij prioriteiten?",
                                "Op wat het meest beperkend, onduidelijk of emotioneel geladen is in iemands taal.",
                            ),
                            (
                                "Waarom helpt prioriteren in interventie?",
                                "Omdat het de aandacht richt op de kernstructuur die de meeste invloed heeft op betekenis en gedrag.",
                            ),
                        ],
                    },
                    {
                        "term": "Taalpatronen",
                        "questions": [
                            (
                                "Wat zijn taalpatronen binnen het metamodel?",
                                "Dat zijn terugkerende manieren waarop mensen informatie weglaten, vervormen of generaliseren in hun taal.",
                            ),
                            (
                                "Waarom zijn taalpatronen belangrijk?",
                                "Omdat ze laten zien hoe iemand zijn wereld modelleert en waar beperkingen of misverstanden ontstaan.",
                            ),
                            (
                                "Welke hoofdgroepen van taalpatronen zijn er?",
                                "De hoofdgroepen zijn deleties, generalisaties en vervormingen.",
                            ),
                            (
                                "Wat is het nut van het herkennen van taalpatronen?",
                                "Het maakt gerichte vragen en effectievere communicatie-interventies mogelijk.",
                            ),
                        ],
                    },
                    {
                        "term": "Interventie",
                        "questions": [
                            (
                                "Waarom is het metamodel een interventie-instrument?",
                                "Omdat het niet alleen beschrijft hoe iemand praat, maar actief ingrijpt door die taalstructuur te onderzoeken en te veranderen.",
                            ),
                            (
                                "Wat verandert er door een metamodelinterventie?",
                                "De spreker krijgt vaak een nauwkeuriger, concreter en minder beperkend beeld van de eigen ervaring.",
                            ),
                            (
                                "Hoe helpt interventie bij wereldmodellen?",
                                "Door taalverheldering en uitdaging kan iemand zijn eigen wereldmodel opnieuw bekijken en bijstellen.",
                            ),
                            (
                                "Waarom is dat waardevol?",
                                "Omdat verandering in betekenis vaak ook leidt tot verandering in emotie, gedrag en resultaat.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Valkuilen",
                "distractors": ["Wittgenstein", "Referentieniveau"],
                "terms": [
                    {
                        "term": "Te veel aannames",
                        "questions": [
                            (
                                "Waarom zijn te veel aannames een valkuil?",
                                "Omdat je dan denkt te begrijpen wat iemand bedoelt zonder dat dit voldoende onderzocht is.",
                            ),
                            (
                                "Wat is het risico van aannames in een gesprek?",
                                "Dat je reageert op je eigen interpretatie in plaats van op wat de ander werkelijk zegt of bedoelt.",
                            ),
                            (
                                "Hoe voorkomt het metamodel te veel aannames?",
                                "Door vage of algemene taal terug te brengen naar concrete informatie met gerichte vragen.",
                            ),
                            (
                                "Welke vraag helpt hierbij?",
                                "Bijvoorbeeld: 'Wie precies?', 'Wat bedoel je daarmee?' of 'Hoe weet je dat?'",
                            ),
                        ],
                    },
                    {
                        "term": "Onethisch gebruik",
                        "questions": [
                            (
                                "Waarom kan het metamodel onethisch gebruikt worden?",
                                "Omdat taal en vragen krachtige invloed hebben en dus ook manipulatief ingezet kunnen worden.",
                            ),
                            (
                                "Welke waarschuwing geeft het handboek hierover?",
                                "Dat NLP schade kan aanrichten wanneer het tegen de wil van mensen of voor manipulatie wordt gebruikt.",
                            ),
                            (
                                "Waarom is respect hierbij essentieel?",
                                "Omdat de autonomie, waardigheid en keuzevrijheid van de ander behouden moeten blijven.",
                            ),
                            (
                                "Wat betekent ethisch gebruik in de praktijk?",
                                "Dat vragen worden ingezet om te verhelderen en te helpen, niet om te overheersen, te vernederen of te sturen tegen iemands belang in.",
                            ),
                        ],
                    },
                    {
                        "term": "Overgeneralisatie",
                        "questions": [
                            (
                                "Wat is overgeneralisatie?",
                                "Overgeneralisatie is het trekken van een te brede conclusie op basis van beperkte informatie.",
                            ),
                            (
                                "Waarom is dit een valkuil?",
                                "Omdat iemand een enkele ervaring kan behandelen alsof die altijd en overal geldt.",
                            ),
                            (
                                "Welke woorden verraden vaak overgeneralisatie?",
                                "Woorden als altijd, nooit, iedereen, niemand en alles.",
                            ),
                            (
                                "Hoe daag je overgeneralisatie uit?",
                                "Met vragen als: 'Altijd?', 'Nooit?', 'Zijn er uitzonderingen?' of 'Hoe vaak precies?'",
                            ),
                        ],
                    },
                    {
                        "term": "Onjuiste interpretatie",
                        "questions": [
                            (
                                "Wat is onjuiste interpretatie?",
                                "Dat is wanneer iemand een gebeurtenis of uitspraak verkeerd duidt door deletie, vervorming of generalisatie.",
                            ),
                            (
                                "Waarom gebeurt dit snel?",
                                "Omdat mensen niet reageren op objectieve werkelijkheid, maar op hun eigen wereldmodel en betekenisgeving.",
                            ),
                            (
                                "Hoe kan het metamodel helpen?",
                                "Door de interpretatie open te breken en te toetsen met concrete en verhelderende vragen.",
                            ),
                            (
                                "Waarom is dit belangrijk in communicatie?",
                                "Omdat veel misverstanden ontstaan doordat mensen reageren op hun interpretatie in plaats van op de feitelijke bedoeling.",
                            ),
                        ],
                    },
                ],
            },
            {
                "concept": "Patronen",
                "distractors": ["Fenomenologie", "Constructivisme"],
                "terms": [
                    {
                        "term": "Deleties",
                        "questions": [
                            (
                                "Wat is een deletie?",
                                "Een deletie is het weglaten of negeren van informatie, waardoor een uitspraak onvolledig wordt.",
                            ),
                            (
                                "Waarom zijn deleties belangrijk in NLP?",
                                "Omdat deleties laten zien welke informatie uit de ervaring is verdwenen en dus teruggevraagd kan worden.",
                            ),
                            (
                                "Wat is een risico van deleties?",
                                "Dat belangrijke details ontbreken en dat iemand daardoor een vertekend of beperkt beeld van de situatie houdt.",
                            ),
                            (
                                "Hoe daag je een deletie uit?",
                                "Door te vragen wat precies weggelaten is, bijvoorbeeld: 'Wie?', 'Wat precies?', 'Waar?' of 'Hoe dan?'",
                            ),
                        ],
                    },
                    {
                        "term": "Generalisaties",
                        "questions": [
                            (
                                "Wat is een generalisatie?",
                                "Een generalisatie is een brede conclusie die uit een beperkt aantal ervaringen wordt getrokken.",
                            ),
                            (
                                "Waarom kunnen generalisaties nuttig zijn?",
                                "Omdat ze helpen om snel orde te scheppen in ervaringen.",
                            ),
                            (
                                "Waarom kunnen generalisaties problematisch zijn?",
                                "Omdat ze te absoluut kunnen worden, waardoor nuance en uitzonderingen verdwijnen.",
                            ),
                            (
                                "Hoe toets je een generalisatie?",
                                "Door te zoeken naar uitzonderingen, frequentie en concrete voorbeelden.",
                            ),
                        ],
                    },
                    {
                        "term": "Vervormingen",
                        "questions": [
                            (
                                "Wat is een vervorming?",
                                "Een vervorming is een interpretatie waarbij feiten worden verdraaid of anders ingevuld dan feitelijk onderbouwd is.",
                            ),
                            (
                                "Waarom ontstaan vervormingen?",
                                "Omdat mensen informatie vaak passend maken bij bestaande overtuigingen, emoties of verwachtingen.",
                            ),
                            (
                                "Wat is het effect van vervormingen?",
                                "Dat iemand gebeurtenissen anders gaat ervaren dan ze feitelijk zijn, met gevolgen voor emotie en gedrag.",
                            ),
                            (
                                "Hoe help je iemand bij een vervorming?",
                                "Door de redenering te onderzoeken en terug te gaan naar concrete observaties en specifieke informatie.",
                            ),
                        ],
                    },
                    {
                        "term": "Universal quantifiers",
                        "questions": [
                            (
                                "Wat zijn universal quantifiers?",
                                "Dat zijn woorden die een uitspraak absoluut of universeel maken, zoals altijd, nooit, iedereen en niemand.",
                            ),
                            (
                                "Waarom zijn universal quantifiers belangrijk?",
                                "Omdat ze vaak wijzen op overgeneralisatie en daardoor beperkende overtuigingen kunnen versterken.",
                            ),
                            (
                                "Hoe herken je een universal quantifier?",
                                "Aan taal die doet alsof iets zonder uitzondering geldt.",
                            ),
                            (
                                "Hoe daag je een universal quantifier uit?",
                                "Met vragen als: 'Altijd?', 'Nooit?', 'Zijn er uitzonderingen?' en 'Hoe vaak precies?'",
                            ),
                        ],
                    },
                    {
                        "term": "Referentiële index",
                        "questions": [
                            (
                                "Wat is een referentiële index?",
                                "Een referentiële index gaat over naar wie of wat precies verwezen wordt in een uitspraak.",
                            ),
                            (
                                "Wanneer is een referentiële index onduidelijk?",
                                "Wanneer iemand spreekt in vage termen als 'iedereen', 'men', 'ze' of 'je' zonder duidelijke verwijzing.",
                            ),
                            (
                                "Waarom is dat problematisch?",
                                "Omdat onduidelijke verwijzingen betekenis vervagen en aannames oproepen die niet gecontroleerd zijn.",
                            ),
                            (
                                "Hoe daag je een onduidelijke referentiële index uit?",
                                "Door te vragen: 'Wie precies?', 'Wie zijn ze?' of 'Wie zegt dat?'",
                            ),
                        ],
                    },
                    {
                        "term": "Nominalisaties",
                        "questions": [
                            (
                                "Wat is een nominalisatie?",
                                "Een nominalisatie is een proces of actie die in taal wordt omgezet in een ding of begrip, waardoor het statisch gaat lijken.",
                            ),
                            (
                                "Waarom zijn nominalisaties belangrijk?",
                                "Omdat ze de dynamiek van een proces verbergen en daardoor onduidelijk maken wat er feitelijk gebeurt.",
                            ),
                            (
                                "Hoe herken je een nominalisatie?",
                                "Vaak aan een zelfstandig naamwoord dat eigenlijk verwijst naar een proces, zoals communicatie, liefde, verandering of beleid.",
                            ),
                            (
                                "Hoe daag je een nominalisatie uit?",
                                "Door het woord weer terug te brengen naar een proces, met vragen als: 'Hoe gebeurt dat precies?' of 'Beschrijf eens wat er dan gebeurt.'",
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


def build_module3_topics() -> list[dict]:
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
        for topic in MODULE3_STRUCTURE
    ]


MODULE3_TOPIC_BLUEPRINT = build_module3_topics()


def build_module3_exercises() -> list[dict]:
    topic_names = [topic["topic"] for topic in MODULE3_STRUCTURE]
    heading_options = topic_names + [
        "Wereldmodellen van NLP",
        "Fundamenten van NLP",
    ]
    exercises = [
        _build_multi_select(
            title="De kunst van magische taalpatronen - hoofdstukkoppen",
            topic_title=MODULE3_STRUCTURE[0]["topic"],
            concept_title=MODULE3_STRUCTURE[0]["concepts"][0]["concept"],
            prompt="Welke koppen vallen onder het hoofdstuk De kunst van magische taalpatronen?",
            question="Selecteer de koppen die bij het hoofdstuk De kunst van magische taalpatronen horen.",
            option_labels=heading_options,
            correct_labels=topic_names,
        )
    ]

    for topic in MODULE3_STRUCTURE:
        concept_names = [concept["concept"] for concept in topic["concepts"]]
        exercises.append(
            _build_multi_select(
                title=f"De kunst van magische taalpatronen - {topic['topic']} subkoppen",
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
                    title=f"De kunst van magische taalpatronen - {concept['concept']} termen",
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
                                f"De kunst van magische taalpatronen - {concept['concept']} - {term['term']} - vraag {question_index}"
                            ),
                            topic_title=topic["topic"],
                            concept_title=concept["concept"],
                            prompt=question,
                            question=question,
                            model_answer=model_answer,
                        )
                    )

    return exercises