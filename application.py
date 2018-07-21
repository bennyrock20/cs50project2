import os

from flask import Flask, render_template,session,redirect,url_for,request,jsonify,flash,send_from_directory
from flask_socketio import SocketIO, emit
from flask_session import Session
from message import Message
import pickle
import json
from flask_restplus import fields, marshal
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["SECRET_KEY"] = "cdc&^^*&^876687GHJg"
socketio = SocketIO(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


Session(app)

channel_list =[]

channel_list.append("Default");
channel_list.append("Private");
channel_list.append("Public");

messages = []
resource_fields = {'nickname': fields.String, "channel": fields.String, "message": fields.String, "date": fields.Date, "hours": fields.String,"filename": fields.String}

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
    already_exists= False
    if channel_name != None:
        for channel in channel_list:
            if channel == channel_name:
                already_exists= True
        if already_exists == False:
            channel_list.append(channel_name);
            emit("added-new-channel", {"channel_list": channel_list }, broadcast=True)
        else:
            print("Duplicate Channel Name")
    return redirect(url_for("index"))

@socketio.on('send-message')
def send_message(data):
    """ Add Channel to Channel List"""
    print(data)
    message = data["message"]
    channel = data["channel"]
    nickname = data["nickname"]
    filename = data["filename"]
    if channel != None and message != None and nickname != None:
        message = Message(nickname = nickname , channel = channel, message = message,filename=filename)
        add_message(message)
        emit("new-message-" + str(channel), {"message": marshal(message,resource_fields) }, broadcast=True)
    return redirect(url_for("index"))

def add_message(message):
    cont = 0
    index_of_first_element =None;
    for m in messages:
        if m.channel == message.channel:
            cont =cont +1
            if index_of_first_element == None:
                index_of_first_element = m
    #print("the is a total " + str(cont) + " messsages in th channel "+ message.channel + "y el primero es en el index "+ str(index_of_first_element))
    messages.append(message)
    return True

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'afile' not in request.files:
            flash('No file part')
            return jsonify({"error": "Please select a válid file"}), 406

        file = request.files['afile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return jsonify({"error": "File required"}), 406

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"filename": url_for('uploaded_file',
                                    filename=filename)}), 200
        else:
            return jsonify({"error": "File type no allowed"}), 406
    return jsonify({"error": "Invalid method"}), 405

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def get_messsages_by_channel(channel_name):
    new_messsage = []
    for message in messages:
        print(message.nickname)
        if message.channel == channel_name:
            new_messsage.append(marshal(message,resource_fields))
    return new_messsage
