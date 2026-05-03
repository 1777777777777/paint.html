CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    bio TEXT
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

CREATE TABLE IF NOT EXISTS tags (
    name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS drawing_tags (
    drawing_id INTEGER NOT NULL REFERENCES drawings,
    tag TEXT NOT NULL REFERENCES tags(name),
    PRIMARY KEY (drawing_id, tag)
);
