from __future__ import annotations

import mesop as me
import json
from Database.db import DATA_DIR
from Service.teacher_service import get_student_progress
from Service.session_service import get_session


@me.page(path="/student-progress")
def student_progress_page():
    user = get_session()
    
    if not user:
        with me.box(style=me.Style(padding=me.Padding.all(24))):
            me.text("Erreur: Aucune session active.")
        return
    
    current_student_path = DATA_DIR / "current_student.json"
    if not current_student_path.exists():
        with me.box():
            me.text("Aucun étudiant sélectionné. Retournez au tableau de bord de l'enseignant.")
        return

    with open(current_student_path, "r", encoding="utf-8") as f:
        stu = json.load(f)

    student_id = stu.get("id")
    student_name = stu.get("full_name", "-")

    progress = get_student_progress(student_id)

    with me.box(style=me.Style(padding=me.Padding.all(24))):
        me.text(f"Progression — {student_name}", style=me.Style(font_size=22, font_weight="700"))
        profile = progress.get("profile")
        avg_score = progress.get("avg_score")

        me.text(f"Score moyen diagnostics: {avg_score:.2f}" if avg_score is not None else "Aucun score disponible", style=me.Style(margin=me.Margin(top=8, bottom=12)))

        if profile:
            me.text(f"Confiance: {profile.get('confidence_score', 0):.2f}")

        me.text("Diagnostics:")
        for d in progress.get("diagnostics", []):
            with me.box(style=me.Style(border=me.Border.all(me.BorderSide(width=1, color="#e0e6ef")), padding=me.Padding.all(8), margin=me.Margin(bottom=6), border_radius=8)):
                me.text(f"{d.get('chapter')} — score: {d.get('score')}")

        me.text("Séances:")
        for s in progress.get("seances", []):
            with me.box(style=me.Style(border=me.Border.all(me.BorderSide(width=1, color="#e0e6ef")), padding=me.Padding.all(8), margin=me.Margin(bottom=6), border_radius=8)):
                me.text(f"{s.get('exercise_title')} — {s.get('status')}")

        def _back(ev):
            del ev
            me.navigate("/home-enseignant")

        me.button("Retour au tableau", on_click=_back, style=me.Style(margin=me.Margin(top=12)))
