from __future__ import annotations

from . import game_extension as game_module
from .web import WebApp, h

_PATCHED = False


def _render_game_style_block() -> str:
    return """
    <style>
      body {
        background:
          radial-gradient(circle at top left, rgba(88, 28, 135, 0.18), transparent 32%),
          radial-gradient(circle at top right, rgba(20, 184, 166, 0.14), transparent 28%),
          linear-gradient(180deg, #070b15 0%, #0d1323 45%, #131825 100%);
        color: #edf4ff;
      }
      .shell {
        background: transparent !important;
      }
      .topbar {
        background: rgba(7, 11, 21, 0.82);
        border-color: rgba(148, 163, 184, 0.16);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.28);
      }
      .brand-name,
      .nav-link,
      .page h1,
      .page h2,
      .page h3,
      .page strong,
      .page label,
      .page p,
      .page li,
      .page span {
        color: inherit;
      }
      .brand-subtitle,
      .helper,
      .eyebrow,
      .game-node-meta,
      .game-section-copy p,
      .game-hud small,
      .page .tag {
        color: rgba(226, 232, 240, 0.72);
      }
      .page {
        max-width: 1380px;
      }
      .panel,
      .panel.inset,
      .hero,
      .hero.compact {
        background: rgba(14, 19, 33, 0.84);
        border: 1px solid rgba(148, 163, 184, 0.14);
        box-shadow: 0 22px 48px rgba(0, 0, 0, 0.28);
      }
      .progress-panel,
      .exercise-panel,
      .quiz-feedback {
        background: rgba(14, 19, 33, 0.88);
      }
      .button-secondary {
        background: rgba(15, 23, 42, 0.66);
        color: #edf4ff;
        border-color: rgba(148, 163, 184, 0.18);
      }
      .tag {
        background: rgba(148, 163, 184, 0.16);
        border-color: rgba(148, 163, 184, 0.18);
      }
      .progress-bar {
        background: rgba(148, 163, 184, 0.16);
      }
      .progress-bar span {
        background: linear-gradient(90deg, #60a5fa, #2dd4bf);
      }
      .progress-pill {
        background: rgba(59, 130, 246, 0.16);
        border: 1px solid rgba(96, 165, 250, 0.2);
        color: #eff6ff;
      }
      .notice {
        background: rgba(34, 197, 94, 0.16);
        color: #ecfdf5;
        border: 1px solid rgba(74, 222, 128, 0.22);
      }
      .game-stage {
        display: grid;
        gap: 1.4rem;
      }
      .game-stage-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 0.4rem 0 0.2rem;
      }
      .game-stage-head h1 {
        margin: 0;
      }
      .game-hud {
        display: inline-flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.8rem 1rem;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.18);
        font-weight: 700;
      }
      .game-hud small {
        display: block;
        font-size: 0.76rem;
        font-weight: 500;
      }
      .game-board {
        display: grid;
        gap: 1.35rem;
      }
      .game-section-panel {
        overflow: hidden;
        padding-bottom: 1.2rem;
      }
      .game-section-header {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: flex-start;
        margin-bottom: 1rem;
      }
      .game-section-copy {
        max-width: 42rem;
      }
      .game-section-label {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(226, 232, 240, 0.68);
      }
      .game-section-index {
        display: inline-flex;
        width: 2rem;
        height: 2rem;
        align-items: center;
        justify-content: center;
        border-radius: 999px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.24), rgba(45, 212, 191, 0.2));
        color: #eff6ff;
        font-weight: 700;
      }
      .game-section-status {
        padding: 0.4rem 0.7rem;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.14);
        color: #dbeafe;
        font-size: 0.82rem;
        font-weight: 600;
      }
      .game-map-shell {
        position: relative;
        overflow: hidden;
        border-radius: 1.4rem;
        padding: 1.25rem;
        background:
          radial-gradient(circle at top left, rgba(59, 130, 246, 0.16), transparent 26%),
          radial-gradient(circle at bottom right, rgba(45, 212, 191, 0.14), transparent 24%),
          rgba(8, 12, 23, 0.94);
        border: 1px solid rgba(148, 163, 184, 0.12);
      }
      .game-map-canvas {
        position: relative;
        min-height: 12rem;
      }
      .game-map-svg {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        overflow: visible;
        pointer-events: none;
      }
      .game-path {
        fill: none;
        stroke-width: 4;
        stroke-linecap: round;
        stroke-linejoin: round;
        opacity: 0.82;
      }
      .game-path.completed {
        stroke: url(#gamePathDone);
      }
      .game-path.available {
        stroke: rgba(96, 165, 250, 0.72);
      }
      .game-path.locked {
        stroke: rgba(148, 163, 184, 0.26);
      }
      .game-map-node {
        position: absolute;
        transform: translateX(-50%);
        width: 10rem;
        display: grid;
        justify-items: center;
        gap: 0.45rem;
        text-decoration: none;
        color: inherit;
      }
      .game-map-node.completed {
        cursor: pointer;
      }
      .game-map-node.upgrade,
      .game-map-node.locked {
        cursor: default;
      }
      .game-map-node.locked,
      .game-map-node.upgrade {
        opacity: 0.75;
      }
      .game-map-node.active .game-node-core {
        animation: gamePulse 2s ease-in-out infinite;
      }
      .game-node-stars {
        display: inline-flex;
        gap: 0.16rem;
        min-height: 1.1rem;
      }
      .game-star {
        font-size: 0.95rem;
        line-height: 1;
      }
      .game-star.filled {
        color: #fbbf24;
        text-shadow: 0 0 14px rgba(251, 191, 36, 0.38);
      }
      .game-star.empty {
        color: rgba(226, 232, 240, 0.24);
      }
      .game-node-core {
        width: 4.65rem;
        height: 4.65rem;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        border: 3px solid rgba(148, 163, 184, 0.22);
        background: radial-gradient(circle at 35% 30%, rgba(255,255,255,0.18), rgba(15, 23, 42, 0.92));
        color: #f8fafc;
        box-shadow: 0 18px 32px rgba(0, 0, 0, 0.24);
      }
      .game-map-node.active .game-node-core {
        border-color: rgba(96, 165, 250, 0.7);
        background: radial-gradient(circle at 35% 30%, rgba(96,165,250,0.58), rgba(30,41,59,0.96));
      }
      .game-map-node.completed .game-node-core {
        border-color: rgba(45, 212, 191, 0.72);
        background: radial-gradient(circle at 35% 30%, rgba(45,212,191,0.48), rgba(19, 78, 74, 0.92));
      }
      .game-map-node.upgrade .game-node-core {
        border-color: rgba(251, 191, 36, 0.44);
        background: radial-gradient(circle at 35% 30%, rgba(251,191,36,0.22), rgba(69,39,5,0.88));
      }
      .game-map-node.locked .game-node-core {
        border-color: rgba(148, 163, 184, 0.18);
        background: rgba(30, 41, 59, 0.72);
      }
      .game-node-title {
        font-size: 0.88rem;
        line-height: 1.28;
        font-weight: 700;
        text-align: center;
        color: #f8fafc;
      }
      .game-node-meta {
        font-size: 0.72rem;
        text-align: center;
      }
      .game-player {
        position: absolute;
        transform: translate(-50%, -115%);
        z-index: 3;
        animation: gameBob 1.9s ease-in-out infinite;
      }
      .game-player-token {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.38rem 0.65rem;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(96, 165, 250, 0.34);
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.28);
        color: #eff6ff;
        font-size: 0.72rem;
        font-weight: 700;
      }
      .game-player-icon {
        width: 1.35rem;
        height: 1.35rem;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #60a5fa, #2dd4bf);
        color: #0f172a;
      }
      .game-feedback-note {
        padding: 0.85rem 1rem;
        border-radius: 0.9rem;
        background: rgba(59, 130, 246, 0.12);
      }
      @keyframes gamePulse {
        0%, 100% { transform: scale(1); box-shadow: 0 18px 32px rgba(0, 0, 0, 0.24); }
        50% { transform: scale(1.08); box-shadow: 0 22px 42px rgba(59, 130, 246, 0.24); }
      }
      @keyframes gameBob {
        0%, 100% { transform: translate(-50%, -115%); }
        50% { transform: translate(-50%, -126%); }
      }
      @media (max-width: 900px) {
        .game-stage-head,
        .game-section-header {
          display: grid;
        }
        .game-map-node {
          width: 8.25rem;
        }
        .game-node-core {
          width: 4rem;
          height: 4rem;
        }
      }
    </style>
    """


def _game_star_count(score_value) -> int:
    try:
        score = float(score_value or 0)
    except (TypeError, ValueError):
        score = 0.0
    if score >= 100:
        return 3
    if score >= 75:
        return 2
    if score >= 50:
        return 1
    return 0


def _render_game_stars(score_value) -> str:
    star_count = _game_star_count(score_value)
    stars = []
    for index in range(3):
        state = "filled" if index < star_count else "empty"
        stars.append(f"<span class='game-star {state}'>&#9733;</span>")
    return "<div class='game-node-stars'>" + "".join(stars) + "</div>"


def _game_node_positions(unit_count: int) -> tuple[list[tuple[int, int]], int]:
    pattern = [18, 48, 78, 42, 16, 58, 82, 34]
    positions = []
    start_y = 54
    step_y = 128
    for index in range(unit_count):
        positions.append((pattern[index % len(pattern)], start_y + (index * step_y)))
    total_height = max(220, (unit_count * step_y) + 36)
    return positions, total_height


def _game_player_marker(sections: list[dict]):
    last_completed = None
    for section in sections:
        for unit in section["units"]:
            marker = (int(section["module"]["id"]), unit["key"])
            if unit["status"] == "active":
                return marker
            if unit["status"] == "completed":
                last_completed = marker
    return last_completed


def _render_game_map_section(section: dict, player_marker) -> str:
    module = section["module"]
    units = section["units"]
    if not units:
        return (
            "<section class='panel game-section-panel'>"
            "<div class='game-section-header'>"
            "<div class='game-section-copy'>"
            + f"<div class='game-section-label'><span class='game-section-index'>{section['index']}</span> Sectie {section['index']}</div>"
            + f"<h2>{h(module['title'])}</h2>"
            + f"<p>{h(module['summary'])}</p>"
            + "</div>"
            + f"<span class='game-section-status'>{h(section['status'])}</span>"
            + "</div>"
            + "<div class='game-map-shell'><p class='helper'>Voor deze sectie staan nog geen game-units klaar.</p></div>"
            + "</section>"
        )

    positions, canvas_height = _game_node_positions(len(units))
    paths = []
    nodes = []
    player_html = ""

    for index, unit in enumerate(units):
        x, y = positions[index]
        progress = unit["progress"] or {}
        score_value = progress.get("best_score") if progress else None
        node_state = unit["status"]

        if node_state == "completed":
            href = f"/game/modules/{module['id']}/units/{unit['key']}/complete"
            open_tag = f"<a class='game-map-node completed' href='{h(href)}' style='left:{x}%; top:{y}px;'>"
            close_tag = "</a>"
            meta = "Voltooid"
        elif node_state == "active":
            href = game_module._build_game_unit_url(int(module["id"]), unit["key"])
            open_tag = f"<a class='game-map-node active' href='{h(href)}' style='left:{x}%; top:{y}px;'>"
            close_tag = "</a>"
            meta = "Speel nu"
        elif node_state == "upgrade":
            open_tag = f"<a class='game-map-node upgrade' href='/pricing' style='left:{x}%; top:{y}px;'>"
            close_tag = "</a>"
            meta = "Upgrade nodig"
        else:
            open_tag = f"<span class='game-map-node locked' style='left:{x}%; top:{y}px;'>"
            close_tag = "</span>"
            meta = "Nog vergrendeld"

        if index < len(units) - 1:
            next_x, next_y = positions[index + 1]
            next_status = units[index + 1]["status"]
            if next_status == "completed":
                path_state = "completed"
            elif next_status == "active":
                path_state = "available"
            else:
                path_state = "locked"
            mid_y = (y + next_y) / 2
            paths.append(
                f"<path class='game-path {path_state}' d='M {x} {y} C {x} {mid_y}, {next_x} {mid_y}, {next_x} {next_y}'></path>"
            )

        nodes.append(
            open_tag
            + _render_game_stars(score_value)
            + f"<span class='game-node-core'>{unit['index']}</span>"
            + f"<span class='game-node-title'>{h(unit['title'])}</span>"
            + f"<span class='game-node-meta'>{h(meta)} - {unit['question_count']} vragen</span>"
            + close_tag
        )

        if player_marker == (int(module["id"]), unit["key"]):
            player_html = (
                f"<div class='game-player' style='left:{x}%; top:{y}px;'>"
                "<span class='game-player-token'>"
                "<span class='game-player-icon'>&#9650;</span>"
                "<span>Jij</span>"
                "</span></div>"
            )

    return (
        "<section class='panel game-section-panel'>"
        "<div class='game-section-header'>"
        "<div class='game-section-copy'>"
        + f"<div class='game-section-label'><span class='game-section-index'>{section['index']}</span> Sectie {section['index']}</div>"
        + f"<h2>{h(module['title'])}</h2>"
        + f"<p>{h(module['summary'])}</p>"
        + "</div>"
        + f"<span class='game-section-status'>{h(section['status'])}</span>"
        + "</div>"
        + "<div class='game-map-shell'>"
        + f"<div class='game-map-canvas' style='height:{canvas_height}px;'>"
        + (
            "<svg class='game-map-svg' viewBox='0 0 100 "
            + str(canvas_height)
            + "' preserveAspectRatio='none'>"
            + "<defs><linearGradient id='gamePathDone' x1='0%' y1='0%' x2='100%' y2='100%'>"
            + "<stop offset='0%' stop-color='#60a5fa'></stop>"
            + "<stop offset='100%' stop-color='#2dd4bf'></stop>"
            + "</linearGradient></defs>"
            + "".join(paths)
            + "</svg>"
        )
        + player_html
        + "".join(nodes)
        + "</div></div></section>"
    )


def _game_page(self: WebApp, connection, request, context: dict):
    profile = game_module._game_profile_state(self, connection, context)
    sections = game_module._build_game_sections(self, connection, context)
    player_marker = _game_player_marker(sections)
    if profile["unlimited"]:
        hud = "<div class='game-hud'><span>Levens: onbeperkt</span><small>Betaalde toegang of organisatieaccount</small></div>"
    else:
        hud = (
            "<div class='game-hud'>"
            + f"<span>Levens: {profile['lives_remaining']}/{profile['max_lives']}</span>"
            + "<small>Dagelijks opnieuw gevuld tot 5</small></div>"
        )

    body = [
        _render_game_style_block(),
        "<section class='game-stage'>"
        + "<div class='game-stage-head'>"
        + "<div><span class='eyebrow'>The Game</span><h1>The Game</h1></div>"
        + hud
        + "</div>"
        + "<div class='game-board'>"
        + "".join(_render_game_map_section(section, player_marker) for section in sections)
        + "</div></section>",
    ]
    return self.html("The Game", "".join(body), context)


def _render_nav(self: WebApp, context: dict) -> str:
    nav = _render_nav.original(self, context)
    if not context.get("user"):
        return nav
    original_link = "<a class='nav-link' href='/game'>The Game</a>"
    new_link = "<a class='nav-link' href='/game' target='_blank' rel='noopener'>The Game</a>"
    if original_link in nav:
        return nav.replace(original_link, new_link, 1)
    return nav.replace(
        "<a class='nav-link' href='/dashboard'>Dashboard</a>",
        "<a class='nav-link' href='/dashboard'>Dashboard</a>" + new_link,
        1,
    )


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    current_render_nav = getattr(WebApp, "render_nav", None)
    _render_nav.original = getattr(current_render_nav, "original", current_render_nav)
    game_module._render_game_style_block = _render_game_style_block
    game_module._game_page = _game_page
    game_module._render_nav = _render_nav
    WebApp.render_nav = _render_nav

    _PATCHED = True


apply()
