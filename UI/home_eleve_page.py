from __future__ import annotations

import mesop as me


@me.page(path="/home-eleve")
def home_eleve_page():
    # Conteneur principal de toute la page eleve.
    with me.box(
        style=me.Style(
            min_height="100vh",
            background="#f6fbff",
            padding=me.Padding.all(24),
        )
    ):
        # Header en haut de la page avec logo et boutons.
        with me.box(
            style=me.Style(
                width="100%",
                display="flex",
                justify_content="space-between",
                align_items="center",
                border=me.Border.all(me.BorderSide(width=2, color="#99c8eb")),
                border_radius=18,
                background="#000000",
                padding=me.Padding(top=18, right=24, bottom=18, left=24),
                margin=me.Margin(bottom=24),
            )
        ):
            # Zone gauche du header pour afficher le logo MathSocrates.
            with me.box(
                style=me.Style(
                    display="flex",
                    align_items="center",
                    gap="12px",
                )
            ):
                # Cercle decoratif qui contient la lettre M du logo.
                with me.box(
                    style=me.Style(
                        width=44,
                        height=44,
                        border_radius="50%",
                        background="linear-gradient(135deg, #9fe0ff 0%, #3aa7ff 100%)",
                        display="flex",
                        justify_content="center",
                        align_items="center",
                    )
                ):
                    me.text(
                        "M",
                        style=me.Style(
                            font_size=22,
                            font_weight="700",
                            color="#04111d",
                        ),
                    )

                me.text(
                    "MathSocrates",
                    style=me.Style(
                        font_size=28,
                        font_weight="700",
                        color="#ffffff",
                    ),
                )

            # Zone droite du header pour afficher les boutons de navigation.
            with me.box(
                style=me.Style(
                    display="flex",
                    align_items="center",
                    gap="12px",
                )
            ):
                me.button(
                    "apprentissage",
                    type="stroked",
                    style=me.Style(
                        color="#ffffff",
                        border=me.Border.all(me.BorderSide(width=1, color="#ffffff")),
                        border_radius=12,
                    ),
                )
                me.button(
                    "seance socratique",
                    type="stroked",
                    style=me.Style(
                        color="#ffffff",
                        border=me.Border.all(me.BorderSide(width=1, color="#ffffff")),
                        border_radius=12,
                    ),
                )
                me.button(
                    "deconnexion",
                    type="stroked",
                    style=me.Style(
                        color="#ffffff",
                        border=me.Border.all(me.BorderSide(width=1, color="#ffffff")),
                        border_radius=12,
                    ),
                )

        # Zone centrale de contenu de la page eleve.
        with me.box(
            style=me.Style(
                display="flex",
                justify_content="center",
                align_items="center",
                min_height="70vh",
            )
        ):
            me.text(
                "Home eleve",
                style=me.Style(font_size=28, font_weight="700", color="#16324f"),
            )
