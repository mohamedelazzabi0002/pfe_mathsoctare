from __future__ import annotations

from Database.db import fetch_one

## connexion user
def authenticate_user(email: str, password: str) -> dict:
    """
    Vérifie les identifiants de connexion dans la base.
    Retourne un dictionnaire homogène pour simplifier l'usage côté UI.
    """
    normalized_email = email.strip().lower()
    normalized_password = password.strip()

    if not normalized_email or not normalized_password:
        return {
            "success": False,
            "message": "Veuillez remplir l'email et le mot de passe.",
            "user": None,
        }

    user = fetch_one(
        """
        SELECT id, full_name, email, password, role, class_name, cognitive_profile
        FROM users
        WHERE lower(email) = ?
        """,
        (normalized_email,),
    )

    if user is None:
        return {
            "success": False,
            "message": "Aucun utilisateur trouve avec cet email.",
            "user": None,
        }

    if user["password"] != normalized_password:
        return {
            "success": False,
            "message": "Mot de passe incorrect.",
            "user": None,
        }
    ## securise user
    safe_user = {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"],
        "class_name": user["class_name"],
        "cognitive_profile": user["cognitive_profile"],
    }

    return {
        "success": True,
        "message": f"Bienvenue {safe_user['full_name']} !",
        "user": safe_user,
    }
