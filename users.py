import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (?, ?)"

    try:
        db.execute(sql, [username, password_hash])
        return True
    except sqlite3.IntegrityError:
        return False

def check_login(username, password):
    sql = "SELECT password FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        password_hash = result[0]["password"]
        if check_password_hash(password_hash, password):
            return True

    return False

def get_user_bio(username):
    sql = "SELECT bio FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if result and len(result) > 0:
        return result[0]["bio"]
    return None

def update_user_bio(username, bio):
    sql = "UPDATE users SET bio = ? WHERE username = ?"
    db.execute(sql, [bio, username])

def get_user_stats(username):
    stats = {}
    
    drawings = db.query("SELECT COUNT(*) as c FROM drawings WHERE username = ?", [username])
    stats["drawings_count"] = drawings[0]["c"] if drawings else 0
    
    likes_given = db.query("SELECT COUNT(*) as c FROM likes WHERE username = ?", [username])
    stats["likes_given"] = likes_given[0]["c"] if likes_given else 0
    
    likes_received = db.query("""
        SELECT COUNT(*) as c 
        FROM likes 
        JOIN drawings ON likes.drawing_id = drawings.id 
        WHERE drawings.username = ?
    """, [username])
    stats["likes_received"] = likes_received[0]["c"] if likes_received else 0
    
    return stats
