from flask import Flask
app = Flask(__name__)


@app.route("/api/v1/hello-world-<username>")
def hello_world(username):
    return 'Hello World %s !' % username


