from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = "school.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        roll = request.form["roll"]
        name = request.form["name"]
        clas = request.form["class"]
        section = request.form["section"]

        cursor.execute(
            "INSERT INTO students (roll, name, class, section) VALUES (?, ?, ?, ?)",
            (roll, name, clas, section),
        )
        conn.commit()
        return redirect(url_for("index"))

    search = request.args.get("search", "")
    if search:
        cursor.execute(
            "SELECT * FROM students WHERE roll LIKE ? OR name LIKE ?",
            (f"%{search}%", f"%{search}%"),
        )
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)


@app.route("/delete/<int:roll>")
def delete(roll):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/edit/<int:roll>", methods=["POST"])
def edit(roll):
    name = request.form["name"]
    clas = request.form["class"]
    section = request.form["section"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name=?, class=?, section=? WHERE roll=?",
        (name, clas, section, roll),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
