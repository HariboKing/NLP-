from __future__ import annotations

from urllib.parse import quote_plus

from . import content_admin_extension as cms
from . import db
from .web import Response, WebApp, h

_PATCHED = False


def _is_platform_owner(context: dict) -> bool:
    user = context.get("user") or {}
    return bool(user.get("is_platform_admin") and not context.get("active_membership"))


def _ensure_editor_schema(connection) -> None:
    cms.ensure_content_schema(connection)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS content_admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            granted_by_user_id INTEGER NULL,
            created_at TEXT NOT NULL
        )
        """
    )


def _is_content_editor(connection, user_id: int | None) -> bool:
    if not user_id:
        return False
    _ensure_editor_schema(connection)
    row = connection.execute(
        "SELECT id FROM content_admin_users WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return row is not None


def _can_manage_content(*args) -> bool:
    if len(args) == 1:
        connection = None
        context = args[0]
    else:
        connection, context = args

    if context.get("_content_access_granted"):
        return True
    if _is_platform_owner(context):
        return True

    user = context.get("user") or {}
    user_id = user.get("user_id")
    if not user_id:
        return False

    if connection is not None:
        return _is_content_editor(connection, user_id)
    with db.connect() as nav_connection:
        return _is_content_editor(nav_connection, user_id)


def _inject_editor_card(response: Response, context: dict) -> Response:
    if not _is_platform_owner(context):
        return response
    body = response.body.decode("utf-8", errors="ignore")
    if "</main>" not in body or "/content/editors" in body:
        return response
    panel = (
        "<section class='panel inset'><h2>Contentbeheerders</h2>"
        "<p>Geef een bestaande gebruiker toegang tot inhoudsbeheer zonder owner-rechten.</p>"
        "<a class='button button-secondary' href='/content/editors'>Contentbeheerders beheren</a>"
        "</section>"
    )
    body = body.replace("</main>", panel + "</main>", 1)
    return Response(response.status, body.encode("utf-8"), list(response.headers))


def _content_editors_page(self: WebApp, connection, request, context: dict) -> Response:
    _ensure_editor_schema(connection)
    if not _is_platform_owner(context):
        return self.forbidden(context)

    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")

        action = request.get("action")
        if action == "add_editor":
            email = request.get("email").strip().lower()
            user = connection.execute(
                "SELECT id, email, first_name, last_name FROM users WHERE lower(email) = ? AND is_active = 1",
                (email,),
            ).fetchone()
            if not user:
                return self.redirect("/content/editors?notice=" + quote_plus("Geen actieve gebruiker gevonden met dit e-mailadres."))
            connection.execute(
                """
                INSERT INTO content_admin_users (user_id, granted_by_user_id, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT (user_id) DO UPDATE SET
                    granted_by_user_id = excluded.granted_by_user_id,
                    created_at = excluded.created_at
                """,
                (user["id"], context["user"]["user_id"], db.utc_now_iso()),
            )
            connection.commit()
            return self.redirect("/content/editors?notice=" + quote_plus("Contentbeheerder toegevoegd."))

        if action == "remove_editor":
            connection.execute(
                "DELETE FROM content_admin_users WHERE user_id = ?",
                (int(request.get("user_id")),),
            )
            connection.commit()
            return self.redirect("/content/editors?notice=" + quote_plus("Contentbeheerder verwijderd."))

    rows = connection.execute(
        """
        SELECT content_admin_users.user_id, content_admin_users.created_at,
               users.first_name, users.last_name, users.email
        FROM content_admin_users
        JOIN users ON users.id = content_admin_users.user_id
        ORDER BY users.last_name, users.first_name, users.email
        """
    ).fetchall()
    table_rows = [
        [
            h(f"{row['first_name']} {row['last_name']}".strip() or row["email"]),
            h(row["email"]),
            h((row["created_at"] or "").replace("T", " ")),
            (
                f"<form method='post' action='/content/editors'>"
                f"<input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>"
                f"<input type='hidden' name='user_id' value='{row['user_id']}'>"
                "<button class='button button-secondary small' type='submit' name='action' value='remove_editor'>Verwijderen</button>"
                "</form>"
            ),
        ]
        for row in rows
    ]
    body = f"""
    <section class='hero compact'><div><span class='eyebrow'>Contentbeheer</span><h1>Contentbeheerders</h1>
    <p>Voeg een bestaande gebruiker toe. Die gebruiker krijgt alleen toegang tot leerpaden, vragenflows en modellen.</p></div>
    <div class='actions'><a class='button button-secondary' href='/content'>Terug</a></div></section>
    <section class='panel form-panel'>
      <form method='post' action='/content/editors'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <input type='hidden' name='action' value='add_editor'>
        <label class='field'><span>E-mailadres bestaande gebruiker</span><input type='email' name='email' required></label>
        <button class='button button-primary' type='submit'>Toegang geven</button>
      </form>
    </section>
    <section class='panel'><h2>Huidige contentbeheerders</h2>{self.render_table(["Naam", "E-mail", "Toegevoegd", "Actie"], table_rows)}</section>
    """
    return self.html("Contentbeheerders", body, context)


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    original_ensure_content_schema = cms.ensure_content_schema

    def ensure_content_schema(connection) -> None:
        original_ensure_content_schema(connection)
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS content_admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                granted_by_user_id INTEGER NULL,
                created_at TEXT NOT NULL
            )
            """
        )

    cms.ensure_content_schema = ensure_content_schema
    cms._can_manage_content = _can_manage_content

    original_content_dispatch = cms._content_dispatch

    def content_dispatch(self: WebApp, connection, request, context: dict) -> Response:
        _ensure_editor_schema(connection)
        if request.path == "/content/editors":
            return _content_editors_page(self, connection, request, context)
        context["_content_access_granted"] = _can_manage_content(connection, context)
        return original_content_dispatch(self, connection, request, context)

    cms._content_dispatch = content_dispatch

    original_content_dashboard = cms._content_dashboard

    def content_dashboard(self: WebApp, connection, context: dict) -> Response:
        response = original_content_dashboard(self, connection, context)
        return _inject_editor_card(response, context)

    cms._content_dashboard = content_dashboard

    original_render_nav = WebApp.render_nav

    def render_nav(self: WebApp, context: dict) -> str:
        nav = original_render_nav(self, context)
        if "/content" in nav or not context.get("user"):
            return nav
        if _can_manage_content(context):
            return nav.replace(
                "<a class='nav-link' href='/logout'>Logout</a>",
                "<a class='nav-link' href='/content'>Contentbeheer</a><a class='nav-link' href='/logout'>Logout</a>",
                1,
            )
        return nav

    WebApp.render_nav = render_nav
    _PATCHED = True


apply()
