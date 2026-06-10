from flask import Flask, render_template, request, redirect
import sqlite3
import os
from werkzeug.utils import secure_filename
import sqlite3

# Créer la base de données si elle n'existe pas
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()
app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


@app.route("/")
def home():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    products = conn.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        products=products
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        name = request.form["name"]

        description = request.form.get(
            "description",
            ""
        )

        price = request.form["price"]

        category = request.form["category"]

        image_file = request.files["image"]

        filename = ""

        if image_file and image_file.filename:

            filename = secure_filename(
                image_file.filename
            )

            image_file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        conn = sqlite3.connect("database.db")

        conn.execute(
            """
            INSERT INTO products
            (name, description, price, category, image)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                description,
                price,
                category,
                filename
            )
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("admin.html")


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("database.db")

    conn.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)