from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db()

    data = conn.execute("SELECT * FROM Designer").fetchall()

    total_team = conn.execute(
        "SELECT COUNT(*) FROM Designer"
    ).fetchone()[0]

    total_document_control = conn.execute(
        "SELECT COUNT(*) FROM Designer WHERE jabatan = 'Document Control'"
    ).fetchone()[0]

    total_designer = total_team - total_document_control

    conn.close()

    return render_template(
        "index.html",
        data=data,
        total_team=total_team,
        total_designer=total_designer,
        total_document_control=total_document_control
    )

@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        nama = request.form["nama"]
        jabatan = request.form["jabatan"]
        jobdesk = request.form["jobdesk"]

        conn = get_db()

        conn.execute(
            "INSERT INTO Designer (nama, jabatan, Jobdesk) VALUES (?, ?, ?)",
            (nama, jabatan, jobdesk)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("tambah.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()

    if request.method == "POST":
        nama = request.form["nama"]
        jabatan = request.form["jabatan"]
        jobdesk = request.form["jobdesk"]

        conn.execute(
            """
            UPDATE Designer
            SET nama = ?, jabatan = ?, Jobdesk = ?
            WHERE id = ?
            """,
            (nama, jabatan, jobdesk, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    data = conn.execute(
        "SELECT * FROM Designer WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit.html", data=data)
@app.route("/hapus/<int:id>")
def hapus(id):
    conn = get_db()

    conn.execute(
        "DELETE FROM Designer WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)