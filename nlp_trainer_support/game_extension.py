from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from urllib.parse import quote_plus

from . import db
from .scoring import score_submission
from .web import Response, WebApp, format_score, h, parse_json

_PATCHED = False
_GAME_MAX_LIVES = 5
_GAME_EXERCISE_TYPES = {
    "multiple_choice",
    "multi_select",
    "match_pairs",
    "short_answer",
    "text_analysis",
}


def _ensure_game_schema(connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS game_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            lives_remaining INTEGER NOT NULL DEFAULT 5,
            max_lives INTEGER NOT NULL DEFAULT 5,
            last_refill_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS game_unit_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            unit_key TEXT NOT NULL,
            unit_title TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            queue_json TEXT NOT NULL,
            current_position INTEGER NOT NULL DEFAULT 0,
            answered_json TEXT NOT NULL DEFAULT '[]',
            correct_json TEXT NOT NULL DEFAULT '[]',
            results_json TEXT NOT NULL DEFAULT '{}',
            last_result_json TEXT NOT NULL DEFAULT '{}',
            last_response_json TEXT NOT NULL DEFAULT '{}',
            last_exercise_id INTEGER NULL,
            lives_spent INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'active',
            last_score DOUBLE PRECISION NULL,
            best_score DOUBLE PRECISION NULL,
            started_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            completed_at TEXT NULL,
            UNIQUE (user_id, module_id, unit_key),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
            FOREIGN KEY (last_exercise_id) REFERENCES exercises(id) ON DELETE SET NULL
        )
        """
    )


def _game_slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", (value or "").strip().lower())
    return cleaned.strip("-") or "unit"


def _chunk_list(values: list, size: int) -> list[list]:
    if size <= 0:
        return [values]
    return [values[index:index + size] for index in range(0, len(values), size)]


def _game_has_unlimited_lives(self: WebApp, context: dict) -> bool:
    if self.is_platform_owner(context):
        return True
    if context.get("active_membership"):
        return True
    return self.is_public_user(context) and self.public_has_full_access(context)


def _get_game_profile(connection, user_id: int):
    return connection.execute(
        """
        SELECT *
        FROM game_profiles
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()


def _ensure_game_profile(connection, user_id: int, max_lives: int = _GAME_MAX_LIVES):
    profile = _get_game_profile(connection, user_id)
    if profile:
        return profile
    now = db.utc_now_iso()
    connection.execute(
        """
        INSERT INTO game_profiles (user_id, lives_remaining, max_lives, last_refill_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, max_lives, max_lives, now, now),
    )
    return _get_game_profile(connection, user_id)


def _refresh_game_lives(connection, user_id: int, max_lives: int = _GAME_MAX_LIVES):
    profile = _ensure_game_profile(connection, user_id, max_lives=max_lives)
    now = db.utc_now()
    try:
        last_refill_at = datetime.fromisoformat(profile["last_refill_at"])
        if last_refill_at.tzinfo is None:
            last_refill_at = last_refill_at.replace(tzinfo=timezone.utc)
        needs_refill = last_refill_at.date() < now.date()
    except (TypeError, ValueError):
        needs_refill = True

    if needs_refill or int(profile["max_lives"]) != int(max_lives):
        now_iso = db.utc_now_iso()
        connection.execute(
            """
            UPDATE game_profiles
            SET lives_remaining = ?, max_lives = ?, last_refill_at = ?, updated_at = ?
            WHERE user_id = ?
            """,
            (max_lives, max_lives, now_iso, now_iso, user_id),
        )
        return _get_game_profile(connection, user_id)
    return profile


def _spend_game_life(connection, user_id: int, max_lives: int = _GAME_MAX_LIVES):
    profile = _refresh_game_lives(connection, user_id, max_lives=max_lives)
    remaining = max(0, int(profile["lives_remaining"]))
    if remaining <= 0:
        return profile
    connection.execute(
        """
        UPDATE game_profiles
        SET lives_remaining = ?, updated_at = ?
        WHERE user_id = ?
        """,
        (remaining - 1, db.utc_now_iso(), user_id),
    )
    return _get_game_profile(connection, user_id)


def _game_profile_state(self: WebApp, connection, context: dict) -> dict:
    if _game_has_unlimited_lives(self, context):
        return {
            "unlimited": True,
            "lives_remaining": None,
            "max_lives": None,
            "label": "Onbeperkt",
        }

    profile = _refresh_game_lives(connection, int(context["user"]["user_id"]))
    return {
        "unlimited": False,
        "lives_remaining": int(profile["lives_remaining"]),
        "max_lives": int(profile["max_lives"]),
        "label": f"{profile['lives_remaining']}/{profile['max_lives']}",
    }


def _game_modules(connection) -> list[dict]:
    return [
        dict(row)
        for row in connection.execute(
            """
            SELECT id, title, summary, sort_order
            FROM modules
            ORDER BY sort_order, id
            """
        ).fetchall()
    ]


def _game_exercises(connection, module_id: int) -> list[dict]:
    return [
        dict(row)
        for row in connection.execute(
            """
            SELECT exercises.*, COALESCE(topics.title, 'Algemene les') AS topic_title,
                   COALESCE(topics.sort_order, 9999) AS topic_sort_order
            FROM exercises
            LEFT JOIN topics ON topics.id = exercises.topic_id
            WHERE exercises.module_id = ?
              AND exercises.status = 'published'
              AND COALESCE(exercises.requires_manual_review, 0) = 0
            ORDER BY topic_sort_order, exercises.id
            """,
            (module_id,),
        ).fetchall()
        if row["exercise_type"] in _GAME_EXERCISE_TYPES
    ]


def _build_game_units(exercises: list[dict]) -> list[dict]:
    if not exercises:
        return []

    groups = []
    for exercise in exercises:
        marker = (exercise.get("topic_id") or 0, exercise.get("topic_title") or "Algemene les")
        if not groups or groups[-1]["marker"] != marker:
            groups.append({"marker": marker, "title": marker[1], "items": []})
        groups[-1]["items"].append(exercise)

    units = []
    for group_index, group in enumerate(groups, start=1):
        chunks = _chunk_list(group["items"], 10)
        topic_id = group["marker"][0] or group_index
        for chunk_index, chunk in enumerate(chunks, start=1):
            suffix = f"-{chunk_index}" if len(chunks) > 1 else ""
            units.append(
                {
                    "key": f"{_game_slug(group['title'])}-{topic_id}{suffix}",
                    "title": group["title"] if len(chunks) == 1 else f"{group['title']} - unit {chunk_index}",
                    "exercise_ids": [int(exercise["id"]) for exercise in chunk],
                    "question_count": len(chunk),
                }
            )
    return units


def _list_game_progress(connection, user_id: int) -> list[dict]:
    return [
        dict(row)
        for row in connection.execute(
            """
            SELECT *
            FROM game_unit_progress
            WHERE user_id = ?
            ORDER BY updated_at DESC, id DESC
            """,
            (user_id,),
        ).fetchall()
    ]


def _get_game_progress(connection, user_id: int, module_id: int, unit_key: str):
    return connection.execute(
        """
        SELECT *
        FROM game_unit_progress
        WHERE user_id = ? AND module_id = ? AND unit_key = ?
        """,
        (user_id, module_id, unit_key),
    ).fetchone()


def _save_game_progress(connection, payload: dict):
    existing = _get_game_progress(
        connection,
        int(payload["user_id"]),
        int(payload["module_id"]),
        str(payload["unit_key"]),
    )
    queue_json = json.dumps(payload.get("queue", []))
    answered_json = json.dumps(payload.get("answered", []))
    correct_json = json.dumps(payload.get("correct", []))
    results_json = json.dumps(payload.get("results", {}))
    last_result_json = json.dumps(payload.get("last_result", {}))
    last_response_json = json.dumps(payload.get("last_response", {}))
    updated_at = payload.get("updated_at") or db.utc_now_iso()

    if existing:
        connection.execute(
            """
            UPDATE game_unit_progress
            SET unit_title = ?, total_questions = ?, queue_json = ?, current_position = ?,
                answered_json = ?, correct_json = ?, results_json = ?, last_result_json = ?,
                last_response_json = ?, last_exercise_id = ?, lives_spent = ?, status = ?,
                last_score = ?, best_score = ?, updated_at = ?, completed_at = ?
            WHERE user_id = ? AND module_id = ? AND unit_key = ?
            """,
            (
                payload["unit_title"],
                int(payload["total_questions"]),
                queue_json,
                int(payload["current_position"]),
                answered_json,
                correct_json,
                results_json,
                last_result_json,
                last_response_json,
                payload.get("last_exercise_id"),
                int(payload.get("lives_spent", 0)),
                payload["status"],
                payload.get("last_score"),
                payload.get("best_score"),
                updated_at,
                payload.get("completed_at"),
                int(payload["user_id"]),
                int(payload["module_id"]),
                payload["unit_key"],
            ),
        )
    else:
        connection.execute(
            """
            INSERT INTO game_unit_progress (
                user_id, module_id, unit_key, unit_title, total_questions, queue_json, current_position,
                answered_json, correct_json, results_json, last_result_json, last_response_json,
                last_exercise_id, lives_spent, status, last_score, best_score, started_at, updated_at, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(payload["user_id"]),
                int(payload["module_id"]),
                payload["unit_key"],
                payload["unit_title"],
                int(payload["total_questions"]),
                queue_json,
                int(payload["current_position"]),
                answered_json,
                correct_json,
                results_json,
                last_result_json,
                last_response_json,
                payload.get("last_exercise_id"),
                int(payload.get("lives_spent", 0)),
                payload["status"],
                payload.get("last_score"),
                payload.get("best_score"),
                payload.get("started_at") or updated_at,
                updated_at,
                payload.get("completed_at"),
            ),
        )
    return _get_game_progress(connection, int(payload["user_id"]), int(payload["module_id"]), str(payload["unit_key"]))


def _reset_game_progress(connection, user_id: int, module_id: int, unit_key: str) -> None:
    connection.execute(
        """
        DELETE FROM game_unit_progress
        WHERE user_id = ? AND module_id = ? AND unit_key = ?
        """,
        (user_id, module_id, unit_key),
    )


def _render_game_style_block() -> str:
    return """
    <style>
      .game-board { display: grid; gap: 1.25rem; }
      .game-hero { display: grid; gap: 1rem; align-items: start; }
      .game-life-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.8rem 1rem;
        border-radius: 999px;
        background: rgba(228, 140, 82, 0.14);
        border: 1px solid rgba(228, 140, 82, 0.28);
        font-weight: 700;
      }
      .game-life-badge small {
        display: block;
        font-size: 0.78rem;
        font-weight: 500;
        color: #5b6672;
      }
      .game-section-panel { overflow: hidden; }
      .game-section-header {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: flex-start;
        margin-bottom: 1rem;
      }
      .game-section-label {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #5b6672;
      }
      .game-section-index {
        display: inline-flex;
        width: 2rem;
        height: 2rem;
        align-items: center;
        justify-content: center;
        border-radius: 999px;
        background: rgba(36, 92, 115, 0.12);
        color: var(--primary);
        font-weight: 700;
      }
      .game-section-status {
        padding: 0.4rem 0.7rem;
        border-radius: 999px;
        background: rgba(36, 92, 115, 0.08);
        color: var(--primary);
        font-size: 0.82rem;
        font-weight: 600;
      }
      .game-unit-track {
        display: flex;
        flex-wrap: wrap;
        gap: 0.9rem;
      }
      .game-unit-node {
        min-width: 12rem;
        max-width: 15rem;
        flex: 1 1 12rem;
        display: grid;
        gap: 0.35rem;
        padding: 1rem;
        border-radius: 1rem;
        border: 1px solid rgba(36, 92, 115, 0.16);
        background: #fff;
        text-decoration: none;
        color: inherit;
        box-shadow: 0 14px 32px rgba(18, 42, 66, 0.06);
      }
      .game-unit-node strong { font-size: 1rem; }
      .game-unit-node small { color: #5b6672; }
      .game-unit-node.active {
        border-color: rgba(36, 92, 115, 0.32);
        box-shadow: 0 18px 38px rgba(36, 92, 115, 0.12);
      }
      .game-unit-node.completed {
        border-color: rgba(69, 149, 104, 0.3);
        background: linear-gradient(180deg, rgba(69,149,104,0.08), #fff);
      }
      .game-unit-node.locked,
      .game-unit-node.upgrade {
        opacity: 0.75;
        background: rgba(15, 23, 42, 0.03);
        box-shadow: none;
      }
      .game-unit-node.upgrade {
        border-style: dashed;
        border-color: rgba(228, 140, 82, 0.32);
      }
      .game-unit-step {
        width: 2.1rem;
        height: 2.1rem;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        background: rgba(36, 92, 115, 0.12);
        color: var(--primary);
      }
      .game-unit-node.completed .game-unit-step {
        background: rgba(69, 149, 104, 0.18);
        color: #2c6d49;
      }
      .game-unit-node.locked .game-unit-step,
      .game-unit-node.upgrade .game-unit-step {
        background: rgba(91, 102, 114, 0.16);
        color: #5b6672;
      }
      .game-summary-list {
        display: grid;
        gap: 0.8rem;
      }
      .game-summary-row {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.85rem 1rem;
        border-radius: 0.9rem;
        background: rgba(36, 92, 115, 0.05);
      }
      .game-summary-row span:last-child {
        font-weight: 700;
      }
      .game-feedback-note {
        padding: 0.85rem 1rem;
        border-radius: 0.9rem;
        background: rgba(228, 140, 82, 0.1);
      }
    </style>
    """


def _build_game_unit_url(module_id: int, unit_key: str, position: int | None = None, feedback: bool = False) -> str:
    base_url = f"/game/modules/{module_id}/units/{unit_key}"
    query_parts = []
    if position is not None:
        query_parts.append(f"position={position}")
    if feedback:
        query_parts.append("feedback=1")
    if not query_parts:
        return base_url
    return base_url + "?" + "&".join(query_parts)


def _build_game_sections(self: WebApp, connection, context: dict) -> list[dict]:
    user_id = int(context["user"]["user_id"])
    progress_rows = _list_game_progress(connection, user_id)
    progress_map = {(int(row["module_id"]), row["unit_key"]): row for row in progress_rows}
    sections = []
    previous_section_completed = True

    for section_index, module in enumerate(_game_modules(connection), start=1):
        access_granted = self.public_can_access_module(connection, context, int(module["id"]))
        units = _build_game_units(_game_exercises(connection, int(module["id"])))
        section_locked = access_granted and not previous_section_completed
        section_completed = bool(units)
        first_incomplete_found = False
        unit_rows = []

        for unit_index, unit in enumerate(units, start=1):
            progress = progress_map.get((int(module["id"]), unit["key"]))
            completed = bool(progress and progress["status"] == "completed")
            started = bool(progress and int(progress["current_position"]) > 0)
            if not completed:
                section_completed = False

            if not access_granted:
                status = "upgrade"
            elif section_locked:
                status = "locked"
            elif completed:
                status = "completed"
            elif not first_incomplete_found:
                status = "active"
                first_incomplete_found = True
            else:
                status = "locked"

            unit_rows.append(
                {
                    **unit,
                    "index": unit_index,
                    "status": status,
                    "started": started,
                    "progress": progress,
                }
            )

        if access_granted and units and not section_completed:
            previous_section_completed = False

        if not access_granted:
            section_status = "Upgrade"
        elif section_locked:
            section_status = "Vergrendeld"
        elif not units:
            section_status = "In aanbouw"
        elif section_completed:
            section_status = "Voltooid"
        else:
            section_status = "Beschikbaar"

        sections.append(
            {
                "index": section_index,
                "module": module,
                "status": section_status,
                "requires_upgrade": not access_granted,
                "locked": section_locked,
                "completed": section_completed and bool(units),
                "units": unit_rows,
                "completed_units": len([unit for unit in unit_rows if unit["status"] == "completed"]),
            }
        )
    return sections


def _locate_game_unit(sections: list[dict], module_id: int, unit_key: str):
    for section in sections:
        if int(section["module"]["id"]) != int(module_id):
            continue
        for unit in section["units"]:
            if unit["key"] == unit_key:
                return section, unit
    return None, None


def _game_page(self: WebApp, connection, request, context: dict):
    profile = _game_profile_state(self, connection, context)
    sections = _build_game_sections(self, connection, context)
    total_units = sum(len(section["units"]) for section in sections)
    completed_units = sum(section["completed_units"] for section in sections)
    accessible_sections = len([section for section in sections if not section["requires_upgrade"]])
    life_detail = (
        "<span class='game-life-badge'>Levens <span>Onbeperkt</span><small>Betaalde toegang of organisatieaccount</small></span>"
        if profile["unlimited"]
        else (
            "<span class='game-life-badge'>Levens "
            f"<span>{profile['lives_remaining']}/{profile['max_lives']}</span>"
            "<small>Gratis accounts krijgen dagelijks opnieuw maximaal 5 levens.</small></span>"
        )
    )

    section_html = []
    for section in sections:
        module = section["module"]
        if not section["units"]:
            unit_track = "<p class='helper'>Voor deze sectie staan nog geen game-units klaar.</p>"
        else:
            nodes = []
            for unit in section["units"]:
                subtitle = f"{unit['question_count']} vragen"
                progress = unit["progress"] or {}
                if progress and progress.get("last_score") is not None:
                    subtitle += f" - {format_score(progress['last_score'])}"
                if unit["status"] == "completed":
                    href = f"/game/modules/{module['id']}/units/{unit['key']}/complete"
                    nodes.append(
                        "<a class='game-unit-node completed' href='"
                        + h(href)
                        + "'>"
                        + f"<span class='game-unit-step'>{unit['index']}</span>"
                        + f"<strong>{h(unit['title'])}</strong>"
                        + f"<small>{h(subtitle)}</small>"
                        + "<small>Voltooid</small>"
                        + "</a>"
                    )
                elif unit["status"] == "active":
                    href = _build_game_unit_url(int(module["id"]), unit["key"])
                    action_label = "Ga verder" if unit["started"] else "Start unit"
                    nodes.append(
                        "<a class='game-unit-node active' href='"
                        + h(href)
                        + "'>"
                        + f"<span class='game-unit-step'>{unit['index']}</span>"
                        + f"<strong>{h(unit['title'])}</strong>"
                        + f"<small>{h(subtitle)}</small>"
                        + f"<small>{h(action_label)}</small>"
                        + "</a>"
                    )
                elif unit["status"] == "upgrade":
                    nodes.append(
                        "<a class='game-unit-node upgrade' href='/pricing'>"
                        + f"<span class='game-unit-step'>{unit['index']}</span>"
                        + f"<strong>{h(unit['title'])}</strong>"
                        + f"<small>{h(subtitle)}</small>"
                        + "<small>Upgrade nodig</small>"
                        + "</a>"
                    )
                else:
                    nodes.append(
                        "<span class='game-unit-node locked'>"
                        + f"<span class='game-unit-step'>{unit['index']}</span>"
                        + f"<strong>{h(unit['title'])}</strong>"
                        + f"<small>{h(subtitle)}</small>"
                        + "<small>Rond eerst eerdere units af</small>"
                        + "</span>"
                    )
            unit_track = "<div class='game-unit-track'>" + "".join(nodes) + "</div>"

        section_html.append(
            "<section class='panel game-section-panel'>"
            "<div class='game-section-header'>"
            "<div>"
            + f"<div class='game-section-label'><span class='game-section-index'>{section['index']}</span> Sectie {section['index']}</div>"
            + f"<h2>{h(module['title'])}</h2>"
            + f"<p>{h(module['summary'])}</p>"
            + "</div>"
            + f"<span class='game-section-status'>{h(section['status'])}</span>"
            + "</div>"
            + unit_track
            + "</section>"
        )

    body = [
        _render_game_style_block(),
        "<section class='hero compact game-hero'><div><span class='eyebrow'>The Game</span><h1>Visueel leerpad</h1><p>Werk per sectie en per unit door het curriculum. Iedere unit is een compacte quiz van maximaal tien vragen. Eerst de standaardomgeving, daarnaast een spelmodus met progressie, locks en levens.</p></div><div class='actions'>"
        + life_detail
        + "</div></section>",
        self.metrics_row(
            [
                ("Secties", str(len(sections))),
                ("Beschikbaar", str(accessible_sections)),
                ("Units afgerond", f"{completed_units}/{total_units}" if total_units else "0/0"),
            ]
        ),
        "<section class='panel'><h2>Hoe The Game werkt</h2><div class='game-summary-list'>"
        + "<div class='game-summary-row'><span>Secties</span><span>Ieder verdiepingspad is nu een sectie</span></div>"
        + "<div class='game-summary-row'><span>Units</span><span>Iedere unit is een mini-quiz van 1 tot 10 vragen</span></div>"
        + "<div class='game-summary-row'><span>Progressie</span><span>Nieuwe units openen pas nadat de vorige is afgerond</span></div>"
        + "</div></section>",
        "<div class='game-board'>"
        + "".join(section_html)
        + "</div>",
    ]
    return self.html("The Game", "".join(body), context)


def _game_unit_page(self: WebApp, connection, request, context: dict, module_id: int, unit_key: str):
    sections = _build_game_sections(self, connection, context)
    section, unit = _locate_game_unit(sections, module_id, unit_key)
    if not section or not unit:
        return self.not_found(context)
    if unit["status"] == "upgrade":
        return self.upgrade_required_page(context, "The Game", section["module"]["title"])
    if unit["status"] == "locked":
        return self.forbidden(context, "Rond eerst eerdere units of secties af in The Game.")

    if request.get("restart") == "1":
        _reset_game_progress(connection, int(context["user"]["user_id"]), module_id, unit_key)
        connection.commit()
        return self.redirect(_build_game_unit_url(module_id, unit_key))

    profile = _game_profile_state(self, connection, context)
    exercises = _game_exercises(connection, module_id)
    exercise_lookup = {int(exercise["id"]): exercise for exercise in exercises}
    base_queue = [exercise_id for exercise_id in unit["exercise_ids"] if exercise_id in exercise_lookup]
    if not base_queue:
        return self.html(
            "The Game",
            _render_game_style_block()
            + "<section class='panel'><h1>Geen vragen gevonden</h1><p>Voor deze unit staan nog geen speelbare vragen klaar.</p></section>",
            context,
        )

    progress = _get_game_progress(connection, int(context["user"]["user_id"]), module_id, unit_key)
    if not progress:
        progress = _save_game_progress(
            connection,
            {
                "user_id": int(context["user"]["user_id"]),
                "module_id": module_id,
                "unit_key": unit_key,
                "unit_title": unit["title"],
                "total_questions": len(base_queue),
                "queue": base_queue,
                "current_position": 0,
                "answered": [],
                "correct": [],
                "results": {},
                "last_result": {},
                "last_response": {},
                "last_exercise_id": None,
                "lives_spent": 0,
                "status": "active",
                "last_score": None,
                "best_score": None,
                "started_at": db.utc_now_iso(),
                "completed_at": None,
            },
        )
        connection.commit()

    queue = [
        exercise_id
        for exercise_id in parse_json(progress["queue_json"], [])
        if exercise_id in exercise_lookup
    ] or list(base_queue)

    try:
        saved_position = int(progress["current_position"])
    except (TypeError, ValueError):
        saved_position = 0

    feedback_mode = request.get("feedback") == "1"
    try:
        feedback_position = int(request.get("position", str(max(saved_position - 1, 0))))
    except ValueError:
        feedback_position = max(saved_position - 1, 0)

    if progress["status"] == "completed" and not feedback_mode:
        return self.redirect(f"/game/modules/{module_id}/units/{unit_key}/complete")

    if not profile["unlimited"] and int(profile["lives_remaining"]) <= 0 and not feedback_mode:
        body = (
            _render_game_style_block()
            + f"<section class='hero compact'><div><span class='eyebrow'>The Game</span><h1>{h(unit['title'])}</h1><p>Je hebt nu geen levens meer. Morgen wordt je gratis account opnieuw gevuld tot {_GAME_MAX_LIVES} levens, of upgrade naar volledige toegang voor onbeperkt spelen.</p></div></section>"
            + "<section class='panel'><div class='actions'>"
            + ("<a class='button button-primary' href='/pricing'>Upgrade voor onbeperkt spelen</a>" if self.is_public_user(context) else "")
            + "<a class='button button-secondary' href='/game'>Terug naar The Game</a>"
            + "</div></section>"
        )
        return self.html(f"{unit['title']} - geen levens", body, context)

    display_position = feedback_position if feedback_mode else saved_position
    display_position = max(0, min(display_position, len(queue) - 1))
    current_exercise = exercise_lookup[queue[display_position]]

    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")
        if not profile["unlimited"] and int(profile["lives_remaining"]) <= 0:
            return self.redirect("/game?notice=" + quote_plus("Je hebt geen levens meer voor The Game."))

        try:
            posted_position = int(request.get("position", str(saved_position)))
        except ValueError:
            posted_position = saved_position
        posted_position = max(0, min(posted_position, len(queue) - 1))
        try:
            posted_exercise_id = int(request.get("exercise_id", str(current_exercise["id"])))
        except ValueError:
            posted_exercise_id = current_exercise["id"]

        exercise = exercise_lookup.get(posted_exercise_id, current_exercise)
        response_payload = self.collect_response(exercise, request)
        result = score_submission(exercise, response_payload, "learn")
        passed = bool(result.get("passed"))
        life_lost = False

        if not passed and not profile["unlimited"]:
            profile = _game_profile_state(self, connection, context)
            if int(profile["lives_remaining"]) > 0:
                spent_profile = _spend_game_life(connection, int(context["user"]["user_id"]))
                profile = {
                    "unlimited": False,
                    "lives_remaining": int(spent_profile["lives_remaining"]),
                    "max_lives": int(spent_profile["max_lives"]),
                    "label": f"{spent_profile['lives_remaining']}/{spent_profile['max_lives']}",
                }
                life_lost = True

        answered = parse_json(progress["answered_json"], [])
        if exercise["id"] not in answered:
            answered.append(exercise["id"])
        correct = parse_json(progress["correct_json"], [])
        if passed and exercise["id"] not in correct:
            correct.append(exercise["id"])

        results = parse_json(progress["results_json"], {})
        results[str(exercise["id"])] = {
            "exercise_title": exercise["title"],
            "score": result["auto_score"],
            "max_score": result["max_score"],
            "passed": passed,
        }

        total_score = sum(float(item.get("score") or 0) for item in results.values())
        total_max_score = sum(float(item.get("max_score") or 0) for item in results.values()) or 1.0
        current_score = round((total_score / total_max_score) * 100, 1)
        previous_best = float(progress["best_score"] or 0)
        next_position = posted_position + 1
        status = "completed" if next_position >= len(queue) else "active"
        _save_game_progress(
            connection,
            {
                "user_id": int(context["user"]["user_id"]),
                "module_id": module_id,
                "unit_key": unit_key,
                "unit_title": unit["title"],
                "total_questions": len(queue),
                "queue": queue,
                "current_position": next_position,
                "answered": answered,
                "correct": correct,
                "results": results,
                "last_result": {
                    "feedback": result["feedback"],
                    "model_answer": result.get("model_answer", ""),
                    "auto_score": result["auto_score"],
                    "max_score": result["max_score"],
                    "passed": passed,
                    "life_lost": life_lost,
                },
                "last_response": response_payload,
                "last_exercise_id": exercise["id"],
                "lives_spent": int(progress["lives_spent"] or 0) + (1 if life_lost else 0),
                "status": status,
                "last_score": current_score,
                "best_score": max(previous_best, current_score),
                "started_at": progress["started_at"],
                "completed_at": db.utc_now_iso() if status == "completed" else None,
            },
        )
        connection.commit()
        return self.redirect(_build_game_unit_url(module_id, unit_key, position=posted_position, feedback=True))

    last_result = parse_json(progress["last_result_json"], {})
    last_response = parse_json(progress["last_response_json"], {})
    show_feedback = (
        feedback_mode
        and progress["last_exercise_id"] is not None
        and int(progress["last_exercise_id"]) == int(current_exercise["id"])
    )
    progress_percent = round(((display_position + 1) / len(queue)) * 100)
    lives_badge = "Onbeperkt" if profile["unlimited"] else f"{profile['lives_remaining']}/{profile['max_lives']} levens"

    if show_feedback:
        next_url = (
            f"/game/modules/{module_id}/units/{unit_key}/complete"
            if display_position + 1 >= len(queue)
            else _build_game_unit_url(module_id, unit_key)
        )
        next_label = "Unit afronden" if display_position + 1 >= len(queue) else "Volgende vraag"
        if not profile["unlimited"] and int(profile["lives_remaining"]) <= 0 and display_position + 1 < len(queue):
            next_url = "/pricing" if self.is_public_user(context) else "/game"
            next_label = "Terug naar overzicht"

        note_parts = []
        if last_result.get("passed"):
            note_parts.append("Goed genoeg om door te gaan naar de volgende vraag.")
        else:
            note_parts.append("Deze vraag was nog niet goed genoeg.")
        if last_result.get("life_lost") and not profile["unlimited"]:
            note_parts.append(f"Er is 1 leven afgeschreven. Resterend: {profile['lives_remaining']}/{profile['max_lives']}.")

        body = f"""
        {_render_game_style_block()}
        <section class='hero compact'>
          <div>
            <span class='eyebrow'>The Game - {h(section['module']['title'])}</span>
            <h1>{h(unit['title'])}</h1>
            <p>Vraag {display_position + 1} van {len(queue)} - {h(lives_badge)}</p>
          </div>
          <div class='progress-pill'>{progress_percent}%</div>
        </section>
        <section class='panel progress-panel'>
          <div class='progress-bar'><span style='width: {progress_percent}%;'></span></div>
          <p class='game-feedback-note'>{h(" ".join(note_parts))}</p>
        </section>
        <section class='panel quiz-feedback'>
          <h2>Feedback</h2>
          <p>{h(last_result.get('feedback') or 'Je antwoord is opgeslagen.')}</p>
          <div class='grid two-up'>
            <article class='panel inset'>
              <h3>Jouw antwoord</h3>
              {self.render_response_summary(current_exercise['exercise_type'], last_response)}
            </article>
            <article class='panel inset'>
              <h3>Modelantwoord</h3>
              <p>{h(last_result.get('model_answer') or 'Er is geen modelantwoord ingevuld.')}</p>
            </article>
          </div>
          <div class='actions'>
            <a class='button button-secondary' href='/game'>Terug naar The Game</a>
            <a class='button button-primary' href='{h(next_url)}'>{h(next_label)}</a>
          </div>
        </section>
        """
        return self.html(f"{unit['title']} - feedback", body, context)

    content = parse_json(current_exercise["content_json"], {})
    body = f"""
    {_render_game_style_block()}
    <section class='hero compact'>
      <div>
        <span class='eyebrow'>The Game - Sectie {section['index']}</span>
        <h1>{h(unit['title'])}</h1>
        <p>{h(section['module']['title'])} - Vraag {saved_position + 1} van {len(queue)} - {h(lives_badge)}</p>
      </div>
      <div class='progress-pill'>{progress_percent}%</div>
    </section>
    <section class='panel progress-panel'>
      <div class='progress-bar'><span style='width: {progress_percent}%;'></span></div>
      <p>Werk deze unit af om de volgende unit in het visuele leerpad vrij te spelen.</p>
      <p class='helper'>The Game gebruikt een aparte voortgang dan je standaard leeromgeving.</p>
    </section>
    <section class='panel exercise-panel'>
      <div class='exercise-header'>
        <div>
          <span class='eyebrow'>Vraag {saved_position + 1}</span>
          <h2>{h(current_exercise['title'])}</h2>
          <p>{h(current_exercise['prompt'])}</p>
        </div>
        <div class='tag-group'>
          <span class='tag'>{h(current_exercise['exercise_type'])}</span>
          <span class='tag'>{h(current_exercise['difficulty'])}</span>
        </div>
      </div>
      <form method='post' action='/game/modules/{module_id}/units/{unit_key}'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <input type='hidden' name='position' value='{saved_position}'>
        <input type='hidden' name='exercise_id' value='{current_exercise['id']}'>
        {self.render_exercise_form(current_exercise, content)}
        <div class='actions'>
          <a class='button button-secondary' href='/game'>Terug naar The Game</a>
          <button class='button button-primary' type='submit'>Antwoord indienen</button>
        </div>
      </form>
    </section>
    """
    return self.html(f"{unit['title']} - The Game", body, context)


def _game_unit_complete_page(self: WebApp, connection, request, context: dict, module_id: int, unit_key: str):
    if request.get("restart") == "1":
        _reset_game_progress(connection, int(context["user"]["user_id"]), module_id, unit_key)
        connection.commit()
        return self.redirect(_build_game_unit_url(module_id, unit_key))

    sections = _build_game_sections(self, connection, context)
    section, unit = _locate_game_unit(sections, module_id, unit_key)
    if not section or not unit:
        return self.not_found(context)
    if unit["status"] == "upgrade":
        return self.upgrade_required_page(context, "The Game", section["module"]["title"])

    progress = _get_game_progress(connection, int(context["user"]["user_id"]), module_id, unit_key)
    if not progress or progress["status"] != "completed":
        return self.redirect(_build_game_unit_url(module_id, unit_key))

    profile = _game_profile_state(self, connection, context)
    results = parse_json(progress["results_json"], {})
    queue = parse_json(progress["queue_json"], [])
    exercise_lookup = {int(exercise["id"]): exercise for exercise in _game_exercises(connection, module_id)}
    correct_ids = set(parse_json(progress["correct_json"], []))

    rows = []
    for exercise_id in queue:
        exercise = exercise_lookup.get(int(exercise_id))
        result = results.get(str(exercise_id), {})
        rows.append(
            [
                h(exercise["title"] if exercise else f"Vraag {exercise_id}"),
                h("Goed" if int(exercise_id) in correct_ids else "Nog niet goed"),
                format_score(result.get("score")),
            ]
        )

    next_url = "/game"
    next_label = "Terug naar overzicht"
    found_current = False
    for next_section in sections:
        for next_unit in next_section["units"]:
            if found_current and next_unit["status"] == "active":
                next_url = _build_game_unit_url(int(next_section["module"]["id"]), next_unit["key"])
                next_label = "Volgende unit"
                break
            if int(next_section["module"]["id"]) == module_id and next_unit["key"] == unit_key:
                found_current = True
        if next_label == "Volgende unit":
            break

    lives_value = "Onbeperkt" if profile["unlimited"] else f"{profile['lives_remaining']}/{profile['max_lives']}"
    body = [
        _render_game_style_block(),
        f"<section class='hero compact'><div><span class='eyebrow'>The Game - Sectie {section['index']}</span><h1>{h(unit['title'])} voltooid</h1><p>Deze unit is afgerond. Je kunt door naar de volgende unit of deze opnieuw spelen.</p></div><div class='actions'><a class='button button-primary' href='{h(next_url)}'>{h(next_label)}</a><a class='button button-secondary' href='/game/modules/{module_id}/units/{unit_key}/complete?restart=1'>Opnieuw spelen</a></div></section>",
        self.metrics_row(
            [
                ("Goed beantwoorde vragen", f"{len(correct_ids)}/{len(queue)}"),
                ("Score", format_score(progress["last_score"])),
                ("Levens", lives_value),
            ]
        ),
        "<section class='panel'><h2>Resultaten van deze unit</h2>"
        + self.render_table(["Vraag", "Status", "Score"], rows)
        + "</section>",
    ]
    return self.html(f"{unit['title']} voltooid", "".join(body), context)


def _render_nav(self: WebApp, context: dict) -> str:
    nav = _render_nav.original(self, context)
    if not context.get("user") or "/game" in nav:
        return nav
    return nav.replace(
        "<a class='nav-link' href='/dashboard'>Dashboard</a>",
        "<a class='nav-link' href='/dashboard'>Dashboard</a><a class='nav-link' href='/game'>The Game</a>",
        1,
    )


def _dispatch(self: WebApp, request):
    game_root = request.path == "/game"
    game_unit_match = re.fullmatch(r"/game/modules/(\d+)/units/([a-z0-9-]+)", request.path)
    game_complete_match = re.fullmatch(r"/game/modules/(\d+)/units/([a-z0-9-]+)/complete", request.path)
    if not (game_root or game_unit_match or game_complete_match):
        return _dispatch.original(self, request)

    with db.connect() as connection:
        context = self.get_context(connection, request)
        if not context["user"]:
            return self.redirect("/login")
        _ensure_game_schema(connection)
        if game_root:
            return _game_page(self, connection, request, context)
        if game_complete_match:
            return _game_unit_complete_page(
                self,
                connection,
                request,
                context,
                int(game_complete_match.group(1)),
                game_complete_match.group(2),
            )
        return _game_unit_page(
            self,
            connection,
            request,
            context,
            int(game_unit_match.group(1)),
            game_unit_match.group(2),
        )


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    original_render_nav = getattr(WebApp, "render_nav", None)
    if original_render_nav is not None:
        _render_nav.original = original_render_nav
        WebApp.render_nav = _render_nav

    original_dispatch = getattr(WebApp, "dispatch", None)
    if original_dispatch is not None:
        _dispatch.original = original_dispatch
        WebApp.dispatch = _dispatch

    _PATCHED = True


apply()
