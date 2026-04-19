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
                    "image_filename": "virginia_satir_picture.svg",
                    "points": [
                        "Gezinstherapie",
                        "Communicatiecategorieen",
                        "Communicatie en relaties",
                        "Familiestamboom",
                    ],
                },
                {
                    "name": "Milton Erickson",
                    "image_filename": "milton_erickson.svg",
                    "points": [
                        "Hypnotherapie",
                        "Indirecte suggestie",
                        "Metaforen en verhalen",
                        "Taalgebruik",
                    ],
                },
                {
                    "name": "Fritz Perls",
                    "image_filename": "fritz_perls.svg",
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
                    "image_filename": "pucelik.svg",
                    "points": [
                        "Co-grondlegger",
                        "NLP-model",
                        "Menselijke ervaring",
                        "Beperkende overtuigingen en potentieel",
                    ],
                },
                {
                    "name": "Richard Bandler",
                    "image_filename": "richard_bandler.svg",
                    "points": [
                        "Co-creator",
                        "Modelleren van therapeuten",
                        "Taal, denken en gedrag",
                        "Persoonlijke ontwikkeling",
                    ],
                },
                {
                    "name": "John Grinder",
                    "image_filename": "john_grinder.svg",
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



def _history_style_block() -> str:
    return """
    <style>
      .history-learning-panel {
        background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(236,244,246,0.9));
      }
      .history-learning-list {
        margin: 0;
        padding-left: 1.25rem;
        display: grid;
        gap: 0.65rem;
      }
      .history-content-section {
        overflow: hidden;
      }
      .history-section-header {
        margin-bottom: 1.1rem;
      }
      .history-figure-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
      }
      .history-figure-card {
        padding: 1rem;
        border-radius: 1rem;
        background: rgba(236, 244, 246, 0.8);
        border: 1px solid rgba(23, 48, 60, 0.08);
      }
      .history-figure-image {
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
      .history-figure-card h3 {
        margin-bottom: 0.8rem;
      }
      .history-point-list {
        margin: 0;
        padding-left: 1.15rem;
        display: grid;
        gap: 0.5rem;
      }
    </style>
    """



def _render_history_module_sections() -> str:
    layout = _HISTORY_OF_NLP_LAYOUT
    blocks = [
        _history_style_block(),
        "<section class='panel history-learning-panel'>"
        f"<h2>{h(layout['outcomes_heading'])}</h2>"
        "<ul class='history-learning-list'>"
        + "".join(f"<li>{h(item)}</li>" for item in layout["outcomes"])
        + "</ul></section>",
    ]

    for section in layout["sections"]:
        cards = []
        for person in section["people"]:
            image_url = quote(f"/static/Model afbeeldingen/{person['image_filename']}", safe="/")
            cards.append(
                "<article class='history-figure-card'>"
                f"<img class='history-figure-image' src='{h(image_url)}' alt='{h(person['name'])}'>"
                f"<h3>{h(person['name'])}</h3>"
                "<ul class='history-point-list'>"
                + "".join(f"<li>{h(point)}</li>" for point in person["points"])
                + "</ul></article>"
            )
        blocks.append(
            "<section class='panel history-content-section'>"
            f"<div class='history-section-header'><h2>{h(section['title'])}</h2><p>{h(section['summary'])}</p></div>"
            "<div class='history-figure-grid'>"
            + "".join(cards)
            + "</div></section>"
        )
    return "".join(blocks)



def _module_page(self: WebApp, connection, request, context: dict, module_id: int):
    response = _module_page.original(self, connection, request, context, module_id)
    body = response.body.decode("utf-8", errors="ignore")
    if "<h1>De geschiedenis van NLP</h1>" not in body:
        return response

    custom_sections = _render_history_module_sections()
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
