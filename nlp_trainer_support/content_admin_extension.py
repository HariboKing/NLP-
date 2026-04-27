from __future__ import annotations

import json
import re
from urllib.parse import quote_plus

from . import db
from . import deletion_extension as story_module
from . import web as web_module
from .web import MODEL_IMAGE_DIR_NAME, Response, WebApp, h, parse_json

_PATCHED = False


def _can_manage_content(context: dict) -> bool:
    user = context.get("user") or {}
    return bool(user.get("is_platform_admin") and not context.get("active_membership"))


def _clean_lines(text: str) -> list[str]:
    lines = []
    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        lines.append(line)
    return lines


def _split_paragraphs(text: str) -> list[str]:
    paragraphs = []
    current = []
    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current).strip())
    return paragraphs


def _parse_content_sections(text: str) -> list[dict]:
    sections: list[dict] = []
    current_section: dict | None = None
    current_group: dict | None = None

    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("# "):
            current_section = {"title": line[2:].strip(), "summary": "", "groups": []}
            sections.append(current_section)
            current_group = None
            continue
        if line.startswith("## "):
            if current_section is None:
                current_section = {"title": "Inhoud", "summary": "", "groups": []}
                sections.append(current_section)
            current_group = {"heading": line[3:].strip(), "points": []}
            current_section["groups"].append(current_group)
            continue
        if line.startswith("- "):
            point = line[2:].strip()
            if current_group is None:
                if current_section is None:
                    current_section = {"title": "Inhoud", "summary": "", "groups": []}
                    sections.append(current_section)
                current_group = {"heading": "Kernpunten", "points": []}
                current_section["groups"].append(current_group)
            current_group["points"].append(point)
            continue
        if current_group is not None:
            current_group["points"].append(line)
        elif current_section is not None:
            current_section["summary"] = (current_section["summary"] + " " + line).strip()
        else:
            current_section = {"title": line, "summary": "", "groups": []}
            sections.append(current_section)
    return sections


def _format_content_sections(sections: list[dict]) -> str:
    blocks = []
    for section in sections or []:
        blocks.append(f"# {section.get('title', '').strip()}")
        summary = (section.get("summary") or "").strip()
        if summary:
            blocks.append(summary)
        for group in section.get("groups", []):
            blocks.append(f"## {group.get('heading', '').strip()}")
            for point in group.get("points", []):
                blocks.append(f"- {point}")
        blocks.append("")
    return "\n".join(blocks).strip()


def _parse_model_sections(text: str) -> list[dict]:
    blocks: list[dict] = []
    current: dict | None = None
    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("# "):
            current = {"heading": line[2:].strip(), "paragraphs": []}
            blocks.append(current)
            continue
        if current is None:
            current = {"heading": "Inhoud", "paragraphs": []}
            blocks.append(current)
        current["paragraphs"].append(line[2:].strip() if line.startswith("- ") else line)
    return blocks


def _format_model_sections(blocks: list[dict]) -> str:
    lines = []
    for block in blocks or []:
        lines.append(f"# {block.get('heading', '').strip()}")
        for paragraph in block.get("paragraphs", []):
            lines.append(str(paragraph).strip())
        lines.append("")
    return "\n".join(lines).strip()


def ensure_content_schema(connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS content_module_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL UNIQUE,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            outcomes_json TEXT NOT NULL DEFAULT '[]',
            sections_json TEXT NOT NULL DEFAULT '[]',
            reading_text TEXT NOT NULL DEFAULT '',
            more_info_text TEXT NOT NULL DEFAULT '',
            updated_by_user_id INTEGER NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS content_model_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            image_stem TEXT NOT NULL DEFAULT '',
            intro TEXT NOT NULL DEFAULT '',
            blocks_json TEXT NOT NULL DEFAULT '[]',
            updated_by_user_id INTEGER NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS content_exercise_overrides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id INTEGER NOT NULL UNIQUE,
            title TEXT NOT NULL,
            instructions TEXT NOT NULL,
            prompt TEXT NOT NULL,
            content_json TEXT NOT NULL,
            scoring_json TEXT NOT NULL,
            max_score REAL NOT NULL,
            requires_manual_review INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'published',
            updated_by_user_id INTEGER NULL,
            updated_at TEXT NOT NULL
        );
        """
    )


def _module_story_defaults(title: str) -> tuple[list[str], list[dict]] | None:
    layout_entry = story_module._MODULE_STORY_LAYOUTS.get(title)
    if not layout_entry:
        return None
    _layout_type, layout = layout_entry
    return list(layout.get("outcomes", [])), list(layout.get("sections", []))


def _module_default_sections(connection, module_id: int) -> list[dict]:
    topics = connection.execute(
        "SELECT * FROM topics WHERE module_id = ? ORDER BY sort_order",
        (module_id,),
    ).fetchall()
    sections = []
    for topic in topics:
        concepts = connection.execute(
            "SELECT * FROM concepts WHERE topic_id = ? ORDER BY sort_order",
            (topic["id"],),
        ).fetchall()
        sections.append(
            {
                "title": topic["title"],
                "summary": topic["summary"],
                "groups": [
                    {
                        "heading": "Concepten",
                        "points": [f"{concept['title']}: {concept['summary']}" for concept in concepts],
                    }
                ],
            }
        )
    return sections


def _module_default_materials(connection, module_id: int) -> tuple[str, str]:
    resources = connection.execute(
        """
        SELECT *
        FROM resources
        WHERE module_id = ? AND organization_id IS NULL
        ORDER BY sort_order, id
        """,
        (module_id,),
    ).fetchall()
    reading = []
    more_info = []
    for resource in resources:
        block = f"{resource['title']}\n{resource['content']}"
        if resource["link_url"]:
            block += f"\n{resource['link_url']}"
        bucket = web_module.resource_bucket(resource["resource_type"])
        if bucket == "literature":
            more_info.append(block)
        else:
            reading.append(block)
    return "\n\n".join(reading), "\n\n".join(more_info)


def _get_module_override(connection, module_id: int):
    ensure_content_schema(connection)
    return connection.execute(
        "SELECT * FROM content_module_pages WHERE module_id = ?",
        (module_id,),
    ).fetchone()


def _get_model_override(connection, slug: str):
    ensure_content_schema(connection)
    return connection.execute(
        "SELECT * FROM content_model_pages WHERE slug = ?",
        (slug,),
    ).fetchone()


def _apply_exercise_overrides(connection) -> None:
    ensure_content_schema(connection)
    rows = connection.execute("SELECT * FROM content_exercise_overrides").fetchall()
    for row in rows:
        connection.execute(
            """
            UPDATE exercises
            SET title = ?, instructions = ?, prompt = ?, content_json = ?, scoring_json = ?,
                max_score = ?, requires_manual_review = ?, status = ?
            WHERE id = ?
            """,
            (
                row["title"],
                row["instructions"],
                row["prompt"],
                row["content_json"],
                row["scoring_json"],
                row["max_score"],
                row["requires_manual_review"],
                row["status"],
                row["exercise_id"],
            ),
        )


def _apply_module_overrides(connection) -> None:
    ensure_content_schema(connection)
    rows = connection.execute("SELECT * FROM content_module_pages").fetchall()
    for row in rows:
        connection.execute(
            "UPDATE modules SET title = ?, summary = ? WHERE id = ?",
            (row["title"], row["summary"], row["module_id"]),
        )


def _apply_model_overrides_to_runtime(connection) -> None:
    ensure_content_schema(connection)
    rows = connection.execute("SELECT * FROM content_model_pages").fetchall()
    overrides = {row["slug"]: row for row in rows}
    for model in web_module.MODEL_PAGES:
        row = overrides.get(model["slug"])
        if not row:
            continue
        model["title"] = row["title"]
        model["image_stem"] = row["image_stem"] or model.get("image_stem", "")
        model["intro"] = row["intro"]
        model["blocks"] = parse_json(row["blocks_json"], [])
    web_module.MODEL_PAGE_LOOKUP = {model["slug"]: model for model in web_module.MODEL_PAGES}


def apply_content_overrides(connection) -> None:
    ensure_content_schema(connection)
    _apply_module_overrides(connection)
    _apply_exercise_overrides(connection)
    _apply_model_overrides_to_runtime(connection)


def _render_learning_panel(outcomes: list[str]) -> str:
    if not outcomes:
        return ""
    return (
        "<section class='panel pathway-learning-panel'>"
        "<h2>Na dit leerpad kun je</h2>"
        "<ul class='pathway-learning-list'>"
        + "".join(f"<li>{h(item)}</li>" for item in outcomes)
        + "</ul></section>"
    )


def _render_content_sections(sections: list[dict]) -> str:
    if not sections:
        return "<section class='panel'><h2>Inhoudelijke informatie</h2><p class='helper'>Er is nog geen inhoud toegevoegd.</p></section>"
    blocks = [story_module._pathway_story_style_block()]
    for section in sections:
        groups = []
        for group in section.get("groups", []):
            groups.append(
                "<article class='pathway-story-group'>"
                f"<h3>{h(group.get('heading'))}</h3>"
                "<ul class='pathway-story-sublist'>"
                + "".join(f"<li>{h(point)}</li>" for point in group.get("points", []))
                + "</ul></article>"
            )
        blocks.append(
            "<section class='panel pathway-content-section'>"
            f"<div class='pathway-section-header'><h2>{h(section.get('title'))}</h2><p>{h(section.get('summary'))}</p></div>"
            "<div class='pathway-story-copy'>"
            + "".join(groups)
            + "</div></section>"
        )
    return "".join(blocks)


def _render_material_panel(reading_text: str, more_info_text: str) -> str:
    def material_card(title: str, text: str, empty: str) -> str:
        paragraphs = _split_paragraphs(text)
        if not paragraphs:
            return f"<article class='panel inset'><h3>{h(title)}</h3><p class='helper'>{h(empty)}</p></article>"
        return (
            "<article class='panel inset'>"
            f"<h3>{h(title)}</h3>"
            + "".join(f"<p>{h(paragraph)}</p>" for paragraph in paragraphs)
            + "</article>"
        )

    return (
        "<section class='panel'><h2>Lesmateriaal</h2><div class='grid two-up'>"
        + material_card("Leesstof van de les", reading_text, "Er is nog geen leesstof toegevoegd.")
        + material_card("Meer informatie", more_info_text, "Er is nog geen extra informatie toegevoegd.")
        + "</div></section>"
    )


def _content_module_page(self: WebApp, connection, request, context: dict, module_id: int) -> Response:
    override = _get_module_override(connection, module_id)
    if not override:
        return _content_module_page.original(self, connection, request, context, module_id)

    module = connection.execute(
        """
        SELECT modules.*, programs.title AS program_title
        FROM modules
        JOIN programs ON programs.id = modules.program_id
        WHERE modules.id = ?
        """,
        (module_id,),
    ).fetchone()
    if not module:
        return self.not_found(context)
    if not self.public_can_access_module(connection, context, module_id):
        return self.upgrade_required_page(context, "Leerpaden", module["title"])

    exercise_count = connection.execute(
        "SELECT COUNT(*) AS count FROM exercises WHERE module_id = ? AND status = 'published'",
        (module_id,),
    ).fetchone()["count"]
    quiz_session = self.get_module_quiz_session(connection, context["user"]["user_id"], module_id)
    quiz_intro = "Doorloop alle kennisvragen van dit leerpad in een eigen quiz-flow met directe feedback, herhaalvragen en opgeslagen voortgang."
    quiz_action = (
        f"<a class='button button-primary' href='/modules/{module_id}/quiz'>Start vragenflow</a>"
        if exercise_count
        else "<span class='button button-secondary disabled'>Nog geen vragen</span>"
    )
    quiz_extra_action = ""
    if quiz_session and quiz_session["status"] == "active" and exercise_count:
        queue = parse_json(quiz_session["queue_json"], [])
        current_step = min(int(quiz_session["current_position"]) + 1, len(queue) or exercise_count)
        quiz_intro = f"Je hebt al voortgang opgeslagen. Ga verder bij stap {current_step}."
        quiz_action = f"<a class='button button-primary' href='/modules/{module_id}/quiz'>Verder waar je was</a>"
        quiz_extra_action = f"<a class='button button-secondary' href='/modules/{module_id}/quiz?restart=1'>Opnieuw beginnen</a>"

    outcomes = parse_json(override["outcomes_json"], [])
    sections = parse_json(override["sections_json"], [])
    body = [
        "<section class='hero compact'><div><span class='eyebrow'>Verdiepingspad</span>"
        f"<h1>{h(module['title'])}</h1><p>{h(module['summary'])}</p></div>"
        "<div class='actions'><a class='button button-secondary' href='/dashboard'>Terug naar dashboard</a></div></section>",
        self.metrics_row(
            [
                ("Programma", module["program_title"]),
                ("Vragen", str(exercise_count)),
                ("Status", "Beschikbaar"),
            ]
        ),
        "<section class='grid three-up'>"
        "<article class='panel inset'><h2>Vragen van dit leerpad</h2>"
        f"<p>{h(quiz_intro)}</p><div class='actions'>{quiz_action}{quiz_extra_action}</div></article>"
        "<article class='panel inset'><h2>Toepassing met tekstvoorbeelden</h2><p>Oefen taalpatronen en interventies met uitgeschreven cases.</p></article>"
        "<article class='panel inset'><h2>Toepassing met videobeelden</h2><p>Gebruik observatie, kalibratie en feedback aan de hand van videomateriaal.</p></article>"
        "</section>",
        _render_learning_panel(outcomes),
        _render_content_sections(sections),
        _render_material_panel(override["reading_text"], override["more_info_text"]),
    ]
    return self.html(module["title"], "".join(body), context)


def _content_model_page(self: WebApp, connection, context: dict, model_slug: str) -> Response:
    override = _get_model_override(connection, model_slug)
    if not override:
        return _content_model_page.original(self, connection, context, model_slug)
    if not self.public_can_access_model(connection, context, model_slug):
        return self.upgrade_required_page(context, "Model", override["title"])

    image_url, expected_filename = self.model_image_url(override["image_stem"])
    if image_url:
        image_panel = (
            "<section class='panel'>"
            f"<img src='{h(image_url)}' alt='{h(override['title'])}' "
            "style='display:block; width:100%; border-radius:1rem; border:1px solid rgba(23,48,60,0.08);'>"
            "</section>"
        )
    else:
        image_panel = (
            "<section class='panel inset'><span class='eyebrow'>Afbeelding toevoegen</span>"
            f"<h2>{h(override['title'])}</h2>"
            f"<p>Plaats een afbeelding in <code>static/{h(MODEL_IMAGE_DIR_NAME)}</code> met bestandsnaam <code>{h(expected_filename)}</code>.</p>"
            "</section>"
        )

    blocks = parse_json(override["blocks_json"], [])
    text_blocks = "".join(
        "<article class='panel'>"
        f"<h2>{h(block.get('heading'))}</h2>"
        + "".join(f"<p>{h(paragraph)}</p>" for paragraph in block.get("paragraphs", []))
        + "</article>"
        for block in blocks
    )
    content = [
        "<section class='hero compact'><div><span class='eyebrow'>Modellen overzicht</span>"
        f"<h1>{h(override['title'])}</h1><p>{h(override['intro'])}</p></div>"
        "<div class='actions'><a class='button button-secondary' href='/dashboard'>Terug naar dashboard</a></div></section>",
        image_panel,
        "<section class='grid two-up'>" + text_blocks + "</section>",
    ]
    return self.html(override["title"], "".join(content), context)


def _content_dashboard(self: WebApp, connection, context: dict) -> Response:
    module_count = connection.execute("SELECT COUNT(*) AS count FROM modules").fetchone()["count"]
    exercise_count = connection.execute("SELECT COUNT(*) AS count FROM exercises WHERE status = 'published'").fetchone()["count"]
    body = [
        "<section class='hero compact'><div><span class='eyebrow'>Platform beheer</span><h1>Contentbeheer</h1>"
        "<p>Beheer hier leerpaden, vragenflows en modellen zonder codewijzigingen.</p></div></section>",
        self.metrics_row([("Leerpaden", str(module_count)), ("Vragen", str(exercise_count)), ("Modellen", str(len(web_module.MODEL_PAGES)))]),
        "<section class='grid three-up'>"
        "<article class='panel inset'><h2>Verdiepingspaden</h2><p>Pas leerdoelen, inhoudelijke blokken en lesmateriaal aan.</p><a class='button button-primary' href='/content/modules'>Openen</a></article>"
        "<article class='panel inset'><h2>Vragenflows</h2><p>Open een leerpad en wijzig de vragen die in de flow zitten.</p><a class='button button-secondary' href='/content/modules'>Vragen beheren</a></article>"
        "<article class='panel inset'><h2>Modellen overzicht</h2><p>Pas modelpagina's en hun informatieblokken aan.</p><a class='button button-secondary' href='/content/models'>Openen</a></article>"
        "</section>",
    ]
    return self.html("Contentbeheer", "".join(body), context)


def _content_modules(self: WebApp, connection, context: dict) -> Response:
    rows = connection.execute(
        """
        SELECT modules.*, programs.title AS program_title,
               CASE WHEN content_module_pages.id IS NULL THEN 0 ELSE 1 END AS has_override
        FROM modules
        JOIN programs ON programs.id = modules.program_id
        LEFT JOIN content_module_pages ON content_module_pages.module_id = modules.id
        ORDER BY modules.sort_order, modules.id
        """
    ).fetchall()
    table_rows = [
        [
            f"<a href='/content/modules/{row['id']}'>{h(row['title'])}</a>",
            h(row["program_title"]),
            h("Aangepast" if row["has_override"] else "Standaard"),
            f"<a class='button button-secondary small' href='/content/modules/{row['id']}/questions'>Vragen</a>",
        ]
        for row in rows
    ]
    body = (
        "<section class='hero compact'><div><span class='eyebrow'>Contentbeheer</span><h1>Verdiepingspaden</h1></div>"
        "<div class='actions'><a class='button button-secondary' href='/content'>Terug</a></div></section>"
        "<section class='panel'>"
        + self.render_table(["Leerpad", "Programma", "Status", "Vragenflow"], table_rows)
        + "</section>"
    )
    return self.html("Verdiepingspaden beheren", body, context)


def _edit_module(self: WebApp, connection, request, context: dict, module_id: int) -> Response:
    module = connection.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not module:
        return self.not_found(context)
    override = _get_module_override(connection, module_id)

    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")
        title = request.get("title").strip() or module["title"]
        summary = request.get("summary").strip()
        outcomes = _clean_lines(request.get("outcomes"))
        sections = _parse_content_sections(request.get("sections"))
        reading_text = request.get("reading_text").strip()
        more_info_text = request.get("more_info_text").strip()
        updated_at = db.utc_now_iso()
        user_id = context["user"]["user_id"]
        connection.execute(
            """
            INSERT INTO content_module_pages (
                module_id, title, summary, outcomes_json, sections_json, reading_text,
                more_info_text, updated_by_user_id, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (module_id) DO UPDATE SET
                title = excluded.title,
                summary = excluded.summary,
                outcomes_json = excluded.outcomes_json,
                sections_json = excluded.sections_json,
                reading_text = excluded.reading_text,
                more_info_text = excluded.more_info_text,
                updated_by_user_id = excluded.updated_by_user_id,
                updated_at = excluded.updated_at
            """,
            (
                module_id,
                title,
                summary,
                json.dumps(outcomes),
                json.dumps(sections),
                reading_text,
                more_info_text,
                user_id,
                updated_at,
            ),
        )
        connection.execute("UPDATE modules SET title = ?, summary = ? WHERE id = ?", (title, summary, module_id))
        connection.commit()
        return self.redirect(f"/content/modules/{module_id}?notice=" + quote_plus("Leerpad opgeslagen."))

    if override:
        title = override["title"]
        summary = override["summary"]
        outcomes_text = "\n".join(parse_json(override["outcomes_json"], []))
        sections_text = _format_content_sections(parse_json(override["sections_json"], []))
        reading_text = override["reading_text"]
        more_info_text = override["more_info_text"]
    else:
        title = module["title"]
        summary = module["summary"]
        story_defaults = _module_story_defaults(module["title"])
        if story_defaults:
            outcomes, sections = story_defaults
        else:
            outcomes, sections = [], _module_default_sections(connection, module_id)
        outcomes_text = "\n".join(outcomes)
        sections_text = _format_content_sections(sections)
        reading_text, more_info_text = _module_default_materials(connection, module_id)

    body = f"""
    <section class='hero compact'><div><span class='eyebrow'>Contentbeheer</span><h1>{h(title)}</h1><p>Wijzig leerdoelen, inhoud en lesmateriaal.</p></div>
    <div class='actions'><a class='button button-secondary' href='/content/modules'>Terug</a><a class='button button-secondary' href='/content/modules/{module_id}/questions'>Vragenflow</a></div></section>
    <section class='panel form-panel'>
      <form method='post' action='/content/modules/{module_id}'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <label class='field'><span>Titel</span><input type='text' name='title' value='{h(title)}'></label>
        <label class='field'><span>Samenvatting</span><textarea name='summary' rows='3'>{h(summary)}</textarea></label>
        <label class='field'><span>Na dit leerpad kun je</span><textarea name='outcomes' rows='8'>{h(outcomes_text)}</textarea></label>
        <label class='field'><span>Inhoudelijke blokken</span><textarea name='sections' rows='18'>{h(sections_text)}</textarea></label>
        <div class='grid two-up'>
          <label class='field'><span>Leesstof van de les</span><textarea name='reading_text' rows='10'>{h(reading_text)}</textarea></label>
          <label class='field'><span>Meer informatie</span><textarea name='more_info_text' rows='10'>{h(more_info_text)}</textarea></label>
        </div>
        <button class='button button-primary' type='submit'>Opslaan</button>
      </form>
    </section>
    """
    return self.html("Leerpad beheren", body, context)


def _content_questions(self: WebApp, connection, context: dict, module_id: int) -> Response:
    module = connection.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not module:
        return self.not_found(context)
    rows = connection.execute(
        """
        SELECT id, title, exercise_type, difficulty, status
        FROM exercises
        WHERE module_id = ?
        ORDER BY id
        """,
        (module_id,),
    ).fetchall()
    table_rows = [
        [
            f"<a href='/content/questions/{row['id']}'>{h(row['title'])}</a>",
            h(row["exercise_type"]),
            h(row["difficulty"]),
            h(row["status"]),
        ]
        for row in rows
    ]
    body = (
        f"<section class='hero compact'><div><span class='eyebrow'>Vragenflow</span><h1>{h(module['title'])}</h1></div>"
        f"<div class='actions'><a class='button button-secondary' href='/content/modules/{module_id}'>Terug naar leerpad</a></div></section>"
        "<section class='panel'>"
        + self.render_table(["Vraag", "Type", "Niveau", "Status"], table_rows)
        + "</section>"
    )
    return self.html("Vragen beheren", body, context)


def _exercise_editor_payload(exercise) -> tuple[dict, dict]:
    return parse_json(exercise["content_json"], {}), parse_json(exercise["scoring_json"], {})


def _edit_question(self: WebApp, connection, request, context: dict, exercise_id: int) -> Response:
    exercise = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
    if not exercise:
        return self.not_found(context)
    content, scoring = _exercise_editor_payload(exercise)

    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")
        title = request.get("title").strip() or exercise["title"]
        instructions = request.get("instructions").strip()
        question = request.get("question").strip()
        model_answer = request.get("model_answer").strip()
        max_score = float(request.get("max_score", str(exercise["max_score"])) or exercise["max_score"])
        requires_manual_review = 1 if request.get("requires_manual_review") == "1" else 0
        status = request.get("status").strip() or "published"

        new_content = dict(content)
        new_scoring = dict(scoring)
        if question:
            new_content["question"] = question
        new_content["model_answer"] = model_answer

        exercise_type = exercise["exercise_type"]
        if exercise_type in {"multiple_choice", "multi_select"}:
            labels = _clean_lines(request.get("options_text"))
            options = [{"value": f"option_{index}", "label": label} for index, label in enumerate(labels, start=1)]
            new_content["options"] = options
            correct_labels = set(_clean_lines(request.get("correct_text")))
            correct_values = [option["value"] for option in options if option["label"] in correct_labels]
            if exercise_type == "multiple_choice":
                new_scoring["correct_option"] = correct_values[0] if correct_values else ""
            else:
                new_scoring["correct_options"] = correct_values
        elif exercise_type == "short_answer":
            new_scoring["keywords"] = _clean_lines(request.get("keywords_text"))
            try:
                new_scoring["threshold"] = float(request.get("threshold", str(new_scoring.get("threshold", 0.4))))
            except ValueError:
                new_scoring["threshold"] = 0.4
        elif request.get("advanced_content_json").strip():
            new_content = json.loads(request.get("advanced_content_json"))
            new_scoring = json.loads(request.get("advanced_scoring_json") or "{}")

        prompt = question or exercise["prompt"]
        content_json = json.dumps(new_content)
        scoring_json = json.dumps(new_scoring)
        updated_at = db.utc_now_iso()
        user_id = context["user"]["user_id"]
        connection.execute(
            """
            INSERT INTO content_exercise_overrides (
                exercise_id, title, instructions, prompt, content_json, scoring_json, max_score,
                requires_manual_review, status, updated_by_user_id, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (exercise_id) DO UPDATE SET
                title = excluded.title,
                instructions = excluded.instructions,
                prompt = excluded.prompt,
                content_json = excluded.content_json,
                scoring_json = excluded.scoring_json,
                max_score = excluded.max_score,
                requires_manual_review = excluded.requires_manual_review,
                status = excluded.status,
                updated_by_user_id = excluded.updated_by_user_id,
                updated_at = excluded.updated_at
            """,
            (
                exercise_id,
                title,
                instructions,
                prompt,
                content_json,
                scoring_json,
                max_score,
                requires_manual_review,
                status,
                user_id,
                updated_at,
            ),
        )
        _apply_exercise_overrides(connection)
        connection.commit()
        return self.redirect(f"/content/questions/{exercise_id}?notice=" + quote_plus("Vraag opgeslagen."))

    question = content.get("question") or content.get("question_label") or exercise["prompt"]
    model_answer = content.get("model_answer", "")
    options_text = "\n".join(option.get("label", "") for option in content.get("options", []))
    correct_text = ""
    if exercise["exercise_type"] == "multiple_choice":
        correct_value = scoring.get("correct_option", "")
        correct_text = "\n".join(option.get("label", "") for option in content.get("options", []) if option.get("value") == correct_value)
    elif exercise["exercise_type"] == "multi_select":
        correct_values = set(scoring.get("correct_options", []))
        correct_text = "\n".join(option.get("label", "") for option in content.get("options", []) if option.get("value") in correct_values)
    keywords_text = "\n".join(scoring.get("keywords", []))
    advanced = ""
    if exercise["exercise_type"] not in {"multiple_choice", "multi_select", "short_answer", "study_card", "reflection"}:
        advanced = (
            f"<label class='field'><span>Geavanceerd: content JSON</span><textarea name='advanced_content_json' rows='12'>{h(json.dumps(content, indent=2, ensure_ascii=False))}</textarea></label>"
            f"<label class='field'><span>Geavanceerd: scoring JSON</span><textarea name='advanced_scoring_json' rows='8'>{h(json.dumps(scoring, indent=2, ensure_ascii=False))}</textarea></label>"
        )

    option_fields = ""
    if exercise["exercise_type"] in {"multiple_choice", "multi_select"}:
        option_fields = (
            f"<label class='field'><span>Antwoordopties</span><textarea name='options_text' rows='8'>{h(options_text)}</textarea></label>"
            f"<label class='field'><span>Juiste antwoord(en)</span><textarea name='correct_text' rows='5'>{h(correct_text)}</textarea></label>"
        )
    keyword_fields = ""
    if exercise["exercise_type"] == "short_answer":
        keyword_fields = (
            f"<label class='field'><span>Kernwoorden voor automatische score</span><textarea name='keywords_text' rows='7'>{h(keywords_text)}</textarea></label>"
            f"<label class='field'><span>Drempel</span><input type='number' min='0' max='1' step='0.05' name='threshold' value='{h(scoring.get('threshold', 0.4))}'></label>"
        )

    checked = " checked" if exercise["requires_manual_review"] else ""
    body = f"""
    <section class='hero compact'><div><span class='eyebrow'>Vraag beheren</span><h1>{h(exercise['title'])}</h1><p>{h(exercise['exercise_type'])}</p></div>
    <div class='actions'><a class='button button-secondary' href='/content/modules/{exercise['module_id']}/questions'>Terug</a></div></section>
    <section class='panel form-panel'>
      <form method='post' action='/content/questions/{exercise_id}'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <label class='field'><span>Titel</span><input type='text' name='title' value='{h(exercise['title'])}'></label>
        <label class='field'><span>Instructie</span><textarea name='instructions' rows='3'>{h(exercise['instructions'])}</textarea></label>
        <label class='field'><span>Vraag</span><textarea name='question' rows='5'>{h(question)}</textarea></label>
        <label class='field'><span>Modelantwoord / feedback</span><textarea name='model_answer' rows='6'>{h(model_answer)}</textarea></label>
        {option_fields}
        {keyword_fields}
        {advanced}
        <div class='field-row'>
          <label class='field'><span>Max score</span><input type='number' name='max_score' min='1' max='100' step='1' value='{h(exercise['max_score'])}'></label>
          <label class='field'><span>Status</span><select name='status'><option value='published'>published</option><option value='archived'>archived</option></select></label>
          <label class='field checkbox-row'><input type='checkbox' name='requires_manual_review' value='1'{checked}><span>Handmatige review verplicht</span></label>
        </div>
        <button class='button button-primary' type='submit'>Opslaan</button>
      </form>
    </section>
    """
    return self.html("Vraag beheren", body, context)


def _content_models(self: WebApp, connection, context: dict) -> Response:
    _apply_model_overrides_to_runtime(connection)
    rows = [
        [
            f"<a href='/content/models/{model['slug']}'>{h(model['title'])}</a>",
            h(model["slug"]),
            h(model.get("image_stem", "")),
        ]
        for model in web_module.MODEL_PAGES
    ]
    body = (
        "<section class='hero compact'><div><span class='eyebrow'>Contentbeheer</span><h1>Modellen overzicht</h1></div>"
        "<div class='actions'><a class='button button-secondary' href='/content'>Terug</a></div></section>"
        "<section class='panel'>"
        + self.render_table(["Model", "Slug", "Afbeelding"], rows)
        + "</section>"
    )
    return self.html("Modellen beheren", body, context)


def _edit_model(self: WebApp, connection, request, context: dict, slug: str) -> Response:
    base_model = web_module.MODEL_PAGE_LOOKUP.get(slug)
    if not base_model:
        return self.not_found(context)
    override = _get_model_override(connection, slug)
    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")
        title = request.get("title").strip() or base_model["title"]
        image_stem = request.get("image_stem").strip() or base_model.get("image_stem", "")
        intro = request.get("intro").strip()
        blocks = _parse_model_sections(request.get("blocks"))
        connection.execute(
            """
            INSERT INTO content_model_pages (
                slug, title, image_stem, intro, blocks_json, updated_by_user_id, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (slug) DO UPDATE SET
                title = excluded.title,
                image_stem = excluded.image_stem,
                intro = excluded.intro,
                blocks_json = excluded.blocks_json,
                updated_by_user_id = excluded.updated_by_user_id,
                updated_at = excluded.updated_at
            """,
            (
                slug,
                title,
                image_stem,
                intro,
                json.dumps(blocks),
                context["user"]["user_id"],
                db.utc_now_iso(),
            ),
        )
        connection.commit()
        _apply_model_overrides_to_runtime(connection)
        return self.redirect(f"/content/models/{slug}?notice=" + quote_plus("Model opgeslagen."))

    if override:
        title = override["title"]
        image_stem = override["image_stem"]
        intro = override["intro"]
        blocks_text = _format_model_sections(parse_json(override["blocks_json"], []))
    else:
        title = base_model["title"]
        image_stem = base_model.get("image_stem", "")
        intro = base_model.get("intro", "")
        blocks_text = _format_model_sections(web_module.build_model_information_blocks(base_model))
    body = f"""
    <section class='hero compact'><div><span class='eyebrow'>Model beheren</span><h1>{h(title)}</h1></div>
    <div class='actions'><a class='button button-secondary' href='/content/models'>Terug</a></div></section>
    <section class='panel form-panel'>
      <form method='post' action='/content/models/{h(slug)}'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <label class='field'><span>Titel</span><input type='text' name='title' value='{h(title)}'></label>
        <label class='field'><span>Afbeelding bestandsnaam zonder extensie</span><input type='text' name='image_stem' value='{h(image_stem)}'></label>
        <label class='field'><span>Intro</span><textarea name='intro' rows='4'>{h(intro)}</textarea></label>
        <label class='field'><span>Informatieblokken</span><textarea name='blocks' rows='18'>{h(blocks_text)}</textarea></label>
        <button class='button button-primary' type='submit'>Opslaan</button>
      </form>
    </section>
    """
    return self.html("Model beheren", body, context)


def _content_dispatch(self: WebApp, connection, request, context: dict) -> Response:
    ensure_content_schema(connection)
    _apply_model_overrides_to_runtime(connection)
    if not _can_manage_content(context):
        return self.forbidden(context)
    if request.path == "/content":
        return _content_dashboard(self, connection, context)
    if request.path == "/content/modules":
        return _content_modules(self, connection, context)
    module_match = re.fullmatch(r"/content/modules/(\d+)", request.path)
    if module_match:
        return _edit_module(self, connection, request, context, int(module_match.group(1)))
    module_questions_match = re.fullmatch(r"/content/modules/(\d+)/questions", request.path)
    if module_questions_match:
        return _content_questions(self, connection, context, int(module_questions_match.group(1)))
    question_match = re.fullmatch(r"/content/questions/(\d+)", request.path)
    if question_match:
        return _edit_question(self, connection, request, context, int(question_match.group(1)))
    if request.path == "/content/models":
        return _content_models(self, connection, context)
    model_match = re.fullmatch(r"/content/models/([a-z0-9-]+)", request.path)
    if model_match:
        return _edit_model(self, connection, request, context, model_match.group(1))
    return self.not_found(context)


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    original_runtime_migrations = db.apply_runtime_migrations

    def patched_runtime_migrations(connection) -> None:
        original_runtime_migrations(connection)
        apply_content_overrides(connection)
        connection.commit()

    db.apply_runtime_migrations = patched_runtime_migrations

    original_render_nav = WebApp.render_nav

    def render_nav(self: WebApp, context: dict) -> str:
        nav = original_render_nav(self, context)
        if _can_manage_content(context) and "/content" not in nav:
            nav = nav.replace(
                "<a class='nav-link' href='/logout'>Logout</a>",
                "<a class='nav-link' href='/content'>Contentbeheer</a><a class='nav-link' href='/logout'>Logout</a>",
                1,
            )
        return nav

    original_dispatch = WebApp.dispatch

    def dispatch(self: WebApp, request) -> Response:
        if request.path == "/content" or request.path.startswith("/content/"):
            with db.connect() as connection:
                context = self.get_context(connection, request)
                return _content_dispatch(self, connection, request, context)
        return original_dispatch(self, request)

    original_module_page = WebApp.module_page
    _content_module_page.original = original_module_page
    WebApp.module_page = _content_module_page

    original_model_page = WebApp.model_page
    _content_model_page.original = original_model_page
    WebApp.model_page = _content_model_page

    WebApp.render_nav = render_nav
    WebApp.dispatch = dispatch
    _PATCHED = True


apply()
