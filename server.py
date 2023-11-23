from flask import Flask
from flask import request

app = Flask(__name__)
app.secret_key = "thisKeyIsSuperSecure"

stream = ["Welcome to FSTREAM, friends"]

@app.route("/")
def get_messages():
    return { "messages": stream }

@app.post("/submit")
def submit_message():
    message = request.form['message']
    stream.append(message)
    return { "message": message }

if __name__ == "__main__":
    app.run(debug=True)