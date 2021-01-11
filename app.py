# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
from flask import request
import flask_sqlalchemy
import flask_socketio
import chatbot
from chatbot import KEY_IS_BOT, KEY_MESSAGE


MESSAGES_RECEIVED_CHANNEL = "messages received"
USERS_RECEIVED_CHANNEL = "users received"
COUNT_RECEIVED_CHANNEL = "count received"

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

lst = {}
all_users = []
user_count = len(lst)
all_messages = []
output = ""

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

database_uri = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri


db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

import models

# get command "help, about, date, funtranslate, random joke"
# def get_command(data):

#    words = data['message'].split()
#    print("_",words)

# chat = []
#    if(words[0] == "!!"):
#        out = chatbot.switch(words)
# chat.append(out)
#        return out


def emit_all_users(text):
    # all_users = []
    for u in lst:
        all_users.append(lst[u])
    # chat user
    socketio.emit(text, {"all_users": all_users})


# user count
def emit_user_count(text):
    user_count = len(lst)

    socketio.emit(text, {"user_count": user_count})


def emit_all_messages(text):

    # chat message in db
    all_messages = [
        db_message.message for db_message in db.session.query(models.Messages).all()
    ]

    # chat message
    socketio.emit(text, {"allMessages": all_messages})


@socketio.on("connect")
def on_connect():
    print("Someone connected!")
    socketio.emit("connected", {"test": "connected"})

    emit_all_users(USERS_RECEIVED_CHANNEL)
    emit_user_count(COUNT_RECEIVED_CHANNEL)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@socketio.on("disconnect")
def on_disconnect():
    print("Someone disconnected!")
    del lst[request.sid]

    emit_all_users(USERS_RECEIVED_CHANNEL)
    emit_user_count(COUNT_RECEIVED_CHANNEL)


@socketio.on("new google user")
def on_login(data):
    print("New login from user:", data["user"])
    lst[request.sid] = data["user"]

    try:
        db.session.add(models.user_info(data["email"], data["user"], data["picture"]))
        db.session.commit()
    except Exception:
        db.session.rollback()
        print("User already in db")

    emit_all_users(USERS_RECEIVED_CHANNEL)
    emit_user_count(COUNT_RECEIVED_CHANNEL)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@socketio.on("new message input")
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    output = chatbot.switch(data["message"])
    print(output)
    try:
        db.session.add(
            models.Messages(
                lst[request.sid] + ": " + data["message"],
                db.session.query(models.user_info.id)
                .filter(models.user_info.user == lst[request.sid])
                .first()
                .id,
            )
        )
        db.session.commit()
        if output[KEY_IS_BOT] == True:
            db.session.add(
                models.Messages(
                    "ChatBot: " + output[KEY_MESSAGE],
                    db.session.query(models.user_info.id)
                    .filter(models.user_info.user == "Chatbot")
                    .first()
                    .id,
                )
            )
            db.session.commit()

    except Exception:
        db.session.rollback()
        db.session.add(
            models.Messages(
                "ERROR: User "
                + lst[request.sid]
                + "'s message has failed to send! Please try again!",
                db.session.query(models.user_info.id)
                .filter(models.user_info.user == lst[request.sid])
                .first()
                .id,
            )
        )
        db.session.commit()

    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


# @socketio.on('Chatbot Info')
# def chatbot_info(data):
#    print("Chatbot information:", data)

#    try:
#        db.session.add(models.user_info('chatbot@gmail.com', 'Chatbot', 'https://www.kunocreative.com/hubfs/Chatbot-evolution-1.png'));
#        db.session.commit();
#    except Exception:
#        db.session.rollback();
#        print("User already in db")


@app.route("/")
def index():

    try:
        db.session.add(
            models.user_info(
                "chatbot@gmail.com",
                "Chatbot",
                "https://www.kunocreative.com/hubfs/Chatbot-evolution-1.png",
            )
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        print("User already in db")

    emit_all_users(USERS_RECEIVED_CHANNEL)
    emit_user_count(COUNT_RECEIVED_CHANNEL)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
