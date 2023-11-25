from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO, send, emit
from datetime import datetime

app = Flask(__name__)
app.secret_key = "thisKeyIsSuperSecure"
socketio = SocketIO(app)

stream = [
  (
      "This message will self-destruct in 10 seconds",
      int(datetime.now().timestamp())
  )
]


@app.route("/")
def get_messages():
    stream = clear_expired_messages()
    return render_template('home.html', messages=stream)


@socketio.on('connect')
def on_connect(data):
    send("Connected")


def timeout():
    socketio.sleep(10)
    clear_expired_messages()
    emit('clean_messages', stream, broadcast=True)


@socketio.on('message')
def on_message(data):
    clear_expired_messages()
    add_message_to_queue(data['data'])
    print(f"Message received: {data}")
    emit('message', stream, broadcast=True)
    # socketio.start_background_task(target=timeout)


@app.route("/api")
def api_get_messages():
    stream = clear_expired_messages()
    return {"messages": stream}


def add_message_to_queue(message):
    creation_time = int(datetime.now().timestamp())
    stream.append((message, creation_time))


def clear_expired_messages(TTL=10):
    now = int(datetime.now().timestamp())
    return list(filter(lambda x: now - x[1] < TTL, stream))


@app.post("/submit")
def submit_message():
    add_message_to_queue(request.form['message'])
    return get_messages()


@app.post("/api/submit")
def api_submit_message():
    _ = clear_expired_messages()
    add_message_to_queue(request.form['message'])
    return {"message": request.form['message']}


# This is a utility method.
# Not fit for production use because it wipes to global queue.
@app.route("/clear")
def clear_messages():
    stream.clear()
    return get_messages()


if __name__ == "__main__":
    app.run(debug=False)
