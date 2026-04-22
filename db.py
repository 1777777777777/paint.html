import sqlite3
from flask import g


def get_connection():
    if "db" not in g:
        conn = sqlite3.connect('database.db')
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        g.db = conn

    return g.db


def execute(sql, params=[]):
    conn = get_connection()
    with conn:
        result = conn.execute(sql, params)
        g.last_insert_id = result.lastrowid


def query(sql, params=[]):
    conn = get_connection()
    with conn:
        result = conn.execute(sql, params).fetchall()
        return result


def last_insert_id():
    return g.last_insert_id


def close_connection(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


