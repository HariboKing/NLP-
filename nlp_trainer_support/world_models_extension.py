from __future__ import annotations

from . import deletion_extension as story_module

_PATCHED = False

_WORLD_MODELS_LAYOUT = {
    "outcomes_heading": "Na dit leerpad kun je",
    "outcomes": [
        "uitleggen hoe gebeurtenissen, gedachten, gevoelens en gedrag met elkaar samenhangen binnen een wereldmodel",
        "beschrijven welke invloed Aaron T. Beck, Albert Ellis en REBT hebben op het denken over wereldmodellen",
        "uitleggen wat de 4G-theorie is en hoe irrationele overtuigingen daarin een rol spelen",
        "beschrijven wat het structureel differentiaal en de algemene semantiek bijdragen aan NLP",
        "uitleggen wat bedoeld wordt met de uitspraak de kaart is niet het gebied",
        "herkennen hoe taal, denken en ervaring samen een wereldmodel vormen",
        "beschrijven hoe filosofische stromingen zoals fenomenologie, constructivisme, postmodernisme en existentialisme aansluiten op NLP",
        "uitleggen waarom subjectieve interpretatie centraal staat in communicatie, verandering en persoonlijke verantwoordelijkheid",
    ],
    "sections": [
        {
            "title": "Het G6 model / de G4 theorie",
            "summary": "De relatie tussen gebeurtenis, gedachte, gevoel en gedrag als basis van wereldmodellen.",
            "image_filename": "g6-model_afbeelding.png",
            "groups": [
                {
                    "heading": "Oorsprong en ontwikkeling van het model",
                    "points": [
                        "Aaron T. Beck",
                        "Albert Ellis",
                        "REBT",
                    ],
                },
                {
                    "heading": "De 4G theorie",
                    "points": [
                        "Gebeurtenis",
                        "Geloof / gedachte",
                        "Gevoel / emotie",
                        "Gedrag",
                        "Irrationele overtuigingen",
                        "Verandering van denken",
                    ],
                },
            ],
        },
        {
            "title": "Het structureel differentiaal",
            "summary": "De basis van het onderscheid tussen werkelijkheid, waarneming en representatie.",
            "image_filename": "structureel-differentiaal_afbeelding.png",
            "groups": [
                {
                    "heading": "Alfred Korzybski",
                    "points": [
                        "Algemene semantiek",
                        "De kaart is niet het gebied",
                        "Werkelijkheid versus representatie",
                    ],
                },
            ],
        },
        {
            "title": "Algemene semantiek",
            "summary": "Hoe taal, denken en ervaring samen bepalen hoe mensen de werkelijkheid structureren.",
            "image_filename": "alfred_korzybski.jpg",
            "groups": [
                {
                    "heading": "Kern van algemene semantiek",
                    "points": [
                        "Taal",
                        "Denken",
                        "Ervaring",
                        "Structureren van ervaring",
                    ],
                },
                {
                    "heading": "Reflectie en communicatie",
                    "points": [
                        "Kritisch reflecteren",
                        "Communicatie verbeteren",
                        "Openere en inclusievere maatschappij",
                    ],
                },
                {
                    "heading": "Korzybski citaten en hun betekenis",
                    "points": [
                        "De kaart is niet het gebied",
                        "Niet de dingen zelf, maar onze ideeen erover",
                        "Onderscheidingen en verschillen",
                        "Woorden zijn symbolen",
                    ],
                },
            ],
        },
        {
            "title": "Filosofie en NLP",
            "summary": "De filosofische achtergronden die helpen om wereldmodellen, ervaring en verantwoordelijkheid te begrijpen.",
            "image_filename": "",
            "groups": [
                {
                    "heading": "Taal en betekenis",
                    "points": [
                        "Taal vormt realiteit",
                        "Wittgenstein",
                    ],
                },
                {
                    "heading": "Bewustzijn en ervaring",
                    "points": [
                        "Bewustzijn",
                        "Husserl / fenomenologie",
                        "Herstructureren van ervaring",
                    ],
                },
                {
                    "heading": "Constructie van realiteit",
                    "points": [
                        "Kaart van de werkelijkheid",
                        "Constructivisme",
                        "Subjectieve interpretatie",
                        "Postmodernisme",
                    ],
                },
                {
                    "heading": "Ethiek en verantwoordelijkheid",
                    "points": [
                        "Persoonlijke verantwoordelijkheid",
                        "Jean-Paul Sartre",
                        "Controle over eigen ervaring",
                    ],
                },
            ],
        },
    ],
}


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    story_module._MODULE_STORY_LAYOUTS["Wereldmodellen van NLP"] = ("cards", _WORLD_MODELS_LAYOUT)
    _PATCHED = True


apply()
