from __future__ import annotations

from .module0_question_bank import build_module0_exercises
from .module1_question_bank import MODULE1_TOPIC_BLUEPRINT, build_module1_exercises
from .module2_question_bank import MODULE2_TOPIC_BLUEPRINT, build_module2_exercises
from .module3_question_bank import MODULE3_TOPIC_BLUEPRINT, build_module3_exercises
from .module4_question_bank import MODULE4_TOPIC_BLUEPRINT, build_module4_exercises
from .module5_question_bank import MODULE5_TOPIC_BLUEPRINT, build_module5_exercises
from .module6_question_bank import MODULE6_TOPIC_BLUEPRINT, build_module6_exercises
from .module7_question_bank import MODULE7_TOPIC_BLUEPRINT, build_module7_exercises
from .module8_question_bank import MODULE8_TOPIC_BLUEPRINT, build_module8_exercises
from .module9_question_bank import MODULE9_TOPIC_BLUEPRINT, build_module9_exercises
from .module10_question_bank import MODULE10_TOPIC_BLUEPRINT, build_module10_exercises
from .module11_question_bank import MODULE11_TOPIC_BLUEPRINT, build_module11_exercises
from .module12_question_bank import MODULE12_TOPIC_BLUEPRINT, build_module12_exercises
from .module13_question_bank import MODULE13_TOPIC_BLUEPRINT, build_module13_exercises



DEMO_ORGANIZATION = {
    "name": "NeuroFlow Academy",
    "slug": "neuroflow-academy",
    "description": (
        "Demo tenant voor een NLP opleider. De inhoud is ingericht rond een "
        "practical-first practitioner traject met theorie, tekstanalyse, "
        "reflectie en trainerfeedback."
    ),
    "theme": {
        "brand_name": "NeuroFlow Academy",
        "logo_label": "NF",
        "logo_url": "",
        "hero_url": "",
        "background_image_opacity": 0.18,
        "primary_color": "#245c73",
        "secondary_color": "#ecf4f6",
        "accent_color": "#e48c52",
        "surface_color": "#ffffff",
        "background_style": (
            "linear-gradient(135deg, rgba(36,92,115,0.14), rgba(228,140,82,0.10))"
        ),
    },
}


DEMO_USERS = [
    {
        "email": "owner@platform.local",
        "password": "demo123",
        "first_name": "Platform",
        "last_name": "Owner",
        "is_platform_admin": True,
        "memberships": [],
    },
    {
        "email": "admin@neuroflow.local",
        "password": "demo123",
        "first_name": "Nina",
        "last_name": "Admin",
        "is_platform_admin": False,
        "memberships": ["organization_admin"],
    },
    {
        "email": "trainer@neuroflow.local",
        "password": "demo123",
        "first_name": "Timo",
        "last_name": "Trainer",
        "is_platform_admin": False,
        "memberships": ["trainer"],
    },
    {
        "email": "student@neuroflow.local",
        "password": "demo123",
        "first_name": "Sara",
        "last_name": "Student",
        "is_platform_admin": False,
        "memberships": ["student"],
    },
    {
        "email": "student2@neuroflow.local",
        "password": "demo123",
        "first_name": "Milan",
        "last_name": "Student",
        "is_platform_admin": False,
        "memberships": ["student"],
    },
]


DEMO_STUDENT_GROUPS = [
    {
        "name": "Practitioner groep A",
        "student_emails": ["student@neuroflow.local", "student2@neuroflow.local"],
    }
]


PRACTITIONER_PROGRAM = {
    "title": "NLP Practitioner",
    "level": "Practitioner",
    "description": (
        "Een curriculum voor studenten die NLP theoretisch en praktisch willen "
        "beheersen. Het programma combineert verplichte lesstof, verdieping, "
        "tekstanalyse, reflectie en trainerbeoordeling."
    ),
    "modules": [
        {
            "title": "De geschiedenis van NLP",
            "summary": (
                "Historische wortels van NLP, de belangrijkste voorlopers en "
                "de grondleggers van het vakgebied."
            ),
            "resources": [
                {
                    "title": "Intro op het speelveld",
                    "resource_type": "reader",
                    "content": (
                        "Gebruik dit blok om context te geven aan de ontwikkeling "
                        "van NLP. Focus op de brug tussen therapie, communicatie "
                        "en modelleren."
                    ),
                    "sort_order": 1,
                }
            ],
            "topics": [
                {
                    "title": "Pre-NLP",
                    "summary": "Voorlopers die de denkrichting van NLP sterk hebben beinvloed.",
                    "concepts": [
                        {
                            "title": "Virginia Satir",
                            "summary": "Gezinstherapie, communicatiecategorieen, communicatie en relaties en familiestamboom.",
                            "tags": ["gezinstherapie", "communicatiecategorieen", "communicatie en relaties", "familiestamboom"],
                        },
                        {
                            "title": "Milton Erickson",
                            "summary": "Hypnotherapie, indirecte suggestie, metaforen en verhalen en taalgebruik.",
                            "tags": ["hypnotherapie", "indirecte suggestie", "metaforen en verhalen", "taalgebruik"],
                        },
                        {
                            "title": "Fritz Perls",
                            "summary": "Gestalttherapie, hier-en-nu, zelfbewustzijn en verantwoordelijkheid.",
                            "tags": ["gestalttherapie", "hier-en-nu", "zelfbewustzijn", "verantwoordelijkheid"],
                        },
                    ],
                },
                {
                    "title": "Grondleggers van NLP",
                    "summary": "De co-creators en hun inhoudelijke accenten.",
                    "concepts": [
                        {
                            "title": "Frank Pucelik",
                            "summary": "Co-grondlegger met focus op het NLP-model, menselijke ervaring en het veranderen van beperkende overtuigingen.",
                            "tags": ["co-grondlegger", "nlp-model", "menselijke ervaring", "beperkende overtuigingen en potentieel"],
                        },
                        {
                            "title": "Richard Bandler",
                            "summary": "Co-creator met focus op modelleren van therapeuten, taal, denken en gedrag en persoonlijke ontwikkeling.",
                            "tags": ["co-creator", "modelleren van therapeuten", "taal, denken en gedrag", "persoonlijke ontwikkeling"],
                        },
                        {
                            "title": "John Grinder",
                            "summary": "Linguistiek, modelleren, taalstructuren en communicatiepatronen.",
                            "tags": ["linguistiek", "modelleren", "taalstructuren", "communicatiepatronen"],
                        },
                    ],
                },
            ],
        },
        {
            "title": "Fundamenten van NLP",
            "summary": (
                "Definities, houding, grondbeginselen, major beliefs, zintuigen, "
                "cybernetica en leerprocessen."
            ),
            "resources": [
                {
                    "title": "Practitioner reader - fundamenten",
                    "resource_type": "reader",
                    "content": (
                        "Gebruik dit deel als verplichte basiskennis. Studenten "
                        "moeten de termen kennen en kunnen toepassen in korte cases."
                    ),
                    "sort_order": 1,
                },
                {
                    "title": "Slides - fundamenten van NLP",
                    "resource_type": "slides",
                    "content": (
                        "Samenvatting van de begrippen neuro, linguistisch, programmeren, "
                        "het speelveld, Miller, cybernetica en het vierstaps leerproces."
                    ),
                    "sort_order": 2,
                },
            ],
            "topics": MODULE1_TOPIC_BLUEPRINT,
        },
        {
            "title": "Wereldmodellen van NLP",
            "summary": "Structuur van betekenisgeving en abstractieniveaus.",
            "resources": [
                {
                    "title": "Reader - wereldmodellen",
                    "resource_type": "reader",
                    "content": (
                        "Gebruik deze module om taal, betekenisgeving en abstractie "
                        "in kaart te brengen. Laat studenten de koppeling maken tussen "
                        "observatie en interpretatie."
                    ),
                    "sort_order": 1,
                }
            ],
            "topics": MODULE2_TOPIC_BLUEPRINT,
        },
        {
            "title": "De kunst van magische taalpatronen",
            "summary": "Metamodel, taalverwerking en complexe equivalentie.",
            "resources": [
                {
                    "title": "Metamodel veldgids",
                    "resource_type": "reader",
                    "content": (
                        "Gebruik dit document om deleties, generalisaties en vervormingen "
                        "systematisch te herkennen in tekst en gesprek."
                    ),
                    "sort_order": 1,
                }
            ],
            "topics": [
                {
                    "title": "Taal en neurologie",
                    "summary": "Taalgeneratie, taalbegrip, interne dialoog en negatieven in taal.",
                    "concepts": [
                        {
                            "title": "Taalverwerking",
                            "summary": "Taalgeneratie, taalbegrip, interne dialoog en beslissingen.",
                            "tags": ["taalgeneratie", "taalbegrip", "interne dialoog", "beslissingen"],
                        },
                        {
                            "title": "Negatieven en taal",
                            "summary": "Interne representatie, focus en suggestie.",
                            "tags": ["interne representatie", "focus", "suggestie"],
                        },
                    ],
                },
                {
                    "title": "Complexe equivalentie",
                    "summary": "Betekenisgeving, logica, overtuigingen en verdiepingen.",
                    "concepts": [
                        {
                            "title": "Betekenisgeving",
                            "summary": "Koppelingen, logica, overtuigingen en cartesian logics.",
                            "tags": ["koppelingen", "logica", "overtuigingen", "cartesian logics"],
                        }
                    ],
                },
                {
                    "title": "Het metamodel",
                    "summary": "Verhelderen, specificeren en uitdagen van taal.",
                    "concepts": [
                        {
                            "title": "Doel",
                            "summary": "Verhelderen, specificeren en uitdagen.",
                            "tags": ["verhelderen", "specificeren", "uitdagen"],
                        },
                        {
                            "title": "Functies",
                            "summary": "Vragen, prioriteiten, taalpatronen en interventie.",
                            "tags": ["vragen", "prioriteiten", "taalpatronen", "interventie"],
                        },
                        {
                            "title": "Valkuilen",
                            "summary": "Te veel aannames, onethisch gebruik en onjuiste interpretatie.",
                            "tags": ["te veel aannames", "onethisch gebruik", "onjuiste interpretatie"],
                        },
                        {
                            "title": "Patronen",
                            "summary": "Deleties, generalisaties, vervormingen, universal quantifiers, referential index en nominalisaties.",
                            "tags": ["deleties", "generalisaties", "vervormingen", "universal quantifiers", "referential index", "nominalisaties"],
                        },
                    ],
                },
            ],
            "topics": MODULE3_TOPIC_BLUEPRINT,            
        },
        {
            "title": "De verborgen wereld van metaforen",
            "summary": "Indirecte communicatie en betekenis via metaforen.",
            "resources": [
                {
                    "title": "Metaforen reader",
                    "resource_type": "reader",
                    "content": "Metaforen kunnen verandering faciliteren zonder frontale weerstand op te roepen.",
                    "sort_order": 1,
                }
            ],
            "topics": MODULE4_TOPIC_BLUEPRINT,         
        },
        {
            "title": "De transformatie van droom naar outcome",
            "summary": "Doelen formuleren en ecologisch naar resultaat bewegen.",
            "resources": [
                {
                    "title": "Outcome frame worksheet",
                    "resource_type": "worksheet",
                    "content": "Laat studenten dromen vertalen naar een ecologisch en zintuiglijk specifiek outcome.",
                    "sort_order": 1,
                }
            ],
            "topics": MODULE5_TOPIC_BLUEPRINT,         
        },
        {
            "title": "De ontdekking van het zelf",
            "summary": "Zelfonderzoek, identiteit en voorwaarden voor veiligheid en groei.",
            "resources": [
                {
                    "title": "Reflectieblad identiteit",
                    "resource_type": "worksheet",
                    "content": "Gebruik dit blad om persoonlijke veiligheid, zelfbeeld en ontwikkelruimte te onderzoeken.",
                    "sort_order": 1,
                },
            ],
            "topics": MODULE6_TOPIC_BLUEPRINT,         
        },
        {
            "title": "De kracht van excellente communicatie",
            "summary": "Rapport, luisteren, afstemmen en feedbackvaardigheden.",
            "resources": [
                {
                    "title": "Communicatie praktijkreader",
                    "resource_type": "reader",
                    "content": "Oefen pacing, testing, leading en verschillende vormen van feedback.",
                    "sort_order": 1,
                },
            ],
            "topics": MODULE7_TOPIC_BLUEPRINT,         
        },
        {
            "title": "Emoties en states",
            "summary": "State management, regulatie en emotionele schakeling.",
            "resources": [
                {
                    "title": "States practice note",
                    "resource_type": "reader",
                    "content": "Observeer hoe states gedrag, interpretatie en toegang tot hulpbronnen beinvloeden.",
                    "sort_order": 1,
                }
            ],
            "topics": MODULE8_TOPIC_BLUEPRINT,         
        },
        {
            "title": "NLP technieken",
            "summary": "Perceptuele posities, submodaliteiten en eye accessing cues.",
            "resources": [
                {
                    "title": "Technieken overzicht",
                    "resource_type": "slides",
                    "content": "Een kort overzicht van de meest gebruikte NLP technieken in het practitioner domein.",
                    "sort_order": 1,
                }
            ],
            "topics": MODULE9_TOPIC_BLUEPRINT,         
        },
        {
            "title": "Strategieën ontcijferen",
            "summary": "TOTE, eliciteren en installeren van strategieen.",
            "resources": [
                {
                    "title": "Strategie analyse blad",
                    "resource_type": "worksheet",
                    "content": "Leg per situatie de zintuiglijke sequentie en het TOTE-patroon vast.",
                    "sort_order": 1,
                }
            ],
            "topics": MODULE10_TOPIC_BLUEPRINT,         
        },
        {
            "title": "Ankeren",
            "summary": "Conditionering, associatie en contextverandering.",
            "resources": [
                {
                    "title": "Ankers in de praktijk",
                    "resource_type": "reader",
                    "content": "Verbind klassieke conditionering aan NLP ankerwerk en contextwissels.",
                    "sort_order": 1,
                }
            ],
            "topics": MODULE11_TOPIC_BLUEPRINT,         
        },
        {
            "title": "Interventies",
            "summary": "Verandermodel van NLP en belangrijke interventies.",
            "resources": [
                {
                    "title": "Interventiekaart",
                    "resource_type": "reader",
                    "content": "Gebruik dit overzicht om interventies te kiezen op basis van doel, context en ecologie.",
                    "sort_order": 1,
                },
            ],
            "topics": MODULE12_TOPIC_BLUEPRINT,         
        },
        {
            "title": "NLP en spiritualiteit",
            "summary": "Spirituele principes en persoonlijk leiderschap.",
            "resources": [
                {
                    "title": "Spiritueel NLP samenvatting",
                    "resource_type": "reader",
                    "content": "De taal van eigenwaarde, aannames vermijden en niets persoonlijk nemen.",
                    "sort_order": 1,
                },
            ],
            "topics": MODULE13_TOPIC_BLUEPRINT,         
        },
    ]
}

SEED_EXERCISES = build_module0_exercises() + build_module1_exercises() + build_module2_exercises() + build_module3_exercises() + build_module4_exercises() + build_module5_exercises() + build_module6_exercises() + build_module7_exercises() + build_module8_exercises() + build_module9_exercises() + build_module10_exercises() + build_module11_exercises() + build_module12_exercises() + build_module13_exercises() + [
    {
        "title": "G6-model koppeloefening",
        "exercise_type": "match_pairs",
        "mode_support": "learn",
        "difficulty": "core",
        "module_title": "Wereldmodellen van NLP",
        "topic_title": "Het G6 model/de G4 theorie",
        "concept_title": "De 4G theorie",
        "instructions": "Koppel elk element aan de juiste omschrijving.",
        "prompt": "Kun je de lagen van het G6-model herkennen?",
        "content": {
            "pairs": [
                {"left": "Gebeurtenis", "options": ["Wat er feitelijk gebeurt", "De emotionele respons op de betekenis"]},
                {"left": "Geloof", "options": ["Dieper oordeel of overtuiging achter de interpretatie", "Een directe zintuiglijke observatie"]},
                {"left": "Gedrag", "options": ["Zichtbare respons of actie", "De gedachte die voor het gevoel komt"]},
            ],
            "model_answer": "Gebeurtenis = feitelijk; Geloof = diepere overtuiging; Gedrag = zichtbare respons.",
        },
        "scoring": {
            "correct_matches": {
                "Gebeurtenis": "Wat er feitelijk gebeurt",
                "Geloof": "Dieper oordeel of overtuiging achter de interpretatie",
                "Gedrag": "Zichtbare respons of actie",
            }
        },
        "max_score": 100,
        "requires_manual_review": False,
    },
    {
        "title": "Metamodel patroon herkennen",
        "exercise_type": "text_analysis",
        "mode_support": "learn,exam",
        "difficulty": "core",
        "module_title": "De kunst van magische taalpatronen",
        "topic_title": "Het metamodel",
        "concept_title": "Patronen",
        "instructions": "Lees het fragment, kies het patroon en formuleer daarna een passende metamodel-vraag.",
        "prompt": "Analyseer een zin op taalpatroon en interventie.",
        "content": {
            "text": "Niemand luistert ooit echt naar mij.",
            "pattern_question": "Welk patroon is hier het meest dominant?",
            "options": [
                {"value": "a", "label": "Universal quantifier"},
                {"value": "b", "label": "Nominalisatie"},
                {"value": "c", "label": "Lost performative"},
                {"value": "d", "label": "Mind read"},
            ],
            "follow_up_prompt": "Welke vraag zou je als trainer kunnen stellen om de uitspraak te specificeren?",
            "model_answer": (
                "Het patroon is een universal quantifier. Een passende vraag is bijvoorbeeld: "
                "'Niemand? Echt helemaal niemand?' of 'Wie luistert er precies niet naar je?'"
            ),
        },
        "scoring": {
            "correct_option": "a",
            "follow_up_keywords": ["wie", "niemand", "precies", "helemaal"],
            "threshold": 0.5,
        },
        "max_score": 100,
        "requires_manual_review": False,
    },
    {
        "title": "Metamodel vraag formuleren",
        "exercise_type": "short_answer",
        "mode_support": "learn,exam",
        "difficulty": "core",
        "module_title": "De kunst van magische taalpatronen",
        "topic_title": "Het metamodel",
        "concept_title": "Functies",
        "instructions": "Schrijf een concrete vraag die meer specificatie oproept.",
        "prompt": "Je hoort de uitspraak: 'Dat is gewoon niet professioneel.' Welke metamodel-vraag past het best?",
        "content": {
            "question": "Formuleer een metamodel-vraag die deze uitspraak specificeert.",
            "placeholder": "Bijvoorbeeld een vraag die naar bron, criteria of betekenis vraagt...",
            "model_answer": "Volgens wie is dat niet professioneel? Waaraan merk je dat precies?",
        },
        "scoring": {
            "keywords": ["volgens wie", "waaraan merk", "precies", "professioneel"],
            "threshold": 0.4,
        },
        "max_score": 100,
        "requires_manual_review": False,
    },
    {
        "title": "Outcome frame voorwaarden",
        "exercise_type": "multi_select",
        "mode_support": "learn,exam",
        "difficulty": "core",
        "module_title": "De transformatie van droom naar outcome",
        "topic_title": "Outcome frame",
        "concept_title": "Vormvoorwaarden",
        "instructions": "Selecteer alle elementen die in een sterk outcome frame horen.",
        "prompt": "Welke elementen horen bij een goed geformuleerd outcome?",
        "content": {
            "question": "Selecteer alle juiste vormvoorwaarden.",
            "options": [
                {"value": "a", "label": "Positief geformuleerd"},
                {"value": "b", "label": "Volledig afhankelijk van anderen"},
                {"value": "c", "label": "Zintuiglijk specifiek"},
                {"value": "d", "label": "Ecologisch"},
            ],
            "model_answer": "Een sterk outcome frame is positief, eigen-beinvloedbaar, zintuiglijk specifiek en ecologisch.",
        },
        "scoring": {"correct_options": ["a", "c", "d"]},
        "max_score": 100,
        "requires_manual_review": False,
    },
    {
        "title": "Rapport case review",
        "exercise_type": "case_review",
        "mode_support": "learn,exam",
        "difficulty": "advanced",
        "module_title": "De kracht van excellente communicatie",
        "topic_title": "Rapport",
        "concept_title": "Proces",
        "instructions": "Analyseer de case en beschrijf hoe jij pacing, testing en leading zou inzetten.",
        "prompt": "Een deelnemer antwoordt kort, kijkt weg en zakt achterover zodra jij over een gevoelig onderwerp begint.",
        "content": {
            "case": (
                "Je merkt dat het contact afneemt zodra het gesprek persoonlijker wordt. "
                "Beschrijf wat je eerst zou doen om rapport te herstellen en hoe je daarna "
                "een volgende stap zou zetten zonder te pushen."
            ),
            "guidance_points": [
                "Noem pacing of afstemmen op tempo, houding of taal.",
                "Noem een testmoment om te checken of rapport hersteld is.",
                "Beschrijf pas daarna een vorm van leading.",
            ],
            "model_answer": (
                "Een sterk antwoord benoemt eerst pacing op non-verbaal en verbaal niveau, "
                "daarna een test of de afstemming werkt, en pas daarna een zachte leading."
            ),
        },
        "scoring": {"rubric_points": ["pacing", "testen", "leading"]},
        "max_score": 100,
        "requires_manual_review": True,
    },
    {
        "title": "State reflectie",
        "exercise_type": "reflection",
        "mode_support": "learn",
        "difficulty": "core",
        "module_title": "Emoties en states",
        "topic_title": "Emoties en toestanden",
        "concept_title": "Kern",
        "instructions": "Reflecteer kort maar concreet op je eigen observaties.",
        "prompt": "Beschrijf een recente situatie waarin jouw state jouw communicatie positief of negatief heeft beinvloed.",
        "content": {
            "question": "Wat gebeurde er, wat veranderde in jouw state en wat zou je de volgende keer anders doen?",
            "placeholder": "Beschrijf situatie, state, effect en alternatief...",
            "model_answer": "Een sterk antwoord beschrijft situatie, state, gedragseffect en een bewuste interventie voor de volgende keer.",
        },
        "scoring": {},
        "max_score": 100,
        "requires_manual_review": True,
    },
    {
        "title": "Eye accessing cues basischeck",
        "exercise_type": "multiple_choice",
        "mode_support": "learn,exam",
        "difficulty": "core",
        "module_title": "NLP technieken",
        "topic_title": "Technieken",
        "concept_title": "Eye Accessing Cues",
        "instructions": "Kies het beste antwoord.",
        "prompt": "Wat is een veilige manier om met eye accessing cues om te gaan?",
        "content": {
            "question": "Welke uitspraak is het meest passend?",
            "options": [
                {"value": "a", "label": "Oogbewegingen geven altijd onfeilbaar aan of iemand liegt."},
                {"value": "b", "label": "Eye accessing cues zijn contextgevoelig en moeten voorzichtig worden geinterpreteerd."},
                {"value": "c", "label": "Iedereen heeft exact hetzelfde patroon."},
                {"value": "d", "label": "Ze vervangen calibreren en doorvragen."},
            ],
            "model_answer": "Eye accessing cues zijn hypothesevormend, niet absoluut. Observeer voorzichtig en koppel ze aan context en calibratie.",
        },
        "scoring": {"correct_option": "b"},
        "max_score": 100,
        "requires_manual_review": False,
    },
    {
        "title": "Anker uitleg in eigen woorden",
        "exercise_type": "short_answer",
        "mode_support": "learn,exam",
        "difficulty": "core",
        "module_title": "Ankeren",
        "topic_title": "Conditionering en associatie",
        "concept_title": "Ankeren",
        "instructions": "Beschrijf het mechanisme van ankeren kort en praktisch.",
        "prompt": "Wat is ankeren binnen NLP?",
        "content": {
            "question": "Leg uit wat een anker is en hoe het werkt.",
            "placeholder": "Denk aan stimulus, respons, state en trigger...",
            "model_answer": (
                "Een anker is een gekoppelde trigger die een bepaalde state of respons oproept. "
                "Door een stimulus consequent te verbinden aan een state kan de state later sneller "
                "worden opgeroepen."
            ),
        },
        "scoring": {
            "keywords": ["trigger", "state", "stimulus", "respons", "oproepen"],
            "threshold": 0.4,
        },
        "max_score": 100,
        "requires_manual_review": False,
    },
    {
        "title": "Interventiekeuze bij beperkte hulpbronnen",
        "exercise_type": "multiple_choice",
        "mode_support": "learn,exam",
        "difficulty": "advanced",
        "module_title": "Interventies",
        "topic_title": "Belangrijke interventies",
        "concept_title": "Technieken",
        "instructions": "Kies de meest passende interventierichting op basis van de casus.",
        "prompt": "Een client kan zich wel een gewenst gedrag voorstellen, maar komt telkens terug in een oud automatisch beeld. Welke techniek past het best als eerste verkenning?",
        "content": {
            "question": "Welke techniek ligt hier het meest voor de hand?",
            "options": [
                {"value": "a", "label": "Swish pattern"},
                {"value": "b", "label": "Familiestamboom"},
                {"value": "c", "label": "Backtrack mismatch"},
                {"value": "d", "label": "Magical number seven"},
            ],
            "model_answer": "Swish pattern ligt voor de hand wanneer iemand een automatische representatie wil vervangen door een nieuw gewenst patroon.",
        },
        "scoring": {"correct_option": "a"},
        "max_score": 100,
        "requires_manual_review": False,
    },
]


DEMO_ASSIGNMENTS = [
    {
        "title": "Week 1 - Fundamenten en zintuigen",
        "description": "Instapopdracht rond de basis van NLP, major beliefs en zintuiglijke predikaten.",
        "mode": "learn",
        "due_in_days": 7,
        "created_by_email": "trainer@neuroflow.local",
        "target_emails": ["student@neuroflow.local", "student2@neuroflow.local"],
        "exercise_titles": [
            "Fundamenten van NLP - hoofdstukkoppen",
            "Fundamenten van NLP - NLP staat voor termen",
            "Fundamenten van NLP - Overzicht van de Nine Major Beliefs termen",
            "Fundamenten van NLP - Auditief termen",
        ],
    },
    {
        "title": "Week 2 - Wereldmodellen en taal",
        "description": "Oefenset voor cybernetica, wereldmodellen en metamodeldenken.",
        "mode": "learn",
        "due_in_days": 14,
        "created_by_email": "trainer@neuroflow.local",
        "target_emails": ["student@neuroflow.local", "student2@neuroflow.local"],
        "exercise_titles": [
            "Fundamenten van NLP - Benodigde variatie termen",
            "G6-model koppeloefening",
            "Metamodel patroon herkennen",
            "Metamodel vraag formuleren",
        ],
    },
    {
        "title": "Reflectie op state management",
        "description": "Persoonlijke reflectie ter voorbereiding op feedback van de trainer.",
        "mode": "learn",
        "due_in_days": 10,
        "created_by_email": "trainer@neuroflow.local",
        "target_emails": ["student@neuroflow.local"],
        "exercise_titles": ["State reflectie"],
    },
]


DEMO_ATTEMPTS = [
    {
        "student_email": "student@neuroflow.local",
        "assignment_title": "Week 1 - Fundamenten en zintuigen",
        "exercise_title": "Fundamenten van NLP - NLP staat voor termen",
        "response": {"selected": ["a", "b", "c", "d"]},
    },
    {
        "student_email": "student@neuroflow.local",
        "assignment_title": "Week 1 - Fundamenten en zintuigen",
        "exercise_title": "Fundamenten van NLP - Auditief termen",
        "response": {"selected": ["a", "b"]},
    },
    {
        "student_email": "student@neuroflow.local",
        "assignment_title": "Reflectie op state management",
        "exercise_title": "State reflectie",
        "response": {
            "answer": (
                "Tijdens een lastig gesprek met een collega merkte ik dat mijn state "
                "naar irritatie schoof. Daardoor werd mijn toon scherper en luisterde ik "
                "minder goed. De volgende keer wil ik eerder ademen en mijn intentie checken."
            )
        },
    },
]
