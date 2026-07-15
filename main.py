
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Создали объект класса flask, для работы с веб-приложением (передаем базовый аргумент __name__)
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)



















