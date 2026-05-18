from __future__ import annotations

import hashlib
import base64
import secrets
import logging

from Database.db import fetch_one, execute_query

_logger = logging.getLogger("mathsocrates.login")


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    iterations = 100_000
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${base64.b64encode(salt).decode()}${base64.b64encode(dk).decode()}"


def _verify_password(stored: str, password: str) -> bool:
    try:
        if stored.startswith("pbkdf2_sha256$"):
            parts = stored.split("$")
            if len(parts) != 4:
                return False
            _, iter_str, salt_b64, dk_b64 = parts
            iterations = int(iter_str)
            salt = base64.b64decode(salt_b64)
            expected = base64.b64decode(dk_b64)
            dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
            return secrets.compare_digest(dk, expected)
        else:
            # legacy plaintext comparison
            return stored == password
    except Exception:
        _logger.exception("Error verifying password")
        return False


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

    try:
        user = fetch_one(
            """
            SELECT id, full_name, email, password, role, class_name, cognitive_profile
            FROM users
            WHERE lower(email) = ?
            """,
            (normalized_email,),
        )
    except Exception:
        _logger.exception("Database error during user lookup")
        return {"success": False, "message": "Erreur de serveur. Réessayez plus tard.", "user": None}

    if user is None:
        return {"success": False, "message": "Aucun utilisateur trouve avec cet email.", "user": None}

    stored_password = user.get("password", "")

    if stored_password.startswith("pbkdf2_sha256$"):
        if not _verify_password(stored_password, normalized_password):
            return {"success": False, "message": "Mot de passe incorrect.", "user": None}
    else:
        # legacy: plaintext or unsalted. Verify and migrate.
        if stored_password != normalized_password:
            return {"success": False, "message": "Mot de passe incorrect.", "user": None}
        # Re-hash and update the DB
        try:
            new_hash = _hash_password(normalized_password)
            execute_query("UPDATE users SET password = ? WHERE id = ?", (new_hash, user["id"]))
            _logger.info("Migrated user %s to hashed password", user["id"])
        except Exception:
            _logger.exception("Failed to migrate user's password to hashed format")

    safe_user = {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"],
        "class_name": user["class_name"],
        "cognitive_profile": user["cognitive_profile"],
    }

    return {"success": True, "message": f"Bienvenue {safe_user['full_name']} !", "user": safe_user}
