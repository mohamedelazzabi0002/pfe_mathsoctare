PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK (
        role IN ('eleve', 'enseignant')
    ) NOT NULL,
    class_name TEXT,
    cognitive_profile TEXT CHECK (
        cognitive_profile IN ('normal', 'hesitant', 'error_prone')
    )
);

CREATE TABLE IF NOT EXISTS student_profiles (
    student_id INTEGER PRIMARY KEY,
    current_level TEXT CHECK (
        current_level IN ('faible', 'moyen', 'bon')
    ) DEFAULT 'faible',
    confidence_score REAL DEFAULT 0.5,
    error_tendency_score REAL DEFAULT 0.0,
    FOREIGN KEY (student_id) REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS diagnostics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    chapter TEXT NOT NULL,
    status TEXT CHECK (
        status IN ('active', 'completed', 'interrupted')
    ) DEFAULT 'active',
    score REAL DEFAULT 0,
    cognitive_profile_detected TEXT CHECK (
        cognitive_profile_detected IN ('normal', 'hesitant', 'error_prone')
    ),
    FOREIGN KEY (student_id) REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS diagnostic_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diagnostic_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    student_answer TEXT,
    is_correct INTEGER CHECK (
        is_correct IN (0, 1)
    ) DEFAULT 0,
    error_type TEXT CHECK (
        error_type IN (
            'erreur_de_signe',
            'confusion_formule',
            'erreur_calcul',
            'erreur_methode',
            'erreur_notation',
            'concept_non_maitrise',
            'aucune',
            'autre'
        )
    ) DEFAULT 'aucune',
    FOREIGN KEY (diagnostic_id) REFERENCES diagnostics(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS seances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    diagnostic_id INTEGER,
    exercise_title TEXT NOT NULL,
    exercise_statement TEXT,
    exercise_concept TEXT,
    exercise_difficulty TEXT CHECK (
        exercise_difficulty IN ('faible', 'moyen', 'bon')
    ),
    expected_answer TEXT,
    solution_steps TEXT,
    resume TEXT,
    chapter TEXT NOT NULL,
    status TEXT CHECK (
        status IN ('active', 'completed', 'interrupted')
    ) DEFAULT 'active',
    current_phase TEXT CHECK (
        current_phase IN (
            'activation',
            'comprehension',
            'progression',
            'correction',
            'verification'
        )
    ) DEFAULT 'activation',
    phase_history_json TEXT DEFAULT '[]',
    last_student_input_type TEXT CHECK (
        last_student_input_type IN ('text', 'image', 'latex')
    ) DEFAULT 'text',
    FOREIGN KEY (student_id) REFERENCES users(id)
        ON DELETE CASCADE,
    FOREIGN KEY (diagnostic_id) REFERENCES diagnostics(id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seance_id INTEGER NOT NULL,
    sender TEXT CHECK (
        sender IN ('tutor', 'eleve')
    ) NOT NULL,
    content TEXT NOT NULL,
    message_type TEXT CHECK (
        message_type IN ('text', 'image', 'latex')
    ) DEFAULT 'text',
    metadata_json TEXT,
    role_phase TEXT CHECK (
        role_phase IN (
            'activation',
            'comprehension',
            'progression',
            'correction',
            'verification'
        )
    ),
    FOREIGN KEY (seance_id) REFERENCES seances(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    seance_id INTEGER,
    error_type TEXT CHECK (
        error_type IN (
            'erreur_de_signe',
            'confusion_formule',
            'erreur_calcul',
            'erreur_methode',
            'erreur_notation',
            'concept_non_maitrise',
            'autre'
        )
    ) NOT NULL,
    description TEXT,
    source_excerpt TEXT,
    chapter TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES users(id)
        ON DELETE CASCADE,
    FOREIGN KEY (seance_id) REFERENCES seances(id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    concept_name TEXT NOT NULL,
    chapter TEXT NOT NULL,
    mastery_level TEXT CHECK (
        mastery_level IN ('not_mastered', 'partial', 'mastered')
    ) DEFAULT 'not_mastered',
    source_excerpt TEXT,
    FOREIGN KEY (student_id) REFERENCES users(id)
        ON DELETE CASCADE
);
