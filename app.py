from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import config
import db
import users
from draw import ffloodfill, GRID_SIZE, TOTAL_PIXELS, ITERATIONS

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.create_user(username, password):
            session["username"] = username
            return redirect("/")
        else:
            flash("Username is already taken.")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.check_login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            flash("Invalid username or password")
            filled = {"username": username}
            return render_template("login.html", filled=filled)

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
            db.execute("INSERT INTO drawings (username, title, payload) VALUES (?, ?, ?)", (username, title, final_payload))

        return redirect("/gallery")
        
    return render_template("draw.html", grid_size=GRID_SIZE, total_pixels=TOTAL_PIXELS, iterations=ITERATIONS)


@app.route("/gallery")
def gallery():
    if "username" not in session:
        return redirect("/login")

    search_query = request.args.get("q", "")
    
    if search_query:
        drawings = db.query('''
            SELECT * FROM drawings 
            WHERE title LIKE ? OR username LIKE ? 
            ORDER BY id DESC
        ''', (f"%{search_query}%", f"%{search_query}%"))

    else:
        drawings = db.query("SELECT * FROM drawings ORDER BY id DESC")
        
        
    return render_template("gallery.html", drawings=drawings, search_query=search_query)


@app.route("/edit_title/<int:drawing_id>", methods=["POST"])
def edit_title(drawing_id):
    if "username" not in session:
        return redirect("/login")

    new_title = request.form.get("title")
    username = session["username"]

    if new_title:
        db.execute("UPDATE drawings SET title = ? WHERE id = ? AND username = ?", (new_title, drawing_id, username))

    return redirect(request.referrer or "/gallery")


@app.route("/delete/<int:drawing_id>", methods=["POST"])
def delete_drawing(drawing_id):
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    db.execute("DELETE FROM drawings WHERE id = ? AND username = ?", (drawing_id, username))

    return redirect(request.referrer or "/gallery")


@app.route("/profile")
def profile():
    session.pop("username", None)
    return render_template("profile.html"), 403




app.run()
