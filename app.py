from flask import Flask, render_template, request, redirect, session
import sqlite3
import sys

app = Flask(__name__)
app.secret_key = "12345" 

GRID_SIZE = 10
TOTAL_PIXELS = GRID_SIZE * GRID_SIZE
ITERATIONS = 55

if "--iterations" in sys.argv:
    try:
        idx = sys.argv.index("--iterations")
        ITERATIONS = int(sys.argv[idx + 1])
    except (ValueError, IndexError):
        pass

conn = sqlite3.connect('database.db')
with open('schema.sql', 'r') as f:
    conn.executescript(f.read())
conn.commit()
conn.close()


def ffloodfill (raw_payload, width, height):
    grid = [i for i in raw_payload if i in ["0", "1", "b"]]
    queue = [i for i, j in enumerate(grid) if j == 'b']
    
    while queue:
        near = []
        curr = queue.pop(0)
        row = curr // width
        col = curr % width

        if row > 0:
            near.append(curr - width)
        if row < height - 1:
            near.append(curr + width)
        if col > 0:
            near.append(curr - 1)
        if col < width - 1:
            near.append(curr + 1)

        for n in near:
            if grid[n] == "0":
                grid[n] = "b"

                queue.append(n)
                

    return "".join(grid).replace("b", "1")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
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

        conn = sqlite3.connect("database.db")
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
            conn = sqlite3.connect("database.db")
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

    conn = sqlite3.connect("database.db")
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
        conn = sqlite3.connect("database.db")
        conn.execute("UPDATE drawings SET title = ? WHERE id = ? AND username = ?", (new_title, drawing_id, username))
        conn.commit()
        conn.close()

    return redirect(request.referrer or "/gallery")


@app.route("/delete/<int:drawing_id>", methods=["POST"])
def delete_drawing(drawing_id):
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM drawings WHERE id = ? AND username = ?", (drawing_id, username))
    conn.commit()
    conn.close()

    return redirect(request.referrer or "/gallery")


@app.route("/profile")
def profile():
    session.pop("username", None)
    return render_template("profile.html"), 403




app.run()
