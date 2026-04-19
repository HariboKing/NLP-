from __future__ import annotations

from urllib.parse import quote_plus

from . import db, deletion_requests, web as web_module
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


def _build_model_information_blocks(model: dict) -> list[dict[str, list[str] | str]]:
    blocks = model.get("blocks", [])
    existing_groups = [block.get("paragraphs", []) for block in blocks]
    while len(existing_groups) < 3:
        existing_groups.append([])

    return [
        {
            "heading": "Wat is het model",
            "paragraphs": web_module.combine_unique_paragraphs(
                [model.get("intro", "")],
                existing_groups[0],
                existing_groups[1],
            ),
        },
        {
            "heading": "Wat kan je met het model",
            "paragraphs": web_module.combine_unique_paragraphs(
                existing_groups[2],
                model.get(
                    "application_paragraphs",
                    [
                        f"Gebruik dit vak om uit te werken hoe {model['title']} in gesprekken, analyses, oefeningen of reflectie wordt toegepast, inclusief concrete voorbeelden.",
                    ],
                ),
            ),
        },
        {
            "heading": "Waar komt het model vandaan",
            "paragraphs": web_module.combine_unique_paragraphs(
                model.get(
                    "history_paragraphs",
                    [
                        f"Voeg hier achtergrondinformatie toe over de ontwikkelaar of ontwikkelaars van {model['title']}, de context waarin het model ontstond en de reden waarom dit model werd ontwikkeld.",
                    ],
                ),
            ),
        },
        {
            "heading": "Verdere informatie, uitleg en oefeningen",
            "paragraphs": web_module.combine_unique_paragraphs(
                model.get(
                    "reference_paragraphs",
                    [
                        f"Verwijs hier naar reader, map, hoofdstukken, boeken, verdiepingspaden en oefeningen waarin {model['title']} verder wordt uitgelegd.",
                    ],
                ),
            ),
        },
    ]


def _account_deactivation_page(self: WebApp, connection, request, context: dict) -> Response:
    if not context["user"]:
        return self.redirect("/login")
    if context["user"].get("is_platform_admin"):
        return self.forbidden(context, "Het owner-account kan niet worden gedeactiveerd.")

    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")

        decision = request.get("decision")
        if decision == "no":
            return self.redirect("/dashboard")
        if decision != "yes":
            return self.redirect("/account/deactivate")

        deletion_requests.create_user_deletion_request(
            connection,
            user_id=int(context["user"]["user_id"]),
            reason="Aangevraagd via accountdeactivatie.",
        )
        db.deactivate_user_account(connection, int(context["user"]["user_id"]))
        connection.commit()
        response = self.redirect("/login?notice=" + quote_plus("Account gedeactiveerd."))
        response.headers.append(("Set-Cookie", "session_token=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0"))
        return response

    body = (
        "<section class='hero compact'><div><span class='eyebrow'>Account</span><h1>Account deactiveren</h1>"
        "<p>Na bevestiging wordt je account direct gedeactiveerd. Je wordt uitgelogd, kunt daarna niet meer inloggen en de eigenaar ontvangt een verwijderverzoek.</p></div>"
        "<div class='actions'><a class='button button-secondary' href='/dashboard'>Terug naar dashboard</a></div></section>"
        "<section class='panel form-panel'>"
        "<h2>Weet je het zeker?</h2>"
        "<p class='helper'>Kies <strong>Ja</strong> om je account te deactiveren. Kies <strong>Nee</strong> om terug te gaan naar je homepagina.</p>"
        f"<form method='post' action='/account/deactivate' style='display:flex; gap:0.75rem; flex-wrap:wrap;'>"
        f"<input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>"
        "<button class='button button-primary' type='submit' name='decision' value='yes'>Ja</button>"
        "<button class='button button-secondary' type='submit' name='decision' value='no'>Nee</button>"
        "</form>"
        "</section>"
    )
    return self.html("Account deactiveren", body, context)


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
            return self.redirect("/account/deactivate")

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

    if not organization_panel:
        return ""
    return "<section class='grid two-up'>" + organization_panel + "</section>"


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
    original_module_page = WebApp.module_page

    def render_nav(self: WebApp, context: dict) -> str:
        nav = original_render_nav(self, context)
        if _is_platform_owner(context):
            if "/deletion-requests" not in nav:
                nav = nav.replace(
                    "<a class='nav-link' href='/logout'>Logout</a>",
                    "<a class='nav-link' href='/deletion-requests'>Verwijderverzoeken</a><a class='nav-link' href='/logout'>Logout</a>",
                    1,
                )
            return nav

        if context.get("user") and "/account/deactivate" not in nav:
            return nav.replace(
                "<a class='nav-link' href='/logout'>Logout</a>",
                "<a class='nav-link' href='/account/deactivate'>Deactiveer account</a><a class='nav-link' href='/logout'>Logout</a>",
                1,
            )
        return nav

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

    def module_page(self: WebApp, connection, request, context: dict, module_id: int) -> Response:
        response = original_module_page(self, connection, request, context, module_id)
        body = response.body.decode("utf-8", errors="ignore")
        replacements = {
            "<h3>Leeswerk</h3>": "<h3>Leesstof van de les</h3>",
            "Reader-, map- en naslaglinks die direct bij dit leerpad horen.": "Reader-, map- en lesinformatie die direct bij dit verdiepingspad horen.",
            "<h3>Verdiepende literatuur</h3>": "<h3>Meer informatie</h3>",
            "Boeken en aanvullende bronnen waarmee leerlingen dieper op een concept kunnen doorleren.": "Verwijzingen naar verdiepende boeken, extra uitleg, video-links en andere bronnen om verder te verdiepen.",
            "Er is nog geen leeswerk gekoppeld aan dit leerpad.": "Er is nog geen leesstof toegevoegd aan dit leerpad.",
            "Er is nog geen verdiepende literatuur toegevoegd voor dit leerpad.": "Er is nog geen extra informatie toegevoegd voor dit leerpad.",
        }
        for old, new in replacements.items():
            body = body.replace(old, new)
        return Response(response.status, body.encode("utf-8"), list(response.headers))

    web_module.build_model_information_blocks = _build_model_information_blocks
    WebApp.account_deactivation_page = _account_deactivation_page
    WebApp.deletion_request_page = _deletion_request_page
    WebApp.render_account_deletion_panels = _render_account_deletion_panels
    WebApp.platform_deletion_request_dashboard = _platform_deletion_request_dashboard
    WebApp.render_nav = render_nav
    WebApp.dispatch = dispatch
    WebApp.public_student_dashboard = public_student_dashboard
    WebApp.student_dashboard = student_dashboard
    WebApp.trainer_dashboard = trainer_dashboard
    WebApp.organization_admin_dashboard = organization_admin_dashboard
    WebApp.module_page = module_page
    _PATCHED = True


apply()
