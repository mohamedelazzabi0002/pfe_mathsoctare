from __future__ import annotations

from Database.db import fetch_all, fetch_one
import logging

_logger = logging.getLogger("mathsocrates.teacher")


def get_all_classes():
    """Retourne la liste de toutes les classes avec au moins un élève"""
    return fetch_all(
        """
        SELECT DISTINCT class_name FROM users 
        WHERE role = 'eleve' AND class_name IS NOT NULL
        ORDER BY class_name
        """
    )


def get_students_by_class(class_name: str):
    """Retourne la liste des élèves pour une classe donnée."""
    if not class_name:
        return []
    return fetch_all(
        "SELECT id, full_name, email, class_name FROM users WHERE class_name = ? AND role = 'eleve'",
        (class_name,),
    )


def get_class_progress(class_name: str):
    """Calcule des métriques simples de progression pour la classe."""
    students = get_students_by_class(class_name)
    ids = [s["id"] for s in students]
    total = len(students)

    avg_confidence = 0.0
    avg_score = 0.0

    if ids:
        placeholders = ",".join("?" for _ in ids)
        profiles = fetch_all(
            f"SELECT student_id, confidence_score FROM student_profiles WHERE student_id IN ({placeholders})",
            tuple(ids),
        )
        if profiles:
            avg_confidence = sum(p["confidence_score"] for p in profiles) / len(profiles)

        scores = []
        for sid in ids:
            row = fetch_one("SELECT AVG(score) as avg_score FROM diagnostics WHERE student_id = ?", (sid,))
            if row and row.get("avg_score") is not None:
                scores.append(row["avg_score"])
        if scores:
            avg_score = sum(scores) / len(scores)

    return {
        "students": students,
        "total_students": total,
        "avg_confidence": avg_confidence,
        "avg_score": avg_score,
    }


def get_student_progress(student_id: int):
    """Retourne un résumé de progression pour un élève donné."""
    if not student_id:
        return {"profile": None, "diagnostics": [], "seances": [], "avg_score": None}

    profile = fetch_one("SELECT * FROM student_profiles WHERE student_id = ?", (student_id,))
    diagnostics = fetch_all("SELECT id, chapter, score, status FROM diagnostics WHERE student_id = ?", (student_id,))
    seances = fetch_all("SELECT id, exercise_title, status, chapter FROM seances WHERE student_id = ?", (student_id,))
    avg_row = fetch_one("SELECT AVG(score) as avg_score FROM diagnostics WHERE student_id = ?", (student_id,))
    avg_score = avg_row.get("avg_score") if avg_row else None

    return {"profile": profile, "diagnostics": diagnostics, "seances": seances, "avg_score": avg_score}
