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
