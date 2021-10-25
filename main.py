from flask import Flask, render_template, url_for, request, abort, redirect, session, flash, send_file, make_response, jsonify, Response
from flask_bootstrap import Bootstrap
from functools import wraps
from datetime import timedelta, date, datetime
from pyzbar.pyzbar import decode
from flask_socketio import SocketIO, emit, disconnect
from PIL import Image
from io import BytesIO
import base64
import sys
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
Bootstrap(app)
socketio = SocketIO(app)

output = []

@socketio.on('connect')
def connect():
    output = []
    print("client connected")

@socketio.on('message')
def message(msg):
    emit('test echo', '\n\nSERVER TO CLIENT')

@socketio.on('process')
def test_connect(data):
#     emit('test echo', data)
    data = data.split(",")[1]
    img = Image.open(BytesIO(base64.b64decode(data)))
    emit('test echo', '\n\nProcessing')
    
    decode_frame = decode(img)
    
    if len(decode_frame) > 0:
        # print(decode_frame)
        emit('results', decode_frame[0][0].decode("utf-8") )
        disconnect(request.sid)
        

@app.route('/', methods=['GET', 'POST'])
def home():
    output.clear()
    return render_template("scanner.html"
                        )

@app.route('/result', methods=['GET', 'POST'])
def result():
    
    data = request.get_json()
    
    if data!=None:
        output.append(data['data'])
        
    print("FOUND", data)
    
    with open("static/DB_proxy.json", 'r') as file:
        db_proxy = json.load(file)
             
    return render_template("result.html",
                    key=output[0],
                    data=db_proxy
                )
    
    
if __name__ == '__main__':
    socketio.run(app)
    

