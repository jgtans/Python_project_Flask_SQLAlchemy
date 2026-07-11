from flask import Flask, render_template

# Создали объект класса flask, для работы с веб-приложением (передаем базовый аргумент __name__)
app = Flask(__name__)

# Создаем базовый маршрут, для проверки работы нашего сайта
@app.route("/") # Декоратор
def index():
    # при инициализации функции индекс, во время ретурн тригерется и возвращает index.html
    return render_template("404.html"), 404

@app.route("/hello")
def hello():
    return "Hello"

# Вводим любое имя
@app.route("/hello/<name>")
def greetings(name):
    return f"Hello, {name}"

# Обработка ошибок
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", 404)

# С помощью этой строчки проверяем, что этот файл является основным
if __name__ == "__main__":
    # В том случае если наш файл основной, мы хотим запустить приложение, а debug=True - покажет нам ошибку, но не закроет сайт
    app.run(debug=True)
















