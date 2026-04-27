from __future__ import annotations

import json
from urllib.parse import quote_plus

from . import content_admin_extension as cms
from . import db
from .web import Response, WebApp, h, parse_json

_PATCHED = False


def _resolve_image_source(self: WebApp, image_value: str) -> tuple[str | None, str]:
    value = (image_value or "").strip()
    if not value:
        return None, ""
    if value.startswith("/uploads/"):
        return value, value.rsplit("/", 1)[-1]
    return _resolve_image_source.original(self, value)


def _image_gallery_style() -> str:
    return """
    <style>
      .content-media-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin-bottom: 1.15rem;
      }
      .content-media-gallery img {
        width: 100%;
        height: 100%;
        min-height: 220px;
        object-fit: cover;
        border-radius: 1rem;
        border: 1px solid rgba(23,48,60,0.1);
        box-shadow: 0 16px 30px rgba(23,48,60,0.08);
        background: rgba(255,255,255,0.92);
      }
      .content-media-gallery.count-1 {
        grid-template-columns: minmax(0, 1fr);
      }
      .content-media-gallery.count-1 img {
        max-width: 560px;
        min-height: 320px;
        margin: 0 auto;
      }
      .content-media-gallery.count-2 {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
      .content-media-gallery.count-3 .content-media-item:first-child,
      .content-media-gallery.count-4 .content-media-item:first-child,
      .content-media-gallery.count-5 .content-media-item:first-child,
      .content-media-gallery.count-6 .content-media-item:first-child {
        grid-column: span 2;
      }
      .content-media-preview-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 0.85rem;
        margin-top: 0.85rem;
      }
      .content-media-preview-card {
        padding: 0.75rem;
        border-radius: 1rem;
        background: rgba(236,244,246,0.62);
        border: 1px solid rgba(23,48,60,0.08);
      }
      .content-media-preview-card img {
        display: block;
        width: 100%;
        aspect-ratio: 4 / 3;
        object-fit: cover;
        border-radius: 0.85rem;
        margin-bottom: 0.65rem;
      }
      @media (max-width: 720px) {
        .content-media-gallery.count-2 {
          grid-template-columns: 1fr;
        }
        .content-media-gallery.count-3 .content-media-item:first-child,
        .content-media-gallery.count-4 .content-media-item:first-child,
        .content-media-gallery.count-5 .content-media-item:first-child,
        .content-media-gallery.count-6 .content-media-item:first-child {
          grid-column: span 1;
        }
      }
    </style>
    """


def _render_gallery(image_urls: list[str], alt_text: str) -> str:
    cleaned = [url for url in image_urls if url]
    if not cleaned:
        return ""
    count = len(cleaned)
    return (
        _image_gallery_style()
        + f"<div class='content-media-gallery count-{count}'>"
        + "".join(
            "<figure class='content-media-item'>"
            f"<img src='{h(url)}' alt='{h(alt_text)}'>"
            "</figure>"
            for url in cleaned
        )
        + "</div>"
    )


def _merge_section_images(current_sections: list[dict], previous_sections: list[dict]) -> list[dict]:
    previous_by_title = {str(section.get("title", "")).strip(): section for section in previous_sections}
    merged = []
    for index, section in enumerate(current_sections):
        result = dict(section)
        previous = previous_by_title.get(str(section.get("title", "")).strip())
        if previous is None and index < len(previous_sections):
            previous = previous_sections[index]
        image_urls = [url for url in (previous or {}).get("image_urls", []) if url]
        if image_urls:
            result["image_urls"] = image_urls
        merged.append(result)
    return merged


def _render_content_sections(sections: list[dict]) -> str:
    if not sections:
        return "<section class='panel'><h2>Inhoudelijke informatie</h2><p class='helper'>Er is nog geen inhoud toegevoegd.</p></section>"
    blocks = [cms.story_module._pathway_story_style_block(), _image_gallery_style()]
    for section in sections:
        gallery = _render_gallery(section.get("image_urls", []), section.get("title", "Verdiepingspad"))
        groups = []
        for group in section.get("groups", []):
            groups.append(
                "<article class='pathway-story-group'>"
                f"<h3>{h(group.get('heading'))}</h3>"
                "<ul class='pathway-story-sublist'>"
                + "".join(f"<li>{h(point)}</li>" for point in group.get("points", []))
                + "</ul></article>"
            )
        blocks.append(
            "<section class='panel pathway-content-section'>"
            f"<div class='pathway-section-header'><h2>{h(section.get('title'))}</h2><p>{h(section.get('summary'))}</p></div>"
            + gallery
            + "<div class='pathway-story-copy'>"
            + "".join(groups)
            + "</div></section>"
        )
    return "".join(blocks)


def _module_image_manager(sections: list[dict]) -> str:
    if not sections:
        return "<p class='helper'>Sla eerst inhoudelijke blokken op voordat je sectie-afbeeldingen toevoegt.</p>"
    blocks = []
    for index, section in enumerate(sections):
        current_urls = [url for url in section.get("image_urls", []) if url]
        previews = (
            "<div class='content-media-preview-grid'>"
            + "".join(
                "<article class='content-media-preview-card'>"
                f"<img src='{h(url)}' alt='{h(section.get('title'))}'>"
                f"<label class='checkbox-row'><input type='checkbox' name='remove_section_image_{index}' value='{h(url)}'><span>Verwijderen</span></label>"
                "</article>"
                for url in current_urls
            )
            + "</div>"
            if current_urls
            else "<p class='helper'>Nog geen afbeeldingen gekoppeld aan deze sectie.</p>"
        )
        blocks.append(
            "<article class='panel inset'>"
            f"<h3>{h(section.get('title'))}</h3>"
            + previews
            + f"<label class='field'><span>Afbeelding toevoegen</span><input type='file' name='section_image_{index}' accept='image/*'></label>"
            + "</article>"
        )
    return "<div class='grid two-up'>" + "".join(blocks) + "</div>"


def _edit_module(self: WebApp, connection, request, context: dict, module_id: int) -> Response:
    module = connection.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not module:
        return self.not_found(context)
    override = cms._get_module_override(connection, module_id)

    if override:
        previous_sections = parse_json(override["sections_json"], [])
    else:
        story_defaults = cms._module_story_defaults(module["title"])
        if story_defaults:
            _outcomes, previous_sections = story_defaults
        else:
            previous_sections = cms._module_default_sections(connection, module_id)

    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")

        title = request.get("title").strip() or module["title"]
        summary = request.get("summary").strip()
        outcomes = cms._clean_lines(request.get("outcomes"))
        sections = cms._parse_content_sections(request.get("sections"))
        sections = _merge_section_images(sections, previous_sections)
        reading_text = request.get("reading_text").strip()
        more_info_text = request.get("more_info_text").strip()
        updated_at = db.utc_now_iso()
        user_id = context["user"]["user_id"]

        for index, section in enumerate(sections):
            kept_urls = [url for url in section.get("image_urls", []) if url]
            removed = set(request.getlist(f"remove_section_image_{index}"))
            if removed:
                kept_urls = [url for url in kept_urls if url not in removed]
            upload = request.getfile(f"section_image_{index}")
            if upload:
                kept_urls.append(self.save_theme_upload(upload, 0, f"content-module-{module_id}-{index}"))
            if kept_urls:
                section["image_urls"] = kept_urls
            elif "image_urls" in section:
                del section["image_urls"]

        connection.execute(
            """
            INSERT INTO content_module_pages (
                module_id, title, summary, outcomes_json, sections_json, reading_text,
                more_info_text, updated_by_user_id, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (module_id) DO UPDATE SET
                title = excluded.title,
                summary = excluded.summary,
                outcomes_json = excluded.outcomes_json,
                sections_json = excluded.sections_json,
                reading_text = excluded.reading_text,
                more_info_text = excluded.more_info_text,
                updated_by_user_id = excluded.updated_by_user_id,
                updated_at = excluded.updated_at
            """,
            (
                module_id,
                title,
                summary,
                json.dumps(outcomes),
                json.dumps(sections),
                reading_text,
                more_info_text,
                user_id,
                updated_at,
            ),
        )
        connection.execute("UPDATE modules SET title = ?, summary = ? WHERE id = ?", (title, summary, module_id))
        connection.commit()
        return self.redirect(f"/content/modules/{module_id}?notice=" + quote_plus("Leerpad opgeslagen."))

    if override:
        title = override["title"]
        summary = override["summary"]
        outcomes_text = "\n".join(parse_json(override["outcomes_json"], []))
        sections = parse_json(override["sections_json"], [])
        sections_text = cms._format_content_sections(sections)
        reading_text = override["reading_text"]
        more_info_text = override["more_info_text"]
    else:
        title = module["title"]
        summary = module["summary"]
        story_defaults = cms._module_story_defaults(module["title"])
        if story_defaults:
            outcomes, sections = story_defaults
        else:
            outcomes, sections = [], cms._module_default_sections(connection, module_id)
        sections = _merge_section_images(sections, previous_sections)
        outcomes_text = "\n".join(outcomes)
        sections_text = cms._format_content_sections(sections)
        reading_text, more_info_text = cms._module_default_materials(connection, module_id)

    body = f"""
    <section class='hero compact'><div><span class='eyebrow'>Contentbeheer</span><h1>{h(title)}</h1><p>Wijzig leerdoelen, inhoud, lesmateriaal en afbeeldingen.</p></div>
    <div class='actions'><a class='button button-secondary' href='/content/modules'>Terug</a><a class='button button-secondary' href='/content/modules/{module_id}/questions'>Vragenflow</a></div></section>
    <section class='panel form-panel'>
      <form method='post' action='/content/modules/{module_id}' enctype='multipart/form-data'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <label class='field'><span>Titel</span><input type='text' name='title' value='{h(title)}'></label>
        <label class='field'><span>Samenvatting</span><textarea name='summary' rows='3'>{h(summary)}</textarea></label>
        <label class='field'><span>Na dit leerpad kun je</span><textarea name='outcomes' rows='8'>{h(outcomes_text)}</textarea></label>
        <label class='field'><span>Inhoudelijke blokken</span><textarea name='sections' rows='18'>{h(sections_text)}</textarea></label>
        <section class='panel inset'><h2>Sectie-afbeeldingen</h2><p class='helper'>Per sectie kun je een of meer afbeeldingen toevoegen. De pagina schaalt automatisch mee met 0, 1 of meerdere beelden.</p>{_module_image_manager(sections)}</section>
        <div class='grid two-up'>
          <label class='field'><span>Leesstof van de les</span><textarea name='reading_text' rows='10'>{h(reading_text)}</textarea></label>
          <label class='field'><span>Meer informatie</span><textarea name='more_info_text' rows='10'>{h(more_info_text)}</textarea></label>
        </div>
        <button class='button button-primary' type='submit'>Opslaan</button>
      </form>
    </section>
    """
    return self.html("Leerpad beheren", body, context)


def _edit_model(self: WebApp, connection, request, context: dict, slug: str) -> Response:
    base_model = cms.web_module.MODEL_PAGE_LOOKUP.get(slug)
    if not base_model:
        return self.not_found(context)
    override = cms._get_model_override(connection, slug)
    current_image_value = (
        override["image_stem"]
        if override
        else base_model.get("image_stem", "")
    )

    if request.method == "POST":
        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")
        title = request.get("title").strip() or base_model["title"]
        intro = request.get("intro").strip()
        blocks = cms._parse_model_sections(request.get("blocks"))
        image_value = current_image_value
        if request.get("remove_image") == "1":
            image_value = ""
        upload = request.getfile("image_upload")
        if upload:
            image_value = self.save_theme_upload(upload, 0, f"content-model-{slug}")
        connection.execute(
            """
            INSERT INTO content_model_pages (
                slug, title, image_stem, intro, blocks_json, updated_by_user_id, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (slug) DO UPDATE SET
                title = excluded.title,
                image_stem = excluded.image_stem,
                intro = excluded.intro,
                blocks_json = excluded.blocks_json,
                updated_by_user_id = excluded.updated_by_user_id,
                updated_at = excluded.updated_at
            """,
            (
                slug,
                title,
                image_value,
                intro,
                json.dumps(blocks),
                context["user"]["user_id"],
                db.utc_now_iso(),
            ),
        )
        connection.commit()
        cms._apply_model_overrides_to_runtime(connection)
        return self.redirect(f"/content/models/{slug}?notice=" + quote_plus("Model opgeslagen."))

    if override:
        title = override["title"]
        intro = override["intro"]
        blocks_text = cms._format_model_sections(parse_json(override["blocks_json"], []))
    else:
        title = base_model["title"]
        intro = base_model.get("intro", "")
        blocks_text = cms._format_model_sections(cms.web_module.build_model_information_blocks(base_model))

    preview_url, preview_name = self.model_image_url(current_image_value)
    preview_html = (
        "<article class='panel inset'>"
        f"<h2>Huidige afbeelding</h2><img src='{h(preview_url)}' alt='{h(title)}' style='display:block; width:min(100%, 460px); border-radius:1rem; border:1px solid rgba(23,48,60,0.08);'>"
        f"<p class='helper'>{h(preview_name)}</p>"
        "<label class='checkbox-row'><input type='checkbox' name='remove_image' value='1'><span>Afbeelding verwijderen</span></label>"
        "</article>"
        if preview_url
        else "<article class='panel inset'><h2>Huidige afbeelding</h2><p class='helper'>Nog geen afbeelding geupload.</p></article>"
    )
    body = f"""
    <section class='hero compact'><div><span class='eyebrow'>Model beheren</span><h1>{h(title)}</h1></div>
    <div class='actions'><a class='button button-secondary' href='/content/models'>Terug</a></div></section>
    <section class='panel form-panel'>
      <form method='post' action='/content/models/{h(slug)}' enctype='multipart/form-data'>
        <input type='hidden' name='csrf_token' value='{h(context['session']['csrf_token'])}'>
        <label class='field'><span>Titel</span><input type='text' name='title' value='{h(title)}'></label>
        {preview_html}
        <label class='field'><span>Nieuwe afbeelding uploaden</span><input type='file' name='image_upload' accept='image/*'></label>
        <label class='field'><span>Intro</span><textarea name='intro' rows='4'>{h(intro)}</textarea></label>
        <label class='field'><span>Informatieblokken</span><textarea name='blocks' rows='18'>{h(blocks_text)}</textarea></label>
        <button class='button button-primary' type='submit'>Opslaan</button>
      </form>
    </section>
    """
    return self.html("Model beheren", body, context)


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    _resolve_image_source.original = WebApp.model_image_url
    WebApp.model_image_url = _resolve_image_source

    cms._render_content_sections = _render_content_sections
    cms._edit_module = _edit_module
    cms._edit_model = _edit_model

    _PATCHED = True


apply()
