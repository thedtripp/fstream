from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime

app = Flask(__name__)
app.secret_key = "thisKeyIsSuperSecure"

stream = [("This message will self-destruct in 10 seconds", int(datetime.now().timestamp()))]

@app.route("/")
def get_messages():
    stream = clear_expired_messages()
    return render_template('home.html', messages=stream)

@app.route("/api")
def api_get_messages():
    stream = clear_expired_messages()
    return { "messages": stream }

def add_message_to_queue(message):
    creation_time = int(datetime.now().timestamp())
    stream.append((message, creation_time))

def clear_expired_messages(TTL=10):
    now = int(datetime.now().timestamp())
    return list(filter(lambda x: now - x[1] < TTL, stream))

@app.post("/submit")
def submit_message():
    stream = clear_expired_messages()
    add_message_to_queue(request.form['message'])
    return get_messages()

@app.post("/api/submit")
def api_submit_message():
    stream = clear_expired_messages()
    add_message_to_queue(request.form['message'])
    return { "message": request.form['message'] }

# This is a utility method. Not fit for production use because it wipes to global queue.
@app.route("/clear")
def clear_messages():
    stream.clear()
    return get_messages()

if __name__ == "__main__":
    app.run(debug=True)