import os

from flask import Flask, render_template,session,redirect,url_for,request,jsonify
from flask_socketio import SocketIO, emit
from flask_session import Session
from chat import Chat
from channel import Channel
from message import Message
import pickle
import json
from flask_restplus import fields, marshal


app = Flask(__name__)
app.config["SECRET_KEY"] = "cdc&^^*&^876687GHJg"
socketio = SocketIO(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"


Session(app)

channel_list =[]

channel_list.append("Default");
channel_list.append("Private");
channel_list.append("Public");

messages = []

resource_fields = {'nickname': fields.String, "channel": fields.String, "message": fields.String, "date": fields.Date, "hours": fields.String}


@app.route("/")
def index():
    if session.get('logged_in') != True:
        return redirect(url_for("login"))
    return render_template("index.html", nickname =  session.get('nickname'), channels= channel_list)

@app.route("/chat-details/<string:channel_name>")
def chat_details(channel_name):
    """Load messages from chat"""
    if channel_name in channel_list:
        return render_template("chat_details.html", nickname =  session.get('nickname'), channels= channel_list, current_channel= channel_name,messages= get_messsages_by_channel(channel_name))
    return redirect(url_for("index"))

@socketio.on('add-channel')
def add_channel(data):
    """ Add Channel to Channel List"""
    channel_name =  data["channel_name"]
    if channel_name != None:
        channel_list.append(channel_name);
    emit("added-new-channel", {"channel_list": channel_list }, broadcast=True)
    return redirect(url_for("index"))

@socketio.on('send-message')
def send_message(data):
    """ Add Channel to Channel List"""
    message = data["message"]
    channel = data["channel"]
    nickname = data["nickname"]
    if channel != None and message != None and nickname != None:
        message = Message(nickname = nickname , channel = channel, message = message)
        messages.append(message)
        emit("new-message", {"message": marshal(message,resource_fields) }, broadcast=True)
    return redirect(url_for("index"))


@app.route("/login",methods=['post','get'])
def login():
    """Register a Username to enter to the Rooms"""
    if session.get('logged_in') == True:
        return redirect(url_for("index"))
    if request.method == 'POST':
        nickname = request.form.get("nickname")
        if nickname:
            session['logged_in'] = True
            session['nickname'] = nickname
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Remove Username and exit"""
    if session.get('logged_in') == True:
            session['logged_in'] = False
            session['nickname'] = "Anonimus"
    return redirect(url_for("index"))

def get_messsages_by_channel(channel_name):
    new_messsage = []
    for message in messages:
        print(message.nickname)
        if message.channel == channel_name:
            new_messsage.append(marshal(message,resource_fields))
    return new_messsage
