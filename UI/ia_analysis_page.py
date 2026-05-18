from __future__ import annotations

import mesop as me
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


@me.page(path="/ia-analysis")
def ia_analysis_page():
    user = get_session()
    
    if not user:
        with me.box(style=me.Style(padding=me.Padding.all(24))):
            me.text("Erreur: Aucune session active.")
        return
    
    with me.box(style=me.Style(padding=me.Padding.all(24), background=COLORS["bg"], min_height="100vh")):
        me.text("Analyses IA — Données extraites", style=me.Style(font_size=28, font_weight="700", margin=me.Margin(bottom=24)))
        
        me.text(f"Enseignant: {user.get('full_name')} (Classe {user.get('class_name')})", style=me.Style(color=COLORS["muted"], margin=me.Margin(bottom=24)))
        
        # Placeholder section for langextract integration
        with me.box(style=me.Style(
            background=COLORS["surface"],
            border=me.Border.all(me.BorderSide(width=1, color=COLORS["outline"])),
            border_radius=12,
            padding=me.Padding.all(20),
            margin=me.Margin(bottom=20),
        )):
            me.text("Données extraites par IA (langextract)", style=me.Style(font_size=18, font_weight="700", margin=me.Margin(bottom=12)))
            me.text("Cette section affichera les analyses extraites par langextract lors de l'intégration.", style=me.Style(color=COLORS["muted"]))
        
        # Sample cards for future data
        with me.box(style=me.Style(display="grid", grid_template_columns="repeat(auto-fill, minmax(250px, 1fr))", gap=16)):
            for label in ["Concepts clés identifiés", "Erreurs détectées", "Profil cognitif", "Tendances"]:
                with me.box(style=me.Style(
                    background=COLORS["surface"],
                    border=me.Border.all(me.BorderSide(width=1, color=COLORS["outline"])),
                    border_radius=12,
                    padding=me.Padding.all(16),
                )):
                    me.text(label, style=me.Style(font_size=16, font_weight="700", margin=me.Margin(bottom=8)))
                    me.text("Données en attente...", style=me.Style(color=COLORS["muted"], font_size=12))
        
        def _back(ev):
            del ev
            me.navigate("/home-enseignant")
        
        me.button("Retour au tableau", on_click=_back, style=me.Style(margin=me.Margin(top=24)))
