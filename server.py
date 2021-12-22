from flask import Flask, request, render_template
import time  # подключить модуль "time"
from datetime import datetime  # подключаем модуль datetime и из него берем него класс datetime (одноименный)
import json

messages_file = "./data/messages.json"
json_file = open(messages_file, "rb")  # Пока что только читаем файл
data = json.load(json_file)
if "all_messages" not in data:
    print(f"Can't find the key 'all_messages' in {messages_file}")
    exit(1)

all_messages = data["all_messages"]  # Загружаем данные из файла по ключу и присваиваем переменной


def save_messages():
    messages = {
        "all_messages": all_messages
    }
    json_file_messages = open(messages_file, "w")  # Открываем файл для записи
    json.dump(messages, json_file_messages)  # Пишем структуру в файл


app = Flask(__name__)


def time_format(t):
    return str(datetime.fromtimestamp(t))


# all_messages = [  # В этом списке хранятся все сообщения чата
#     {  # каждое сообщение это словарь с полями text, name и time
#         "text": "test message",
#         "name": "Mike",
#         "time": time_format(time.time())
#     },
#     {
#         "text": "lorem redeemer",
#         "name": "Paul",
#         "time": time_format(time.time())
#     },
#     {
#         "text": "tester pester",
#         "name": "Tester",
#         "time": time_format(time.time())
#     }
#
# ]

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
    if len(name) < 3 or len(name) > 100:
        return "ERROR"

    # Проверки на длину сообщения
    if len(text) < 1 or len(text) > 3000:
        return "ERROR"

    message = {
        "text": text,
        "name": name,
        "time": time_format(time.time()),
    }

    all_messages.append(message)
    save_messages()
    return "OK"


app.run(host="0.0.0.0", port=80)
