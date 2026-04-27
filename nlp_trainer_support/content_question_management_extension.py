from __future__ import annotations

import json
import re
from urllib.parse import quote_plus

from . import content_admin_extension as cms
from . import db
from .web import Response, WebApp, h, parse_json

_PATCHED = False

QUESTION_TYPE_OPTIONS = [
    ("multiple_choice", "Meerkeuze (1 goed)"),
    ("multi_select", "Meerkeuze (meerdere goed)"),
    ("short_answer", "Kort antwoord"),
    ("reflection", "Reflectie"),
    ("case_review", "Case review"),
    ("study_card", "Studiekaart"),
    ("text_analysis", "Tekstanalyse"),
    ("match_pairs", "Koppelen"),
]

DIFFICULTY_OPTIONS = [
    ("core", "Core"),
    ("advanced", "Advanced"),
]


def _question_type_select(selected: str = "multiple_choice") -> str:
    return "".join(
        f"<option value='{h(value)}'{' selected' if value == selected else ''}>{h(label)}</option>"
        for value, label in QUESTION_TYPE_OPTIONS
    )


def _difficulty_select(selected: str = "core") -> str:
    return "".join(
        f"<option value='{h(value)}'{' selected' if value == selected else ''}>{h(label)}</option>"
        for value, label in DIFFICULTY_OPTIONS
    )


def _default_question_payload(exercise_type: str, title: str) -> tuple[str, str, str, str, float, int]:
    instructions = "Werk deze vraag verder uit in contentbeheer."
    prompt = title

    if exercise_type == "multiple_choice":
        content = {
            "question": "Schrijf hier de meerkeuzevraag.",
            "options": [
                {"value": "option_1", "label": "Optie 1"},
                {"value": "option_2", "label": "Optie 2"},
                {"value": "option_3", "label": "Optie 3"},
            ],
            "model_answer": "Licht hier toe waarom het juiste antwoord klopt.",
        }
        scoring = {"correct_option": "option_1"}
        return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 0

    if exercise_type == "multi_select":
        content = {
            "question": "Schrijf hier de meerkeuzevraag met meerdere juiste antwoorden.",
            "options": [
                {"value": "option_1", "label": "Optie 1"},
                {"value": "option_2", "label": "Optie 2"},
                {"value": "option_3", "label": "Optie 3"},
                {"value": "option_4", "label": "Optie 4"},
            ],
            "model_answer": "Licht hier toe welke onderdelen juist zijn en waarom.",
        }
        scoring = {"correct_options": ["option_1", "option_2"]}
        return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 0

    if exercise_type == "short_answer":
        content = {
            "question": "Schrijf hier de open vraag.",
            "placeholder": "Schrijf hier je antwoord...",
            "model_answer": "Plaats hier een voorbeeld van een sterk antwoord.",
        }
        scoring = {"keywords": ["kernwoord 1", "kernwoord 2"], "threshold": 0.4}
        return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 0

    if exercise_type == "study_card":
        content = {
            "question": "Schrijf hier de studiekaartvraag.",
            "placeholder": "Schrijf hier je antwoord...",
            "model_answer": "Plaats hier het modelantwoord.",
        }
        scoring = {}
        return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 0

    if exercise_type == "reflection":
        content = {
            "question": "Beschrijf hier de reflectievraag.",
            "placeholder": "Beschrijf hier situatie, inzicht en volgende stap...",
            "model_answer": "Beschrijf hier waar een sterk reflectieantwoord op let.",
        }
        scoring = {}
        return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 1

    if exercise_type == "case_review":
        content = {
            "case": "Beschrijf hier de casus die geanalyseerd moet worden.",
            "guidance_points": [
                "Kernpunt 1",
                "Kernpunt 2",
                "Kernpunt 3",
            ],
            "model_answer": "Beschrijf hier de richting van een sterk antwoord.",
        }
        scoring = {"rubric_points": ["kernpunt 1", "kernpunt 2"]}
        return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 1

    if exercise_type == "text_analysis":
        content = {
            "text": "Plaats hier de te analyseren tekst.",
            "pattern_question": "Welke analyse is hier het meest passend?",
            "options": [
                {"value": "option_1", "label": "Optie 1"},
                {"value": "option_2", "label": "Optie 2"},
                {"value": "option_3", "label": "Optie 3"},
            ],
            "follow_up_prompt": "Welke vervolg- of verdiepingsvraag hoort hierbij?",
            "model_answer": "Beschrijf hier het modelantwoord.",
        }
        scoring = {"correct_option": "option_1", "follow_up_keywords": ["kernwoord 1"], "threshold": 0.4}
        return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 0

    if exercise_type == "match_pairs":
        content = {
            "pairs": [
                {"left": "Onderdeel 1", "options": ["Match 1", "Match 2"]},
                {"left": "Onderdeel 2", "options": ["Match A", "Match B"]},
            ],
            "model_answer": "Beschrijf hier de juiste koppelingen.",
        }
        scoring = {"correct_matches": {"Onderdeel 1": "Match 1", "Onderdeel 2": "Match A"}}
        return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 0

    content = {"question": "Werk deze vraag verder uit.", "model_answer": ""}
    scoring = {}
    return instructions, prompt, json.dumps(content), json.dumps(scoring), 100.0, 0


def _unique_title(connection, desired_title: str) -> str:
    base = (desired_title or "").strip() or "Nieuwe vraag"
    candidate = base
    index = 2
    while connection.execute("SELECT id FROM exercises WHERE title = ?", (candidate,)).fetchone():
        candidate = f"{base} ({index})"
        index += 1
    return candidate


def _create_question(connection, module_id: int, user_id: int, title: str, exercise_type: str, difficulty: str) -> int:
    safe_title = _unique_title(connection, title)
    created_at = db.utc_now_iso()
    instructions, prompt, content_json, scoring_json, max_score, requires_manual_review = _default_question_payload(
        exercise_type,
        safe_title,
    )
    cursor = connection.execute(
        """
        INSERT INTO exercises (
            organization_id, module_id, topic_id, concept_id, title, exercise_type,
            mode_support, difficulty, instructions, prompt, content_json, scoring_json,
            max_score, requires_manual_review, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            None,
            module_id,
            None,
            None,
            safe_title,
            exercise_type,
            "learn,exam",
            difficulty,
            instructions,
            prompt,
            content_json,
            scoring_json,
            max_score,
            requires_manual_review,
            "published",
            created_at,
        ),
    )
    exercise_id = int(cursor.lastrowid)
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
            safe_title,
            instructions,
            prompt,
            content_json,
            scoring_json,
            max_score,
            requires_manual_review,
            "published",
            user_id,
            created_at,
        ),
    )
    return exercise_id


def _archive_question(connection, exercise_id: int, user_id: int) -> int | None:
    exercise = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
    if not exercise:
        return None
    content = parse_json(exercise["content_json"], {})
    scoring = parse_json(exercise["scoring_json"], {})
    updated_at = db.utc_now_iso()
    connection.execute("UPDATE exercises SET status = 'archived' WHERE id = ?", (exercise_id,))
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
            exercise["title"],
            exercise["instructions"],
            exercise["prompt"],
            json.dumps(content),
            json.dumps(scoring),
            float(exercise["max_score"]),
            int(exercise["requires_manual_review"]),
            "archived",
            user_id,
            updated_at,
        ),
    )
    return int(exercise["module_id"])


def _content_questions(self: WebApp, connection, context: dict, module_id: int) -> Response:
    module = connection.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not module:
        return self.not_found(context)
    rows = connection.execute(
        """
        SELECT id, title, exercise_type, difficulty, status
        FROM exercises
        WHERE module_id = ?
        ORDER BY status = 'archived', id
        """,
        (module_id,),
    ).fetchall()
    active_rows = [
        [
            f"<a href='/content/questions/{row['id']}'>{h(row['title'])}</a>",
            h(row["exercise_type"]),
            h(row["difficulty"]),
            h(row["status"]),
            (
                f"<form method='post' action='/content/questions/{row['id']}/delete'>"
                f"<input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>"
                "<button class='button button-secondary small' type='submit'>Verwijderen</button>"
                "</form>"
            ),
        ]
        for row in rows
        if row["status"] == "published"
    ]
    archived_rows = [
        [
            f"<a href='/content/questions/{row['id']}'>{h(row['title'])}</a>",
            h(row["exercise_type"]),
            h(row["difficulty"]),
            h(row["status"]),
        ]
        for row in rows
        if row["status"] != "published"
    ]
    body = f"""
    <section class='hero compact'><div><span class='eyebrow'>Vragenflow</span><h1>{h(module['title'])}</h1></div>
    <div class='actions'><a class='button button-secondary' href='/content/modules/{module_id}'>Terug naar leerpad</a></div></section>
    <section class='panel form-panel'>
      <h2>Nieuwe vraag toevoegen</h2>
      <form method='post' action='/content/modules/{module_id}/questions'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <label class='field'><span>Titel</span><input type='text' name='title' required></label>
        <div class='field-row'>
          <label class='field'><span>Type</span><select name='exercise_type'>{_question_type_select()}</select></label>
          <label class='field'><span>Niveau</span><select name='difficulty'>{_difficulty_select()}</select></label>
        </div>
        <button class='button button-primary' type='submit'>Vraag toevoegen</button>
      </form>
    </section>
    <section class='panel'>
      <h2>Actieve vragen</h2>
      {self.render_table(["Vraag", "Type", "Niveau", "Status", "Actie"], active_rows)}
    </section>
    """
    if archived_rows:
        body += "<section class='panel inset'><h2>Gearchiveerde vragen</h2>" + self.render_table(
            ["Vraag", "Type", "Niveau", "Status"],
            archived_rows,
        ) + "</section>"
    return self.html("Vragen beheren", body, context)


def _edit_question(self: WebApp, connection, request, context: dict, exercise_id: int) -> Response:
    response = _edit_question.original(self, connection, request, context, exercise_id)
    if request.method != "GET":
        return response
    body = response.body.decode("utf-8", errors="ignore")
    if "/delete'" in body:
        return response
    panel = (
        "<section class='panel form-panel'>"
        "<h2>Vraag verwijderen</h2>"
        "<p class='helper'>Verwijderen archiveert de vraag. De vraag verdwijnt uit de actieve flow, maar blijft in contentbeheer zichtbaar zodat je haar later eventueel kunt terugzetten.</p>"
        f"<form method='post' action='/content/questions/{exercise_id}/delete'>"
        f"<input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>"
        "<button class='button button-secondary' type='submit'>Verwijderen</button>"
        "</form>"
        "</section>"
    )
    if "</main>" not in body:
        return response
    body = body.replace("</main>", panel + "</main>", 1)
    return Response(response.status, body.encode("utf-8"), list(response.headers))


def _content_dispatch(self: WebApp, connection, request, context: dict) -> Response:
    module_questions_match = re.fullmatch(r"/content/modules/(\d+)/questions", request.path)
    if module_questions_match and request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")
        exercise_id = _create_question(
            connection,
            int(module_questions_match.group(1)),
            int(context["user"]["user_id"]),
            request.get("title").strip(),
            request.get("exercise_type").strip() or "multiple_choice",
            request.get("difficulty").strip() or "core",
        )
        connection.commit()
        return self.redirect(f"/content/questions/{exercise_id}?notice=" + quote_plus("Vraag toegevoegd."))

    delete_match = re.fullmatch(r"/content/questions/(\d+)/delete", request.path)
    if delete_match and request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")
        module_id = _archive_question(connection, int(delete_match.group(1)), int(context["user"]["user_id"]))
        if module_id is None:
            return self.not_found(context)
        connection.commit()
        return self.redirect(f"/content/modules/{module_id}/questions?notice=" + quote_plus("Vraag verwijderd."))

    return _content_dispatch.original(self, connection, request, context)


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    _content_questions.original = cms._content_questions
    cms._content_questions = _content_questions

    _edit_question.original = cms._edit_question
    cms._edit_question = _edit_question

    _content_dispatch.original = cms._content_dispatch
    cms._content_dispatch = _content_dispatch

    _PATCHED = True


apply()
