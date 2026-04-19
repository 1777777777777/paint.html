import db

def draw_save(username, title, payload):
    db.execute("INSERT INTO drawings (username, title, payload) VALUES (?, ?, ?)", (username, title, payload))

def drawings_search(search_query=""):
    if search_query:
        drawings = db.query("""
            SELECT * FROM drawings 
            WHERE title LIKE ? OR username LIKE ? 
            ORDER BY id DESC
        """, (f"%{search_query}%", f"%{search_query}%"))
    
    else:
        drawings = db.query("SELECT * FROM drawings ORDER BY id DESC")
        
    result = []
    for row in drawings:
        d = dict(row)
        likes = db.query("SELECT username FROM likes WHERE drawing_id = ? ORDER BY id ASC", (d['id'],))
        d['like_users'] = [l['username'] for l in likes]
        result.append(d)
        
    return result


def drawing_edit_title(drawing_id, username, new_title):
    db.execute("UPDATE drawings SET title = ? WHERE id = ? AND username = ?", (new_title, drawing_id, username))

def drawing_delete(drawing_id, username):
    db.execute("DELETE FROM drawings WHERE id = ? AND username = ?", (drawing_id, username))

def drawing_like(drawing_id, username):
    existing = db.query("""SELECT id
                        FROM likes
                        WHERE drawing_id = ? 
                        AND username = ?""", (drawing_id, username))
    if existing:
        db.execute("DELETE FROM likes WHERE drawing_id = ? AND username = ?", (drawing_id, username))
    else:
        db.execute("INSERT INTO likes (drawing_id, username) VALUES (?, ?)", (drawing_id, username))

