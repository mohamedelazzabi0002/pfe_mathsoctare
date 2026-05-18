from __future__ import annotations

import mesop as me


@me.page(path="/diagnostic")
def diagnostic_page():
    # Conteneur principal de la page diagnostique.
    with me.box(
        style=me.Style(
            min_height="100vh",
            background="#f6fbff",
            padding=me.Padding.all(24),
        )
    ):
        # Header noir pour le titre de la page diagnostique.
        with me.box(
            style=me.Style(
                width="100%",
                border=me.Border.all(me.BorderSide(width=2, color="#99c8eb")),
                border_radius=18,
                background="#000000",
                padding=me.Padding(top=18, right=24, bottom=18, left=24),
                margin=me.Margin(bottom=24),
            )
        ):
            me.text(
                "Page diagnostique",
                style=me.Style(
                    font_size=30,
                    font_weight="700",
                    color="#ffffff",
                ),
            )

        # Zone centrale temporaire en attendant le contenu diagnostique.
        with me.box(
            style=me.Style(
                display="flex",
                justify_content="center",
                align_items="center",
                min_height="60vh",
            )
        ):
            me.text(
                "Diagnostic Page",
                style=me.Style(
                    font_size=28,
                    font_weight="700",
                    color="#16324f",
                ),
            )
