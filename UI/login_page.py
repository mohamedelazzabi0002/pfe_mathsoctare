from __future__ import annotations

import mesop as me

from Service.login_service import authenticate_user
from Service.session_service import set_current_user

# Style général de la page
PAGE_STYLE = me.Style(
    min_height="100vh",
    background="linear-gradient(135deg, #ffffff 0%, #f3fbff 35%, #dff2ff 100%)",
    padding=me.Padding.all(24),
)
# Style pour centrer le contenu dans la page
CENTER_STYLE = me.Style(
    min_height="100vh",
    display="flex",
    justify_content="center",
    align_items="center",
    position="relative",
)

# Style de la carte/formulaire
CARD_STYLE = me.Style(
    width="100%",
    max_width=420,
    background="#d3dff3",
    border_radius=18,
    padding=me.Padding(top=28, right=24, bottom=24, left=24),
)
# Style pour chaque bloc de champ/input
FIELD_BLOCK_STYLE = me.Style(
    margin=me.Margin(bottom=18),
)

## cette classe garde les données de la page login pendant l’utilisation.
# est un décorateur. sert à dire à Mesop que la classe suivante est une classe d’état (state).
@me.stateclass
class LoginState:
    email: str = ""
    password: str = ""
    message: str = ""
    is_error: bool = False

## crée une page de connexion /login avec Mesop.
@me.page(path="/login")
def login_page():
    state = me.state(LoginState)

    with me.box(style=PAGE_STYLE):
        with me.box(style=CENTER_STYLE):
            with me.box(
                style=me.Style(
                    position="absolute",
                    right="-140px",
                    bottom="-140px",
                    width=360,
                    height=360,
                    border_radius="50%",
                    border=me.Border.all(me.BorderSide(width=1, color="#a7dfff")),
                )
            ):
                pass

            with me.box(
                style=me.Style(
                    position="absolute",
                    right="-90px",
                    bottom="-90px",
                    width=260,
                    height=260,
                    border_radius="50%",
                    border=me.Border.all(me.BorderSide(width=1, color="#a7dfff")),
                )
            ):
                pass

            with me.box(style=CARD_STYLE):
                me.text(
                    "MathSocrates",
                    style=me.Style(
                        font_size=32,
                        font_weight="700",
                        color="#111111",
                        margin=me.Margin(bottom=10),
                    ),
                )
                me.text(
                    "Connectez-vous a MathSocrates",
                    style=me.Style(
                        font_size=18,
                        font_weight="500",
                        color="#111111",
                        margin=me.Margin(bottom=28),
                    ),
                )

                if state.message:
                    with me.box(
                        style=me.Style(
                            background="#fde7e9" if state.is_error else "#e7f6eb",
                            color="#a1222f" if state.is_error else "#17663a",
                            border_radius=12,
                            padding=me.Padding.all(12),
                            margin=me.Margin(bottom=18),
                        )
                    ):
                        me.text(state.message)

                with me.box(style=FIELD_BLOCK_STYLE):
                    me.text(
                        "Adresse e-mail",
                        style=me.Style(
                            font_size=20,
                            font_weight="700",
                            color="#000000",
                            margin=me.Margin(bottom=8),
                        ),
                    )
                    me.input(
                        label="",
                        placeholder="Email Address",
                        type="email",
                        appearance="outline",
                        value=state.email,
                        on_blur=on_email_blur,
                    )

                with me.box(style=FIELD_BLOCK_STYLE):
                    me.text(
                        "Mot de passe",
                        style=me.Style(
                            font_size=20,
                            font_weight="700",
                            color="#000000",
                            margin=me.Margin(bottom=8),
                        ),
                    )
                    me.input(
                        label="",
                        placeholder="Password",
                        type="password",
                        appearance="outline",
                        value=state.password,
                        on_blur=on_password_blur,
                        on_enter=on_login,
                    )

                me.button(
                    "Login",
                    on_click=on_login,
                    type="raised",
                    style=me.Style(
                        width="100%",
                        margin=me.Margin(top=6, bottom=18),
                    ),
                )

## cette fonction enregistre l’email tapé par l’utilisateur et efface le message affiché.
def on_email_blur(event: me.InputBlurEvent):
    state = me.state(LoginState)
    state.email = event.value
    state.message = ""

## elle enregistre le mot de passe saisi par l’utilisateur.
def on_password_blur(event: me.InputBlurEvent):
    state = me.state(LoginState)
    state.password = event.value
    state.message = ""

## cette fonction lance la connexion et affiche le résultat à l’utilisateur + navigation
def on_login(event: me.ClickEvent | me.InputEnterEvent):
    del event

    state = me.state(LoginState)
    result = authenticate_user(state.email, state.password)

    state.message = result["message"]
    state.is_error = not result["success"]

    if not result["success"]:
        return

    user = result["user"]
    set_current_user(user)
    if user["role"] == "eleve":
        me.navigate("/home-eleve")
