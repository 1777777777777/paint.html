import db


def draw_save(username, title, payload):
    db.execute(
               "INSERT INTO drawings (username, title, payload) VALUES (?, ?, ?)",
               (username, title, payload))


def drawings_search(search_query="", page=1, page_size=10):
    offset = (page - 1) * page_size
    
    if search_query:
        drawings = db.query(
            """
            SELECT id, username, title, payload
            FROM drawings 
            WHERE title LIKE ?
            OR username LIKE ? 
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (f"%{search_query}%", f"%{search_query}%", page_size, offset))
    else:
        drawings = db.query(
            """
            SELECT id, username, title, payload
            FROM drawings
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (page_size, offset))
        
    result = []
    
    for row in drawings:
        d = dict(row)
        likes = db.query(
            """
            SELECT username 
            FROM likes
            WHERE drawing_id = ?
            ORDER BY id ASC
            """,
            (d["id"],))
        
        d['like_users'] = [l['username'] for l in likes]
        result.append(d)
        
    return result


def drawing_edit_title(drawing_id, username, new_title):
    db.execute(
        """
        UPDATE drawings
        SET title = ?
        WHERE id = ?
        AND username = ?
        """,
        (new_title, drawing_id, username))


def drawing_delete(drawing_id, username):
    db.execute(
        """
        DELETE FROM drawings
        WHERE id = ?
        AND username = ?
        """,
        (drawing_id, username))


def drawing_like(drawing_id, username):
    existing = db.query(
        """
        SELECT id
        FROM likes
        WHERE drawing_id = ? 
        AND username = ?
        """,
        (drawing_id, username))
    
    if existing:
        db.execute(
            """
            DELETE FROM likes
            WHERE drawing_id = ?
            AND username = ?
            """,
            (drawing_id, username))
    else:
        db.execute(
            "INSERT INTO likes (drawing_id, username) VALUES (?, ?)",
            (drawing_id, username))


def drawings_count(search_query=""):
    if search_query:
        result = db.query(
            """
            SELECT COUNT(id) AS count
            FROM drawings 
            WHERE title LIKE ?
            OR username LIKE ? 
            """,
            (f"%{search_query}%", f"%{search_query}%"))
    else:
        result = db.query("SELECT COUNT(id) AS count FROM drawings")
    
    return result[0]["count"]
