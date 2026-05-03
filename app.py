from flask import Flask, render_template, request, redirect, session, flash, abort
import sqlite3
import secrets
import re
import config
import db
import users
import drawings
from draw import ffloodfill, GRID_SIZE, TOTAL_PIXELS, ITERATIONS
import math
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    if not content:
        return ""
    
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

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
        password_confirm = request.form["password_confirm"]

        if not username:
            flash("Username cannot be empty or only spaces.")
            return render_template("register.html")

        if not re.match(r"^[a-z0-9._-]+$", username):
            flash("Username can only contain a-z, 0-9, ., -, _")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        if len(username) > 12:
            abort(403)

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
        title = request.form.get("title", "").strip() or "untitled"
        tags = request.form.getlist("tags")

        if len(title) > 12:
            abort(403)

        username = session["username"]
        
        db_tags = db.query("SELECT name FROM tags")
        all_tags = [t["name"] for t in db_tags]
        valid_tags = [tag for tag in tags if tag in all_tags]

        if raw_payload:
            final_payload = ffloodfill(raw_payload, GRID_SIZE, GRID_SIZE)
            drawings.draw_save(username, title, final_payload, tags=valid_tags)

        return redirect("/gallery")
        
    barcode_vis_id = secrets.token_hex(4)
    db_tags = db.query("SELECT name FROM tags")
    all_tags = [t["name"] for t in db_tags]
    return render_template("draw.html", grid_size=GRID_SIZE, total_pixels=TOTAL_PIXELS, iterations=ITERATIONS, barcode_vis_id=barcode_vis_id, all_tags=all_tags)


@app.route("/gallery")
@app.route("/gallery/<int:page>")
def gallery(page=1):
    if "username" not in session:
        return redirect("/login")

    search_query = request.args.get("q", "")
    tag_query = request.args.getlist("tag")
    page_size = 12
    
    total_count = drawings.drawings_count(search_query, tag_query)
    page_count = math.ceil(total_count / page_size)
    page_count = max(page_count, 1)

    if search_query != "":
        query_string = "?q=" + search_query
    else:
        query_string = ""
        
    for t in tag_query:
        if query_string != "":
            query_string = query_string + "&tag=" + t
        else:
            query_string = "?tag=" + t

    if page < 1:
        return redirect(f"/gallery/1{query_string}")
    if page > page_count:
        return redirect(f"/gallery/{page_count}{query_string}")
    
    drawings_list = drawings.drawings_search(search_query, page, page_size, tag_query)
    
    db_tags = db.query("SELECT name FROM tags")
    all_tags = [t["name"] for t in db_tags]
        
    return render_template("gallery.html", drawings=drawings_list, search_query=search_query, tag_query=tag_query, page=page, page_count=page_count, all_tags=all_tags)


@app.route("/edit_info/<int:drawing_id>", methods=["POST"])
def edit_info(drawing_id):
    if "username" not in session:
        return redirect("/login")

    check_csrf()

    new_title = request.form.get("title", "").strip() or "untitled"
    tags = request.form.getlist("tags")
    username = session["username"]

    if len(new_title) > 12:
        abort(403)

    db_tags = db.query("SELECT name FROM tags")
    all_tags = [t["name"] for t in db_tags]
    valid_tags = [tag for tag in tags if tag in all_tags]

    drawings.drawing_edit_info(drawing_id, username, new_title, valid_tags)

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


@app.route("/profile/<username>/bio", methods=["POST"])
def update_bio(username):
    if "username" not in session or session["username"] != username:
        return redirect("/login")
        
    bio = request.form.get("bio", "").strip()
    if len(bio) > 255:
        abort(403)
        
    users.update_user_bio(username, bio)
    return redirect(f"/profile/{username}")

@app.route("/profile")
@app.route("/profile/<username>")
@app.route("/profile/<username>/<int:page>")
def profile(username=None, page=1):
    if "username" not in session:
        return redirect("/login")

    if username is None:
        username = session["username"]

    user_check = db.query("SELECT username FROM users WHERE username = ?", [username])
    if not user_check:
        abort(404)

    stats = users.get_user_stats(username)
    bio = users.get_user_bio(username)
    
    edit_bio = request.args.get("edit_bio") == "1" and username == session.get("username")
    
    page_size = 12
    total_count = db.query("SELECT COUNT(id) as count FROM drawings WHERE username = ?", [username])[0]["count"]
    page_count = math.ceil(total_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/profile/{username}/1")
    if page > page_count:
        return redirect(f"/profile/{username}/{page_count}")
        
    offset = (page - 1) * page_size

    user_drawings_raw = db.query("SELECT id, username, title, payload FROM drawings WHERE username = ? ORDER BY id DESC LIMIT ? OFFSET ?", [username, page_size, offset])
    user_drawings = []
    for row in user_drawings_raw:
        d = dict(row)
        likes = db.query("SELECT username FROM likes WHERE drawing_id = ? ORDER BY id ASC", (d["id"],))
        d["like_users"] = [l["username"] for l in likes]
        tags = db.query("SELECT tag FROM drawing_tags WHERE drawing_id = ?", (d["id"],))
        d["tags"] = [t["tag"] for t in tags]
        user_drawings.append(d)

    db_tags = db.query("SELECT name FROM tags")
    all_tags = [t["name"] for t in db_tags]
    
    return render_template("profile.html", profile_user=username, stats=stats, bio=bio, edit_bio=edit_bio, drawings=user_drawings, all_tags=all_tags, page=page, page_count=page_count)


@app.teardown_appcontext
def teardown_db(exception):
    db.close_connection(exception)




app.run()
