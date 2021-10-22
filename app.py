from flask import Flask, render_template, url_for, request, abort, redirect, session, flash, send_file, make_response, jsonify, Response
from flask_bootstrap import Bootstrap
from functools import wraps
from datetime import timedelta, date, datetime
from pyzbar.pyzbar import decode
from flask_socketio import SocketIO, emit, disconnect
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
Bootstrap(app)
socketio = SocketIO(app, logger=True, engineio_logger=True)

@app.route('/', methods=['GET', 'POST'])
def vid():
    return render_template("scanner.html",
                        )

@socketio.on('connect')
def connect():
    print("client connected")

@socketio.on('message')
def message(msg):
    print("\n\nmessage: ", msg)

# @socketio.on('process')
# def test_connect(data):
#     print(data)
#     emit('test echo', 'echoed')
#     disconnect(request.sid)


if __name__ == '__main__':
    app.run(debug='True')
