import db


def draw_save(username, title, payload, tags=None):
    db.execute(
               "INSERT INTO drawings (username, title, payload) VALUES (?, ?, ?)",
               (username, title, payload))
    
    if tags:
        drawing_id = db.last_insert_id()
        for tag in tags:
            db.execute("INSERT INTO drawing_tags (drawing_id, tag) VALUES (?, ?)", (drawing_id, tag))


def drawings_search(search_query="", page=1, page_size=10, tag_query=None):
    if tag_query is None:
        tag_query = []
        
    offset = (page - 1) * page_size
    
    query = ["SELECT id, username, title, payload FROM drawings"]
    wheres = []
    variables = []
    

    if search_query:
        wheres.append("(title LIKE ? OR username LIKE ?)")
        variables.append(f"%{search_query}%")
        variables.append(f"%{search_query}%")
        
    for tag in tag_query:
        wheres.append("id IN (SELECT drawing_id FROM drawing_tags WHERE tag = ?)")
        variables.append(tag)
        
    if wheres:
        query.append("WHERE " + " AND ".join(wheres))
        
    query.append("ORDER BY id DESC LIMIT ? OFFSET ?")
    variables.append(page_size)
    variables.append(offset)
    
    drawings = db.query(" ".join(query), tuple(variables))
        
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
        
        d["like_users"] = [l["username"] for l in likes]

        tags = db.query(
            """
            SELECT tag
            FROM drawing_tags
            WHERE drawing_id = ?
            """,
            (d["id"],))
        d["tags"] = [t["tag"] for t in tags]

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
        DELETE FROM drawing_tags
        WHERE drawing_id IN (
            SELECT id FROM drawings WHERE id = ? AND username = ?
        )
        """,
        (drawing_id, username))
        
    db.execute(
        """
        DELETE FROM likes
        WHERE drawing_id IN (
            SELECT id FROM drawings WHERE id = ? AND username = ?
        )
        """,
        (drawing_id, username))
        
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


def drawings_count(search_query="", tag_query=None):
    if tag_query is None:
        tag_query = []
        
    query = ["SELECT COUNT(id) AS count FROM drawings"]
    wheres = []
    variables = []
    
    if search_query:
        wheres.append("(title LIKE ? OR username LIKE ?)")
        variables.append(f"%{search_query}%")
        variables.append(f"%{search_query}%")
        
    for tag in tag_query:
        wheres.append("id IN (SELECT drawing_id FROM drawing_tags WHERE tag = ?)")
        variables.append(tag)
        
    if wheres:
        query.append("WHERE " + " AND ".join(wheres))
        
    result = db.query(" ".join(query), tuple(variables))
    
    return result[0]["count"]
