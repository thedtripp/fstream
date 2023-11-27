from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.secret_key = "thisKeyIsSuperSecure"
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def get_messages():
    return render_template('home.html')


@socketio.on('connect')
def on_connect(data):
    send("This message will self-destruct in 10 seconds")


@socketio.on('message')
def on_message(data):
    message = data['data']
    print(f"Message received: {message}")
    emit('message', message, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=False)