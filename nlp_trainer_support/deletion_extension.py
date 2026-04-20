from __future__ import annotations

from urllib.parse import quote

from .web import Response, WebApp, h

_PATCHED = False

_HISTORY_OF_NLP_LAYOUT = {
    "outcomes_heading": "Na dit leerpad kun je",
    "outcomes": [
        "uitleggen welke denkers en stromingen aan de basis van NLP liggen",
        "de belangrijkste voorlopers van NLP herkennen",
        "de drie grondleggers van NLP benoemen",
        "per persoon de belangrijkste concepten koppelen aan de juiste naam",
        "begrijpen hoe thema's als taal, communicatie, therapie en verandering samenkomen in de ontstaansgeschiedenis van NLP",
    ],
    "sections": [
        {
            "title": "Pre-NLP",
            "summary": "Voorlopers die de denkrichting van NLP sterk hebben beinvloed.",
            "people": [
                {
                    "name": "Virginia Satir",
                    "image_filename": "virginia_satir_picture.jpg",
                    "points": [
                        "Gezinstherapie",
                        "Communicatiecategorieen",
                        "Communicatie en relaties",
                        "Familiestamboom",
                    ],
                },
                {
                    "name": "Milton Erickson",
                    "image_filename": "milton_erickson.jpg",
                    "points": [
                        "Hypnotherapie",
                        "Indirecte suggestie",
                        "Metaforen en verhalen",
                        "Taalgebruik",
                    ],
                },
                {
                    "name": "Fritz Perls",
                    "image_filename": "fritz_perls.jpg",
                    "points": [
                        "Gestalttherapie",
                        "Hier-en-nu",
                        "Zelfbewustzijn",
                        "Verantwoordelijkheid",
                    ],
                },
            ],
        },
        {
            "title": "Grondleggers van NLP",
            "summary": "De grondleggers van NLP en hun inhoudelijke accenten.",
            "people": [
                {
                    "name": "Frank Pucelik",
                    "image_filename": "frank_pucelik.jpg",
                    "points": [
                        "Co-grondlegger",
                        "NLP-model",
                        "Menselijke ervaring",
                        "Beperkende overtuigingen en potentieel",
                    ],
                },
                {
                    "name": "Richard Bandler",
                    "image_filename": "richard_bandler.jpg",
                    "points": [
                        "Co-creator",
                        "Modelleren van therapeuten",
                        "Taal, denken en gedrag",
                        "Persoonlijke ontwikkeling",
                    ],
                },
                {
                    "name": "John Grinder",
                    "image_filename": "john_grinder.jpg",
                    "points": [
                        "Linguistiek",
                        "Modelleren",
                        "Taalstructuren",
                        "Communicatiepatronen",
                    ],
                },
            ],
        },
    ],
}

_FOUNDATIONS_OF_NLP_LAYOUT = {
    "outcomes_heading": "Na dit leerpad kun je",
    "outcomes": [
        "uitleggen wat NLP is en waar het voor staat",
        "beschrijven hoe NLP is ontstaan en waarom modelleren daarin centraal staat",
        "onderscheiden hoe NLP wordt gepositioneerd als attitude, methodologie, technologie en communicatie-instrument",
        "herkennen hoe trainers en het vakgebied binnen deze leeromgeving worden neergezet",
        "uitleggen hoe het NLP-speelveld werkt, inclusief rollen, feedback en basisregels",
        "de wetten van George Miller koppelen aan informatieverwerking en communicatie",
        "de Nine Major Beliefs en basisaannamen van klassiek NLP benoemen en uitleggen",
        "uitleggen hoe zintuigen, modaliteiten en representatiesystemen werken binnen NLP",
        "beschrijven wat de wet van cybernetica en benodigde variatie betekent voor communicatie en verandering",
    ],
    "sections": [
        {
            "title": "Wat is NLP / NLP staat voor / Over NLP",
            "summary": "De basisdefinities, oorsprong en positionering van NLP.",
            "image_filename": "",
            "groups": [
                {
                    "heading": "Wat is NLP",
                    "points": [
                        "Definitie van NLP",
                        "Ontstaan van NLP",
                        "Modelleren",
                        "Structuur van subjectieve ervaring",
                    ],
                },
                {
                    "heading": "NLP staat voor",
                    "points": [
                        "Neuro",
                        "Linguistisch",
                        "Programmeren",
                        "Van wens naar resultaat",
                    ],
                },
                {
                    "heading": "Over NLP",
                    "points": [
                        "NLP als attitude",
                        "NLP als methodologie",
                        "NLP als technologie",
                        "NLP als holistisch communicatie-instrument",
                        "Toepassingsgebieden van NLP",
                    ],
                },
            ],
        },
        {
            "title": "Trainers en positionering van NLP",
            "summary": "De trainers binnen deze leeromgeving, het NLP-speelveld en de bredere plaats van NLP in deze tijd.",
            "image_filename": "rob_en_caroline.png",
            "groups": [
                {
                    "heading": "Rob Kamps",
                    "points": [
                        "Opleiding en ervaring",
                        "NLP-certificeringen",
                        "Trainingsstijl",
                    ],
                },
                {
                    "heading": "Caroline Kamps",
                    "points": [
                        "Wetenschappelijke achtergrond",
                        "Profiling en aanvullende specialisaties",
                        "NLP-certificeringen en trainerschap",
                    ],
                },
                {
                    "heading": "NLP anno nu",
                    "points": [
                        "Ontwikkeling van NLP",
                        "Eenzijdig beeld van NLP",
                        "Brede toepasbaarheid",
                    ],
                },
                {
                    "heading": "Spelend leren",
                    "points": [
                        "Oefenomgeving",
                        "Feedback",
                    ],
                },
                {
                    "heading": "Rollen in de oefening",
                    "points": [
                        "Subject",
                        "Programmer",
                        "Meta",
                    ],
                },
                {
                    "heading": "Basisregels in oefeningen",
                    "points": [
                        "Rapport",
                        "Kalibreren",
                        "Ecologie",
                    ],
                },
            ],
        },
        {
            "title": "Fundament 1: De wetten van Miller",
            "summary": "Uitgangspunten over informatieverwerking, geheugen en communicatie.",
            "image_filename": "george_miller.jpg",
            "groups": [
                {
                    "heading": "De eerste wet van George Miller",
                    "points": [
                        "Magical Number Seven",
                        "Chunking",
                    ],
                },
                {
                    "heading": "De tweede wet van George Miller",
                    "points": [
                        "Waarheidsaanname",
                        "Empathische communicatie",
                        "Praktische toepasbaarheid",
                    ],
                },
            ],
        },
        {
            "title": "Fundament 2: Nine Major Beliefs",
            "summary": "De belangrijkste overtuigingen die richting geven aan hoe NLP naar menselijk gedrag en verandering kijkt.",
            "image_filename": "map.jpg",
            "groups": [
                {
                    "heading": "Overzicht van de Nine Major Beliefs",
                    "points": [
                        "De kaart is niet het gebied",
                        "Respect / positieve intentie",
                        "Schoonheid zit in verschillen",
                        "Communicatie is beinvloeding",
                        "Weerstand is kracht",
                        "50/50-regel",
                        "Vertrouw je onbewuste",
                        "Het recht om te leren",
                        "Jij bent de belangrijkste persoon in je leven",
                    ],
                },
                {
                    "heading": "Soorten aannamen binnen NLP",
                    "points": [
                        "Basisaannamen",
                        "Vooronderstellingen",
                        "Meta-programma's",
                        "Identiteitsaannamen",
                        "Overtuigingen",
                    ],
                },
                {
                    "heading": "Basisaannamen van klassiek NLP",
                    "points": [
                        "Uniek wereldmodel",
                        "Proces belangrijker dan inhoud",
                        "Betekenisgeving",
                        "Respons op communicatie",
                        "Falen bestaat niet",
                        "Hulpbronnen",
                        "Positieve intentie",
                        "Meerdere keuzes",
                        "Ervaring heeft structuur",
                    ],
                },
                {
                    "heading": "Koppeling major beliefs en basisaannamen",
                    "points": [
                        "Filosofisch fundament en praktische toepassing",
                    ],
                },
            ],
        },
        {
            "title": "Fundament 3: Zintuigen",
            "summary": "Hoe mensen informatie via zintuigen waarnemen, representeren en gebruiken in communicatie.",
            "image_filename": "zintuigen.jpg",
            "groups": [
                {
                    "heading": "Modaliteiten",
                    "points": [
                        "Zintuigen als modaliteiten",
                        "Primair representatiesysteem",
                    ],
                },
                {
                    "heading": "Visueel",
                    "points": [
                        "Visuele voorkeur",
                        "Visuele predikaten",
                    ],
                },
                {
                    "heading": "Kinesthetisch",
                    "points": [
                        "Kinesthetische voorkeur",
                        "Kinesthetische predikaten",
                    ],
                },
                {
                    "heading": "Digitaal",
                    "points": [
                        "Digitaal als verwerkingssysteem",
                        "Digitale predikaten",
                    ],
                },
                {
                    "heading": "Auditief",
                    "points": [
                        "Auditieve voorkeur",
                        "Auditieve predikaten",
                    ],
                },
                {
                    "heading": "Geur en smaak",
                    "points": [
                        "Olfactorisch",
                        "Gustatorisch",
                    ],
                },
                {
                    "heading": "Zintuigen en functionaliteit / perceptie",
                    "points": [
                        "Rapport via modaliteiten",
                        "Rijkere innerlijke wereld",
                        "Perceptie en illusie",
                    ],
                },
            ],
        },
        {
            "title": "Fundament 4: Wet van Cybernetica",
            "summary": "Hoe flexibiliteit, variatie en keuzemogelijkheden invloed geven binnen systemen en communicatie.",
            "image_filename": "cybernetics.jpg",
            "groups": [
                {
                    "heading": "Benodigde variatie",
                    "points": [
                        "Wet van benodigde variatie",
                        "Macht en systeemverstoring",
                    ],
                },
                {
                    "heading": "Toepassingen van cybernetica in NLP en daarbuiten",
                    "points": [
                        "Toepassingen in praktijkvelden",
                        "Toepassing binnen NLP",
                    ],
                },
            ],
        },
    ],
}

_MODULE_STORY_LAYOUTS = {
    "De geschiedenis van NLP": ("people", _HISTORY_OF_NLP_LAYOUT),
    "Fundamenten van NLP": ("cards", _FOUNDATIONS_OF_NLP_LAYOUT),
}


def _sorted_archive_rows(rows):
    return sorted(
        rows,
        key=lambda row: ((row["archive_date"] or row["created_at"] or ""), int(row["id"] or 0)),
        reverse=True,
    )


def _archive_page(self: WebApp, connection, context: dict):
    active = context["active_membership"]
    if not active:
        return self.forbidden(context)

    if active["role"] in {"trainer", "organization_admin"}:
        assignments = connection.execute(
            """
            SELECT assignments.id, assignments.title, assignments.mode, assignments.created_at,
                   (
                       SELECT COUNT(*) FROM assignment_items WHERE assignment_id = assignments.id
                   ) AS item_count,
                   (
                       SELECT COUNT(*) FROM assignment_targets WHERE assignment_id = assignments.id
                   ) AS target_count,
                   (
                       SELECT COUNT(*)
                       FROM (
                           SELECT DISTINCT attempts.user_id, attempts.exercise_id
                           FROM attempts
                           WHERE attempts.assignment_id = assignments.id
                             AND attempts.status IN ('reviewed', 'scored')
                       ) completed_attempt_pairs
                   ) AS completed_pairs,
                   (
                       SELECT COUNT(*)
                       FROM attempts
                       WHERE attempts.assignment_id = assignments.id
                         AND attempts.status = 'submitted'
                   ) AS pending_reviews,
                   (
                       SELECT MAX(COALESCE(reviews.reviewed_at, attempts.submitted_at))
                       FROM attempts
                       LEFT JOIN reviews ON reviews.attempt_id = attempts.id
                       WHERE attempts.assignment_id = assignments.id
                   ) AS archive_date
            FROM assignments
            WHERE assignments.organization_id = ?
            """,
            (active["organization_id"],),
        ).fetchall()

        group_rows = connection.execute(
            """
            SELECT assignment_target_groups.assignment_id, student_groups.name
            FROM assignment_target_groups
            JOIN student_groups ON student_groups.id = assignment_target_groups.group_id
            JOIN assignments ON assignments.id = assignment_target_groups.assignment_id
            WHERE assignments.organization_id = ?
            ORDER BY student_groups.name
            """,
            (active["organization_id"],),
        ).fetchall()
        group_names_by_assignment: dict[int, list[str]] = {}
        for row in group_rows:
            assignment_id = int(row["assignment_id"])
            group_names_by_assignment.setdefault(assignment_id, [])
            name = row["name"]
            if name and name not in group_names_by_assignment[assignment_id]:
                group_names_by_assignment[assignment_id].append(name)

        archived = [
            row
            for row in _sorted_archive_rows(assignments)
            if int(row["item_count"] or 0) > 0
            and int(row["target_count"] or 0) > 0
            and int(row["pending_reviews"] or 0) == 0
            and int(row["completed_pairs"] or 0) >= int(row["item_count"]) * int(row["target_count"])
        ]
        exam_rows = [
            [
                f"<a href='/assignments/{row['id']}'>{h(row['title'])}</a>",
                h(", ".join(group_names_by_assignment.get(int(row["id"]), [])) or "Geen groep gekoppeld"),
                h((row["archive_date"] or row["created_at"]).split("T")[0]),
            ]
            for row in archived
            if (row["mode"] or "").lower() == "exam"
        ]
        learn_rows = [
            [
                f"<a href='/assignments/{row['id']}'>{h(row['title'])}</a>",
                h(", ".join(group_names_by_assignment.get(int(row["id"]), [])) or "Geen groep gekoppeld"),
                h((row["archive_date"] or row["created_at"]).split("T")[0]),
            ]
            for row in archived
            if (row["mode"] or "").lower() != "exam"
        ]
        body = [
            "<section class='hero compact'><div><span class='eyebrow'>Archief</span><h1>Opdrachtarchief</h1><p>Bekijk afgeronde en beoordeelde opdrachten per groep en per type.</p></div></section>",
            "<section class='grid two-up'>"
            + "<article class='panel'><h2>Examenopdrachten</h2>"
            + self.render_table(["Opdracht", "Groep", "Datum"], exam_rows)
            + "</article>"
            + "<article class='panel inset'><h2>Oefenopdrachten</h2>"
            + self.render_table(["Opdracht", "Groep", "Datum"], learn_rows)
            + "</article></section>",
        ]
        return self.html("Archief", "".join(body), context)

    user_id = context["user"]["user_id"]
    assignments = connection.execute(
        """
        SELECT assignments.id, assignments.title, assignments.mode, assignments.created_at,
               (
                   SELECT COUNT(*) FROM assignment_items WHERE assignment_id = assignments.id
               ) AS item_count,
               (
                   SELECT COUNT(DISTINCT attempts.exercise_id)
                   FROM attempts
                   WHERE attempts.assignment_id = assignments.id
                     AND attempts.user_id = ?
                     AND attempts.status IN ('reviewed', 'scored')
               ) AS completed_items,
               (
                   SELECT COUNT(*)
                   FROM attempts
                   WHERE attempts.assignment_id = assignments.id
                     AND attempts.user_id = ?
                     AND attempts.status = 'submitted'
               ) AS pending_reviews,
               (
                   SELECT MAX(COALESCE(reviews.reviewed_at, attempts.submitted_at))
                   FROM attempts
                   LEFT JOIN reviews ON reviews.attempt_id = attempts.id
                   WHERE attempts.assignment_id = assignments.id
                     AND attempts.user_id = ?
               ) AS archive_date
        FROM assignments
        JOIN assignment_targets ON assignment_targets.assignment_id = assignments.id
        WHERE assignment_targets.target_user_id = ?
          AND assignments.organization_id = ?
        """,
        (user_id, user_id, user_id, user_id, active["organization_id"]),
    ).fetchall()

    archived = [
        row
        for row in _sorted_archive_rows(assignments)
        if int(row["item_count"] or 0) > 0
        and int(row["pending_reviews"] or 0) == 0
        and int(row["completed_items"] or 0) >= int(row["item_count"])
    ]
    exam_rows = [
        [
            f"<a href='/assignments/{row['id']}'>{h(row['title'])}</a>",
            h((row["archive_date"] or row["created_at"]).split("T")[0]),
        ]
        for row in archived
        if (row["mode"] or "").lower() == "exam"
    ]
    learn_rows = [
        [
            f"<a href='/assignments/{row['id']}'>{h(row['title'])}</a>",
            h((row["archive_date"] or row["created_at"]).split("T")[0]),
        ]
        for row in archived
        if (row["mode"] or "").lower() != "exam"
    ]
    body = [
        "<section class='hero compact'><div><span class='eyebrow'>Archief</span><h1>Jouw archief</h1><p>Bekijk afgeronde opdrachten die volledig zijn beoordeeld.</p></div></section>",
        "<section class='grid two-up'>"
        + "<article class='panel'><h2>Examenopdrachten</h2>"
        + self.render_table(["Opdracht", "Datum"], exam_rows)
        + "</article>"
        + "<article class='panel inset'><h2>Oefenopdrachten</h2>"
        + self.render_table(["Opdracht", "Datum"], learn_rows)
        + "</article></section>",
    ]
    return self.html("Archief", "".join(body), context)


def _extract_section(body: str, marker: str):
    start = body.find(marker)
    if start == -1:
        return None
    end = body.find("</section>", start)
    if end == -1:
        return None
    end += len("</section>")
    return start, end, body[start:end]


def _pathway_story_style_block() -> str:
    return """
    <style>
      .pathway-learning-panel {
        background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(236,244,246,0.9));
      }
      .pathway-learning-list {
        margin: 0;
        padding-left: 1.25rem;
        display: grid;
        gap: 0.65rem;
      }
      .pathway-content-section {
        overflow: hidden;
      }
      .pathway-section-header {
        margin-bottom: 1.1rem;
      }
      .pathway-figure-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
      }
      .pathway-figure-card {
        padding: 1rem;
        border-radius: 1rem;
        background: rgba(236, 244, 246, 0.8);
        border: 1px solid rgba(23, 48, 60, 0.08);
      }
      .pathway-figure-image {
        display: block;
        width: min(100%, 220px);
        aspect-ratio: 4 / 5;
        object-fit: cover;
        margin: 0 auto 0.9rem;
        border-radius: 0.9rem;
        border: 1px solid rgba(23,48,60,0.1);
        box-shadow: 0 16px 30px rgba(23,48,60,0.08);
        background: rgba(255,255,255,0.92);
      }
      .pathway-figure-card h3 {
        margin-bottom: 0.8rem;
      }
      .pathway-point-list {
        margin: 0;
        padding-left: 1.15rem;
        display: grid;
        gap: 0.5rem;
      }
      .pathway-story-grid {
        display: grid;
        grid-template-columns: minmax(240px, 300px) minmax(0, 1fr);
        gap: 1.2rem;
        align-items: start;
      }
      .pathway-story-image,
      .pathway-story-placeholder {
        display: block;
        width: 100%;
        max-width: 280px;
        aspect-ratio: 4 / 5;
        object-fit: cover;
        margin: 0 auto;
        border-radius: 1rem;
        border: 1px solid rgba(23,48,60,0.1);
        box-shadow: 0 16px 30px rgba(23,48,60,0.08);
        background: rgba(255,255,255,0.92);
      }
      .pathway-story-placeholder {
        display: grid;
        place-items: center;
        padding: 1rem;
        text-align: center;
        color: rgba(23,48,60,0.58);
        font-weight: 700;
      }
      .pathway-story-copy {
        display: grid;
        gap: 1rem;
      }
      .pathway-story-group {
        padding: 0.95rem 1rem;
        border-radius: 1rem;
        background: rgba(236,244,246,0.55);
        border: 1px solid rgba(23,48,60,0.06);
      }
      .pathway-story-group h3 {
        margin: 0 0 0.65rem;
        font-size: 1rem;
      }
      .pathway-story-sublist {
        margin: 0;
        padding-left: 1.15rem;
        display: grid;
        gap: 0.45rem;
      }
      @media (max-width: 900px) {
        .pathway-story-grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
    """


def _render_people_sections(layout: dict) -> str:
    blocks = [
        _pathway_story_style_block(),
        "<section class='panel pathway-learning-panel'>"
        f"<h2>{h(layout['outcomes_heading'])}</h2>"
        "<ul class='pathway-learning-list'>"
        + "".join(f"<li>{h(item)}</li>" for item in layout["outcomes"])
        + "</ul></section>",
    ]

    for section in layout["sections"]:
        cards = []
        for person in section["people"]:
            image_url = quote(f"/static/Model afbeeldingen/{person['image_filename']}", safe="/")
            cards.append(
                "<article class='pathway-figure-card'>"
                f"<img class='pathway-figure-image' src='{h(image_url)}' alt='{h(person['name'])}'>"
                f"<h3>{h(person['name'])}</h3>"
                "<ul class='pathway-point-list'>"
                + "".join(f"<li>{h(point)}</li>" for point in person["points"])
                + "</ul></article>"
            )
        blocks.append(
            "<section class='panel pathway-content-section'>"
            f"<div class='pathway-section-header'><h2>{h(section['title'])}</h2><p>{h(section['summary'])}</p></div>"
            "<div class='pathway-figure-grid'>"
            + "".join(cards)
            + "</div></section>"
        )
    return "".join(blocks)


def _render_card_sections(layout: dict) -> str:
    blocks = [
        _pathway_story_style_block(),
        "<section class='panel pathway-learning-panel'>"
        f"<h2>{h(layout['outcomes_heading'])}</h2>"
        "<ul class='pathway-learning-list'>"
        + "".join(f"<li>{h(item)}</li>" for item in layout["outcomes"])
        + "</ul></section>",
    ]

    for section in layout["sections"]:
        image_filename = (section.get("image_filename") or "").strip()
        if image_filename:
            image_block = (
                f"<img class='pathway-story-image' src='{h(quote(f'/static/Model afbeeldingen/{image_filename}', safe='/'))}' "
                f"alt='{h(section['title'])}'>"
            )
        else:
            image_block = "<div class='pathway-story-placeholder'>Afbeelding volgt later</div>"

        group_blocks = []
        for group in section["groups"]:
            group_blocks.append(
                "<article class='pathway-story-group'>"
                f"<h3>{h(group['heading'])}</h3>"
                "<ul class='pathway-story-sublist'>"
                + "".join(f"<li>{h(point)}</li>" for point in group["points"])
                + "</ul></article>"
            )

        blocks.append(
            "<section class='panel pathway-content-section'>"
            f"<div class='pathway-section-header'><h2>{h(section['title'])}</h2><p>{h(section['summary'])}</p></div>"
            "<div class='pathway-story-grid'>"
            f"<div>{image_block}</div>"
            "<div class='pathway-story-copy'>"
            + "".join(group_blocks)
            + "</div></div></section>"
        )
    return "".join(blocks)


def _module_story_sections(title: str) -> str | None:
    module_layout = _MODULE_STORY_LAYOUTS.get(title)
    if not module_layout:
        return None
    layout_type, layout = module_layout
    if layout_type == "people":
        return _render_people_sections(layout)
    if layout_type == "cards":
        return _render_card_sections(layout)
    return None


def _module_page(self: WebApp, connection, request, context: dict, module_id: int):
    response = _module_page.original(self, connection, request, context, module_id)
    body = response.body.decode("utf-8", errors="ignore")

    active_title = None
    for title in _MODULE_STORY_LAYOUTS:
        if f"<h1>{title}</h1>" in body:
            active_title = title
            break
    if not active_title:
        return response

    custom_sections = _module_story_sections(active_title)
    if not custom_sections:
        return response

    lesson = _extract_section(body, "<section class='panel'><h2>Lesmateriaal</h2>")
    topics = _extract_section(body, "<section class='panel'><h2>Onderwerpen en concepten</h2>")

    if lesson and topics:
        lesson_start, lesson_end, lesson_html = lesson
        topics_start, topics_end, _topics_html = topics
        start = min(lesson_start, topics_start)
        end = max(lesson_end, topics_end)
        body = body[:start] + custom_sections + lesson_html + body[end:]
    elif topics:
        topics_start, topics_end, _topics_html = topics
        body = body[:topics_start] + custom_sections + body[topics_end:]
    elif lesson:
        lesson_start, lesson_end, lesson_html = lesson
        body = body[:lesson_start] + custom_sections + lesson_html + body[lesson_end:]
    else:
        body = body.replace("</main>", custom_sections + "</main>", 1)

    return Response(response.status, body.encode("utf-8"), list(response.headers))


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    original_module_page = getattr(WebApp, "module_page", None)
    if original_module_page is not None:
        _module_page.original = original_module_page
        WebApp.module_page = _module_page

    WebApp.archive_page = _archive_page
    _PATCHED = True


apply()
