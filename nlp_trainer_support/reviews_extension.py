from __future__ import annotations

from .web import WebApp, h

_PATCHED = False


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    def review_queue(self: WebApp, connection, request, context: dict):
        if not self.require_role(context, {"trainer", "organization_admin"}):
            return self.forbidden(context)
        active = context["active_membership"]
        rows = connection.execute(
            """
            SELECT assignments.id, assignments.title, assignments.mode, assignments.due_date,
                   users.first_name AS creator_first_name, users.last_name AS creator_last_name,
                   COUNT(attempts.id) AS pending_items,
                   COUNT(DISTINCT attempts.user_id) AS pending_students,
                   MAX(attempts.submitted_at) AS latest_submission
            FROM attempts
            JOIN assignments ON assignments.id = attempts.assignment_id
            JOIN users ON users.id = assignments.created_by_user_id
            JOIN exercises ON exercises.id = attempts.exercise_id
            WHERE assignments.organization_id = ?
              AND attempts.status = 'submitted'
              AND exercises.requires_manual_review = 1
            GROUP BY assignments.id, assignments.title, assignments.mode, assignments.due_date,
                     users.first_name, users.last_name
            ORDER BY latest_submission DESC
            """,
            (active["organization_id"],),
        ).fetchall()
        content = (
            "<section class='panel'><h1>Open reviews</h1>"
            + self.render_table(
                ["Opdracht", "Mode", "Trainer", "Open vragen", "Studenten", "Laatste inzending", "Actie"],
                [
                    [
                        f"<a href='/assignments/{row['id']}'>{h(row['title'])}</a>",
                        h((row["mode"] or "").title()),
                        h(f"{row['creator_first_name']} {row['creator_last_name']}"),
                        h(row["pending_items"]),
                        h(row["pending_students"]),
                        h((row["latest_submission"] or "").replace("T", " ")),
                        f"<a class='button button-secondary small' href='/assignments/{row['id']}'>Verder gaan met beoordelen</a>",
                    ]
                    for row in rows
                ],
            )
            + "</section>"
        )
        return self.html("Reviews", content, context)

    WebApp.review_queue = review_queue
    _PATCHED = True


apply()
