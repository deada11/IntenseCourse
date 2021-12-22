from flask import Flask, request, render_template
import time  # подключить модуль "time"
from datetime import datetime  # подключаем модуль datetime и из него берем него класс datetime (одноименный)

app = Flask(__name__)


def time_format(t):
    return datetime.fromtimestamp(t)


all_messages = [  # В этом списке хранятся все сообщения чата
    {  # каждое сообщение это словарь с полями text, name и time
        "text": "test message",
        "name": "Mike",
        "time": time_format(time.time())
    },
    {
        "text": "lorem redeemer",
        "name": "Paul",
        "time": time_format(time.time())
    },
    {
        "text": "tester pester",
        "name": "Tester",
        "time": time_format(time.time())
    }

]


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/")
def root():
    return "Test page"


@app.route("/get_messages")  # А тут метод GET срабатывает
def get_messages():
    return {"messages": all_messages}


@app.route("/send")  # Запрос на изменение данных
def send_message():

    name = request.args['name']
    text = request.args['text']

    # Проверки на длину имени
    if len(name) < 3:
        return "Имя пользователя не может быть короче 3 символов"
    elif len(name) > 100:
        return "Имя пользователя не может быть длиннее 100 символов"

    # Проверки на длину сообщения
    if len(text) < 1:
        return "Текст сообщения не может быть пустым"
    elif len(text) > 3000:
        return "Текст сообщения не может превышать 3000 символов"

    message = {
        "text": text,
        "name": name,
        "time": time_format(time.time()),
    }

    all_messages.append(message)
    return "OK"


app.run()
