from __future__ import annotations

from urllib.parse import quote

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
            "image_filenames": [
                "structureel-differentiaal_afbeelding.png",
                "alfred_korzybski.jpg",
            ],
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
            "image_filename": "",
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


def _render_card_sections(layout: dict) -> str:
    blocks = [
        story_module._pathway_story_style_block(),
        """
        <style>
          .pathway-story-media-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            align-items: start;
          }
          .pathway-story-grid.pathway-story-grid-gallery {
            grid-template-columns: 1fr;
          }
          .pathway-story-grid.pathway-story-grid-gallery .pathway-story-image {
            max-width: none;
            width: 100%;
          }
        </style>
        """,
        "<section class='panel pathway-learning-panel'>"
        f"<h2>{story_module.h(layout['outcomes_heading'])}</h2>"
        "<ul class='pathway-learning-list'>"
        + "".join(f"<li>{story_module.h(item)}</li>" for item in layout["outcomes"])
        + "</ul></section>",
    ]

    for section in layout["sections"]:
        image_filenames = [
            filename.strip()
            for filename in section.get("image_filenames", [])
            if (filename or "").strip()
        ]
        if not image_filenames:
            fallback_image = (section.get("image_filename") or "").strip()
            if fallback_image:
                image_filenames = [fallback_image]

        if len(image_filenames) > 1:
            image_block = (
                "<div class='pathway-story-media-grid'>"
                + "".join(
                    f"<img class='pathway-story-image' src='{story_module.h(quote(f'/static/Model afbeeldingen/{filename}', safe='/'))}' alt='{story_module.h(section['title'])}'>"
                    for filename in image_filenames
                )
                + "</div>"
            )
            grid_class = "pathway-story-grid pathway-story-grid-gallery"
        elif len(image_filenames) == 1:
            filename = image_filenames[0]
            image_block = (
                f"<img class='pathway-story-image' src='{story_module.h(quote(f'/static/Model afbeeldingen/{filename}', safe='/'))}' "
                f"alt='{story_module.h(section['title'])}'>"
            )
            grid_class = "pathway-story-grid"
        else:
            image_block = "<div class='pathway-story-placeholder'>Afbeelding volgt later</div>"
            grid_class = "pathway-story-grid"

        group_blocks = []
        for group in section["groups"]:
            group_blocks.append(
                "<article class='pathway-story-group'>"
                f"<h3>{story_module.h(group['heading'])}</h3>"
                "<ul class='pathway-story-sublist'>"
                + "".join(f"<li>{story_module.h(point)}</li>" for point in group["points"])
                + "</ul></article>"
            )

        blocks.append(
            "<section class='panel pathway-content-section'>"
            f"<div class='pathway-section-header'><h2>{story_module.h(section['title'])}</h2><p>{story_module.h(section['summary'])}</p></div>"
            + f"<div class='{grid_class}'>"
            + f"<div>{image_block}</div>"
            + "<div class='pathway-story-copy'>"
            + "".join(group_blocks)
            + "</div></div></section>"
        )
    return "".join(blocks)


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    story_module._render_card_sections = _render_card_sections
    story_module._MODULE_STORY_LAYOUTS["Wereldmodellen van NLP"] = ("cards", _WORLD_MODELS_LAYOUT)
    _PATCHED = True


apply()
