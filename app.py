from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    words = ["apina", "banaani", "cembalo"]
    return render_template("index.html", message="Tervetuloa!", items=words)

@app.route("/page1")
def page1():
    return "Tämä on sivu 1"

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"

@app.route("/test")
def test():
    content = ""
    for i in range(100):
        content += str(i + 1) + " "
    return content

@app.route("/page/<int:id>")
def page(id):
    return "Tämä on sivu " + str(id)