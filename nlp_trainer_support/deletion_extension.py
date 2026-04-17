from __future__ import annotations

from urllib.parse import quote_plus

from . import db, deletion_requests
from .web import Response, WebApp, h

_PATCHED = False


def _is_platform_owner(context: dict) -> bool:
    user = context.get("user")
    return bool(user and user.get("is_platform_admin") and not context.get("active_membership"))


def _inject_panel(response: Response, panel_html: str) -> Response:
    if not panel_html:
        return response
    body = response.body.decode("utf-8", errors="ignore")
    if "</main>" not in body:
        return response
    body = body.replace("</main>", panel_html + "</main>", 1)
    return Response(response.status, body.encode("utf-8"), list(response.headers))


def _deletion_request_page(self: WebApp, connection, request, context: dict) -> Response:
    if not context["user"]:
        return self.redirect("/login")

    if request.method == "GET":
        if _is_platform_owner(context):
            return self.platform_deletion_request_dashboard(connection, context)
        return self.redirect("/dashboard")

    if not self.verify_csrf(request, context):
        return self.forbidden(context, "Ongeldige CSRF token.")

    action = request.get("action")
    try:
        if action == "request_account_deletion":
            if _is_platform_owner(context):
                return self.forbidden(context, "Het owner-account kan geen verwijderverzoek voor zichzelf indienen.")
            deletion_requests.create_user_deletion_request(
                connection,
                user_id=context["user"]["user_id"],
                reason=request.get("reason").strip(),
            )
            connection.commit()
            return self.redirect(
                "/dashboard?notice="
                + quote_plus("Je verwijderverzoek is ingediend. Alleen de eigenaar kan dit goedkeuren of afwijzen.")
            )

        if action == "request_organization_deletion":
            if not self.require_role(context, {"organization_admin"}):
                return self.forbidden(context)
            deletion_requests.create_organization_deletion_request(
                connection,
                organization_id=context["active_membership"]["organization_id"],
                requested_by_user_id=context["user"]["user_id"],
                reason=request.get("reason").strip(),
            )
            connection.commit()
            return self.redirect(
                "/dashboard?notice="
                + quote_plus("Het organisatieverwijderverzoek is ingediend. Alleen de eigenaar kan dit goedkeuren of afwijzen.")
            )

        if action == "approve_deletion_request":
            if not _is_platform_owner(context):
                return self.forbidden(context)
            deletion_requests.approve_request(
                connection,
                request_id=int(request.get("request_id")),
                decided_by_user_id=context["user"]["user_id"],
                note=request.get("decision_note").strip(),
            )
            connection.commit()
            return self.redirect("/deletion-requests?notice=" + quote_plus("Verwijderverzoek goedgekeurd en uitgevoerd."))

        if action == "deny_deletion_request":
            if not _is_platform_owner(context):
                return self.forbidden(context)
            deletion_requests.deny_request(
                connection,
                request_id=int(request.get("request_id")),
                decided_by_user_id=context["user"]["user_id"],
                note=request.get("decision_note").strip(),
            )
            connection.commit()
            return self.redirect("/deletion-requests?notice=" + quote_plus("Verwijderverzoek afgewezen."))
    except ValueError as exc:
        target = "/deletion-requests" if _is_platform_owner(context) else "/dashboard"
        return self.redirect(target + "?notice=" + quote_plus(str(exc)))

    return self.not_found(context)


def _render_account_deletion_panels(self: WebApp, connection, context: dict) -> str:
    user = context.get("user")
    if not user or user.get("is_platform_admin"):
        return ""

    pending_account_request = deletion_requests.get_pending_user_request(connection, int(user["user_id"]))
    account_panel = (
        "<article class='panel inset'>"
        "<h2>Accountverwijdering</h2>"
        f"<p class='helper'>Je accountverwijderverzoek staat open sinds {h((pending_account_request['created_at'] or '').split('T')[0])}. Alleen de eigenaar kan dit goedkeuren of afwijzen.</p>"
        f"<p><strong>Status:</strong> {h(pending_account_request['status'])}</p>"
        "</article>"
        if pending_account_request
        else (
            "<article class='panel form-panel'>"
            "<h2>Accountverwijdering aanvragen</h2>"
            "<p class='helper'>Je account wordt niet direct verwijderd. Alleen de eigenaar kan het verzoek goedkeuren of afwijzen.</p>"
            f"<form method='post' action='/deletion-requests'>"
            f"<input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>"
            "<input type='hidden' name='action' value='request_account_deletion'>"
            "<label class='field'><span>Reden (optioneel)</span><textarea name='reason' rows='4' placeholder='Waarom wil je je account laten verwijderen?'></textarea></label>"
            "<button class='button button-secondary' type='submit'>Verwijdering aanvragen</button>"
            "</form>"
            "</article>"
        )
    )

    organization_panel = ""
    if self.require_role(context, {"organization_admin"}):
        active = context["active_membership"]
        pending_org_request = deletion_requests.get_pending_organization_request(
            connection,
            int(active["organization_id"]),
        )
        organization_panel = (
            "<article class='panel inset'>"
            "<h2>Organisatieverwijdering</h2>"
            f"<p class='helper'>Voor organisatie <strong>{h(active['organization_name'])}</strong> staat sinds {h((pending_org_request['created_at'] or '').split('T')[0])} een open verwijderverzoek. Alleen de eigenaar kan dit goedkeuren of afwijzen.</p>"
            f"<p><strong>Status:</strong> {h(pending_org_request['status'])}</p>"
            "</article>"
            if pending_org_request
            else (
                "<article class='panel form-panel'>"
                "<h2>Organisatieverwijdering aanvragen</h2>"
                "<p class='helper'>Na goedkeuring worden organisatiegegevens, groepen, opdrachten en gekoppelde beheerde accounts verwijderd.</p>"
                f"<form method='post' action='/deletion-requests'>"
                f"<input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>"
                "<input type='hidden' name='action' value='request_organization_deletion'>"
                "<label class='field'><span>Reden (optioneel)</span><textarea name='reason' rows='4' placeholder='Waarom moet deze organisatie worden verwijderd?'></textarea></label>"
                "<button class='button button-secondary' type='submit'>Organisatieverwijdering aanvragen</button>"
                "</form>"
                "</article>"
            )
        )

    panels = [account_panel]
    if organization_panel:
        panels.append(organization_panel)
    return "<section class='grid two-up'>" + "".join(panels) + "</section>"


def _platform_deletion_request_dashboard(self: WebApp, connection, context: dict) -> Response:
    pending_requests = deletion_requests.list_requests(connection, status="pending")
    recent_requests = deletion_requests.list_requests(connection, limit=20)
    pending_rows = [
        [
            h("Account" if row["request_type"] == "user" else "Organisatie"),
            h(row["target_label"]),
            h(f"{row['requester_name_snapshot']} ({row['requester_email_snapshot']})"),
            h(row["reason"] or "-"),
            h((row["created_at"] or "").replace("T", " ")),
            (
                f"<form method='post' action='/deletion-requests' style='display:flex; gap:0.5rem; flex-wrap:wrap;'>"
                f"<input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>"
                f"<input type='hidden' name='request_id' value='{row['id']}'>"
                "<input type='hidden' name='decision_note' value=''>"
                "<button class='button button-primary small' type='submit' name='action' value='approve_deletion_request'>Goedkeuren</button>"
                "<button class='button button-secondary small' type='submit' name='action' value='deny_deletion_request'>Afwijzen</button>"
                "</form>"
            ),
        ]
        for row in pending_requests
    ]
    recent_rows = [
        [
            h("Account" if row["request_type"] == "user" else "Organisatie"),
            h(row["target_label"]),
            h(row["status"]),
            h((row["created_at"] or "").replace("T", " ")),
            h((row["decided_at"] or "").replace("T", " ") if row["decided_at"] else "-"),
        ]
        for row in recent_requests
        if row["status"] != "pending"
    ]
    body = [
        "<section class='hero compact'><div><span class='eyebrow'>Platform view</span><h1>Verwijderverzoeken</h1><p>Alleen de eigenaar kan hier account- en organisatieverwijderingen goedkeuren of afwijzen.</p></div><div class='actions'><a class='button button-secondary' href='/dashboard'>Terug naar dashboard</a></div></section>",
        self.metrics_row(
            [
                ("Openstaand", str(len(pending_requests))),
                ("Recent afgehandeld", str(len(recent_rows))),
            ]
        ),
        "<section class='panel'><h2>Openstaande verzoeken</h2>"
        + self.render_table(["Type", "Doel", "Aangevraagd door", "Reden", "Datum", "Actie"], pending_rows)
        + "</section>",
        "<section class='panel'><h2>Recente besluiten</h2>"
        + self.render_table(["Type", "Doel", "Status", "Aangevraagd", "Afgehandeld"], recent_rows)
        + "</section>",
    ]
    return self.html("Verwijderverzoeken", "".join(body), context)


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    original_render_nav = WebApp.render_nav
    original_dispatch = WebApp.dispatch
    original_public_student_dashboard = WebApp.public_student_dashboard
    original_student_dashboard = WebApp.student_dashboard
    original_trainer_dashboard = WebApp.trainer_dashboard
    original_organization_admin_dashboard = WebApp.organization_admin_dashboard

    def render_nav(self: WebApp, context: dict) -> str:
        nav = original_render_nav(self, context)
        if not _is_platform_owner(context) or "/deletion-requests" in nav:
            return nav
        return nav.replace(
            "<a class='nav-link' href='/logout'>Logout</a>",
            "<a class='nav-link' href='/deletion-requests'>Verwijderverzoeken</a><a class='nav-link' href='/logout'>Logout</a>",
            1,
        )

    def dispatch(self: WebApp, request) -> Response:
        if request.path == "/deletion-requests":
            with db.connect() as connection:
                context = self.get_context(connection, request)
                return self.deletion_request_page(connection, request, context)
        return original_dispatch(self, request)

    def public_student_dashboard(self: WebApp, connection, context: dict) -> Response:
        response = original_public_student_dashboard(self, connection, context)
        return _inject_panel(response, self.render_account_deletion_panels(connection, context))

    def student_dashboard(self: WebApp, connection, context: dict) -> Response:
        response = original_student_dashboard(self, connection, context)
        return _inject_panel(response, self.render_account_deletion_panels(connection, context))

    def trainer_dashboard(self: WebApp, connection, request, context: dict) -> Response:
        response = original_trainer_dashboard(self, connection, request, context)
        return _inject_panel(response, self.render_account_deletion_panels(connection, context))

    def organization_admin_dashboard(self: WebApp, connection, request, context: dict) -> Response:
        response = original_organization_admin_dashboard(self, connection, request, context)
        return _inject_panel(response, self.render_account_deletion_panels(connection, context))

    WebApp.deletion_request_page = _deletion_request_page
    WebApp.render_account_deletion_panels = _render_account_deletion_panels
    WebApp.platform_deletion_request_dashboard = _platform_deletion_request_dashboard
    WebApp.render_nav = render_nav
    WebApp.dispatch = dispatch
    WebApp.public_student_dashboard = public_student_dashboard
    WebApp.student_dashboard = student_dashboard
    WebApp.trainer_dashboard = trainer_dashboard
    WebApp.organization_admin_dashboard = organization_admin_dashboard
    _PATCHED = True


apply()
