from __future__ import annotations

import mesop as me

from Service.session_service import clear_session


@me.stateclass
class HomeEleveState:
    active_button: str = ""


@me.page(path="/home-eleve")
def home_eleve_page():
    state = me.state(HomeEleveState)

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
                    on_click=on_apprentissage_click,
                    type="stroked",
                    style=button_style(state.active_button == "apprentissage"),
                )
                me.button(
                    "seance socratique",
                    type="stroked",
                    on_click=on_seance_socratique_click,
                    style=button_style(state.active_button == "seance socratique"),
                )
                me.button(
                    "deconnexion",
                    type="stroked",
                    on_click=on_deconnexion_click,
                    style=button_style(state.active_button == "deconnexion"),
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

##cette fonction active le bouton apprentissage puis navigue vers la page des chapitres.
def on_apprentissage_click(event: me.ClickEvent):
    del event
    me.state(HomeEleveState).active_button = "apprentissage"
    me.navigate("/chapter")


def on_seance_socratique_click(event: me.ClickEvent):
    del event
    me.state(HomeEleveState).active_button = "seance socratique"


def on_deconnexion_click(event: me.ClickEvent):
    del event
    me.state(HomeEleveState).active_button = "deconnexion"
    clear_session()
    me.navigate("/login")


def button_style(is_active: bool) -> me.Style:
    return me.Style(
        color="#000000" if is_active else "#ffffff",
        background="#ffffff" if is_active else "#000000",
        border=me.Border.all(me.BorderSide(width=1, color="#ffffff")),
        border_radius=12,
        cursor="pointer",
        transition="all 0.2s ease",
        box_shadow="0 0 0 2px rgba(255,255,255,0.15)" if is_active else "none",
    )
