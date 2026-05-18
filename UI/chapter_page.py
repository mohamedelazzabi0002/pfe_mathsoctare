from __future__ import annotations

from functools import partial

import mesop as me


@me.page(path="/chapter")
def chapter_page():
    # Conteneur principal de toute la page chapitre.
    with me.box(
        style=me.Style(
            min_height="100vh",
            background="#f6fbff",
            padding=me.Padding.all(24),
        )
    ):
        # Header noir en haut de la page pour le titre principal.
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
                "Les chapitres TCS Math",
                style=me.Style(
                    font_size=30,
                    font_weight="700",
                    color="#ffffff",
                ),
            )

        chapitres_tcs_math = {
            1: "Les ensembles de nombres N, Z, Q, D et R",
            2: "Arithmetique dans N",
            3: "Calcul vectoriel dans le plan",
            4: "La projection dans le plan",
            5: "L'ordre dans R",
            6: "La droite dans le plan",
            7: "Les polynomes",
            8: "Equations, inequations et systemes",
            9: "Trigonometrie 1 (Calcul trigonometrique)",
            10: "Trigonometrie 2 (Equations et inequations trigonometriques)",
            11: "Generalites sur les fonctions",
            12: "Transformations du plan",
            13: "Le produit scalaire",
            14: "Geometrie dans l'espace",
            15: "Statistiques",
        }

        # Colonne qui contient toute la liste des chapitres.
        with me.box(
            style=me.Style(
                display="flex",
                flex_direction="column",
                gap="14px",
            )
        ):
            for numero, titre in chapitres_tcs_math.items():
                # Carte individuelle pour afficher un chapitre.
                with me.box(
                    style=me.Style(
                        background="#ffffff",
                        border=me.Border.all(
                            me.BorderSide(width=1, color="#c9def0")
                        ),
                        border_radius=14,
                        padding=me.Padding.all(16),
                    )
                ):
                    # Ligne du haut pour placer le titre du chapitre et le bouton commencer.
                    with me.box(
                        style=me.Style(
                            display="flex",
                            justify_content="space-between",
                            align_items="center",
                            margin=me.Margin(bottom=12),
                        )
                    ):
                        me.text(
                            f"Chapitre {numero}",
                            style=me.Style(
                                font_size=18,
                                font_weight="700",
                                color="#16324f",
                            ),
                        )
                        me.button(
                            "commencer",
                            on_click=partial(on_commencer_click, numero),
                            type="raised",
                            style=me.Style(
                                background="#1f78ff",
                                color="#ffffff",
                                border_radius=10,
                            ),
                        )
                    me.text(
                        titre,
                        style=me.Style(
                            font_size=16,
                            color="#304b63",
                            margin=me.Margin(bottom=4),
                        ),
                    )


def on_commencer_click(chapter_id: int, event: me.ClickEvent):
    del chapter_id
    del event
    me.navigate("/diagnostic")
