from __future__ import annotations

# Stockage temporaire de la session courante en memoire.
_current_session = {
    "user": None,
}


def set_current_user(user: dict | None) -> None:
    """
    Enregistre l'utilisateur courant dans la session.
    """
    _current_session["user"] = user


def get_current_user() -> dict | None:
    """
    Retourne l'utilisateur courant si une session existe.
    """
    return _current_session["user"]


def clear_session() -> None:
    """
    Vide la session courante.
    """
    _current_session["user"] = None


def has_active_session() -> bool:
    """
    Indique si un utilisateur est connecte.
    """
    return _current_session["user"] is not None
