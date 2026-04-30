from flask import Flask, render_template, request, redirect, session, flash, abort
import sqlite3
import secrets
import config
import db
import users
import drawings
from draw import ffloodfill, GRID_SIZE, TOTAL_PIXELS, ITERATIONS
import math

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session.get("csrf_token"):
        abort(403)


def gallery_redirect(drawing_id =None):
    referrer = request.referrer or "/gallery"

    if "#" in referrer:
        referrer = referrer.split("#")[0]
    
    if drawing_id is not None:
        return redirect(f"{referrer}#popup-{drawing_id}")
    else:
        return redirect(referrer)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_confirm = request.form.get("password_confirm")

        if password != password_confirm:
            flash("Passwords do not match.")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        # to whom it may concern: the course example leaked db stuff into routing here by the way for some reason
        if users.create_user(username, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
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
            session["csrf_token"] = secrets.token_hex(16)
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
        check_csrf()

        raw_payload = request.form.get("payload", "")
        title = request.form.get("title") or "untitled"

        if len(title) > 12:
            abort(403)

        username = session["username"]

        if raw_payload:
            final_payload = ffloodfill(raw_payload, GRID_SIZE, GRID_SIZE)
            drawings.draw_save(username, title, final_payload)

        return redirect("/gallery")
        
    return render_template("draw.html", grid_size=GRID_SIZE, total_pixels=TOTAL_PIXELS, iterations=ITERATIONS)


@app.route("/gallery")
@app.route("/gallery/<int:page>")
def gallery(page=1):
    if "username" not in session:
        return redirect("/login")

    search_query = request.args.get("q", "")
    page_size = 12
    
    total_count = drawings.drawings_count(search_query)
    page_count = math.ceil(total_count / page_size)
    page_count = max(page_count, 1)

    query_string = f"?q={search_query}" if search_query else ""

    if page < 1:
        return redirect(f"/gallery/1{query_string}")
    if page > page_count:
        return redirect(f"/gallery/{page_count}{query_string}")
    
    drawings_list = drawings.drawings_search(search_query, page, page_size)
        
    return render_template("gallery.html", drawings=drawings_list, search_query=search_query, page=page, page_count=page_count)


@app.route("/edit_title/<int:drawing_id>", methods=["POST"])
def edit_title(drawing_id):
    if "username" not in session:
        return redirect("/login")

    check_csrf()

    new_title = request.form.get("title")
    username = session["username"]

    if not new_title or len(new_title) > 12:
        abort(403)

    drawings.drawing_edit_title(drawing_id, username, new_title)

    return gallery_redirect(drawing_id)


@app.route("/delete/<int:drawing_id>", methods=["POST"])
def delete_drawing(drawing_id):
    if "username" not in session:
        return redirect("/login")

    check_csrf()
    username = session["username"]

    drawings.drawing_delete(drawing_id, username)

    return gallery_redirect()


@app.route("/like/<int:drawing_id>", methods=["POST"])
def like_drawing(drawing_id):
    if "username" not in session:
        return redirect("/login")

    check_csrf()
    username = session["username"]

    drawings.drawing_like(drawing_id, username)

    return gallery_redirect(drawing_id)


@app.route("/profile")
def profile():
    session.pop("username", None)
    return render_template("profile.html"), 403


@app.teardown_appcontext
def teardown_db(exception):
    db.close_connection(exception)




app.run()
