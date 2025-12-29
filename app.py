from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB_NAME = "school.db"


def get_db():
    return sqlite3.connect(DB_NAME)


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cursor = conn.cursor()

    # ADD STUDENT
    if request.method == "POST":
        roll = request.form["roll"]
        name = request.form["name"]
        class_ = request.form["class"]
        section = request.form["section"]

        cursor.execute(
            "INSERT INTO students (roll, name, class, section) VALUES (?, ?, ?, ?)",
            (roll, name, class_, section),
        )
        conn.commit()
        conn.close()
        return redirect("/")

    # SEARCH
    search = request.args.get("search")
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


@app.route("/edit/<int:roll>", methods=["GET", "POST"])
def edit_student(roll):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        new_roll = request.form["roll"]
        name = request.form["name"]
        class_ = request.form["class"]
        section = request.form["section"]

        cursor.execute(
            "UPDATE students SET roll=?, name=?, class=?, section=? WHERE roll=?",
            (new_roll, name, class_, section, roll),
        )
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
    student = cursor.fetchone()
    conn.close()
    return render_template("edit.html", student=student)


@app.route("/delete/<int:roll>")
def delete_student(roll):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)