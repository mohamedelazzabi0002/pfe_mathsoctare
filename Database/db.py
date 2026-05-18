import sqlite3
import threading
from pathlib import Path


# Dossier du projet
BASE_DIR = Path(__file__).resolve().parent

# Dossier externe pour éviter le hot reload Mesop
DATA_DIR = Path.home() / "Music" / "mathsocrates_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Base SQLite hors du dossier Mathsocrate_pfe
DB_PATH = DATA_DIR / "mathsocrates.db"

# Fichier schema.sql reste dans database/
SCHEMA_PATH = BASE_DIR / "schema.sql"
_SCHEMA_LOCK = threading.Lock()
_SCHEMA_READY = False


def _column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return any(column[1] == column_name for column in columns)


def _run_schema_upgrades():
    conn = sqlite3.connect(DB_PATH, timeout=30)

    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        if not _column_exists(cursor, "seances", "current_phase"):
            cursor.execute(
                """
                ALTER TABLE seances
                ADD COLUMN current_phase TEXT
                CHECK (
                    current_phase IN (
                        'activation',
                        'comprehension',
                        'progression',
                        'correction',
                        'verification'
                    )
                )
                DEFAULT 'activation';
                """
            )

        if not _column_exists(cursor, "seances", "phase_history_json"):
            cursor.execute(
                """
                ALTER TABLE seances
                ADD COLUMN phase_history_json TEXT DEFAULT '[]';
                """
            )

        if not _column_exists(cursor, "seances", "last_student_input_type"):
            cursor.execute(
                """
                ALTER TABLE seances
                ADD COLUMN last_student_input_type TEXT
                CHECK (last_student_input_type IN ('text', 'image', 'latex'))
                DEFAULT 'text';
                """
            )

        if not _column_exists(cursor, "seances", "resume"):
            cursor.execute(
                """
                ALTER TABLE seances
                ADD COLUMN resume TEXT;
                """
            )

        if not _column_exists(cursor, "messages", "metadata_json"):
            cursor.execute(
                """
                ALTER TABLE messages
                ADD COLUMN metadata_json TEXT;
                """
            )

        if not _column_exists(cursor, "messages", "role_phase"):
            cursor.execute(
                """
                ALTER TABLE messages
                ADD COLUMN role_phase TEXT
                CHECK (
                    role_phase IN (
                        'activation',
                        'comprehension',
                        'progression',
                        'correction',
                        'verification'
                    )
                );
                """
            )

        if not _column_exists(cursor, "errors", "source_excerpt"):
            cursor.execute(
                """
                ALTER TABLE errors
                ADD COLUMN source_excerpt TEXT;
                """
            )

        if not _column_exists(cursor, "concepts", "source_excerpt"):
            cursor.execute(
                """
                ALTER TABLE concepts
                ADD COLUMN source_excerpt TEXT;
                """
            )

        conn.commit()

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()


def ensure_schema_ready():
    global _SCHEMA_READY

    if _SCHEMA_READY:
        return

    with _SCHEMA_LOCK:
        if _SCHEMA_READY:
            return

        if SCHEMA_PATH.exists():
            conn = sqlite3.connect(DB_PATH, timeout=30)

            try:
                with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
                    schema = file.read()

                conn.executescript(schema)
                conn.commit()
            finally:
                conn.close()

        _run_schema_upgrades()
        _SCHEMA_READY = True


def get_connection():
    """
    Crée une connexion SQLite.
    La base est stockée hors du projet pour éviter le hot reload Mesop.
    """
    ensure_schema_ready()
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 30000;")
    conn.execute("PRAGMA journal_mode = WAL;")

    return conn


def execute_query(query, params=()):
    """
    Exécute INSERT, UPDATE ou DELETE.
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erreur SQLite : {e}")
        raise

    finally:
        conn.close()

## vexécute une requête SELECT dans la base SQLite, récupère une seule ligne, puis la retourne sous forme de dictionnaire.
def fetch_one(query, params=()):
    """
    Exécute SELECT et retourne une seule ligne.
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
        raise

    finally:
        conn.close()


def fetch_all(query, params=()):
    """
    Exécute SELECT et retourne plusieurs lignes.
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
        raise

    finally:
        conn.close()


def init_db():
    """
    Initialise la base depuis schema.sql.
    """
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError("Le fichier schema.sql est introuvable.")

    conn = get_connection()

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            schema = file.read()

        conn.executescript(schema)
        conn.commit()

        print("Base de données initialisée avec succès.")
        print(f"Chemin de la base : {DB_PATH}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erreur lors de l'initialisation de la base : {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    init_db()

    tables = fetch_all("SELECT name FROM sqlite_master WHERE type='table';")

    print("Tables dans la base :")
    for table in tables:
        print("-", table["name"])
