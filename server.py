from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.secret_key = "thisKeyIsSuperSecure"

stream = []

@app.route("/")
def get_messages():
    return render_template('home.html', messages=stream)

@app.post("/submit")
def submit_message():
    message = request.form['message']
    stream.append(message)
    return get_messages()

@app.route("/api")
def api_get_messages():
    return { "messages": stream }

# This is a utility method. Not fit for production use because it wipes to global queue.
@app.route("/clear")
def clear_messages():
    stream.clear()
    return get_messages()

@app.post("/api/submit")
def api_submit_message():
    message = request.form['message']
    stream.append(message)
    return { "message": message }

if __name__ == "__main__":
    app.run(debug=True)