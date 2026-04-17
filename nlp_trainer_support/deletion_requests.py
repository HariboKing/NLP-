from __future__ import annotations

import sqlite3

from . import db


def ensure_schema(connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS deletion_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_type TEXT NOT NULL,
            requested_by_user_id INTEGER NOT NULL,
            requester_email_snapshot TEXT NOT NULL,
            requester_name_snapshot TEXT NOT NULL,
            target_user_id INTEGER NULL,
            target_organization_id INTEGER NULL,
            target_label TEXT NOT NULL,
            reason TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            decision_note TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            decided_at TEXT NULL,
            decided_by_user_id INTEGER NULL
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_deletion_requests_status_created
        ON deletion_requests(status, created_at)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_deletion_requests_target_user
        ON deletion_requests(target_user_id, status)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_deletion_requests_target_org
        ON deletion_requests(target_organization_id, status)
        """
    )


def get_request(connection, request_id: int):
    ensure_schema(connection)
    return connection.execute(
        """
        SELECT *
        FROM deletion_requests
        WHERE id = ?
        """,
        (request_id,),
    ).fetchone()


def get_pending_user_request(connection, user_id: int):
    ensure_schema(connection)
    return connection.execute(
        """
        SELECT *
        FROM deletion_requests
        WHERE request_type = 'user'
          AND target_user_id = ?
          AND status = 'pending'
        ORDER BY created_at DESC, id DESC
        LIMIT 1
        """,
        (user_id,),
    ).fetchone()


def get_pending_organization_request(connection, organization_id: int):
    ensure_schema(connection)
    return connection.execute(
        """
        SELECT *
        FROM deletion_requests
        WHERE request_type = 'organization'
          AND target_organization_id = ?
          AND status = 'pending'
        ORDER BY created_at DESC, id DESC
        LIMIT 1
        """,
        (organization_id,),
    ).fetchone()


def list_requests(connection, *, status: str | None = None, limit: int | None = None) -> list[sqlite3.Row]:
    ensure_schema(connection)
    sql = """
        SELECT *
        FROM deletion_requests
    """
    params: list[object] = []
    if status:
        sql += " WHERE status = ?"
        params.append(status)
    sql += " ORDER BY created_at DESC, id DESC"
    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)
    return connection.execute(sql, tuple(params)).fetchall()


def create_user_deletion_request(connection, *, user_id: int, reason: str):
    ensure_schema(connection)
    user = connection.execute(
        """
        SELECT id, email, first_name, last_name, is_platform_admin
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()
    if not user:
        raise ValueError("Account niet gevonden.")
    if user["is_platform_admin"]:
        raise ValueError("De platformeigenaar kan geen verwijderverzoek voor zichzelf indienen.")

    existing = get_pending_user_request(connection, user_id)
    if existing:
        return existing

    requester_name = f"{user['first_name']} {user['last_name']}".strip()
    cursor = connection.execute(
        """
        INSERT INTO deletion_requests (
            request_type,
            requested_by_user_id,
            requester_email_snapshot,
            requester_name_snapshot,
            target_user_id,
            target_organization_id,
            target_label,
            reason,
            status,
            decision_note,
            created_at,
            decided_at,
            decided_by_user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', '', ?, NULL, NULL)
        """,
        (
            "user",
            user["id"],
            user["email"],
            requester_name,
            user["id"],
            None,
            f"{requester_name} ({user['email']})",
            reason.strip(),
            db.utc_now_iso(),
        ),
    )
    return get_request(connection, cursor.lastrowid)


def create_organization_deletion_request(
    connection,
    *,
    organization_id: int,
    requested_by_user_id: int,
    reason: str,
):
    ensure_schema(connection)
    organization = connection.execute(
        """
        SELECT id, name
        FROM organizations
        WHERE id = ?
        """,
        (organization_id,),
    ).fetchone()
    if not organization:
        raise ValueError("Organisatie niet gevonden.")

    requester = connection.execute(
        """
        SELECT id, email, first_name, last_name
        FROM users
        WHERE id = ?
        """,
        (requested_by_user_id,),
    ).fetchone()
    if not requester:
        raise ValueError("Aanvrager niet gevonden.")

    existing = get_pending_organization_request(connection, organization_id)
    if existing:
        return existing

    requester_name = f"{requester['first_name']} {requester['last_name']}".strip()
    cursor = connection.execute(
        """
        INSERT INTO deletion_requests (
            request_type,
            requested_by_user_id,
            requester_email_snapshot,
            requester_name_snapshot,
            target_user_id,
            target_organization_id,
            target_label,
            reason,
            status,
            decision_note,
            created_at,
            decided_at,
            decided_by_user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', '', ?, NULL, NULL)
        """,
        (
            "organization",
            requester["id"],
            requester["email"],
            requester_name,
            None,
            organization["id"],
            organization["name"],
            reason.strip(),
            db.utc_now_iso(),
        ),
    )
    return get_request(connection, cursor.lastrowid)


def deny_request(connection, *, request_id: int, decided_by_user_id: int, note: str = ""):
    ensure_schema(connection)
    request_row = get_request(connection, request_id)
    if not request_row:
        raise ValueError("Verwijderverzoek niet gevonden.")
    if request_row["status"] != "pending":
        raise ValueError("Alleen openstaande verwijderverzoeken kunnen worden afgewezen.")

    connection.execute(
        """
        UPDATE deletion_requests
        SET status = 'denied',
            decision_note = ?,
            decided_at = ?,
            decided_by_user_id = ?
        WHERE id = ?
        """,
        (note.strip(), db.utc_now_iso(), decided_by_user_id, request_id),
    )
    return get_request(connection, request_id)


def approve_request(connection, *, request_id: int, decided_by_user_id: int, note: str = ""):
    ensure_schema(connection)
    request_row = get_request(connection, request_id)
    if not request_row:
        raise ValueError("Verwijderverzoek niet gevonden.")
    if request_row["status"] != "pending":
        raise ValueError("Alleen openstaande verwijderverzoeken kunnen worden goedgekeurd.")

    if request_row["request_type"] == "user":
        if request_row["target_user_id"] is None:
            raise ValueError("Dit accountverzoek heeft geen doelaccount.")
        delete_user_account(connection, int(request_row["target_user_id"]))
    elif request_row["request_type"] == "organization":
        if request_row["target_organization_id"] is None:
            raise ValueError("Dit organisatieverzoek heeft geen doelorganisatie.")
        delete_organization(connection, int(request_row["target_organization_id"]), request_row["id"], decided_by_user_id)
    else:
        raise ValueError("Onbekend verwijderverzoektype.")

    connection.execute(
        """
        UPDATE deletion_requests
        SET status = 'approved',
            decision_note = ?,
            decided_at = ?,
            decided_by_user_id = ?
        WHERE id = ?
        """,
        (note.strip(), db.utc_now_iso(), decided_by_user_id, request_id),
    )
    return get_request(connection, request_id)


def delete_user_account(connection, user_id: int) -> None:
    user = connection.execute(
        """
        SELECT id, is_platform_admin
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()
    if not user:
        return
    if user["is_platform_admin"]:
        raise ValueError("Het platformowner-account kan niet worden verwijderd.")

    connection.execute(
        "UPDATE users SET managed_by_user_id = NULL WHERE managed_by_user_id = ?",
        (user_id,),
    )
    connection.execute("DELETE FROM users WHERE id = ?", (user_id,))


def delete_organization(connection, organization_id: int, current_request_id: int, decided_by_user_id: int) -> None:
    members = connection.execute(
        """
        SELECT users.id,
               users.is_platform_admin,
               COUNT(DISTINCT memberships.organization_id) AS membership_count
        FROM memberships
        JOIN users ON users.id = memberships.user_id
        WHERE memberships.organization_id = ?
        GROUP BY users.id, users.is_platform_admin
        ORDER BY users.id
        """,
        (organization_id,),
    ).fetchall()
    member_ids = [int(row["id"]) for row in members]
    if member_ids:
        placeholders = ",".join("?" for _ in member_ids)
        connection.execute(
            f"""
            UPDATE users
            SET managed_by_user_id = NULL
            WHERE managed_by_user_id IN ({placeholders})
            """,
            tuple(member_ids),
        )
        connection.execute(
            f"""
            UPDATE deletion_requests
            SET status = 'approved',
                decision_note = 'Automatisch verwerkt via organisatieverwijdering.',
                decided_at = ?,
                decided_by_user_id = ?
            WHERE status = 'pending'
              AND id <> ?
              AND (
                    target_organization_id = ?
                    OR target_user_id IN ({placeholders})
                  )
            """,
            (db.utc_now_iso(), decided_by_user_id, current_request_id, organization_id, *member_ids),
        )
    else:
        connection.execute(
            """
            UPDATE deletion_requests
            SET status = 'approved',
                decision_note = 'Automatisch verwerkt via organisatieverwijdering.',
                decided_at = ?,
                decided_by_user_id = ?
            WHERE status = 'pending'
              AND id <> ?
              AND target_organization_id = ?
            """,
            (db.utc_now_iso(), decided_by_user_id, current_request_id, organization_id),
        )

    for member in members:
        if member["is_platform_admin"]:
            continue
        if int(member["membership_count"] or 0) <= 1:
            delete_user_account(connection, int(member["id"]))

    connection.execute("DELETE FROM organizations WHERE id = ?", (organization_id,))
