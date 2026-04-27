from __future__ import annotations

import json
import re
from urllib.parse import quote_plus

from . import content_admin_extension as cms
from . import db
from .web import Response, WebApp, h, parse_json

_PATCHED = False
SIMPLE_EXERCISE_TYPES = {"multiple_choice", "multi_select", "short_answer", "study_card", "reflection"}
ADVANCED_EXERCISE_TYPES = {"text_analysis", "match_pairs", "case_review"}


def _ensure_question_override_columns(connection) -> None:
    cms.ensure_content_schema(connection)
    db.ensure_column(connection, "content_exercise_overrides", "exercise_type", "TEXT NOT NULL DEFAULT ''")
    db.ensure_column(connection, "content_exercise_overrides", "difficulty", "TEXT NOT NULL DEFAULT 'core'")


def _default_question_payload(title: str) -> tuple[str, str, str, str, float, int, str, str]:
    instructions = "Werk deze vraag verder uit in contentbeheer."
    prompt = title
    content = {
        "question": "Schrijf hier de vraag.",
        "placeholder": "Schrijf hier je antwoord...",
        "model_answer": "Plaats hier het modelantwoord of de toelichting.",
    }
    scoring = {}
    return (
        instructions,
        prompt,
        json.dumps(content),
        json.dumps(scoring),
        100.0,
        0,
        "study_card",
        "core",
    )


def _unique_title(connection, desired_title: str) -> str:
    base = (desired_title or "").strip() or "Nieuwe vraag"
    candidate = base
    index = 2
    while connection.execute("SELECT id FROM exercises WHERE title = ?", (candidate,)).fetchone():
        candidate = f"{base} ({index})"
        index += 1
    return candidate


def _upsert_question_override(connection, exercise, *, exercise_type: str | None = None, difficulty: str | None = None, status: str | None = None, user_id: int) -> None:
    _ensure_question_override_columns(connection)
    content = parse_json(exercise["content_json"], {})
    scoring = parse_json(exercise["scoring_json"], {})
    connection.execute(
        """
        INSERT INTO content_exercise_overrides (
            exercise_id, title, instructions, prompt, content_json, scoring_json, max_score,
            requires_manual_review, status, updated_by_user_id, updated_at, exercise_type, difficulty
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            updated_at = excluded.updated_at,
            exercise_type = excluded.exercise_type,
            difficulty = excluded.difficulty
        """,
        (
            int(exercise["id"]),
            exercise["title"],
            exercise["instructions"],
            exercise["prompt"],
            json.dumps(content),
            json.dumps(scoring),
            float(exercise["max_score"]),
            int(exercise["requires_manual_review"]),
            status or exercise["status"],
            user_id,
            db.utc_now_iso(),
            exercise_type or exercise["exercise_type"],
            difficulty or exercise["difficulty"],
        ),
    )


def _create_question(connection, module_id: int, user_id: int, title: str) -> int:
    safe_title = _unique_title(connection, title)
    created_at = db.utc_now_iso()
    instructions, prompt, content_json, scoring_json, max_score, requires_manual_review, exercise_type, difficulty = _default_question_payload(safe_title)
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
    exercise = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
    _upsert_question_override(
        connection,
        exercise,
        exercise_type=exercise_type,
        difficulty=difficulty,
        status="published",
        user_id=user_id,
    )
    return exercise_id


def _archive_question(connection, exercise_id: int, user_id: int) -> int | None:
    exercise = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
    if not exercise:
        return None
    connection.execute("UPDATE exercises SET status = 'archived' WHERE id = ?", (exercise_id,))
    updated = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
    _upsert_question_override(connection, updated, status="archived", user_id=user_id)
    return int(exercise["module_id"])


def _option_lines_from_exercise(exercise_type: str, content: dict, scoring: dict) -> str:
    if exercise_type not in {"multiple_choice", "multi_select"}:
        return ""
    if exercise_type == "multiple_choice":
        correct_values = {scoring.get("correct_option", "")}
    else:
        correct_values = set(scoring.get("correct_options", []))
    lines = []
    for option in content.get("options", []):
        prefix = "* " if option.get("value") in correct_values else ""
        lines.append(prefix + option.get("label", ""))
    return "\n".join(lines)


def _parse_option_lines(text: str) -> list[tuple[str, bool]]:
    parsed = []
    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        is_correct = False
        for marker in ("* ", "[x] ", "+ "):
            if line.lower().startswith(marker.lower()):
                line = line[len(marker):].strip()
                is_correct = True
                break
        if line:
            parsed.append((line, is_correct))
    return parsed


def _build_simple_payload(question: str, model_answer: str, options_text: str, keywords_text: str, requires_manual_review: bool) -> tuple[str, dict, dict]:
    parsed_options = _parse_option_lines(options_text)
    if parsed_options:
        options = [{"value": f"option_{index}", "label": label} for index, (label, _correct) in enumerate(parsed_options, start=1)]
        correct_values = [option["value"] for option, (_label, is_correct) in zip(options, parsed_options) if is_correct]
        if not correct_values:
            raise ValueError("Markeer minstens een juist antwoord met '* '.")
        content = {
            "question": question,
            "options": options,
            "model_answer": model_answer,
        }
        if len(correct_values) == 1:
            return "multiple_choice", content, {"correct_option": correct_values[0]}
        return "multi_select", content, {"correct_options": correct_values}

    keywords = cms._clean_lines(keywords_text)
    if requires_manual_review:
        return (
            "reflection",
            {
                "question": question,
                "placeholder": "Schrijf hier je antwoord...",
                "model_answer": model_answer,
            },
            {},
        )
    if keywords:
        return (
            "short_answer",
            {
                "question": question,
                "placeholder": "Schrijf hier je antwoord...",
                "model_answer": model_answer,
            },
            {"keywords": keywords, "threshold": 0.4},
        )
    return (
        "study_card",
        {
            "question": question,
            "placeholder": "Schrijf hier je antwoord...",
            "model_answer": model_answer,
        },
        {},
    )


def _inject_delete_panel(response: Response, exercise_id: int, csrf_token: str) -> Response:
    body = response.body.decode("utf-8", errors="ignore")
    if "/delete'" in body or "</main>" not in body:
        return response
    panel = (
        "<section class='panel form-panel'>"
        "<h2>Vraag verwijderen</h2>"
        "<p class='helper'>Verwijderen archiveert de vraag. De vraag verdwijnt uit de actieve flow, maar blijft in contentbeheer zichtbaar zodat je haar later eventueel kunt terugzetten.</p>"
        f"<form method='post' action='/content/questions/{exercise_id}/delete'>"
        f"<input type='hidden' name='csrf_token' value='{h(csrf_token)}'>"
        "<button class='button button-secondary' type='submit'>Verwijderen</button>"
        "</form>"
        "</section>"
    )
    body = body.replace("</main>", panel + "</main>", 1)
    return Response(response.status, body.encode("utf-8"), list(response.headers))


def _content_questions(self: WebApp, connection, context: dict, module_id: int) -> Response:
    module = connection.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not module:
        return self.not_found(context)
    rows = connection.execute(
        """
        SELECT id, title, status
        FROM exercises
        WHERE module_id = ?
        ORDER BY status = 'archived', id
        """,
        (module_id,),
    ).fetchall()
    active_rows = [
        [
            f"<a href='/content/questions/{row['id']}'>{h(row['title'])}</a>",
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
      <p class='helper'>Nieuwe vragen beginnen als lege vraag. In de bewerkpagina bepaalt de inhoud daarna automatisch of het een keuzevraag, open vraag, studiekaart of reflectievraag wordt.</p>
      <form method='post' action='/content/modules/{module_id}/questions'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <label class='field'><span>Titel</span><input type='text' name='title' required></label>
        <button class='button button-primary' type='submit'>Vraag toevoegen</button>
      </form>
    </section>
    <section class='panel'>
      <h2>Actieve vragen</h2>
      {self.render_table(["Vraag", "Status", "Actie"], active_rows)}
    </section>
    """
    if archived_rows:
        body += "<section class='panel inset'><h2>Gearchiveerde vragen</h2>" + self.render_table(
            ["Vraag", "Status"],
            archived_rows,
        ) + "</section>"
    return self.html("Vragen beheren", body, context)


def _edit_question(self: WebApp, connection, request, context: dict, exercise_id: int) -> Response:
    exercise = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
    if not exercise:
        return self.not_found(context)

    if exercise["exercise_type"] in ADVANCED_EXERCISE_TYPES:
        response = _edit_question.original(self, connection, request, context, exercise_id)
        if request.method != "GET":
            return response
        return _inject_delete_panel(response, exercise_id, context["session"]["csrf_token"])

    content = parse_json(exercise["content_json"], {})
    scoring = parse_json(exercise["scoring_json"], {})
    notice = ""
    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")
        try:
            title = request.get("title").strip() or exercise["title"]
            instructions = request.get("instructions").strip()
            question = request.get("question").strip() or exercise["prompt"]
            model_answer = request.get("model_answer").strip()
            options_text = request.get("options_text")
            keywords_text = request.get("keywords_text")
            requires_manual_review = 1 if request.get("requires_manual_review") == "1" else 0
            max_score = float(request.get("max_score", str(exercise["max_score"])) or exercise["max_score"])
            status = request.get("status").strip() or "published"
            exercise_type, new_content, new_scoring = _build_simple_payload(
                question,
                model_answer,
                options_text,
                keywords_text,
                bool(requires_manual_review),
            )
            content_json = json.dumps(new_content)
            scoring_json = json.dumps(new_scoring)
            prompt = question

            connection.execute(
                """
                UPDATE exercises
                SET title = ?, exercise_type = ?, instructions = ?, prompt = ?, content_json = ?, scoring_json = ?,
                    max_score = ?, requires_manual_review = ?, status = ?
                WHERE id = ?
                """,
                (
                    title,
                    exercise_type,
                    instructions,
                    prompt,
                    content_json,
                    scoring_json,
                    max_score,
                    requires_manual_review,
                    status,
                    exercise_id,
                ),
            )
            updated = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
            _upsert_question_override(
                connection,
                updated,
                exercise_type=exercise_type,
                difficulty=updated["difficulty"],
                status=status,
                user_id=int(context["user"]["user_id"]),
            )
            connection.commit()
            return self.redirect(f"/content/questions/{exercise_id}?notice=" + quote_plus("Vraag opgeslagen."))
        except ValueError as exc:
            notice = str(exc)
            exercise = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
            content = parse_json(exercise["content_json"], {})
            scoring = parse_json(exercise["scoring_json"], {})

    question = content.get("question") or exercise["prompt"]
    model_answer = content.get("model_answer", "")
    options_text = _option_lines_from_exercise(exercise["exercise_type"], content, scoring)
    keywords_text = "\n".join(scoring.get("keywords", [])) if exercise["exercise_type"] == "short_answer" else ""
    checked = " checked" if exercise["requires_manual_review"] else ""
    notice_html = f"<div class='notice'>{h(notice)}</div>" if notice else ""
    body = f"""
    <section class='hero compact'><div><span class='eyebrow'>Vraag beheren</span><h1>{h(exercise['title'])}</h1><p>De vorm van de vraag wordt automatisch bepaald door de inhoud.</p></div>
    <div class='actions'><a class='button button-secondary' href='/content/modules/{exercise['module_id']}/questions'>Terug</a></div></section>
    {notice_html}
    <section class='panel form-panel'>
      <form method='post' action='/content/questions/{exercise_id}'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <label class='field'><span>Titel</span><input type='text' name='title' value='{h(exercise['title'])}'></label>
        <label class='field'><span>Instructie</span><textarea name='instructions' rows='3'>{h(exercise['instructions'])}</textarea></label>
        <label class='field'><span>Vraag</span><textarea name='question' rows='5'>{h(question)}</textarea></label>
        <label class='field'><span>Antwoordopties (optioneel)</span><textarea name='options_text' rows='8' placeholder='Zet 1 antwoord per regel. Begin juiste antwoorden met * .'>{h(options_text)}</textarea></label>
        <label class='field'><span>Modelantwoord / toelichting</span><textarea name='model_answer' rows='6'>{h(model_answer)}</textarea></label>
        <label class='field'><span>Kernwoorden voor automatische score (optioneel)</span><textarea name='keywords_text' rows='5' placeholder='Laat leeg voor studiekaart. Gebruik 1 kernwoord of frase per regel.'>{h(keywords_text)}</textarea></label>
        <div class='field-row'>
          <label class='field'><span>Max score</span><input type='number' name='max_score' min='1' max='100' step='1' value='{h(exercise['max_score'])}'></label>
          <label class='field'><span>Status</span><select name='status'><option value='published'{' selected' if exercise['status'] == 'published' else ''}>published</option><option value='archived'{' selected' if exercise['status'] == 'archived' else ''}>archived</option></select></label>
          <label class='field checkbox-row'><input type='checkbox' name='requires_manual_review' value='1'{checked}><span>Handmatige beoordeling</span></label>
        </div>
        <button class='button button-primary' type='submit'>Opslaan</button>
      </form>
    </section>
    <section class='panel form-panel'>
      <h2>Vraag verwijderen</h2>
      <p class='helper'>Verwijderen archiveert de vraag. De vraag verdwijnt uit de actieve flow, maar blijft in contentbeheer zichtbaar zodat je haar later eventueel kunt terugzetten.</p>
      <form method='post' action='/content/questions/{exercise_id}/delete'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <button class='button button-secondary' type='submit'>Verwijderen</button>
      </form>
    </section>
    """
    return self.html("Vraag beheren", body, context)


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

    original_ensure_content_schema = cms.ensure_content_schema

    def ensure_content_schema(connection) -> None:
        original_ensure_content_schema(connection)
        _ensure_question_override_columns(connection)

    cms.ensure_content_schema = ensure_content_schema

    original_apply_exercise_overrides = cms._apply_exercise_overrides

    def apply_exercise_overrides(connection) -> None:
        original_apply_exercise_overrides(connection)
        _ensure_question_override_columns(connection)
        rows = connection.execute("SELECT * FROM content_exercise_overrides").fetchall()
        for row in rows:
            exercise_type = (row["exercise_type"] or "").strip()
            difficulty = (row["difficulty"] or "").strip()
            updates = []
            params = []
            if exercise_type:
                updates.append("exercise_type = ?")
                params.append(exercise_type)
            if difficulty:
                updates.append("difficulty = ?")
                params.append(difficulty)
            if not updates:
                continue
            params.append(row["exercise_id"])
            connection.execute(
                f"UPDATE exercises SET {', '.join(updates)} WHERE id = ?",
                tuple(params),
            )

    cms._apply_exercise_overrides = apply_exercise_overrides

    _content_questions.original = cms._content_questions
    cms._content_questions = _content_questions

    _edit_question.original = cms._edit_question
    cms._edit_question = _edit_question

    _content_dispatch.original = cms._content_dispatch
    cms._content_dispatch = _content_dispatch

    _PATCHED = True


apply()
