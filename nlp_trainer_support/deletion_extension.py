from __future__ import annotations

from . import web as web_module
from .web import Response, WebApp

_PATCHED = False


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


def _extract_section(body: str, marker: str) -> tuple[int, int, str] | None:
    start = body.find(marker)
    if start == -1:
        return None
    end = body.find("</section>", start)
    if end == -1:
        return None
    end += len("</section>")
    return start, end, body[start:end]


def _swap_module_sections(body: str) -> str:
    lesson = _extract_section(body, "<section class='panel'><h2>Lesmateriaal</h2>")
    topics = _extract_section(body, "<section class='panel'><h2>Onderwerpen en concepten</h2>")
    if not lesson or not topics:
        return body

    lesson_start, lesson_end, lesson_html = lesson
    topics_start, topics_end, topics_html = topics
    if topics_start < lesson_start:
        return body

    return body[:lesson_start] + topics_html + body[lesson_end:topics_start] + lesson_html + body[topics_end:]


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    web_module.build_model_information_blocks = _build_model_information_blocks

    original_module_page = getattr(WebApp, "module_page", None)
    if original_module_page is not None:

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
                "<option value='reader'>Leeswerk</option>": "<option value='reader'>Leesstof van de les</option>",
                "<option value='literature'>Verdiepende literatuur</option>": "<option value='literature'>Meer informatie</option>",
            }
            for old, new in replacements.items():
                body = body.replace(old, new)
            body = _swap_module_sections(body)
            return Response(response.status, body.encode("utf-8"), list(response.headers))

        WebApp.module_page = module_page

    _PATCHED = True


apply()
