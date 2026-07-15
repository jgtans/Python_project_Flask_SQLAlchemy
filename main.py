
from flask import Flask, render_template, request, redirect, url_for

# Создали объект класса flask, для работы с веб-приложением (передаем базовый аргумент __name__)
app = Flask(__name__)

notes_db = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/notes")
def notes():
    return render_template("notes.html", notes=notes_db)

@app.route("/prog")
def prog():
    return render_template("programmer_diary.html")

@app.route("/add_note", methods=["POST"])
def add_note():
    title = request.form.get("title")
    text = request.form.get("text")

    if title and text:
        notes_db[title] = text

    return redirect(url_for("notes"))

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    return f"Привет {name}"

if __name__ == "__main__":
    app.run(debug=True)



















