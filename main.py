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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
Bootstrap(app)
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def vid():
    return render_template("scanner.html",
                        )

@socketio.on('connect')
def connect():
    print("client connected")
    sys.stdout.flush()

@socketio.on('message')
def message(msg):
    emit('test echo', '\n\n SERVER TO CLIENT')
#     print("Incoming Message: ", msg)
#     sys.stdout.flush()

@socketio.on('process')
def test_connect(data):
#     emit('test echo', data)
    data = data.split(",")[1]
    img = Image.open(BytesIO(base64.b64decode(data)))
    emit('test echo', '\n\nProcessing')
    
    decode_frame = decode(img)
#     emit('bar found', decode_frame )
    
    if len(decode_frame) > 0:
        # print(decode_frame)
        emit('bar found', '\n\nCAUGHT')
        disconnect(request.sid)


if __name__ == '__main__':
    socketio.run()
