from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Создали объект класса flask, для работы с веб-приложением (передаем базовый аргумент __name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/notes")
def notes():
    all_notes = Note.query.all()
    return render_template("notes.html", notes=all_notes)

@app.route("/add_note", methods=["POST"])
def add_note():
    title = request.form.get("title")
    text = request.form.get("text")
    
    if title and text:
        new_note = Note(title=title, text=text)
        db.session.add(new_note)
        db.session.commit()
    
    return redirect(url_for("notes"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



















