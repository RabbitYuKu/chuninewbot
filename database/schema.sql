CREATE TABLE IF NOT EXISTS cookies(
    discord_id INTEGER PRIMARY KEY,
    cookie TEXT
);

CREATE TABLE IF NOT EXISTS chunirec_songs(
    id TEXT PRIMARY KEY,
    chunithm_id INTEGER,
    title TEXT,
    chunithm_catcode INTEGER,
    genre TEXT,
    artist TEXT,
    release TEXT,
    bpm INTEGER,
    jacket TEXT
);

CREATE TABLE IF NOT EXISTS chunirec_charts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_id TEXT,
    difficulty TEXT,
    level REAL,
    const REAL,
    maxcombo INTEGER,
    is_const_unknown BOOLEAN,
    FOREIGN KEY(song_id) REFERENCES chunirec_songs(id),
    UNIQUE(song_id, difficulty)
);