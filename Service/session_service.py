from __future__ import annotations

import json
import logging
from Database.db import DATA_DIR

_logger = logging.getLogger("mathsocrates.session")


def save_session(user: dict):
    """Sauvegarde l'utilisateur en session et en fichier"""
    try:
        current_user_path = DATA_DIR / "current_user.json"
        with open(current_user_path, "w", encoding="utf-8") as f:
            json.dump(user, f, ensure_ascii=False)
        _logger.info("Session saved for user: %s", user.get("id"))
    except Exception as e:
        _logger.exception("Failed to save session: %s", e)


def get_session() -> dict | None:
    """Récupère l'utilisateur en session (toujours lire depuis le fichier)"""
    try:
        current_user_path = DATA_DIR / "current_user.json"
        
        if current_user_path.exists():
            with open(current_user_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        _logger.exception("Failed to read session: %s", e)
    
    return None


def clear_session():
    """Nettoie la session"""
    try:
        current_user_path = DATA_DIR / "current_user.json"
        if current_user_path.exists():
            current_user_path.unlink()
        current_student_path = DATA_DIR / "current_student.json"
        if current_student_path.exists():
            current_student_path.unlink()
    except Exception:
        pass
