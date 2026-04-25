from __future__ import annotations

from urllib.parse import quote_plus

from .web import Response, WebApp, h

_PATCHED = False


def apply() -> None:
    global _PATCHED
    if _PATCHED:
        return

    original_theme_settings = WebApp.theme_settings

    def theme_settings(self: WebApp, connection, request, context: dict) -> Response:
        if request.method != "POST":
            return original_theme_settings(self, connection, request, context)

        if not self.require_role(context, {"organization_admin"}):
            return self.forbidden(context)

        active = context.get("active_membership")
        if not active:
            return self.forbidden(context)

        if not self.verify_csrf(request, context):
            return self.forbidden(context, "Ongeldige CSRF token.")

        defaults = self.default_theme()
        theme = {**defaults, **(context.get("theme") or {})}

        logo_url = theme.get("logo_url", "")
        hero_url = theme.get("hero_url", "")
        if request.get("remove_logo") == "1":
            logo_url = ""
        if request.get("remove_background") == "1":
            hero_url = ""

        try:
            logo_upload = request.getfile("logo_image")
            if logo_upload:
                logo_url = self.save_theme_upload(
                    logo_upload,
                    active["organization_id"],
                    "logo",
                )
            background_upload = request.getfile("background_image")
            if background_upload:
                hero_url = self.save_theme_upload(
                    background_upload,
                    active["organization_id"],
                    "background",
                )
        except (OSError, ValueError) as exc:
            return self.redirect("/settings/theme?notice=" + quote_plus(str(exc)))

        try:
            background_opacity = float(
                request.get("background_image_opacity", str(theme.get("background_image_opacity", 0.18)))
            )
        except ValueError:
            background_opacity = float(theme.get("background_image_opacity", 0.18))
        background_opacity = min(max(background_opacity, 0.0), 0.95)

        brand_name = request.get("brand_name").strip() or theme.get("brand_name") or defaults["brand_name"]
        logo_label = request.get("logo_label").strip() or theme.get("logo_label") or defaults["logo_label"]
        primary_color = request.get("primary_color").strip() or theme.get("primary_color") or defaults["primary_color"]
        secondary_color = request.get("secondary_color").strip() or theme.get("secondary_color") or defaults["secondary_color"]
        accent_color = request.get("accent_color").strip() or theme.get("accent_color") or defaults["accent_color"]
        surface_color = request.get("surface_color").strip() or theme.get("surface_color") or defaults["surface_color"]
        background_style = request.get("background_style").strip() or theme.get("background_style") or defaults["background_style"]

        connection.execute(
            """
            INSERT INTO themes (
                organization_id, brand_name, logo_label, logo_url, hero_url,
                primary_color, secondary_color, accent_color, surface_color,
                background_style, background_image_opacity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (organization_id) DO UPDATE SET
                brand_name = excluded.brand_name,
                logo_label = excluded.logo_label,
                logo_url = excluded.logo_url,
                hero_url = excluded.hero_url,
                primary_color = excluded.primary_color,
                secondary_color = excluded.secondary_color,
                accent_color = excluded.accent_color,
                surface_color = excluded.surface_color,
                background_style = excluded.background_style,
                background_image_opacity = excluded.background_image_opacity
            """,
            (
                active["organization_id"],
                brand_name,
                logo_label,
                logo_url,
                hero_url,
                primary_color,
                secondary_color,
                accent_color,
                surface_color,
                background_style,
                background_opacity,
            ),
        )
        connection.commit()
        return self.redirect("/settings/theme?notice=" + quote_plus("Branding opgeslagen."))

    WebApp.theme_settings = theme_settings
    _PATCHED = True


apply()
