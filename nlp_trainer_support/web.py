from __future__ import annotations

import json
import mimetypes
import re
import secrets
from dataclasses import dataclass
from email.parser import BytesParser
from email.policy import default as email_policy
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, quote, quote_plus

from . import db
from .config import APP_TITLE, STATIC_DIR, UPLOADS_DIR
from .scoring import score_submission


def h(value) -> str:
    return escape("" if value is None else str(value), quote=True)


def as_text_list(values) -> str:
    if not values:
        return "-"
    return ", ".join(str(value) for value in values)


def parse_json(text: str | None, fallback):
    if not text:
        return fallback
    return json.loads(text)


def format_score(value) -> str:
    if value is None:
        return "Pending"
    return f"{round(float(value))}%"


def role_priority(role: str) -> int:
    order = {
        "organization_admin": 0,
        "trainer": 1,
        "student": 2,
    }
    return order.get(role, 99)


MODEL_IMAGE_DIR_NAME = "Model afbeeldingen"
MODEL_PAGES = [
    {
        "slug": "nlp-model",
        "title": "NLP-model",
        "image_stem": "nlp-model_afbeelding",
        "intro": "Het NLP-model laat zien hoe mensen via waarneming, taal, betekenis en gedrag hun subjectieve ervaring opbouwen.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Dit model helpt studenten zien dat zij niet rechtstreeks op de werkelijkheid reageren, maar op hun eigen interne representatie ervan.",
                    "Daarmee wordt zichtbaar hoe zintuiglijke input, selectie, betekenisgeving en reactie elkaar opvolgen en elkaar beinvloeden.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let vooral op het verschil tussen wat iemand waarneemt, wat iemand daarvan maakt en hoe dat doorwerkt in gevoel en gedrag.",
                    "Dat onderscheid is de basis voor bijna alle andere NLP-modellen die later volgen.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik dit model om gesprekken te analyseren: wat was de prikkel, welke betekenis werd eraan gegeven en welke reactie volgde daaruit?",
                    "Juist die stap van betekenisgeving geeft ingangen voor nieuwe keuzes en ander gedrag.",
                ],
            },
        ],
    },
    {
        "slug": "metamodel",
        "title": "Metamodel",
        "image_stem": "metamodel_afbeelding",
        "intro": "Het metamodel helpt taal preciezer te maken door deleties, generalisaties en vervormingen zichtbaar en bevraagbaar te maken.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Het model laat zien hoe mensen in taal informatie weglaten, overdrijven of betekenis inkleuren zonder dat dit direct opvalt.",
                    "Door die patronen te herkennen ontstaat meer helderheid over iemands wereldmodel.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let op woorden als altijd, nooit, iedereen, niemand, maar ook op vage verwijzingen, aannames en onduidelijke oorzaken.",
                    "Het metamodel is vooral sterk wanneer je het koppelt aan concrete, verhelderende vragen.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik het metamodel in coaching, feedback en analyse van geschreven tekst om de structuur achter uitspraken bloot te leggen.",
                    "Het doel is niet om iemand vast te zetten, maar om meer keuzevrijheid en precisie te creeren.",
                ],
            },
        ],
    },
    {
        "slug": "g6-model",
        "title": "G6-model",
        "image_stem": "g6-model_afbeelding",
        "intro": "Het G6-model maakt inzichtelijk hoe een gebeurtenis via betekenis en overtuiging doorwerkt in emotie en gedrag.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Dit model helpt studenten onderscheiden tussen de gebeurtenis zelf en de interpretatie die erop volgt.",
                    "Daardoor wordt duidelijk waarom twee mensen totaal anders kunnen reageren op dezelfde situatie.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Besteed aandacht aan de schakel tussen gebeurtenis, gedachte of geloof, gevoel en gedrag.",
                    "Juist in die tussenlaag zitten vaak de overtuigingen die verandering mogelijk of juist moeilijk maken.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik het model om cases stap voor stap uit te pluizen en te onderzoeken waar een patroon vastloopt.",
                    "Het is een sterk model om studenten van reactief naar reflectief kijken te brengen.",
                ],
            },
        ],
    },
    {
        "slug": "structureel-differentiaal",
        "title": "Structureel differentiaal",
        "image_stem": "structureel-differentiaal_afbeelding",
        "intro": "Het structureel differentiaal visualiseert hoe ervaringen worden gefilterd, gelabeld en geabstraheerd voordat ze taal worden.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Het model maakt zichtbaar dat woorden nooit de volledige werkelijkheid bevatten, maar altijd een beperkte representatie zijn.",
                    "Daarmee ondersteunt het de bekende gedachte dat de kaart niet hetzelfde is als het gebied.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let op de verschillende abstractieniveaus en op wat onderweg verloren gaat wanneer ervaring wordt samengevat in taal.",
                    "Dit helpt studenten nauwkeuriger te kijken naar interpretatie en generalisatie.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik het model wanneer iemand te snel conclusies trekt of wanneer een begrip te abstract wordt ingezet.",
                    "Het helpt om terug te bewegen van labels naar concreet waarneembare informatie.",
                ],
            },
        ],
    },
    {
        "slug": "tote-model",
        "title": "TOTE-model",
        "image_stem": "tote-model_afbeelding",
        "intro": "Het TOTE-model beschrijft gedrag als een lus van testen, uitvoeren, opnieuw testen en afronden.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Het model laat zien dat doelgericht gedrag niet lineair hoeft te zijn, maar vaak een terugkerend proces van afstemmen en bijstellen is.",
                    "Daarmee is het een krachtig hulpmiddel om strategieen zichtbaar te maken.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let op het verschil tussen een interne test, een actie, een nieuwe vergelijking en het moment waarop iemand stopt of doorgaat.",
                    "Juist die logica maakt gedrag overdraagbaar en analyseerbaar.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik TOTE om leer- en successtrategien te ontleden: hoe weet iemand dat het werkt, wat doet diegene daarna en wanneer is het genoeg?",
                    "Dat maakt het model waardevol voor modelleren, coaching en performance-analyse.",
                ],
            },
        ],
    },
    {
        "slug": "neuro-logische-niveaus",
        "title": "Neuro-logische niveaus",
        "image_stem": "neuro-logische-niveaus_afbeelding",
        "intro": "De neuro-logische niveaus helpen onderscheiden op welk niveau een vraagstuk speelt: omgeving, gedrag, vaardigheden, overtuigingen, identiteit of missie.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Het model geeft structuur aan veranderwerk door te laten zien dat niet elk probleem op hetzelfde niveau opgelost wordt.",
                    "Daardoor wordt duidelijk waarom een gedragsvraag soms eigenlijk een identiteits- of overtuigingsvraag is.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let goed op de taal van elk niveau en op de manier waarop de niveaus elkaar beinvloeden.",
                    "Voor studenten is vooral het onderscheid tussen gedrag, vaardigheden en overtuigingen vaak erg verhelderend.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik dit model om gesprekken te structureren en om te bepalen waar een interventie het meeste effect heeft.",
                    "Het is ook bruikbaar als reflectiekader voor coaching, persoonlijke ontwikkeling en feedback.",
                ],
            },
        ],
    },
    {
        "slug": "nine-major-beliefs",
        "title": "Nine Major Beliefs",
        "image_stem": "nine-major-beliefs_afbeelding",
        "intro": "De Nine Major Beliefs vormen een set overtuigingen die binnen NLP richting geven aan waarnemen, communiceren en veranderen.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Deze overtuigingen bieden geen harde wetten, maar een denkkader waarmee studenten anders leren kijken naar gedrag, keuzevrijheid en communicatie.",
                    "Ze vormen daarmee een basislaag onder veel NLP-toepassingen.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Kijk niet alleen naar de formuleringen zelf, maar vooral naar de praktische gevolgen wanneer iemand vanuit zo'n overtuiging handelt.",
                    "De waarde zit in toepassen, niet in het opdreunen van losse zinnen.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik deze beliefs als reflectievragen: welke aanname helpt hier vooruit en welke belemmert juist?",
                    "Zo worden ze een werkbaar kader voor houding, gesprek en interventiekeuze.",
                ],
            },
        ],
    },
    {
        "slug": "chunken",
        "title": "Chunken",
        "image_stem": "chunken_afbeelding",
        "intro": "Chunken gaat over schakelen tussen abstractieniveaus: groter, kleiner of op hetzelfde niveau van informatie kijken.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Het model laat zien hoe betekenis verandert wanneer je uitzoomt naar grotere gehelen of juist inzoomt op details.",
                    "Daardoor wordt taal flexibeler en worden gesprekken makkelijker te sturen.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let op vragen die omhoog chunken, omlaag chunken of lateraal vergelijken.",
                    "Voor studenten wordt dan zichtbaar hoe abstractie invloed heeft op begrip, motivatie en besluitvorming.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik chunken om vaagheid te concretiseren, details weer betekenis te geven of mensen uit een vastgelopen perspectief te halen.",
                    "Het model werkt goed in sales, coaching, onderwijs en structurering van uitleg.",
                ],
            },
        ],
    },
    {
        "slug": "zintuigen",
        "title": "Zintuigen",
        "image_stem": "zintuigen_afbeelding",
        "intro": "Het model van de zintuigen richt de aandacht op de representatiesystemen waarmee mensen ervaring intern coderen en extern beschrijven.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Het model helpt zichtbaar maken of iemand vooral in beelden, geluiden, gevoel, woorden of interne dialoog codeert.",
                    "Dat geeft aanknopingspunten voor afstemming en didactiek.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let op predikaten, taalgebruik en beschrijvingen die wijzen op visueel, auditief of kinesthetisch verwerken.",
                    "Voor studenten wordt dan tastbaar hoe waarneming samenhangt met taal.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik dit model om communicatie beter af te stemmen en om leerstof op meerdere manieren aan te bieden.",
                    "Het helpt ook om ervaring specifieker te onderzoeken in coaching en analyse.",
                ],
            },
        ],
    },
    {
        "slug": "submodaliteiten",
        "title": "Submodaliteiten",
        "image_stem": "submodaliteiten_afbeelding",
        "intro": "Submodaliteiten gaan over de fijne bouwstenen van interne ervaring, zoals grootte, helderheid, afstand, volume, tempo en intensiteit.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Het model laat zien dat niet alleen de inhoud van een ervaring telt, maar ook de manier waarop die ervaring intern is opgebouwd.",
                    "Kleine verschuivingen in submodaliteiten kunnen de beleving verrassend sterk veranderen.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let op contrasten: dichtbij versus ver weg, fel versus dof, luid versus zacht, snel versus traag.",
                    "Daarmee leren studenten ervaring ontleden in concrete, manipuleerbare elementen.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik submodaliteiten in oefeningen rond state management, motivatie, herinnering en verandering van beleving.",
                    "Het model is vooral sterk wanneer je abstracte ervaring tastbaar en experimenteerbaar wilt maken.",
                ],
            },
        ],
    },
    {
        "slug": "cartesiaanse-vragen",
        "title": "Cartesiaanse vragen",
        "image_stem": "cartesiaanse-vragen_afbeelding",
        "intro": "Cartesiaanse vragen helpen overtuigingen en aannames systematisch te onderzoeken door meerdere logische richtingen te bevragen.",
        "blocks": [
            {
                "heading": "Wat dit model duidelijk maakt",
                "paragraphs": [
                    "Het model doorbreekt vanzelfsprekende conclusies door niet alleen te vragen wat waar is, maar ook wat waar is als het tegendeel geldt.",
                    "Daardoor worden verborgen aannames zichtbaar.",
                ],
            },
            {
                "heading": "Waar je tijdens het bestuderen op let",
                "paragraphs": [
                    "Let op de logische combinaties en op hoe een overtuiging verandert zodra je de vraagstelling draait of omkeert.",
                    "Voor studenten is dit een sterk hulpmiddel om denkstructuren kritisch te toetsen.",
                ],
            },
            {
                "heading": "Hoe je dit in de praktijk gebruikt",
                "paragraphs": [
                    "Gebruik cartesiaanse vragen om beperkende overtuigingen, complexe equivalenties en snelle gevolgtrekkingen te onderzoeken.",
                    "Het model past goed bij verdieping, reflectie en het openen van nieuwe perspectieven.",
                ],
            },
        ],
    },
]
MODEL_PAGE_LOOKUP = {model["slug"]: model for model in MODEL_PAGES}


@dataclass
class UploadedFile:
    filename: str
    content_type: str
    data: bytes


@dataclass
class Request:
    method: str
    path: str
    query: dict[str, list[str]]
    form: dict[str, list[str]]
    cookies: dict[str, str]
    files: dict[str, UploadedFile]

    @classmethod
    def from_environ(cls, environ) -> "Request":
        method = environ.get("REQUEST_METHOD", "GET").upper()
        path = environ.get("PATH_INFO", "/")
        query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)

        form: dict[str, list[str]] = {}
        files: dict[str, UploadedFile] = {}
        if method == "POST":
            length = int(environ.get("CONTENT_LENGTH") or 0)
            raw_body = environ["wsgi.input"].read(length) if length else b""
            content_type = environ.get("CONTENT_TYPE", "")
            if raw_body and content_type.startswith("multipart/form-data"):
                form, files = cls.parse_multipart_form(raw_body, content_type)
            else:
                body = raw_body.decode("utf-8") if raw_body else ""
                form = parse_qs(body, keep_blank_values=True)

        cookie_header = environ.get("HTTP_COOKIE", "")
        cookies: dict[str, str] = {}
        if cookie_header:
            for part in cookie_header.split(";"):
                if "=" not in part:
                    continue
                key, value = part.strip().split("=", 1)
                cookies[key] = value

        return cls(method=method, path=path, query=query, form=form, cookies=cookies, files=files)

    @staticmethod
    def parse_multipart_form(raw_body: bytes, content_type: str) -> tuple[dict[str, list[str]], dict[str, UploadedFile]]:
        message = BytesParser(policy=email_policy).parsebytes(
            f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8") + raw_body
        )
        form: dict[str, list[str]] = {}
        files: dict[str, UploadedFile] = {}
        if not message.is_multipart():
            return form, files

        for part in message.iter_parts():
            if part.get_content_disposition() != "form-data":
                continue

            field_name = part.get_param("name", header="content-disposition")
            if not field_name:
                continue

            payload = part.get_payload(decode=True) or b""
            filename = part.get_filename()
            if filename:
                if payload:
                    files[field_name] = UploadedFile(
                        filename=filename,
                        content_type=part.get_content_type(),
                        data=payload,
                    )
                continue

            charset = part.get_content_charset() or "utf-8"
            value = payload.decode(charset, errors="replace")
            form.setdefault(field_name, []).append(value)

        return form, files

    def get(self, key: str, default: str = "") -> str:
        if key in self.form and self.form[key]:
            return self.form[key][0]
        if key in self.query and self.query[key]:
            return self.query[key][0]
        return default

    def getlist(self, key: str) -> list[str]:
        if key in self.form:
            return self.form[key]
        if key in self.query:
            return self.query[key]
        return []

    def getfile(self, key: str) -> UploadedFile | None:
        return self.files.get(key)


@dataclass
class Response:
    status: str
    body: bytes
    headers: list[tuple[str, str]]

    def __call__(self, start_response):
        start_response(self.status, self.headers)
        return [self.body]


class WebApp:
    def __init__(self) -> None:
        db.initialize_database(reset=False)

    def __call__(self, environ, start_response):
        request = Request.from_environ(environ)
        response = self.dispatch(request)
        return response(start_response)

    def dispatch(self, request: Request) -> Response:
        if request.path == "/health":
            return Response("200 OK", b"ok", [("Content-Type", "text/plain; charset=utf-8")])

        if request.path.startswith("/uploads/"):
            return self.serve_upload(request.path)

        if request.path.startswith("/static/"):
            return self.serve_static(request.path)

        with db.connect() as connection:
            context = self.get_context(connection, request)

            if request.path == "/":
                if context["user"]:
                    return self.redirect("/dashboard")
                return self.html("Welkom", self.render_landing(), context)

            if request.path == "/login":
                if request.method == "POST":
                    return self.handle_login(connection, request)
                return self.html("Login", self.render_login(), context)

            if request.path == "/logout":
                db.destroy_session(connection, request.cookies.get("session_token"))
                return self.redirect("/login?notice=" + quote_plus("Je bent uitgelogd."))

            if not context["user"]:
                return self.redirect("/login")

            if request.path == "/dashboard":
                return self.render_dashboard(connection, request, context)

            if request.path == "/assignments/new":
                return self.assignment_builder(connection, request, context)

            if request.path == "/reviews":
                return self.review_queue(connection, request, context)

            if request.path == "/settings/theme":
                return self.theme_settings(connection, request, context)

            model_match = re.fullmatch(r"/models/([a-z0-9-]+)", request.path)
            if model_match:
                return self.model_page(context, model_match.group(1))

            module_quiz_complete_match = re.fullmatch(r"/modules/(\d+)/quiz/complete", request.path)
            if module_quiz_complete_match:
                return self.module_quiz_complete_page(connection, request, context, int(module_quiz_complete_match.group(1)))

            module_quiz_match = re.fullmatch(r"/modules/(\d+)/quiz", request.path)
            if module_quiz_match:
                return self.module_quiz_page(connection, request, context, int(module_quiz_match.group(1)))

            module_match = re.fullmatch(r"/modules/(\d+)", request.path)
            if module_match:
                return self.module_page(connection, request, context, int(module_match.group(1)))

            assignment_match = re.fullmatch(r"/assignments/(\d+)", request.path)
            if assignment_match:
                return self.assignment_page(connection, request, context, int(assignment_match.group(1)))

            exercise_match = re.fullmatch(r"/exercises/(\d+)", request.path)
            if exercise_match:
                return self.exercise_page(connection, request, context, int(exercise_match.group(1)))

            attempt_match = re.fullmatch(r"/attempts/(\d+)", request.path)
            if attempt_match:
                return self.attempt_page(connection, request, context, int(attempt_match.group(1)))

            review_match = re.fullmatch(r"/attempts/(\d+)/review", request.path)
            if review_match:
                return self.review_attempt(connection, request, context, int(review_match.group(1)))

            student_match = re.fullmatch(r"/students/(\d+)", request.path)
            if student_match:
                return self.student_detail(connection, request, context, int(student_match.group(1)))

            return self.not_found(context)

    def get_context(self, connection, request: Request) -> dict:
        session = db.get_session(connection, request.cookies.get("session_token"))
        if not session:
            return {
                "user": None,
                "session": None,
                "memberships": [],
                "active_membership": None,
                "theme": self.default_theme(),
                "notice": request.get("notice"),
            }

        memberships = db.get_memberships(connection, session["user_id"])
        memberships = sorted(memberships, key=lambda row: (row["organization_name"], role_priority(row["role"])))
        requested_org = request.get("org")
        active_membership = None
        if requested_org:
            for membership in memberships:
                if str(membership["organization_id"]) == requested_org:
                    active_membership = membership
                    break
        if not active_membership and memberships:
            active_membership = memberships[0]

        theme = self.default_theme()
        if active_membership:
            theme_row = connection.execute(
                "SELECT * FROM themes WHERE organization_id = ?",
                (active_membership["organization_id"],),
            ).fetchone()
            if theme_row:
                theme = dict(theme_row)

        return {
            "user": dict(session),
            "session": dict(session),
            "memberships": [dict(row) for row in memberships],
            "active_membership": dict(active_membership) if active_membership else None,
            "theme": theme,
            "notice": request.get("notice"),
        }

    def default_theme(self) -> dict:
        return {
            "brand_name": APP_TITLE,
            "logo_label": "NLP",
            "logo_url": "",
            "hero_url": "",
            "background_image_opacity": 0.18,
            "primary_color": "#245c73",
            "secondary_color": "#ecf4f6",
            "accent_color": "#e48c52",
            "surface_color": "#ffffff",
            "background_style": "linear-gradient(135deg, rgba(36,92,115,0.10), rgba(228,140,82,0.08))",
        }

    def compose_background_art(self, theme: dict) -> str:
        base_style = theme.get("background_style") or self.default_theme()["background_style"]
        image_url = (theme.get("hero_url") or "").strip()
        if not image_url:
            return base_style

        try:
            image_opacity = float(theme.get("background_image_opacity", 0.18))
        except (TypeError, ValueError):
            image_opacity = 0.18
        image_opacity = min(max(image_opacity, 0.0), 0.95)
        fade = round(1 - image_opacity, 2)
        return (
            f"linear-gradient(rgba(255,255,255,{fade}), rgba(255,255,255,{fade})), "
            f"url(\"{image_url}\"), {base_style}"
        )

    def render_brand_mark(self, theme: dict) -> str:
        if theme.get("logo_url"):
            return (
                "<div class='brand-mark brand-mark-image'>"
                f"<img class='brand-logo' src='{h(theme['logo_url'])}' alt='{h(theme['brand_name'])}'>"
                "</div>"
            )
        return f"<div class='brand-mark'>{h(theme['logo_label'])}</div>"

    def save_theme_upload(self, upload: UploadedFile, organization_id: int, asset_kind: str) -> str:
        if not upload.content_type.startswith("image/"):
            raise ValueError("Upload een geldige afbeelding.")

        suffix = Path(upload.filename).suffix.lower()
        if not suffix:
            suffix = mimetypes.guess_extension(upload.content_type) or ".png"
        safe_suffix = suffix if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"} else ".png"

        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{asset_kind}-{organization_id}-{secrets.token_hex(8)}{safe_suffix}"
        target = UPLOADS_DIR / filename
        target.write_bytes(upload.data)
        return f"/uploads/{filename}"

    def html(self, title: str, content: str, context: dict, status: str = "200 OK") -> Response:
        theme = context["theme"]
        active = context["active_membership"]
        nav = self.render_nav(context)
        background_art = self.compose_background_art(theme)
        brand_mark = self.render_brand_mark(theme)
        shell_class = "shell has-background-image" if (theme.get("hero_url") or "").strip() else "shell"
        notice_html = ""
        if context.get("notice"):
            notice_html = f"<div class='notice'>{h(context['notice'])}</div>"

        body = f"""<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{h(title)} | {h(APP_TITLE)}</title>
  <link rel="stylesheet" href="/static/styles.css">
  <style>
    :root {{
      --primary: {h(theme['primary_color'])};
      --secondary: {h(theme['secondary_color'])};
      --accent: {h(theme['accent_color'])};
      --surface: {h(theme['surface_color'])};
      --background-art: {background_art};
    }}
  </style>
</head>
<body>
  <div class="{shell_class}">
    <header class="topbar">
      <div class="brand">
        {brand_mark}
        <div>
          <div class="brand-name">{h(theme['brand_name'])}</div>
          <div class="brand-subtitle">{h(active['organization_name']) if active else 'Product demo'}</div>
        </div>
      </div>
      {nav}
    </header>
    <main class="page">
      {notice_html}
      {content}
    </main>
  </div>
</body>
</html>"""
        return Response(status, body.encode("utf-8"), [("Content-Type", "text/html; charset=utf-8")])

    def render_nav(self, context: dict) -> str:
        if not context["user"]:
            return "<nav class='topnav'><a class='nav-link' href='/login'>Login</a></nav>"

        links = ["<a class='nav-link' href='/dashboard'>Dashboard</a>"]
        active = context["active_membership"]
        if active and active["role"] in {"trainer", "organization_admin"}:
            links.append("<a class='nav-link' href='/assignments/new'>Nieuwe opdracht</a>")
            links.append("<a class='nav-link' href='/reviews'>Reviews</a>")
        if active and active["role"] == "organization_admin":
            links.append("<a class='nav-link' href='/settings/theme'>Branding</a>")
        links.append("<a class='nav-link' href='/logout'>Logout</a>")
        return "<nav class='topnav'>" + "".join(links) + "</nav>"

    def redirect(self, location: str) -> Response:
        return Response("302 Found", b"", [("Location", location)])

    def not_found(self, context: dict) -> Response:
        return self.html("Niet gevonden", "<section class='panel'><h1>Pagina niet gevonden</h1></section>", context, status="404 Not Found")

    def forbidden(self, context: dict, message: str = "Je hebt hier geen toegang.") -> Response:
        return self.html("Geen toegang", f"<section class='panel'><h1>Geen toegang</h1><p>{h(message)}</p></section>", context, status="403 Forbidden")

    def serve_static(self, path: str) -> Response:
        target = (STATIC_DIR / path.removeprefix("/static/")).resolve()
        if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.exists():
            return Response("404 Not Found", b"Not found", [("Content-Type", "text/plain; charset=utf-8")])
        mime_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        return Response("200 OK", target.read_bytes(), [("Content-Type", mime_type)])

    def serve_upload(self, path: str) -> Response:
        target = (UPLOADS_DIR / path.removeprefix("/uploads/")).resolve()
        if not str(target).startswith(str(UPLOADS_DIR.resolve())) or not target.exists():
            legacy_path = (STATIC_DIR / path.removeprefix("/uploads/")).resolve()
            if not str(legacy_path).startswith(str(STATIC_DIR.resolve())) or not legacy_path.exists():
                return Response("404 Not Found", b"Not found", [("Content-Type", "text/plain; charset=utf-8")])
            target = legacy_path
        mime_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        return Response("200 OK", target.read_bytes(), [("Content-Type", mime_type)])

    def require_role(self, context: dict, allowed: set[str]) -> bool:
        active = context["active_membership"]
        return bool(active and active["role"] in allowed)

    def verify_csrf(self, request: Request, context: dict) -> bool:
        session = context.get("session")
        return bool(session and request.get("csrf_token") == session["csrf_token"])

    def render_landing(self) -> str:
        return """
        <section class="hero">
          <div>
            <span class="eyebrow">Trainer MVP</span>
            <h1>NLP leren, oefenen en beoordelen in een enkele webapp.</h1>
            <p>
              Deze demo bevat student-, trainer-, admin- en platformrollen,
              een seeded practitioner curriculum, opdrachten, oefentypes,
              feedback en reviewflows.
            </p>
            <div class="actions">
              <a class="button button-primary" href="/login">Open demo</a>
            </div>
          </div>
          <div class="panel credential-card">
            <h2>Demo accounts</h2>
            <ul class="credential-list">
              <li><strong>Platform owner:</strong> owner@platform.local / demo123</li>
              <li><strong>Org admin:</strong> admin@neuroflow.local / demo123</li>
              <li><strong>Trainer:</strong> trainer@neuroflow.local / demo123</li>
              <li><strong>Student:</strong> student@neuroflow.local / demo123</li>
            </ul>
          </div>
        </section>
        """

    def render_login(self) -> str:
        return """
        <section class="auth-shell">
          <form class="panel auth-card" method="post" action="/login">
            <h1>Inloggen</h1>
            <p>Gebruik een van de demo-accounts om de rolgebaseerde flows te bekijken.</p>
            <label class="field">
              <span>E-mail</span>
              <input type="email" name="email" required>
            </label>
            <label class="field">
              <span>Wachtwoord</span>
              <input type="password" name="password" required>
            </label>
            <button class="button button-primary" type="submit">Login</button>
          </form>
        </section>
        """

    def handle_login(self, connection, request: Request) -> Response:
        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (request.get("email").strip().lower(),),
        ).fetchone()
        if not user or not db.verify_password(request.get("password"), user["password_hash"]):
            context = {
                "user": None,
                "session": None,
                "memberships": [],
                "active_membership": None,
                "theme": self.default_theme(),
                "notice": "Ongeldige inloggegevens.",
            }
            return self.html("Login", self.render_login(), context, status="401 Unauthorized")

        token, _csrf = db.create_session(connection, user["id"])
        response = self.redirect("/dashboard")
        response.headers.append(("Set-Cookie", f"session_token={token}; Path=/; HttpOnly; SameSite=Lax"))
        return response

    def metrics_row(self, metrics: list[tuple[str, str]]) -> str:
        cards = []
        for label, value in metrics:
            cards.append(
                f"<article class='metric-card'><span>{h(label)}</span><strong>{h(value)}</strong></article>"
            )
        return "<section class='metrics'>" + "".join(cards) + "</section>"

    def render_table(self, headers: list[str], rows: list[list[str]]) -> str:
        head = "".join(f"<th>{h(header)}</th>" for header in headers)
        body_rows = []
        for row in rows:
            body_rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
        if not body_rows:
            body_rows.append(f"<tr><td colspan='{len(headers)}'>Nog geen data.</td></tr>")
        return f"<table class='table'><thead><tr>{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"

    def render_dashboard(self, connection, request: Request, context: dict) -> Response:
        user = context["user"]
        active = context["active_membership"]

        if user["is_platform_admin"] and not active:
            organizations = connection.execute(
                """
                SELECT organizations.id, organizations.name, organizations.slug,
                       COUNT(DISTINCT memberships.user_id) AS user_count,
                       COUNT(DISTINCT assignments.id) AS assignment_count
                FROM organizations
                LEFT JOIN memberships ON memberships.organization_id = organizations.id
                LEFT JOIN assignments ON assignments.organization_id = organizations.id
                GROUP BY organizations.id
                ORDER BY organizations.name
                """
            ).fetchall()
            body = [
                "<section class='hero compact'><div><span class='eyebrow'>Platform view</span><h1>Platform overzicht</h1><p>Gebruik dit scherm om tenants en demo-data te controleren.</p></div></section>",
                self.metrics_row(
                    [
                        ("Organisaties", str(len(organizations))),
                        ("Gebruikers", str(sum(int(row["user_count"]) for row in organizations))),
                        ("Opdrachten", str(sum(int(row["assignment_count"]) for row in organizations))),
                    ]
                ),
                "<section class='panel'><h2>Tenants</h2>"
                + self.render_table(
                    ["Organisatie", "Slug", "Gebruikers", "Opdrachten"],
                    [
                        [
                            h(row["name"]),
                            h(row["slug"]),
                            h(row["user_count"]),
                            h(row["assignment_count"]),
                        ]
                        for row in organizations
                    ],
                )
                + "</section>",
            ]
            return self.html("Platform dashboard", "".join(body), context)

        if not active:
            return self.forbidden(context, "Geen actieve organisatie gevonden.")

        if active["role"] == "student":
            return self.student_dashboard(connection, context)
        if active["role"] == "trainer":
            return self.trainer_dashboard(connection, context)
        if active["role"] == "organization_admin":
            return self.organization_admin_dashboard(connection, context)
        return self.forbidden(context)

    def student_dashboard(self, connection, context: dict) -> Response:
        active = context["active_membership"]
        user_id = context["user"]["user_id"]
        assignments = connection.execute(
            """
            SELECT a.*,
                   (SELECT COUNT(*) FROM assignment_items ai WHERE ai.assignment_id = a.id) AS total_items,
                   (
                     SELECT COUNT(DISTINCT at.exercise_id)
                     FROM attempts at
                     WHERE at.assignment_id = a.id AND at.user_id = ?
                   ) AS completed_items
            FROM assignments a
            JOIN assignment_targets t ON t.assignment_id = a.id
            WHERE t.target_user_id = ? AND a.organization_id = ?
            ORDER BY a.due_date ASC, a.created_at DESC
            """,
            (user_id, user_id, active["organization_id"]),
        ).fetchall()
        modules = connection.execute(
            """
            SELECT modules.id, modules.title,
                   COUNT(DISTINCT exercises.id) AS total_exercises,
                   COUNT(DISTINCT attempts.exercise_id) AS attempted_exercises,
                   ROUND(AVG(COALESCE(attempts.manual_score, attempts.auto_score)), 1) AS avg_score
            FROM modules
            LEFT JOIN exercises ON exercises.module_id = modules.id AND exercises.status = 'published'
            LEFT JOIN attempts ON attempts.exercise_id = exercises.id AND attempts.user_id = ?
            GROUP BY modules.id
            ORDER BY modules.sort_order
            """,
            (user_id,),
        ).fetchall()

        assignment_rows = []
        for assignment in assignments:
            progress = f"{assignment['completed_items']}/{assignment['total_items']}"
            assignment_rows.append(
                [
                    f"<a href='/assignments/{assignment['id']}'>{h(assignment['title'])}</a>",
                    h(assignment["mode"].title()),
                    h(assignment["due_date"]),
                    h(progress),
                ]
            )

        model_rows = [[f"<a href='/models/{model['slug']}'>{h(model['title'])}</a>"] for model in MODEL_PAGES]

        module_rows = []
        for module in modules:
            module_rows.append(
                [
                    f"<a href='/modules/{module['id']}'>{h(module['title'])}</a>",
                    h(f"{module['attempted_exercises']}/{module['total_exercises']}"),
                    format_score(module["avg_score"]),
                ]
            )

        content = [
            "<section class='hero compact'><div><span class='eyebrow'>Student view</span><h1>Jouw leeromgeving</h1><p>Bekijk je examenopdrachten, ga verder in je verdiepingspaden en volg je voortgang.</p></div></section>",
            "<section class='panel'><h2>Examenopdrachten</h2>"
            + self.render_table(["Opdracht", "Mode", "Deadline", "Voortgang"], assignment_rows)
            + "</section>",
            "<section class='grid two-up dashboard-split'>"
            + "<article class='panel'><h2>Modellen overzicht</h2>"
            + self.render_table(["Model"], model_rows)
            + "</article>"
            + "<article class='panel'><h2>Verdiepingspaden</h2>"
            + self.render_table(["Leerpad", "Geoefend", "Gemiddelde score"], module_rows)
            + "</article></section>",
        ]
        return self.html("Student dashboard", "".join(content), context)

    def model_image_url(self, image_stem: str) -> tuple[str | None, str]:
        image_dir = STATIC_DIR / MODEL_IMAGE_DIR_NAME
        for suffix in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"):
            candidate = image_dir / f"{image_stem}{suffix}"
            if candidate.exists():
                relative_path = candidate.relative_to(STATIC_DIR).as_posix()
                return quote(f"/static/{relative_path}", safe="/"), candidate.name
        return None, f"{image_stem}.png"

    def model_page(self, context: dict, model_slug: str) -> Response:
        model = MODEL_PAGE_LOOKUP.get(model_slug)
        if not model:
            return self.not_found(context)

        image_url, expected_filename = self.model_image_url(model["image_stem"])
        if image_url:
            image_panel = (
                "<section class='panel'>"
                f"<img src='{h(image_url)}' alt='{h(model['title'])}' "
                "style='display:block; width:100%; border-radius:1rem; border:1px solid rgba(23,48,60,0.08);'>"
                "</section>"
            )
        else:
            image_panel = (
                "<section class='panel inset'>"
                "<span class='eyebrow'>Afbeelding toevoegen</span>"
                f"<h2>{h(model['title'])}</h2>"
                f"<p>Plaats voor dit model een afbeelding in <code>static/{h(MODEL_IMAGE_DIR_NAME)}</code> "
                f"met bestandsnaam <code>{h(expected_filename)}</code>. Extensies zoals <code>.png</code>, "
                "<code>.jpg</code>, <code>.webp</code> en <code>.svg</code> werken direct.</p>"
                "</section>"
            )

        text_blocks = "".join(
            "<article class='panel'>"
            f"<h2>{h(block['heading'])}</h2>"
            + "".join(f"<p>{h(paragraph)}</p>" for paragraph in block["paragraphs"])
            + "</article>"
            for block in model["blocks"]
        )

        content = [
            "<section class='hero compact'>"
            "<div>"
            "<span class='eyebrow'>Modellen overzicht</span>"
            f"<h1>{h(model['title'])}</h1>"
            f"<p>{h(model['intro'])}</p>"
            "</div>"
            "<div class='actions'>"
            "<a class='button button-secondary' href='/dashboard'>Terug naar dashboard</a>"
            "</div>"
            "</section>",
            image_panel,
            "<section class='grid two-up'>"
            + text_blocks
            + "</section>",
        ]
        return self.html(model["title"], "".join(content), context)

    def trainer_dashboard(self, connection, context: dict) -> Response:
        active = context["active_membership"]
        assignments = connection.execute(
            """
            SELECT assignments.*,
                   (SELECT COUNT(*) FROM assignment_targets WHERE assignment_id = assignments.id) AS target_count,
                   (SELECT COUNT(*) FROM attempts WHERE assignment_id = assignments.id) AS attempt_count
            FROM assignments
            WHERE assignments.organization_id = ?
            ORDER BY assignments.created_at DESC
            """,
            (active["organization_id"],),
        ).fetchall()
        pending_reviews = connection.execute(
            """
            SELECT attempts.id, attempts.submitted_at, users.first_name, users.last_name,
                   exercises.title AS exercise_title
            FROM attempts
            JOIN assignments ON assignments.id = attempts.assignment_id
            JOIN exercises ON exercises.id = attempts.exercise_id
            JOIN users ON users.id = attempts.user_id
            WHERE assignments.organization_id = ?
              AND attempts.status = 'submitted'
              AND exercises.requires_manual_review = 1
            ORDER BY attempts.submitted_at DESC
            """,
            (active["organization_id"],),
        ).fetchall()
        students = connection.execute(
            """
            SELECT users.id, users.first_name, users.last_name,
                   COUNT(DISTINCT attempts.id) AS attempt_count,
                   ROUND(AVG(COALESCE(attempts.manual_score, attempts.auto_score)), 1) AS avg_score
            FROM memberships
            JOIN users ON users.id = memberships.user_id
            LEFT JOIN attempts ON attempts.user_id = users.id
            WHERE memberships.organization_id = ? AND memberships.role = 'student'
            GROUP BY users.id
            ORDER BY users.first_name, users.last_name
            """,
            (active["organization_id"],),
        ).fetchall()

        assignment_rows = [
            [
                f"<a href='/assignments/{row['id']}'>{h(row['title'])}</a>",
                h(row["mode"].title()),
                h(row["target_count"]),
                h(row["attempt_count"]),
                h(row["due_date"]),
            ]
            for row in assignments
        ]
        review_rows = [
            [
                f"<a href='/attempts/{row['id']}/review'>{h(row['exercise_title'])}</a>",
                h(f"{row['first_name']} {row['last_name']}"),
                h(row["submitted_at"].replace('T', ' ')),
            ]
            for row in pending_reviews
        ]
        student_rows = [
            [
                f"<a href='/students/{row['id']}'>{h(row['first_name'])} {h(row['last_name'])}</a>",
                h(row["attempt_count"]),
                format_score(row["avg_score"]),
            ]
            for row in students
        ]

        content = [
            "<section class='hero compact'><div><span class='eyebrow'>Trainer view</span><h1>Begeleiden en beoordelen</h1><p>Volg voortgang, maak opdrachten en behandel open inzendingen.</p></div><div class='actions'><a class='button button-primary' href='/assignments/new'>Nieuwe opdracht</a><a class='button button-secondary' href='/reviews'>Open reviews</a></div></section>",
            self.metrics_row(
                [
                    ("Opdrachten", str(len(assignments))),
                    ("Pending reviews", str(len(pending_reviews))),
                    ("Studenten", str(len(students))),
                ]
            ),
            "<section class='grid two-up'>"
            + "<article class='panel'><h2>Opdrachten</h2>"
            + self.render_table(["Titel", "Mode", "Deelnemers", "Inzendingen", "Deadline"], assignment_rows)
            + "</article>"
            + "<article class='panel'><h2>Wacht op review</h2>"
            + self.render_table(["Oefening", "Student", "Ingediend"], review_rows)
            + "</article></section>",
            "<section class='panel'><h2>Student voortgang</h2>"
            + self.render_table(["Student", "Pogingen", "Gemiddelde"], student_rows)
            + "</section>",
        ]
        return self.html("Trainer dashboard", "".join(content), context)

    def organization_admin_dashboard(self, connection, context: dict) -> Response:
        active = context["active_membership"]
        memberships = connection.execute(
            """
            SELECT users.id, users.first_name, users.last_name, users.email, memberships.role
            FROM memberships
            JOIN users ON users.id = memberships.user_id
            WHERE memberships.organization_id = ?
            ORDER BY memberships.role, users.first_name
            """,
            (active["organization_id"],),
        ).fetchall()
        assignment_count = connection.execute(
            "SELECT COUNT(*) AS count FROM assignments WHERE organization_id = ?",
            (active["organization_id"],),
        ).fetchone()["count"]
        body = [
            "<section class='hero compact'><div><span class='eyebrow'>Organization admin</span><h1>Tenant beheer</h1><p>Controleer gebruikers, opdrachten en branding voor jouw opleidersomgeving.</p></div><div class='actions'><a class='button button-primary' href='/settings/theme'>Branding aanpassen</a></div></section>",
            self.metrics_row(
                [
                    ("Gebruikers", str(len(memberships))),
                    ("Opdrachten", str(assignment_count)),
                    ("Rollen", str(len({row['role'] for row in memberships}))),
                ]
            ),
            "<section class='panel'><h2>Gebruikers in deze organisatie</h2>"
            + self.render_table(
                ["Naam", "E-mail", "Rol"],
                [
                    [h(f"{row['first_name']} {row['last_name']}"), h(row["email"]), h(row["role"])]
                    for row in memberships
                ],
            )
            + "</section>",
        ]
        return self.html("Organization dashboard", "".join(body), context)

    def get_module_quiz_session(self, connection, user_id: int, module_id: int):
        return connection.execute(
            """
            SELECT *
            FROM module_quiz_sessions
            WHERE user_id = ? AND module_id = ?
            """,
            (user_id, module_id),
        ).fetchone()

    def save_module_quiz_session(
        self,
        connection,
        user_id: int,
        module_id: int,
        queue: list[int],
        current_position: int,
        status: str = "active",
    ) -> None:
        queue_json = json.dumps(queue)
        updated_at = db.utc_now_iso()
        existing = self.get_module_quiz_session(connection, user_id, module_id)
        if existing:
            connection.execute(
                """
                UPDATE module_quiz_sessions
                SET queue_json = ?, current_position = ?, status = ?, updated_at = ?
                WHERE user_id = ? AND module_id = ?
                """,
                (queue_json, current_position, status, updated_at, user_id, module_id),
            )
            return

        connection.execute(
            """
            INSERT INTO module_quiz_sessions (
                user_id, module_id, queue_json, current_position, status, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, module_id, queue_json, current_position, status, updated_at),
        )

    def module_page(self, connection, request: Request, context: dict, module_id: int) -> Response:
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

        resources = connection.execute(
            "SELECT * FROM resources WHERE module_id = ? ORDER BY sort_order",
            (module_id,),
        ).fetchall()
        topics = connection.execute(
            "SELECT * FROM topics WHERE module_id = ? ORDER BY sort_order",
            (module_id,),
        ).fetchall()
        exercise_count = connection.execute(
            "SELECT COUNT(*) AS count FROM exercises WHERE module_id = ? AND status = 'published'",
            (module_id,),
        ).fetchone()["count"]
        quiz_session = self.get_module_quiz_session(connection, context["user"]["user_id"], module_id)
        topic_blocks = []
        for topic in topics:
            concepts = connection.execute(
                "SELECT * FROM concepts WHERE topic_id = ? ORDER BY sort_order",
                (topic["id"],),
            ).fetchall()
            topic_blocks.append(
                "<article class='topic-card'>"
                f"<h3>{h(topic['title'])}</h3>"
                f"<p>{h(topic['summary'])}</p>"
                + "".join(
                    f"<div class='concept-chip'><strong>{h(concept['title'])}</strong><span>{h(concept['summary'])}</span></div>"
                    for concept in concepts
                )
                + "</article>"
            )

        quiz_intro = "Doorloop alle kennisvragen van dit leerpad in een eigen quiz-flow met directe feedback, herhaalvragen en opgeslagen voortgang."
        quiz_action = (
            f"<a class='button button-primary' href='/modules/{module_id}/quiz'>Start vragenflow</a>"
            if exercise_count
            else "<span class='button button-secondary disabled'>Nog geen vragen</span>"
        )
        quiz_extra_action = ""

        if quiz_session and quiz_session["status"] == "active" and exercise_count:
            saved_queue = parse_json(quiz_session["queue_json"], [])
            total_steps = len(saved_queue) or exercise_count
            current_step = min(int(quiz_session["current_position"]) + 1, total_steps)
            repeat_count = max(0, total_steps - exercise_count)
            repeat_note = (
                f" Er staan ook nog {repeat_count} herhaalvragen klaar."
                if repeat_count
                else ""
            )
            quiz_intro = (
                f"Je hebt al voortgang opgeslagen. Ga verder bij stap {current_step} van {total_steps}."
                f"{repeat_note} Je voortgang wordt na elk antwoord automatisch bewaard."
            )
            quiz_action = f"<a class='button button-primary' href='/modules/{module_id}/quiz'>Verder waar je was</a>"
            quiz_extra_action = f"<a class='button button-secondary' href='/modules/{module_id}/quiz?restart=1'>Opnieuw beginnen</a>"

        pathway_cards = f"""
        <section class='panel'>
          <h2>Verdiepingspaden</h2>
          <div class='pathway-grid'>
            <article class='pathway-card active'>
              <span class='eyebrow'>Nu beschikbaar</span>
              <h3>Vragen van dit leerpad</h3>
              <p>{h(quiz_intro)}</p>
              <div class='actions'>
                {quiz_action}
                {quiz_extra_action}
              </div>
            </article>
            <article class='pathway-card'>
              <span class='eyebrow'>Volgende stap</span>
              <h3>Toepassingen met tekstvoorbeelden</h3>
              <p>Cases en voorbeeldteksten waarmee studenten de theorie leren herkennen en toepassen in geschreven taal.</p>
              <span class='button button-secondary disabled'>Nog niet gebouwd</span>
            </article>
            <article class='pathway-card'>
              <span class='eyebrow'>Latere stap</span>
              <h3>Toepassingen met videovoorbeelden</h3>
              <p>Analyse van gedrag, mimiek en congruentie in video, gekoppeld aan theorie en observatievragen.</p>
              <span class='button button-secondary disabled'>Nog niet gebouwd</span>
            </article>
          </div>
        </section>
        """

        content = [
            f"<section class='hero compact'><div><span class='eyebrow'>{h(module['program_title'])}</span><h1>{h(module['title'])}</h1><p>{h(module['summary'])}</p></div></section>",
            pathway_cards,
            "<section class='panel'><h2>Lesmateriaal</h2>"
            + "".join(
                f"<div class='resource-block'><strong>{h(resource['title'])}</strong><span>{h(resource['resource_type'])}</span><p>{h(resource['content'])}</p></div>"
                for resource in resources
            )
            + "</section>",
            "<section class='panel'><h2>Onderwerpen en concepten</h2><div class='topic-grid'>"
            + "".join(topic_blocks)
            + "</div></section>",
        ]
        return self.html(h(module["title"]), "".join(content), context)

    def parse_module_quiz_queue(self, raw_queue: str, base_queue: list[int]) -> list[int]:
        if not raw_queue:
            return list(base_queue)

        allowed_ids = set(base_queue)
        parsed_queue: list[int] = []
        for token in raw_queue.split(","):
            candidate = token.strip()
            if not candidate:
                continue
            try:
                exercise_id = int(candidate)
            except ValueError:
                continue
            if exercise_id in allowed_ids:
                parsed_queue.append(exercise_id)

        return parsed_queue or list(base_queue)

    def build_module_quiz_url(
        self,
        module_id: int,
        queue: list[int],
        position: int,
        attempt_id: int | None = None,
        auto_repeat: bool = False,
    ) -> str:
        query_parts = [
            f"position={position}",
            "queue=" + quote_plus(",".join(str(exercise_id) for exercise_id in queue)),
        ]
        if attempt_id is not None:
            query_parts.append(f"attempt_id={attempt_id}")
        if auto_repeat:
            query_parts.append("auto_repeat=1")
        return f"/modules/{module_id}/quiz?" + "&".join(query_parts)

    def build_module_quiz_next_url(self, module_id: int, queue: list[int], position: int) -> str:
        if position >= len(queue):
            return f"/modules/{module_id}/quiz/complete"
        return self.build_module_quiz_url(module_id, queue, position)

    def should_requeue_module_question(self, exercise, result: dict) -> bool:
        if exercise["exercise_type"] == "study_card":
            return False
        if result.get("requires_review"):
            return False
        auto_score = result.get("auto_score")
        max_score = result.get("max_score") or exercise["max_score"]
        if auto_score is None:
            return False
        return float(auto_score) < float(max_score)

    def module_quiz_page(self, connection, request: Request, context: dict, module_id: int) -> Response:
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

        exercises = connection.execute(
            """
            SELECT *
            FROM exercises
            WHERE module_id = ? AND status = 'published'
            ORDER BY id
            """,
            (module_id,),
        ).fetchall()
        if not exercises:
            return self.html(
                h(module["title"]),
                f"<section class='panel'><h1>{h(module['title'])}</h1><p>Er zijn nog geen vragen voor dit leerpad.</p></section>",
                context,
            )

        exercise_lookup = {exercise["id"]: exercise for exercise in exercises}
        base_queue = [exercise["id"] for exercise in exercises]
        quiz_session = self.get_module_quiz_session(connection, context["user"]["user_id"], module_id)
        explicit_queue = request.get("queue")
        restarting = request.get("restart") == "1"

        if restarting:
            queue = list(base_queue)
            current_position = 0
            self.save_module_quiz_session(
                connection,
                context["user"]["user_id"],
                module_id,
                queue,
                current_position,
                "active",
            )
            connection.commit()
        elif explicit_queue:
            queue = self.parse_module_quiz_queue(explicit_queue, base_queue)
            position_raw = request.get("position", request.get("index", "0"))
            try:
                current_position = int(position_raw)
            except ValueError:
                current_position = 0
        elif quiz_session and quiz_session["status"] == "active":
            saved_queue = [
                exercise_id
                for exercise_id in parse_json(quiz_session["queue_json"], [])
                if exercise_id in exercise_lookup
            ]
            queue = saved_queue or list(base_queue)
            try:
                current_position = int(quiz_session["current_position"])
            except (TypeError, ValueError):
                current_position = 0
        else:
            queue = list(base_queue)
            current_position = 0
            self.save_module_quiz_session(
                connection,
                context["user"]["user_id"],
                module_id,
                queue,
                current_position,
                "active",
            )
            connection.commit()

        total_steps = len(queue)
        current_position = max(0, current_position)
        if current_position >= total_steps:
            self.save_module_quiz_session(
                connection,
                context["user"]["user_id"],
                module_id,
                queue,
                total_steps,
                "completed",
            )
            connection.commit()
            return self.redirect(f"/modules/{module_id}/quiz/complete")

        if explicit_queue and not request.get("attempt_id"):
            self.save_module_quiz_session(
                connection,
                context["user"]["user_id"],
                module_id,
                queue,
                current_position,
                "active",
            )
            connection.commit()

        current_exercise = exercise_lookup[queue[current_position]]

        if request.method == "POST":
            if not self.verify_csrf(request, context):
                return self.forbidden(context, "Ongeldige CSRF token.")
            posted_queue = self.parse_module_quiz_queue(request.get("queue"), base_queue)
            posted_steps = len(posted_queue)
            try:
                posted_position = int(request.get("position", str(current_position)))
            except ValueError:
                posted_position = current_position
            posted_position = max(0, min(posted_steps - 1, posted_position))
            try:
                posted_exercise_id = int(request.get("exercise_id", str(current_exercise["id"])))
            except ValueError:
                posted_exercise_id = current_exercise["id"]
            exercise = exercise_lookup.get(posted_exercise_id, current_exercise)
            response_payload = self.collect_response(exercise, request)
            result = score_submission(exercise, response_payload, "learn")
            cursor = connection.execute(
                """
                INSERT INTO attempts (
                    assignment_id, exercise_id, user_id, started_at, submitted_at, status,
                    auto_score, manual_score, max_score, feedback
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    None,
                    exercise["id"],
                    context["user"]["user_id"],
                    db.utc_now_iso(),
                    db.utc_now_iso(),
                    "submitted" if result["requires_review"] else "scored",
                    result["auto_score"],
                    None,
                    result["max_score"],
                    result["feedback"],
                ),
            )
            attempt_id = cursor.lastrowid
            updated_queue = list(posted_queue)
            auto_repeat = self.should_requeue_module_question(exercise, result)
            if auto_repeat:
                updated_queue.append(exercise["id"])
            next_position = posted_position + 1
            next_status = "completed" if next_position >= len(updated_queue) else "active"
            connection.execute(
                "INSERT INTO responses (attempt_id, response_json) VALUES (?, ?)",
                (attempt_id, json.dumps(response_payload)),
            )
            self.save_module_quiz_session(
                connection,
                context["user"]["user_id"],
                module_id,
                updated_queue,
                next_position,
                next_status,
            )
            connection.commit()

            return self.redirect(
                self.build_module_quiz_url(
                    module_id,
                    updated_queue,
                    posted_position,
                    attempt_id=attempt_id,
                    auto_repeat=auto_repeat,
                )
            )

        attempt = None
        attempt_response = None
        show_feedback = False
        attempt_id = request.get("attempt_id")
        if attempt_id:
            attempt = connection.execute(
                """
                SELECT attempts.*, exercises.content_json, exercises.exercise_type, exercises.title AS exercise_title
                FROM attempts
                JOIN exercises ON exercises.id = attempts.exercise_id
                WHERE attempts.id = ? AND attempts.user_id = ?
                """,
                (int(attempt_id), context["user"]["user_id"]),
            ).fetchone()
            if attempt and attempt["exercise_id"] == current_exercise["id"]:
                response_row = connection.execute(
                    "SELECT response_json FROM responses WHERE attempt_id = ?",
                    (attempt["id"],),
                ).fetchone()
                attempt_response = parse_json(response_row["response_json"] if response_row else "{}", {})
                show_feedback = True

        auto_repeat = request.get("auto_repeat") == "1"
        repeat_count = max(0, len(queue) - len(base_queue))
        repeat_helper = (
            f"<p class='helper'>Er staan nu {repeat_count} herhaalvragen ingepland op basis van eerdere antwoorden.</p>"
            if repeat_count
            else ""
        )
        previous_link = (
            f"<a class='button button-secondary' href='{h(self.build_module_quiz_url(module_id, queue, current_position - 1))}'>Vorige vraag</a>"
            if current_position > 0
            else f"<a class='button button-secondary' href='/modules/{module_id}'>Terug naar leerpad</a>"
        )
        next_url = self.build_module_quiz_next_url(module_id, queue, current_position + 1)
        next_label = "Volgende vraag" if current_position + 1 < len(queue) else "Afronden"
        progress_percent = round(((current_position + 1) / total_steps) * 100)
        progress_label = f"Stap {current_position + 1} van {total_steps}"
        content = parse_json(current_exercise["content_json"], {})

        if show_feedback:
            model_answer = parse_json(attempt["content_json"], {}).get("model_answer", "")
            feedback_note = ""
            if current_exercise["exercise_type"] == "study_card":
                feedback_note = (
                    "<p class='helper'>Open vragen worden hier nog niet automatisch beoordeeld. "
                    "Vergelijk je antwoord met het modelantwoord en kies daarna of je deze vraag later opnieuw wilt zien.</p>"
                )
                actions_html = (
                    "<div class='actions'>"
                    + previous_link
                    + f"<a class='button button-primary' href='{h(self.build_module_quiz_next_url(module_id, queue + [current_exercise['id']], current_position + 1))}'>Later nogmaals</a>"
                    + f"<a class='button button-secondary' href='{h(next_url)}'>Ga verder</a>"
                    + "</div>"
                )
            else:
                if auto_repeat:
                    feedback_note = (
                        "<p class='helper'>Deze vraag komt later in deze flow nog een keer terug, "
                        "omdat je antwoord nog niet volledig goed was.</p>"
                    )
                else:
                    feedback_note = "<p class='helper'>Deze vraag is afgerond. Je kunt verder met de volgende stap.</p>"
                actions_html = (
                    "<div class='actions'>"
                    + previous_link
                    + f"<a class='button button-primary' href='{h(next_url)}'>{next_label}</a>"
                    + "</div>"
                )
            feedback_html = f"""
            <section class='panel quiz-feedback'>
              <h2>Feedback</h2>
              <p>{h(attempt['feedback'])}</p>
              {feedback_note}
              <div class='grid two-up'>
                <article class='panel inset'>
                  <h3>Jouw antwoord</h3>
                  {self.render_response_summary(current_exercise['exercise_type'], attempt_response)}
                </article>
                <article class='panel inset'>
                  <h3>Modelantwoord</h3>
                  <p>{h(model_answer or 'Er is geen modelantwoord ingevuld.')}</p>
                </article>
              </div>
              {actions_html}
            </section>
            """
            body = f"""
            <section class='hero compact'>
              <div>
                <span class='eyebrow'>{h(module['program_title'])}</span>
                <h1>{h(module['title'])} - vragenflow</h1>
                <p>{h(progress_label)}</p>
              </div>
              <div class='progress-pill'>{progress_percent}%</div>
            </section>
            <section class='panel progress-panel'>
              <div class='progress-bar'><span style='width: {progress_percent}%;'></span></div>
              <p>{h(current_exercise['prompt'])}</p>
              <p class='helper'>Je voortgang wordt automatisch opgeslagen, zodat je later verder kunt gaan waar je bent gebleven.</p>
              {repeat_helper}
            </section>
            {feedback_html}
            """
            return self.html(f"{module['title']} quiz", body, context)

        body = f"""
        <section class='hero compact'>
          <div>
            <span class='eyebrow'>{h(module['program_title'])}</span>
            <h1>{h(module['title'])} - vragenflow</h1>
            <p>{h(progress_label)}</p>
          </div>
          <div class='progress-pill'>{progress_percent}%</div>
        </section>
        <section class='panel progress-panel'>
          <div class='progress-bar'><span style='width: {progress_percent}%;'></span></div>
          <p>Doorloop alle vragen van dit leerpad in volgorde. Vragen die nog niet volledig goed zijn komen later nog een keer terug.</p>
          <p class='helper'>Je voortgang wordt na ieder antwoord automatisch opgeslagen.</p>
          {repeat_helper}
        </section>
        <section class='panel exercise-panel'>
          <div class='exercise-header'>
            <div>
              <span class='eyebrow'>Stap {current_position + 1}</span>
              <h2>{h(current_exercise['title'])}</h2>
              <p>{h(current_exercise['prompt'])}</p>
            </div>
            <div class='tag-group'>
              <span class='tag'>{h(current_exercise['exercise_type'])}</span>
              <span class='tag'>{h(current_exercise['difficulty'])}</span>
            </div>
          </div>
          <form method='post' action='/modules/{module_id}/quiz'>
            <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
            <input type='hidden' name='position' value='{current_position}'>
            <input type='hidden' name='queue' value='{h(",".join(str(exercise_id) for exercise_id in queue))}'>
            <input type='hidden' name='exercise_id' value='{current_exercise['id']}'>
            {self.render_exercise_form(current_exercise, content)}
            <div class='actions'>
              {previous_link}
              <button class='button button-primary' type='submit'>Antwoord indienen</button>
            </div>
          </form>
        </section>
        """
        return self.html(f"{module['title']} quiz", body, context)

    def module_quiz_complete_page(self, connection, request: Request, context: dict, module_id: int) -> Response:
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

        quiz_session = self.get_module_quiz_session(connection, context["user"]["user_id"], module_id)
        if quiz_session:
            saved_queue = parse_json(quiz_session["queue_json"], [])
            self.save_module_quiz_session(
                connection,
                context["user"]["user_id"],
                module_id,
                saved_queue,
                len(saved_queue),
                "completed",
            )
            connection.commit()

        attempts = connection.execute(
            """
            SELECT attempts.*, exercises.title AS exercise_title
            FROM attempts
            JOIN exercises ON exercises.id = attempts.exercise_id
            WHERE attempts.user_id = ?
              AND exercises.module_id = ?
            ORDER BY attempts.submitted_at DESC
            """,
            (context["user"]["user_id"], module_id),
        ).fetchall()

        latest_by_exercise = {}
        for attempt in attempts:
            latest_by_exercise.setdefault(attempt["exercise_id"], attempt)
        latest_attempts = list(latest_by_exercise.values())
        scored_attempts = [attempt for attempt in latest_attempts if db.effective_score(attempt) is not None]
        average_score = (
            round(sum(float(db.effective_score(attempt)) for attempt in scored_attempts) / len(scored_attempts), 1)
            if scored_attempts
            else None
        )

        body = [
            f"<section class='hero compact'><div><span class='eyebrow'>{h(module['program_title'])}</span><h1>{h(module['title'])} afgerond</h1><p>Je hebt de vragenflow van dit leerpad doorlopen. Je kunt terug naar het leerpad of direct opnieuw oefenen.</p></div><div class='actions'><a class='button button-primary' href='/modules/{module_id}/quiz?restart=1'>Opnieuw starten</a><a class='button button-secondary' href='/modules/{module_id}'>Terug naar leerpad</a></div></section>",
            self.metrics_row(
                [
                    ("Beantwoorde vragen", str(len(latest_attempts))),
                    ("Gemiddelde score", format_score(average_score)),
                    ("Reviews in afwachting", str(len([attempt for attempt in latest_attempts if attempt["status"] == "submitted"]))),
                ]
            ),
            "<section class='panel'><h2>Laatste resultaten in dit leerpad</h2>"
            + self.render_table(
                ["Vraag", "Score", "Status"],
                [
                    [
                        h(attempt["exercise_title"]),
                        format_score(db.effective_score(attempt)),
                        h(attempt["status"]),
                    ]
                    for attempt in latest_attempts
                ],
            )
            + "</section>",
        ]
        return self.html(f"{module['title']} afgerond", "".join(body), context)

    def assignment_builder(self, connection, request: Request, context: dict) -> Response:
        if not self.require_role(context, {"trainer", "organization_admin"}):
            return self.forbidden(context)

        active = context["active_membership"]
        if request.method == "POST":
            if not self.verify_csrf(request, context):
                return self.forbidden(context, "Ongeldige CSRF token.")
            title = request.get("title").strip()
            description = request.get("description").strip()
            mode = request.get("mode") or "learn"
            due_date = request.get("due_date")
            target_user_ids = [int(value) for value in request.getlist("target_user_ids") if value]
            exercise_ids = [int(value) for value in request.getlist("exercise_ids") if value]
            if not title or not target_user_ids or not exercise_ids:
                return self.redirect("/assignments/new?notice=" + quote_plus("Vul titel, deelnemers en oefeningen in."))

            cursor = connection.execute(
                """
                INSERT INTO assignments (
                    organization_id, created_by_user_id, title, description, mode, due_date, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?)
                """,
                (
                    active["organization_id"],
                    context["user"]["user_id"],
                    title,
                    description or "Nieuwe opdracht",
                    mode,
                    due_date or db.utc_now().date().isoformat(),
                    db.utc_now_iso(),
                ),
            )
            assignment_id = cursor.lastrowid
            for index, exercise_id in enumerate(exercise_ids, start=1):
                connection.execute(
                    "INSERT INTO assignment_items (assignment_id, exercise_id, sort_order) VALUES (?, ?, ?)",
                    (assignment_id, exercise_id, index),
                )
            for target_user_id in target_user_ids:
                connection.execute(
                    "INSERT INTO assignment_targets (assignment_id, target_user_id) VALUES (?, ?)",
                    (assignment_id, target_user_id),
                )
            connection.commit()
            return self.redirect(
                "/assignments/" + str(assignment_id) + "?notice=" + quote_plus("Opdracht aangemaakt.")
            )

        exercises = connection.execute(
            """
            SELECT exercises.id, exercises.title, exercises.exercise_type, modules.title AS module_title
            FROM exercises
            JOIN modules ON modules.id = exercises.module_id
            WHERE exercises.status = 'published'
            ORDER BY modules.sort_order, exercises.title
            """
        ).fetchall()
        students = connection.execute(
            """
            SELECT users.id, users.first_name, users.last_name
            FROM memberships
            JOIN users ON users.id = memberships.user_id
            WHERE memberships.organization_id = ? AND memberships.role = 'student'
            ORDER BY users.first_name, users.last_name
            """,
            (active["organization_id"],),
        ).fetchall()

        exercise_options = "".join(
            f"<label class='checkbox-row'><input type='checkbox' name='exercise_ids' value='{exercise['id']}'><span><strong>{h(exercise['title'])}</strong><small>{h(exercise['module_title'])} - {h(exercise['exercise_type'])}</small></span></label>"
            for exercise in exercises
        )
        student_options = "".join(
            f"<label class='checkbox-row'><input type='checkbox' name='target_user_ids' value='{student['id']}'><span>{h(student['first_name'])} {h(student['last_name'])}</span></label>"
            for student in students
        )

        body = f"""
        <section class='panel form-panel'>
          <h1>Nieuwe opdracht</h1>
          <form method='post' action='/assignments/new'>
            <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
            <label class='field'><span>Titel</span><input type='text' name='title' required></label>
            <label class='field'><span>Beschrijving</span><textarea name='description' rows='3'></textarea></label>
            <div class='field-row'>
              <label class='field'><span>Mode</span>
                <select name='mode'>
                  <option value='learn'>Learn mode</option>
                  <option value='exam'>Exam mode</option>
                </select>
              </label>
              <label class='field'><span>Deadline</span><input type='date' name='due_date'></label>
            </div>
            <div class='grid two-up'>
              <article class='panel inset'><h2>Studenten</h2>{student_options}</article>
              <article class='panel inset'><h2>Oefeningen</h2>{exercise_options}</article>
            </div>
            <button class='button button-primary' type='submit'>Opslaan</button>
          </form>
        </section>
        """
        return self.html("Nieuwe opdracht", body, context)

    def assignment_page(self, connection, request: Request, context: dict, assignment_id: int) -> Response:
        assignment = connection.execute(
            "SELECT * FROM assignments WHERE id = ?",
            (assignment_id,),
        ).fetchone()
        if not assignment:
            return self.not_found(context)

        items = connection.execute(
            """
            SELECT assignment_items.sort_order, exercises.*
            FROM assignment_items
            JOIN exercises ON exercises.id = assignment_items.exercise_id
            WHERE assignment_items.assignment_id = ?
            ORDER BY assignment_items.sort_order
            """,
            (assignment_id,),
        ).fetchall()

        if self.require_role(context, {"student"}):
            target = connection.execute(
                "SELECT 1 FROM assignment_targets WHERE assignment_id = ? AND target_user_id = ?",
                (assignment_id, context["user"]["user_id"]),
            ).fetchone()
            if not target:
                return self.forbidden(context)

            rows = []
            for item in items:
                latest = connection.execute(
                    """
                    SELECT * FROM attempts
                    WHERE assignment_id = ? AND exercise_id = ? AND user_id = ?
                    ORDER BY submitted_at DESC
                    LIMIT 1
                    """,
                    (assignment_id, item["id"], context["user"]["user_id"]),
                ).fetchone()
                action = (
                    f"<a class='button button-secondary small' href='/attempts/{latest['id']}'>Bekijk resultaat</a>"
                    if latest and assignment["mode"] == "exam"
                    else f"<a class='button button-secondary small' href='/exercises/{item['id']}?assignment={assignment_id}'>Open oefening</a>"
                )
                rows.append(
                    [
                        h(item["title"]),
                        h(item["exercise_type"]),
                        format_score(db.effective_score(latest)) if latest else "Nog niet gestart",
                        action,
                    ]
                )
            body = (
                f"<section class='hero compact'><div><span class='eyebrow'>{h(assignment['mode'].title())}</span><h1>{h(assignment['title'])}</h1><p>{h(assignment['description'])}</p></div></section>"
                + "<section class='panel'><h2>Opdrachtonderdelen</h2>"
                + self.render_table(["Oefening", "Type", "Score", "Actie"], rows)
                + "</section>"
            )
            return self.html(h(assignment["title"]), body, context)

        targets = connection.execute(
            """
            SELECT users.first_name, users.last_name,
                   COUNT(DISTINCT attempts.exercise_id) AS completed_items,
                   ROUND(AVG(COALESCE(attempts.manual_score, attempts.auto_score)), 1) AS avg_score
            FROM assignment_targets
            JOIN users ON users.id = assignment_targets.target_user_id
            LEFT JOIN attempts ON attempts.assignment_id = assignment_targets.assignment_id
                               AND attempts.user_id = assignment_targets.target_user_id
            WHERE assignment_targets.assignment_id = ?
            GROUP BY users.id
            ORDER BY users.first_name
            """,
            (assignment_id,),
        ).fetchall()

        rows = [
            [
                h(f"{row['first_name']} {row['last_name']}"),
                h(row["completed_items"]),
                format_score(row["avg_score"]),
            ]
            for row in targets
        ]
        body = (
            f"<section class='hero compact'><div><span class='eyebrow'>{h(assignment['mode'].title())}</span><h1>{h(assignment['title'])}</h1><p>{h(assignment['description'])}</p></div></section>"
            + "<section class='grid two-up'>"
            + "<article class='panel'><h2>Oefeningen</h2>"
            + self.render_table(
                ["Volgorde", "Titel", "Type"],
                [[h(item["sort_order"]), h(item["title"]), h(item["exercise_type"])] for item in items],
            )
            + "</article>"
            + "<article class='panel'><h2>Deelnemers</h2>"
            + self.render_table(["Student", "Voltooid", "Gemiddelde"], rows)
            + "</article></section>"
        )
        return self.html(h(assignment["title"]), body, context)

    def exercise_page(self, connection, request: Request, context: dict, exercise_id: int) -> Response:
        exercise = connection.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
        if not exercise:
            return self.not_found(context)

        assignment_id = request.get("assignment")
        assignment = None
        mode = request.get("mode") or "learn"
        if assignment_id:
            assignment = connection.execute("SELECT * FROM assignments WHERE id = ?", (int(assignment_id),)).fetchone()
            if assignment:
                mode = assignment["mode"]

        if request.method == "POST":
            if not self.require_role(context, {"student"}):
                return self.forbidden(context)
            if not self.verify_csrf(request, context):
                return self.forbidden(context, "Ongeldige CSRF token.")
            response_payload = self.collect_response(exercise, request)
            result = score_submission(exercise, response_payload, mode)
            cursor = connection.execute(
                """
                INSERT INTO attempts (
                    assignment_id, exercise_id, user_id, started_at, submitted_at, status,
                    auto_score, manual_score, max_score, feedback
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    assignment["id"] if assignment else None,
                    exercise_id,
                    context["user"]["user_id"],
                    db.utc_now_iso(),
                    db.utc_now_iso(),
                    "submitted" if result["requires_review"] else "scored",
                    result["auto_score"],
                    None,
                    result["max_score"],
                    result["feedback"],
                ),
            )
            attempt_id = cursor.lastrowid
            connection.execute(
                "INSERT INTO responses (attempt_id, response_json) VALUES (?, ?)",
                (attempt_id, json.dumps(response_payload)),
            )
            connection.commit()
            return self.redirect(f"/attempts/{attempt_id}?notice=" + quote_plus("Oefening opgeslagen."))

        if self.require_role(context, {"student"}) and assignment and assignment["mode"] == "exam":
            existing = connection.execute(
                """
                SELECT id FROM attempts
                WHERE assignment_id = ? AND exercise_id = ? AND user_id = ?
                ORDER BY submitted_at DESC LIMIT 1
                """,
                (assignment["id"], exercise_id, context["user"]["user_id"]),
            ).fetchone()
            if existing:
                return self.redirect(f"/attempts/{existing['id']}")

        content = parse_json(exercise["content_json"], {})
        body = f"""
        <section class='panel exercise-panel'>
          <div class='exercise-header'>
            <div>
              <span class='eyebrow'>{h(mode.title())}</span>
              <h1>{h(exercise['title'])}</h1>
              <p>{h(exercise['prompt'])}</p>
            </div>
            <div class='tag-group'>
              <span class='tag'>{h(exercise['exercise_type'])}</span>
              <span class='tag'>{h(exercise['difficulty'])}</span>
            </div>
          </div>
          <form method='post' action='/exercises/{exercise_id}{f"?assignment={assignment['id']}" if assignment else "?mode=learn"}'>
            <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
            {self.render_exercise_form(exercise, content)}
            <div class='actions'>
              <button class='button button-primary' type='submit'>Antwoord opslaan</button>
              {f"<a class='button button-secondary' href='/assignments/{assignment['id']}'>Terug naar opdracht</a>" if assignment else "<a class='button button-secondary' href='/dashboard'>Terug naar dashboard</a>"}
            </div>
          </form>
        </section>
        """
        return self.html(h(exercise["title"]), body, context)

    def collect_response(self, exercise, request: Request) -> dict:
        exercise_type = exercise["exercise_type"]
        content = parse_json(exercise["content_json"], {})
        if exercise_type == "multiple_choice":
            return {"selected": request.get("selected")}
        if exercise_type == "multi_select":
            return {"selected": request.getlist("selected")}
        if exercise_type == "match_pairs":
            matches = {}
            for index, pair in enumerate(content.get("pairs", [])):
                matches[pair["left"]] = request.get(f"match_{index}")
            return {"matches": matches}
        if exercise_type == "short_answer":
            return {"answer": request.get("answer")}
        if exercise_type == "study_card":
            return {"answer": request.get("answer")}
        if exercise_type == "text_analysis":
            return {"selected": request.get("selected"), "follow_up": request.get("follow_up")}
        if exercise_type in {"reflection", "case_review"}:
            return {"answer": request.get("answer")}
        return {}

    def render_exercise_form(self, exercise, content: dict) -> str:
        exercise_type = exercise["exercise_type"]
        intro = f"<p class='helper'>{h(exercise['instructions'])}</p>"
        if exercise_type == "multiple_choice":
            options = "".join(
                f"<label class='checkbox-row'><input type='radio' name='selected' value='{h(option['value'])}' required><span>{h(option['label'])}</span></label>"
                for option in content.get("options", [])
            )
            return intro + f"<fieldset class='option-list'><legend>{h(content.get('question', 'Vraag'))}</legend>{options}</fieldset>"
        if exercise_type == "multi_select":
            options = "".join(
                f"<label class='checkbox-row'><input type='checkbox' name='selected' value='{h(option['value'])}'><span>{h(option['label'])}</span></label>"
                for option in content.get("options", [])
            )
            return intro + f"<fieldset class='option-list'><legend>{h(content.get('question', 'Vraag'))}</legend>{options}</fieldset>"
        if exercise_type == "match_pairs":
            rows = []
            for index, pair in enumerate(content.get("pairs", [])):
                options = "".join(
                    f"<option value='{h(option)}'>{h(option)}</option>" for option in pair.get("options", [])
                )
                rows.append(
                    f"<label class='field'><span>{h(pair['left'])}</span><select name='match_{index}' required><option value=''>Kies...</option>{options}</select></label>"
                )
            return intro + "".join(rows)
        if exercise_type == "short_answer":
            return intro + f"<label class='field'><span>{h(content.get('question', 'Vraag'))}</span><textarea name='answer' rows='6' placeholder='{h(content.get('placeholder', ''))}' required></textarea></label>"
        if exercise_type == "study_card":
            return intro + f"<label class='field'><span>{h(content.get('question', 'Vraag'))}</span><textarea name='answer' rows='7' placeholder='{h(content.get('placeholder', ''))}' required></textarea></label>"
        if exercise_type == "text_analysis":
            options = "".join(
                f"<label class='checkbox-row'><input type='radio' name='selected' value='{h(option['value'])}' required><span>{h(option['label'])}</span></label>"
                for option in content.get("options", [])
            )
            return (
                intro
                + f"<article class='analysis-text'>{h(content.get('text', ''))}</article>"
                + f"<fieldset class='option-list'><legend>{h(content.get('pattern_question', 'Patroon'))}</legend>{options}</fieldset>"
                + f"<label class='field'><span>{h(content.get('follow_up_prompt', 'Welke vraag stel je?'))}</span><textarea name='follow_up' rows='5' required></textarea></label>"
            )
        if exercise_type == "reflection":
            return intro + f"<label class='field'><span>{h(content.get('question', 'Reflectie'))}</span><textarea name='answer' rows='8' placeholder='{h(content.get('placeholder', ''))}' required></textarea></label>"
        if exercise_type == "case_review":
            guidance = "".join(f"<li>{h(point)}</li>" for point in content.get("guidance_points", []))
            return (
                intro
                + f"<article class='analysis-text'>{h(content.get('case', ''))}</article>"
                + f"<ul class='guidance-list'>{guidance}</ul>"
                + "<label class='field'><span>Jouw analyse</span><textarea name='answer' rows='8' required></textarea></label>"
            )
        return "<p>Onbekend oefentype.</p>"

    def attempt_page(self, connection, request: Request, context: dict, attempt_id: int) -> Response:
        attempt = connection.execute(
            """
            SELECT attempts.*, exercises.title AS exercise_title, exercises.exercise_type,
                   exercises.content_json, assignments.title AS assignment_title,
                   assignments.mode AS assignment_mode, users.first_name, users.last_name
            FROM attempts
            JOIN exercises ON exercises.id = attempts.exercise_id
            JOIN users ON users.id = attempts.user_id
            LEFT JOIN assignments ON assignments.id = attempts.assignment_id
            WHERE attempts.id = ?
            """,
            (attempt_id,),
        ).fetchone()
        if not attempt:
            return self.not_found(context)
        if self.require_role(context, {"student"}) and attempt["user_id"] != context["user"]["user_id"]:
            return self.forbidden(context)

        response_row = connection.execute(
            "SELECT response_json FROM responses WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        review = connection.execute(
            "SELECT * FROM reviews WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        response_data = parse_json(response_row["response_json"] if response_row else "{}", {})
        content = parse_json(attempt["content_json"], {})
        show_model = (
            not self.require_role(context, {"student"})
            or attempt["assignment_mode"] != "exam"
            or review is not None
        )
        review_block = ""
        if review:
            review_block = f"<article class='panel inset'><h2>Trainerfeedback</h2><p>{h(review['feedback'])}</p><p><strong>Override score:</strong> {format_score(review['score_override'])}</p></article>"

        action = ""
        if self.require_role(context, {"trainer", "organization_admin"}) and attempt["status"] == "submitted":
            action = f"<a class='button button-primary' href='/attempts/{attempt_id}/review'>Review toevoegen</a>"

        body = f"""
        <section class='hero compact'>
          <div>
            <span class='eyebrow'>{h(attempt['assignment_title'] or 'Vrij oefenen')}</span>
            <h1>{h(attempt['exercise_title'])}</h1>
            <p>Student: {h(attempt['first_name'])} {h(attempt['last_name'])}</p>
          </div>
          <div class='actions'>{action}</div>
        </section>
        {self.metrics_row([('Status', attempt['status']), ('Score', format_score(db.effective_score(attempt))), ('Mode', h(attempt['assignment_mode'] or 'learn'))])}
        <section class='grid two-up'>
          <article class='panel'>
            <h2>Antwoord van student</h2>
            {self.render_response_summary(attempt['exercise_type'], response_data)}
          </article>
          <article class='panel'>
            <h2>Automatische feedback</h2>
            <p>{h(attempt['feedback'])}</p>
            {f"<div class='model-answer'><h3>Modelantwoord</h3><p>{h(content.get('model_answer', ''))}</p></div>" if show_model and content.get('model_answer') else ''}
          </article>
        </section>
        {review_block}
        """
        return self.html("Poging", body, context)

    def render_response_summary(self, exercise_type: str, response_data: dict) -> str:
        if exercise_type == "multiple_choice":
            return f"<p>Geselecteerd: <strong>{h(response_data.get('selected'))}</strong></p>"
        if exercise_type == "multi_select":
            return f"<p>Geselecteerd: <strong>{h(as_text_list(response_data.get('selected', [])))}</strong></p>"
        if exercise_type == "match_pairs":
            rows = "".join(
                f"<tr><td>{h(left)}</td><td>{h(right)}</td></tr>"
                for left, right in response_data.get("matches", {}).items()
            )
            return f"<table class='table'><thead><tr><th>Links</th><th>Keuze</th></tr></thead><tbody>{rows}</tbody></table>"
        if exercise_type == "text_analysis":
            return f"<p><strong>Patroon:</strong> {h(response_data.get('selected'))}</p><p><strong>Follow-up:</strong><br>{h(response_data.get('follow_up'))}</p>"
        if exercise_type == "study_card":
            return f"<p>{h(response_data.get('answer', ''))}</p>"
        return f"<p>{h(response_data.get('answer', ''))}</p>"

    def review_queue(self, connection, request: Request, context: dict) -> Response:
        if not self.require_role(context, {"trainer", "organization_admin"}):
            return self.forbidden(context)
        active = context["active_membership"]
        rows = connection.execute(
            """
            SELECT attempts.id, attempts.submitted_at, users.first_name, users.last_name,
                   exercises.title AS exercise_title, assignments.title AS assignment_title
            FROM attempts
            JOIN assignments ON assignments.id = attempts.assignment_id
            JOIN exercises ON exercises.id = attempts.exercise_id
            JOIN users ON users.id = attempts.user_id
            WHERE assignments.organization_id = ?
              AND attempts.status = 'submitted'
              AND exercises.requires_manual_review = 1
            ORDER BY attempts.submitted_at DESC
            """,
            (active["organization_id"],),
        ).fetchall()
        content = (
            "<section class='panel'><h1>Open reviews</h1>"
            + self.render_table(
                ["Oefening", "Student", "Opdracht", "Ingediend"],
                [
                    [
                        f"<a href='/attempts/{row['id']}/review'>{h(row['exercise_title'])}</a>",
                        h(f"{row['first_name']} {row['last_name']}"),
                        h(row["assignment_title"]),
                        h(row["submitted_at"].replace("T", " ")),
                    ]
                    for row in rows
                ],
            )
            + "</section>"
        )
        return self.html("Reviews", content, context)

    def review_attempt(self, connection, request: Request, context: dict, attempt_id: int) -> Response:
        if not self.require_role(context, {"trainer", "organization_admin"}):
            return self.forbidden(context)
        attempt = connection.execute(
            """
            SELECT attempts.*, exercises.title AS exercise_title, exercises.exercise_type,
                   exercises.content_json, users.first_name, users.last_name
            FROM attempts
            JOIN exercises ON exercises.id = attempts.exercise_id
            JOIN users ON users.id = attempts.user_id
            WHERE attempts.id = ?
            """,
            (attempt_id,),
        ).fetchone()
        if not attempt:
            return self.not_found(context)
        if request.method == "POST":
            if not self.verify_csrf(request, context):
                return self.forbidden(context, "Ongeldige CSRF token.")
            score_override = request.get("score_override").strip()
            feedback = request.get("feedback").strip() or "Feedback toegevoegd."
            numeric_score = float(score_override) if score_override else None
            existing = connection.execute(
                "SELECT id FROM reviews WHERE attempt_id = ?",
                (attempt_id,),
            ).fetchone()
            if existing:
                connection.execute(
                    "UPDATE reviews SET score_override = ?, feedback = ?, reviewed_at = ? WHERE attempt_id = ?",
                    (numeric_score, feedback, db.utc_now_iso(), attempt_id),
                )
            else:
                connection.execute(
                    """
                    INSERT INTO reviews (attempt_id, reviewer_user_id, score_override, feedback, reviewed_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (attempt_id, context["user"]["user_id"], numeric_score, feedback, db.utc_now_iso()),
                )
            connection.execute(
                "UPDATE attempts SET manual_score = ?, feedback = ?, status = 'reviewed' WHERE id = ?",
                (numeric_score, feedback, attempt_id),
            )
            connection.commit()
            return self.redirect(f"/attempts/{attempt_id}?notice=" + quote_plus("Review opgeslagen."))

        response_row = connection.execute(
            "SELECT response_json FROM responses WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        response_data = parse_json(response_row["response_json"] if response_row else "{}", {})
        content = parse_json(attempt["content_json"], {})
        guidance_points = "".join(f"<li>{h(point)}</li>" for point in content.get("guidance_points", []))
        body = f"""
        <section class='panel form-panel'>
          <h1>Review: {h(attempt['exercise_title'])}</h1>
          <p>Student: {h(attempt['first_name'])} {h(attempt['last_name'])}</p>
          <div class='grid two-up'>
            <article class='panel inset'>
              <h2>Antwoord</h2>
              {self.render_response_summary(attempt['exercise_type'], response_data)}
              <h3>Beoordelingspunten</h3>
              <ul class='guidance-list'>{guidance_points}</ul>
            </article>
            <article class='panel inset'>
              <form method='post' action='/attempts/{attempt_id}/review'>
                <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
                <label class='field'><span>Score override (0-100)</span><input type='number' min='0' max='100' name='score_override'></label>
                <label class='field'><span>Feedback</span><textarea name='feedback' rows='8' required></textarea></label>
                <button class='button button-primary' type='submit'>Review opslaan</button>
              </form>
            </article>
          </div>
        </section>
        """
        return self.html("Review", body, context)

    def theme_settings(self, connection, request: Request, context: dict) -> Response:
        if not self.require_role(context, {"organization_admin"}):
            return self.forbidden(context)
        theme = context["theme"]
        active = context["active_membership"]
        if request.method == "POST":
            if not self.verify_csrf(request, context):
                return self.forbidden(context, "Ongeldige CSRF token.")
            logo_url = theme.get("logo_url", "")
            hero_url = theme.get("hero_url", "")
            if request.get("remove_logo") == "1":
                logo_url = ""
            if request.get("remove_background") == "1":
                hero_url = ""

            try:
                if request.getfile("logo_image"):
                    logo_url = self.save_theme_upload(
                        request.getfile("logo_image"),
                        active["organization_id"],
                        "logo",
                    )
                if request.getfile("background_image"):
                    hero_url = self.save_theme_upload(
                        request.getfile("background_image"),
                        active["organization_id"],
                        "background",
                    )
            except ValueError as exc:
                return self.redirect("/settings/theme?notice=" + quote_plus(str(exc)))

            try:
                background_opacity = float(
                    request.get("background_image_opacity", str(theme.get("background_image_opacity", 0.18)))
                )
            except ValueError:
                background_opacity = float(theme.get("background_image_opacity", 0.18))
            background_opacity = min(max(background_opacity, 0.0), 0.95)

            connection.execute(
                """
                UPDATE themes
                SET brand_name = ?, logo_label = ?, logo_url = ?, hero_url = ?,
                    primary_color = ?, secondary_color = ?, accent_color = ?,
                    surface_color = ?, background_style = ?, background_image_opacity = ?
                WHERE organization_id = ?
                """,
                (
                    request.get("brand_name"),
                    request.get("logo_label"),
                    logo_url,
                    hero_url,
                    request.get("primary_color"),
                    request.get("secondary_color"),
                    request.get("accent_color"),
                    request.get("surface_color"),
                    request.get("background_style"),
                    background_opacity,
                    active["organization_id"],
                ),
            )
            connection.commit()
            return self.redirect("/settings/theme?notice=" + quote_plus("Branding opgeslagen."))

        logo_preview = (
            f"<article class='panel inset'><h2>Huidig logo</h2><img class='theme-preview theme-preview-logo' src='{h(theme['logo_url'])}' alt='Logo preview'></article>"
            if theme.get("logo_url")
            else "<article class='panel inset'><h2>Huidig logo</h2><p class='helper'>Nog geen logo-afbeelding geupload. Het logo-label wordt nu gebruikt.</p></article>"
        )
        background_preview = (
            f"<article class='panel inset'><h2>Huidige achtergrondafbeelding</h2><img class='theme-preview' src='{h(theme['hero_url'])}' alt='Achtergrond preview'></article>"
            if theme.get("hero_url")
            else "<article class='panel inset'><h2>Huidige achtergrondafbeelding</h2><p class='helper'>Nog geen achtergrondafbeelding geupload.</p></article>"
        )

        body = f"""
        <section class='panel form-panel'>
          <h1>Branding instellingen</h1>
          <p class='helper'>Upload hier een logo en een zachte achtergrondafbeelding. Het logo-label blijft beschikbaar als fallback wanneer er geen logo-afbeelding is ingesteld.</p>
          <div class='grid two-up branding-preview-grid'>
            {logo_preview}
            {background_preview}
          </div>
          <form method='post' action='/settings/theme' enctype='multipart/form-data'>
            <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
            <div class='field-row'>
              <label class='field'><span>Merknaam</span><input type='text' name='brand_name' value='{h(theme['brand_name'])}'></label>
              <label class='field'><span>Logo-label (fallback)</span><input type='text' name='logo_label' value='{h(theme['logo_label'])}'></label>
            </div>
            <div class='field-row'>
              <label class='field'><span>Logo upload</span><input type='file' name='logo_image' accept='image/*'></label>
              <label class='field'><span>Achtergrondafbeelding upload</span><input type='file' name='background_image' accept='image/*'></label>
            </div>
            <div class='field-row'>
              <label class='field checkbox-row'><input type='checkbox' name='remove_logo' value='1'><span>Huidig logo verwijderen</span></label>
              <label class='field checkbox-row'><input type='checkbox' name='remove_background' value='1'><span>Huidige achtergrond verwijderen</span></label>
            </div>
            <div class='field-row'>
              <label class='field'><span>Primary</span><input type='color' name='primary_color' value='{h(theme['primary_color'])}'></label>
              <label class='field'><span>Secondary</span><input type='color' name='secondary_color' value='{h(theme['secondary_color'])}'></label>
              <label class='field'><span>Accent</span><input type='color' name='accent_color' value='{h(theme['accent_color'])}'></label>
              <label class='field'><span>Surface</span><input type='color' name='surface_color' value='{h(theme['surface_color'])}'></label>
            </div>
            <div class='field-row'>
              <label class='field'><span>Zichtbaarheid achtergrondafbeelding</span><input type='number' name='background_image_opacity' min='0' max='0.95' step='0.05' value='{h(theme.get('background_image_opacity', 0.18))}'></label>
              <label class='field'><span>Basisachtergrond / gradient (CSS)</span><input type='text' name='background_style' value='{h(theme['background_style'])}'></label>
            </div>
            <button class='button button-primary' type='submit'>Opslaan</button>
          </form>
        </section>
        """
        return self.html("Branding", body, context)

    def student_detail(self, connection, request: Request, context: dict, student_id: int) -> Response:
        if not self.require_role(context, {"trainer", "organization_admin"}):
            return self.forbidden(context)
        student = connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (student_id,),
        ).fetchone()
        if not student:
            return self.not_found(context)
        attempts = connection.execute(
            """
            SELECT attempts.*, exercises.title AS exercise_title, assignments.title AS assignment_title
            FROM attempts
            JOIN exercises ON exercises.id = attempts.exercise_id
            LEFT JOIN assignments ON assignments.id = attempts.assignment_id
            WHERE attempts.user_id = ?
            ORDER BY attempts.submitted_at DESC
            LIMIT 20
            """,
            (student_id,),
        ).fetchall()
        assignments = connection.execute(
            """
            SELECT assignments.title, assignments.mode,
                   COUNT(DISTINCT attempts.exercise_id) AS completed_items
            FROM assignment_targets
            JOIN assignments ON assignments.id = assignment_targets.assignment_id
            LEFT JOIN attempts ON attempts.assignment_id = assignments.id
                               AND attempts.user_id = assignment_targets.target_user_id
            WHERE assignment_targets.target_user_id = ?
            GROUP BY assignments.id
            ORDER BY assignments.due_date
            """,
            (student_id,),
        ).fetchall()
        body = [
            f"<section class='hero compact'><div><span class='eyebrow'>Student detail</span><h1>{h(student['first_name'])} {h(student['last_name'])}</h1><p>{h(student['email'])}</p></div></section>",
            self.metrics_row(
                [
                    ("Opdrachten", str(len(assignments))),
                    ("Pogingen", str(len(attempts))),
                    ("Gemiddelde", format_score(sum(filter(None, [db.effective_score(row) for row in attempts])) / len([row for row in attempts if db.effective_score(row) is not None])) if [row for row in attempts if db.effective_score(row) is not None] else "Nog geen"),
                ]
            ),
            "<section class='grid two-up'>"
            + "<article class='panel'><h2>Opdrachten</h2>"
            + self.render_table(
                ["Titel", "Mode", "Voltooid"],
                [[h(row["title"]), h(row["mode"]), h(row["completed_items"])] for row in assignments],
            )
            + "</article>"
            + "<article class='panel'><h2>Laatste pogingen</h2>"
            + self.render_table(
                ["Oefening", "Opdracht", "Score", "Status"],
                [
                    [
                        f"<a href='/attempts/{row['id']}'>{h(row['exercise_title'])}</a>",
                        h(row["assignment_title"] or "Vrij oefenen"),
                        format_score(db.effective_score(row)),
                        h(row["status"]),
                    ]
                    for row in attempts
                ],
            )
            + "</article></section>",
        ]
        return self.html("Student detail", "".join(body), context)


def create_app() -> WebApp:
    return WebApp()
