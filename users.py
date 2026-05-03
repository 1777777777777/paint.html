import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import db


def create_user(username, password):
    password_hash = generate_password_hash(password)
    try:
        db.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            [username, password_hash]
        )
        return True
    except sqlite3.IntegrityError:
        return False


def check_login(username, password):
    result = db.query(
        """
        SELECT password
        FROM users
        WHERE username = ?
        """,
        [username]
    )

    if len(result) == 1:
        password_hash = result[0]["password"]
        if check_password_hash(password_hash, password):
            return True

    return False


def get_user_bio(username):
    result = db.query(
        """
        SELECT bio
        FROM users
        WHERE username = ?
        """,
        [username]
    )
    if result and len(result) > 0:
        return result[0]["bio"]
    return None


def update_user_bio(username, bio):
    db.execute(
        """
        UPDATE users
        SET bio = ?
        WHERE username = ?
        """,
        [bio, username]
    )


def get_user_stats(username):
    stats = {}

    drawings = db.query(
        """
        SELECT COUNT(*) AS c
        FROM drawings
        WHERE username = ?
        """,
        [username]
    )
    stats["drawings_count"] = drawings[0]["c"] if drawings else 0

    likes_given = db.query(
        """
        SELECT COUNT(*) AS c
        FROM likes
        WHERE username = ?
        """,
        [username]
    )
    stats["likes_given"] = likes_given[0]["c"] if likes_given else 0

    likes_received = db.query(
        """
        SELECT COUNT(*) AS c
        FROM likes
        JOIN drawings ON likes.drawing_id = drawings.id
        WHERE drawings.username = ?
        """,
        [username]
    )
    stats["likes_received"] = likes_received[0]["c"] if likes_received else 0

    return stats


def check_user_exists(username):
    user_check = db.query(
        """
        SELECT username
        FROM users
        WHERE username = ?
        """,
        [username]
    )
    return bool(user_check)
