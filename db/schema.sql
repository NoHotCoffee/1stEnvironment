-- Scripture Studio schema (PostgreSQL; SQLite-compatible except SERIAL types)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS verses (
    id SERIAL PRIMARY KEY,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    translation TEXT DEFAULT 'KJV',
    text TEXT NOT NULL,
    strong_refs JSONB DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS lexicon (
    id SERIAL PRIMARY KEY,
    strong_number TEXT NOT NULL,
    lemma TEXT NOT NULL,
    transliteration TEXT NOT NULL,
    language TEXT NOT NULL,
    morphology TEXT,
    gloss TEXT,
    example_verses TEXT,
    source_url TEXT
);

CREATE TABLE IF NOT EXISTS study_notes (
    id SERIAL PRIMARY KEY,
    verse_id INTEGER REFERENCES verses(id),
    content JSONB NOT NULL,
    created_by INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS transcripts (
    id SERIAL PRIMARY KEY,
    title TEXT,
    speaker TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    text TEXT,
    raw_audio_url TEXT,
    created_by INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS devotionals (
    id SERIAL PRIMARY KEY,
    title TEXT,
    verse_refs TEXT,
    content TEXT,
    tone TEXT,
    audience TEXT,
    length TEXT,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS apologetics_modules (
    id SERIAL PRIMARY KEY,
    title TEXT,
    lessons JSONB,
    quizzes JSONB
);

CREATE TABLE IF NOT EXISTS flashcards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    front TEXT,
    back TEXT,
    efactor REAL DEFAULT 2.5,
    interval INTEGER DEFAULT 1,
    next_review DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS annotations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    verse_id INTEGER REFERENCES verses(id),
    content TEXT,
    visibility TEXT DEFAULT 'private'
);

CREATE TABLE IF NOT EXISTS highlights (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    verse_id INTEGER REFERENCES verses(id),
    color TEXT DEFAULT '#ffe08a',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SQLite compatibility notes:
-- Replace SERIAL with INTEGER PRIMARY KEY AUTOINCREMENT and JSONB with JSON.
