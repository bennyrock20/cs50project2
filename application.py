import os

from flask import Flask, render_template,session,redirect,url_for,request,jsonify
from flask_socketio import SocketIO, emit
from flask_session import Session
from chat import Chat
from channel import Channel
import pickle
import json


app = Flask(__name__)
app.config["SECRET_KEY"] = "cdc&^^*&^876687GHJg"
socketio = SocketIO(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"


Session(app)


@app.route("/")
def index():
    if session.get('logged_in') != True:
        return redirect(url_for("login"))
    if session.get('channel_list') ==  None:
        session['channel_list'] = []
    return render_template("index.html", nickname =  session.get('nickname'), channels= session.get('channel_list'))

@app.route("/login",methods=['post','get'])
def login():
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
    if session.get('logged_in') == True:
            session['logged_in'] = False
            session['nickname'] = "Anonimus"
    return redirect(url_for("index"))

@app.route("/add-channel", methods=['post'])
def add_channel():
    """ Add Channel to Channel List"""
    if request.method == 'POST':
        if session.get('channel_list') == None:
            session['channel_list'] = []

        channel_list = session.get('channel_list')
        channel_name =  request.form.get("channel_name")
        if channel_name != None:
            channel_list.append(channel_name);
            session['channel_list'] = channel_list
            #emit("added new channel", {"channel_list": session.get('channel_list') }, broadcast=True)
        else:
            print("Ingrese un valor")

    return redirect(url_for("index"))


@app.route("/chat-details/<string:channel_name>")
def chat_details(channel_name):
    """Load messages from chat"""
    return render_template("chat_details.html", nickname =  session.get('nickname'), channels= session.get('channel_list'))

def print_(value):
        print("_________________________________*******_______________________________")
        print(value)
