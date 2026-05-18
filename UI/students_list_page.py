from __future__ import annotations

import json
import mesop as me
from Database.db import DATA_DIR
from Service.teacher_service import get_all_classes, get_students_by_class
from Service.session_service import get_session


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
}


@me.stateclass
class StudentsState:
    selected_class: str = ""


@me.page(path="/students-list")
def students_list_page():
    user = get_session()
    
    if not user:
        with me.box(style=me.Style(padding=me.Padding.all(24))):
            me.text("Erreur: Aucune session active.")
        return
    
    state = me.state(StudentsState)
    
    # Get all available classes
    classes = get_all_classes()
    class_names = [c["class_name"] for c in classes]
    
    # Set default class if none selected
    if not state.selected_class and class_names:
        state.selected_class = class_names[0]
    
    # Get students for selected class
    students = get_students_by_class(state.selected_class) if state.selected_class else []
    
    with me.box(style=me.Style(padding=me.Padding.all(24), background=COLORS["bg"], min_height="100vh")):
        me.text("Liste des élèves", style=me.Style(font_size=28, font_weight="700", margin=me.Margin(bottom=24)))
        
        # Class selection
        me.text("Sélectionnez une classe:", style=me.Style(font_size=16, font_weight="700", margin=me.Margin(bottom=12)))
        
        with me.box(style=me.Style(display="flex", gap=8, margin=me.Margin(bottom=24), flex_wrap="wrap")):
            for class_name in class_names:
                def _select_class(ev, cls=class_name):
                    del ev
                    s = me.state(StudentsState)
                    s.selected_class = cls
                
                me.button(
                    class_name,
                    on_click=_select_class,
                    type="raised" if state.selected_class == class_name else "flat",
                    style=me.Style(
                        padding=me.Padding.symmetric(vertical=8, horizontal=16),
                        background=COLORS["primary"] if state.selected_class == class_name else "transparent",
                        color="white" if state.selected_class == class_name else COLORS["muted"],
                    ),
                )
        
        # Students display
        if state.selected_class:
            me.text(f"Classe {state.selected_class} — {len(students)} élèves", style=me.Style(font_size=18, font_weight="700", color=COLORS["primary"], margin=me.Margin(bottom=20)))
            
            if students:
                with me.box(style=me.Style(display="grid", grid_template_columns="repeat(auto-fill, minmax(300px, 1fr))", gap=16)):
                    for s in students:
                        with me.box(style=me.Style(
                            background=COLORS["surface"],
                            border=me.Border.all(me.BorderSide(width=1, color=COLORS["outline"])),
                            border_radius=12,
                            padding=me.Padding.all(20),
                        )):
                            me.text(s["full_name"], style=me.Style(font_size=18, font_weight="700", margin=me.Margin(bottom=8)))
                            me.text(s.get("email", ""), style=me.Style(font_size=14, color=COLORS["muted"], margin=me.Margin(bottom=16)))
                            
                            def _goto(ev, sid=s['id'], name=s['full_name']):
                                del ev
                                current_student_path = DATA_DIR / "current_student.json"
                                with open(current_student_path, "w", encoding="utf-8") as f:
                                    json.dump({"id": sid, "full_name": name}, f, ensure_ascii=False)
                                me.navigate("/student-progress")
                            
                            me.button("Voir progression", on_click=_goto, type="raised", style=me.Style(width="100%"))
            else:
                me.text("Aucun élève dans cette classe.", style=me.Style(color=COLORS["muted"]))
        
        def _back(ev):
            del ev
            me.navigate("/home-enseignant")
        
        me.button("Retour au tableau", on_click=_back, style=me.Style(margin=me.Margin(top=24)))
