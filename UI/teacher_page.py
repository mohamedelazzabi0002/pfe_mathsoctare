from __future__ import annotations

import json
import mesop as me
from Database.db import DATA_DIR
from Service.teacher_service import get_class_progress
from Service.session_service import get_session, clear_session


def logout():
    """Nettoie la session et redirige vers login"""
    clear_session()
    me.navigate("/login")



COLORS = {
    "bg": "#f8f9ff",
    "surface": "#ffffff",
    "surface_low": "#eff4ff",
    "surface_mid": "#e5eeff",
    "primary": "#4648d4",
    "primary_soft": "#e1e0ff",
    "text": "#0b1c30",
    "muted": "#464554",
    "outline": "#c7c4d7",
    "error": "#ba1a1a",
}


@me.stateclass
class TeacherState:
    selected_student_id: str = ""
    selected_student_name: str = ""


def go_student_progress(e: me.ClickEvent):
    state = me.state(TeacherState)

    current_student_path = DATA_DIR / "current_student.json"
    with open(current_student_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "id": state.selected_student_id,
                "full_name": state.selected_student_name,
            },
            f,
            ensure_ascii=False,
        )

    me.navigate("/student-progress")


def select_student(student_id: str, student_name: str):
    state = me.state(TeacherState)
    state.selected_student_id = str(student_id)
    state.selected_student_name = student_name


@me.page(path="/home-enseignant")
def teacher_page():
    user = get_session()
    
    if not user:
        with me.box(style=me.Style(padding=me.Padding.all(24))):
            me.text("Erreur: Aucune session active. Veuillez vous reconnecter.")
        return

    class_name = user.get("class_name")
    dashboard = get_class_progress(class_name)

    with me.box(style=page_style()):
        sidebar()

        with me.box(style=me.Style(
            margin=me.Margin(left=256),
            width="calc(100% - 256px)",
            min_height="100vh",
        )):
            topbar(class_name)
            dashboard_content(user, dashboard)


def page_style():
    return me.Style(
        background=COLORS["bg"],
        min_height="100vh",
        color=COLORS["text"],
        font_family="Inter, Arial, sans-serif",
    )


def sidebar():
    with me.box(style=me.Style(
        position="fixed",
        left=0,
        top=0,
        width=256,
        height="100vh",
        background=COLORS["surface_low"],
        border=me.Border(right=me.BorderSide(width=1, color=COLORS["outline"])),
        padding=me.Padding.all(16),
        display="flex",
        flex_direction="column",
        gap=14,
    )):
        me.text("🎓 ENT Éducation", style=me.Style(
            font_size=20,
            font_weight="700",
            color=COLORS["primary"],
        ))

        me.text("Portail Enseignant", style=me.Style(
            font_size=12,
            color=COLORS["muted"],
            margin=me.Margin(bottom=16),
        ))

        me.button("＋ Nouvelle Analyse", type="flat", style=me.Style(
            width="100%",
            margin=me.Margin(bottom=16),
        ))

        nav_item("📊 Vue d'ensemble", active=True)
        nav_button("👥 Mes élèves", go_students)
        nav_button("📈 Analyses IA", go_ia_analysis)
        nav_button("📄 Rapports", go_reports)

        with me.box(style=me.Style(flex_grow=1)):
            pass

        nav_item("❓ Aide")
        logout_button()


def nav_item(label: str, active: bool = False, color: str | None = None):
    """Affiche un item de navigation (texte seulement, pas de callback)"""
    me.text(label, style=me.Style(
        padding=me.Padding.symmetric(vertical=10, horizontal=12),
        border_radius=8,
        background=COLORS["primary"] if active else "transparent",
        color="white" if active else color or COLORS["muted"],
        font_weight="700" if active else "500",
        width="100%",
    ))


def go_students(e: me.ClickEvent):
    del e
    me.navigate("/students-list")


def go_ia_analysis(e: me.ClickEvent):
    del e
    me.navigate("/ia-analysis")


def go_reports(e: me.ClickEvent):
    del e
    me.navigate("/report-generation")


def nav_button(label: str, on_click_fn):
    """Bouton de navigation qui redirige vers une page"""
    me.button(label, type="raised", on_click=on_click_fn, style=me.Style(
        padding=me.Padding.symmetric(vertical=10, horizontal=12),
        border_radius=8,
        background="transparent",
        color=COLORS["muted"],
        font_weight="500",
        width="100%",
        text_align="left",
    ))


def logout_button():
    """Bouton de déconnexion"""
    def _on_click(e: me.ClickEvent):
        del e
        logout()
    
    me.button("🚪 Déconnexion", type="flat", on_click=_on_click, style=me.Style(
        padding=me.Padding.symmetric(vertical=10, horizontal=12),
        border_radius=8,
        background="transparent",
        color=COLORS["error"],
        font_weight="500",
        width="100%",
        text_align="left",
    ))


def topbar(class_name: str):
    with me.box(style=me.Style(
        height=64,
        background=COLORS["bg"],
        border=me.Border(bottom=me.BorderSide(width=1, color=COLORS["outline"])),
        display="flex",
        justify_content="space-between",
        align_items="center",
        padding=me.Padding.symmetric(horizontal=24),
        position="sticky",
        top=0,
        z_index=10,
    )):
        me.text("Tableau de bord enseignant", style=me.Style(
            font_size=18,
            font_weight="700",
        ))

        with me.box(style=me.Style(display="flex", gap=12, align_items="center")):
            chip(class_name or "Classe inconnue")
            chip("📅 Cette semaine")
            me.text("🔔")
            me.text("⚙️")


def chip(text: str):
    me.text(text, style=me.Style(
        background=COLORS["surface_low"],
        border=me.Border.all(me.BorderSide(width=1, color=COLORS["outline"])),
        border_radius=8,
        padding=me.Padding.symmetric(vertical=8, horizontal=12),
        font_size=14,
    ))


def dashboard_content(user: dict, dashboard: dict):
    with me.box(style=me.Style(
        padding=me.Padding.all(24),
        display="flex",
        flex_direction="column",
        gap=24,
    )):
        me.text(
            f"Bonjour {user.get('full_name')}",
            style=me.Style(font_size=28, font_weight="700"),
        )

        with me.box(style=me.Style(
            display="grid",
            grid_template_columns="1fr 2fr 1fr",
            gap=24,
        )):
            students_card(dashboard)
            progress_card(dashboard)
            stats_column(dashboard)


def card_style():
    return me.Style(
        background=COLORS["surface"],
        border=me.Border.all(me.BorderSide(width=1, color=COLORS["outline"])),
        border_radius=12,
        padding=me.Padding.all(20),
        box_shadow="0 8px 24px rgba(15, 23, 42, 0.05)",
    )


def students_card(dashboard: dict):
    with me.box(style=card_style()):
        with me.box(style=me.Style(
            display="flex",
            justify_content="space-between",
            align_items="center",
            margin=me.Margin(bottom=16),
        )):
            me.text("Liste des élèves", style=me.Style(font_size=18, font_weight="700"))
            me.text(f"{dashboard['total_students']} élèves", style=me.Style(
                background=COLORS["surface_mid"],
                color=COLORS["primary"],
                padding=me.Padding.symmetric(vertical=4, horizontal=8),
                border_radius=999,
                font_size=12,
                font_weight="700",
            ))

        for s in dashboard["students"]:
            student_item(s)


def student_item(s: dict):
    progress = int(s.get("progress", s.get("score", 0)) or 0)

    with me.box(style=me.Style(
        padding=me.Padding.symmetric(vertical=14),
        border=me.Border(bottom=me.BorderSide(width=1, color=COLORS["outline"])),
    )):
        me.text(s["full_name"], style=me.Style(font_size=16, font_weight="700"))
        me.text(s.get("email", ""), style=me.Style(font_size=12, color=COLORS["muted"]))

        progress_bar(progress)

        me.button(
            "Voir progression",
            type="flat",
            on_click=go_student_progress,
            style=me.Style(margin=me.Margin(top=8)),
        )

        select_student(str(s["id"]), s["full_name"])


def progress_card(dashboard: dict):
    with me.box(style=card_style()):
        me.text("Progression de la classe", style=me.Style(
            font_size=18,
            font_weight="700",
            margin=me.Margin(bottom=20),
        ))

        avg_score = int((dashboard.get("avg_score") or 0) * 100)
        avg_confidence = int((dashboard.get("avg_confidence") or 0) * 100)

        metric_bar("Score moyen", f"{avg_score}%", avg_score)
        metric_bar("Confiance moyenne", f"{avg_confidence}%", avg_confidence)
        metric_bar("Engagement", "72%", 72)
        metric_bar("Risque d'erreur", "28%", 28)


def stats_column(dashboard: dict):
    with me.box(style=me.Style(display="flex", flex_direction="column", gap=24)):
        stat_card("Élèves", str(dashboard["total_students"]), "Classe active")
        stat_card("Score moyen", f"{dashboard['avg_score']:.2f}", "Performance")
        stat_card("Confiance", f"{dashboard['avg_confidence']:.2f}", "Analyse IA")


def stat_card(title: str, value: str, note: str):
    with me.box(style=card_style()):
        me.text(title.upper(), style=me.Style(
            font_size=12,
            color=COLORS["muted"],
            font_weight="700",
        ))
        me.text(value, style=me.Style(
            font_size=28,
            font_weight="700",
            margin=me.Margin(top=8),
        ))
        me.text(note, style=me.Style(
            color=COLORS["primary"],
            font_size=13,
            font_weight="600",
        ))


def metric_bar(label: str, value_label: str, value: int):
    with me.box(style=me.Style(margin=me.Margin(bottom=18))):
        with me.box(style=me.Style(display="flex", justify_content="space-between")):
            me.text(label, style=me.Style(font_weight="700"))
            me.text(value_label, style=me.Style(color=COLORS["muted"]))

        progress_bar(value)


def progress_bar(value: int):
    value = max(0, min(value, 100))

    with me.box(style=me.Style(
        height=8,
        background=COLORS["primary_soft"],
        border_radius=999,
        margin=me.Margin(top=8),
        overflow="hidden",
    )):
        me.box(style=me.Style(
            height=8,
            width=f"{value}%",
            background=COLORS["primary"],
            border_radius=999,
        ))