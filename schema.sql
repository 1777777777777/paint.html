CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drawings (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL REFERENCES users,
    title TEXT NOT NULL,
    payload TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS likes (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL REFERENCES users,
    drawing_id INTEGER NOT NULL REFERENCES drawings,
    UNIQUE(username, drawing_id)
);
