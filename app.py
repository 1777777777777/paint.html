from flask import Flask, render_template, request, redirect, session
import sqlite3
import config
from db import get_connection
from draw import ffloodfill, GRID_SIZE, TOTAL_PIXELS, ITERATIONS

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return render_template("register.html")

        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        
        session["username"] = username
        return redirect("/")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None) 
    return redirect("/login")


@app.route("/", methods=["GET", "POST"])
def draw():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        raw_payload = request.form.get("payload", "")
        title = request.form.get("title", "untitled")
        username = session["username"] 

        if raw_payload:
            final_payload = ffloodfill(raw_payload, GRID_SIZE, GRID_SIZE)
            conn = get_connection()
            conn.execute("INSERT INTO drawings (username, title, payload) VALUES (?, ?, ?)", (username, title, final_payload))
            conn.commit()
            conn.close()

        return redirect("/gallery")
        
    return render_template("draw.html", grid_size=GRID_SIZE, total_pixels=TOTAL_PIXELS, iterations=ITERATIONS)


@app.route("/gallery")
def gallery():
    if "username" not in session:
        return redirect("/login")

    search_query = request.args.get("q", "")

    conn = get_connection()
    conn.row_factory = sqlite3.Row 
    
    if search_query:
        cursor = conn.execute('''
            SELECT * FROM drawings 
            WHERE title LIKE ? OR username LIKE ? 
            ORDER BY id DESC
        ''', (f"%{search_query}%", f"%{search_query}%"))

    else:
        cursor = conn.execute("SELECT * FROM drawings ORDER BY id DESC")
        
    drawings = cursor.fetchall()
    conn.close()

    return render_template("gallery.html", drawings=drawings, search_query=search_query)


@app.route("/edit_title/<int:drawing_id>", methods=["POST"])
def edit_title(drawing_id):
    if "username" not in session:
        return redirect("/login")

    new_title = request.form.get("title")
    username = session["username"]

    if new_title:
        conn = get_connection()
        conn.execute("UPDATE drawings SET title = ? WHERE id = ? AND username = ?", (new_title, drawing_id, username))
        conn.commit()
        conn.close()

    return redirect(request.referrer or "/gallery")


@app.route("/delete/<int:drawing_id>", methods=["POST"])
def delete_drawing(drawing_id):
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = get_connection()
    conn.execute("DELETE FROM drawings WHERE id = ? AND username = ?", (drawing_id, username))
    conn.commit()
    conn.close()

    return redirect(request.referrer or "/gallery")


@app.route("/profile")
def profile():
    session.pop("username", None)
    return render_template("profile.html"), 403




app.run()
