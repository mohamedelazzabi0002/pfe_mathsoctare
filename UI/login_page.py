from __future__ import annotations

import json
import mesop as me

from Service.login_service import authenticate_user
from Service.session_service import save_session
from Database.db import DATA_DIR


COLORS = {
    "bg": "#f8f9ff",
    "surface": "#ffffff",
    "surface_low": "#eff4ff",
    "primary": "#4648d4",
    "primary_container": "#6063ee",
    "text": "#0b1c30",
    "muted": "#464554",
    "outline": "#c7c4d7",
    "error_bg": "#ffdad6",
    "error_text": "#93000a",
    "success_bg": "#e7f6eb",
    "success_text": "#17663a",
}


@me.stateclass
class LoginState:
    email: str = ""
    password: str = ""
    message: str = ""
    is_error: bool = False
    remember: bool = False


@me.page(path="/login")
def login_page():
    state = me.state(LoginState)

    with me.box(style=page_style()):
        header()

        with me.box(style=me.Style(
            flex_grow=1,
            display="flex",
            align_items="center",
            justify_content="center",
            padding=me.Padding.all(32),
        )):
            login_card(state)

        footer()


def page_style():
    return me.Style(
        min_height="100vh",
        background=COLORS["bg"],
        color=COLORS["text"],
        font_family="Inter, Arial, sans-serif",
        display="flex",
        flex_direction="column",
    )


def header():
    with me.box(style=me.Style(
        height=72,
        display="flex",
        align_items="center",
        justify_content="space-between",
        padding=me.Padding.symmetric(horizontal=32),
    )):
        me.text("Mathsocrates", style=me.Style(
            font_size=32,
            font_weight="700",
            color=COLORS["primary"],
        ))

        with me.box(style=me.Style(display="flex", gap=24)):
            me.text("Aide", style=nav_text_style())
            me.text("Contact", style=nav_text_style())


def login_card(state: LoginState):
    with me.box(style=me.Style(
        width="100%",
        max_width=480,
        background=COLORS["surface"],
        border=me.Border.all(me.BorderSide(width=1, color=COLORS["outline"])),
        border_radius=12,
        padding=me.Padding.all(32),
        box_shadow="0 10px 15px rgba(0,0,0,0.05)",
    )):
        with me.box(style=me.Style(text_align="center", margin=me.Margin(bottom=32))):
            me.text("Mathsocrates", style=me.Style(
                font_size=18,
                font_weight="700",
                color=COLORS["primary"],
                margin=me.Margin(bottom=8),
            ))

            me.text("Bon retour parmi nous", style=me.Style(
                font_size=28,
                font_weight="700",
                margin=me.Margin(bottom=8),
            ))

            me.text(
                "Veuillez entrer vos informations pour accéder à votre tableau de bord.",
                style=me.Style(font_size=14, color=COLORS["muted"]),
            )

        if state.message:
            with me.box(style=me.Style(
                background=COLORS["error_bg"] if state.is_error else COLORS["success_bg"],
                color=COLORS["error_text"] if state.is_error else COLORS["success_text"],
                border_radius=12,
                padding=me.Padding.all(12),
                margin=me.Margin(bottom=18),
            )):
                me.text(state.message)

        form_field(
            label="Adresse e-mail ou nom d'utilisateur",
            placeholder="professeur@ecole.fr",
            value=state.email,
            input_type="email",
            on_blur=on_email_blur,
        )

        password_field(state.password)

        with me.box(style=me.Style(
            margin=me.Margin(top=16, bottom=24),
        )):
            me.checkbox(
                label="Se souvenir de moi",
                checked=state.remember,
                on_change=on_remember_change,
            )

        me.button(
            "Se connecter",
            type="flat",
            on_click=on_login,
            style=me.Style(
                width="100%",
                height=48,
                background=COLORS["primary"],
                color="white",
                border_radius=8,
                font_size=18,
                font_weight="700",
            ),
        )


def form_field(
    label: str,
    placeholder: str,
    value: str,
    input_type: str,
    on_blur,
):
    with me.box(style=me.Style(margin=me.Margin(bottom=18))):
        me.text(label, style=label_style())
        me.input(
            label="",
            placeholder=placeholder,
            type=input_type,
            appearance="outline",
            value=value,
            on_blur=on_blur,
            style=input_style(),
        )


def password_field(value: str):
    with me.box(style=me.Style(margin=me.Margin(bottom=8))):
        with me.box(style=me.Style(
            display="flex",
            justify_content="space-between",
            align_items="center",
            margin=me.Margin(bottom=8),
        )):
            me.text("Mot de passe", style=label_style())
            me.text("Mot de passe oublié ?", style=me.Style(
                font_size=12,
                font_weight="600",
                color=COLORS["primary"],
            ))

        me.input(
            label="",
            placeholder="••••••••",
            type="password",
            appearance="outline",
            value=value,
            on_blur=on_password_blur,
            on_enter=on_login,
            style=input_style(),
        )


def footer():
    with me.box(style=me.Style(
        border=me.Border(top=me.BorderSide(width=1, color=COLORS["outline"])),
        padding=me.Padding.all(24),
        display="flex",
        justify_content="space-between",
        align_items="center",
        gap=16,
    )):
        me.text("Mathsocrates", style=me.Style(
            font_size=18,
            font_weight="700",
            color=COLORS["primary"],
        ))

        with me.box(style=me.Style(display="flex", gap=20)):
            me.text("Conditions d'utilisation", style=footer_text_style())
            me.text("Politique de confidentialité", style=footer_text_style())
            me.text("Mentions légales", style=footer_text_style())

        me.text("© 2024 Mathsocrates. Tous droits réservés.", style=footer_text_style())


def nav_text_style():
    return me.Style(
        font_size=16,
        color=COLORS["muted"],
        cursor="pointer",
    )


def footer_text_style():
    return me.Style(
        font_size=14,
        color=COLORS["muted"],
    )


def label_style():
    return me.Style(
        font_size=12,
        font_weight="700",
        color=COLORS["muted"],
        margin=me.Margin(bottom=8),
    )


def input_style():
    return me.Style(
        width="100%",
        height=48,
        background=COLORS["surface_low"],
        border_radius=8,
    )


def on_email_blur(event: me.InputBlurEvent):
    state = me.state(LoginState)
    state.email = event.value
    state.message = ""


def on_password_blur(event: me.InputBlurEvent):
    state = me.state(LoginState)
    state.password = event.value
    state.message = ""


def on_remember_change(event: me.CheckboxChangeEvent):
    state = me.state(LoginState)
    state.remember = event.checked


def on_login(event: me.ClickEvent | me.InputEnterEvent):
    del event

    state = me.state(LoginState)
    result = authenticate_user(state.email, state.password)

    state.message = result["message"]
    state.is_error = not result["success"]

    if not result["success"]:
        return

    user = result["user"]

    try:
        current_user_path = DATA_DIR / "current_user.json"
        with open(current_user_path, "w", encoding="utf-8") as f:
            json.dump(user, f, ensure_ascii=False)
    except Exception:
        pass

    if user["role"] == "eleve":
        me.navigate("/home-eleve")
    elif user["role"] == "enseignant":
        me.navigate("/home-enseignant")
    else:
        me.navigate("/login")