from __future__ import annotations

import mesop as me
from Database.db import fetch_all
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
class ReportState:
    selected_seance_id: str = ""
    report_format: str = "pdf"


@me.page(path="/report-generation")
def report_generation_page():
    user = get_session()
    
    if not user:
        with me.box(style=me.Style(padding=me.Padding.all(24))):
            me.text("Erreur: Aucune session active.")
        return
    
    state = me.state(ReportState)
    
    # Fetch seances for the teacher's class
    seances = fetch_all(
        """
        SELECT s.id, s.exercise_title, s.chapter, s.status, s.current_phase, u.full_name
        FROM seances s
        JOIN users u ON s.student_id = u.id
        WHERE u.class_name = ?
        ORDER BY s.id DESC
        LIMIT 20
        """,
        (user.get("class_name"),),
    )
    
    with me.box(style=me.Style(padding=me.Padding.all(24), background=COLORS["bg"], min_height="100vh")):
        me.text("Génération de Rapports — Séances Socratiques", style=me.Style(font_size=28, font_weight="700", margin=me.Margin(bottom=24)))
        
        me.text("Sélectionnez une séance pour générer un rapport détaillé", style=me.Style(color=COLORS["muted"], margin=me.Margin(bottom=20)))
        
        with me.box(style=me.Style(display="grid", grid_template_columns="1fr 300px", gap=24)):
            # Seances list
            with me.box():
                me.text("Séances disponibles", style=me.Style(font_size=18, font_weight="700", margin=me.Margin(bottom=16)))
                
                if not seances:
                    me.text("Aucune séance disponible.", style=me.Style(color=COLORS["muted"]))
                else:
                    for seance in seances:
                        def _select(ev, sid=seance["id"]):
                            del ev
                            state = me.state(ReportState)
                            state.selected_seance_id = str(sid)
                        
                        with me.box(style=me.Style(
                            background=COLORS["surface"],
                            border=me.Border.all(me.BorderSide(width=2 if str(seance["id"]) == state.selected_seance_id else 1, color=COLORS["primary"] if str(seance["id"]) == state.selected_seance_id else COLORS["outline"])),
                            border_radius=8,
                            padding=me.Padding.all(12),
                            margin=me.Margin(bottom=12),
                            cursor="pointer",
                        )):
                            me.button(
                                f"{seance['exercise_title']} — {seance['full_name']}",
                                on_click=_select,
                                type="flat",
                                style=me.Style(width="100%", text_align="left"),
                            )
                            me.text(f"Phase: {seance['current_phase']} | Status: {seance['status']}", style=me.Style(font_size=12, color=COLORS["muted"]))
            
            # Report options
            with me.box(style=me.Style(
                background=COLORS["surface"],
                border=me.Border.all(me.BorderSide(width=1, color=COLORS["outline"])),
                border_radius=12,
                padding=me.Padding.all(16),
                height="fit-content",
            )):
                me.text("Options du rapport", style=me.Style(font_size=16, font_weight="700", margin=me.Margin(bottom=16)))
                
                me.text("Format:", style=me.Style(font_weight="700", margin=me.Margin(bottom=8)))
                
                # Format selection using buttons instead of select
                with me.box(style=me.Style(display="flex", gap=8, margin=me.Margin(bottom=16))):
                    for fmt in ["pdf", "docx", "html"]:
                        def _set_format(ev, f=fmt):
                            del ev
                            s = me.state(ReportState)
                            s.report_format = f
                        
                        me.button(
                            fmt.upper(),
                            on_click=_set_format,
                            type="raised" if state.report_format == fmt else "flat",
                            style=me.Style(flex=1),
                        )
                
                me.text("Contenu du rapport:", style=me.Style(font_weight="700", margin=me.Margin(bottom=8)))
                
                with me.box(style=me.Style(margin=me.Margin(bottom=16))):
                    me.checkbox("Transcription complète")
                    me.checkbox("Phases de la séance", checked=True)
                    me.checkbox("Aide fournie", checked=True)
                    me.checkbox("Analyse des erreurs", checked=True)
                    me.checkbox("Progrès de l'élève")
                
                def _generate(ev):
                    del ev
                    if not state.selected_seance_id:
                        me.toast("Veuillez sélectionner une séance")
                        return
                    # TODO: Implement PDF generation
                    me.toast(f"Génération du rapport pour séance {state.selected_seance_id} en {state.report_format}")
                
                me.button("Générer le rapport", on_click=_generate, type="raised", style=me.Style(width="100%"))
        
        def _back(ev):
            del ev
            me.navigate("/home-enseignant")
        
        me.button("Retour au tableau", on_click=_back, style=me.Style(margin=me.Margin(top=24)))
