from __future__ import annotations

from .web import WebApp, h

_PATCHED = False


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


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    WebApp.archive_page = _archive_page
    _PATCHED = True


apply()
