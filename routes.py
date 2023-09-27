from app import app
from flask import render_template, redirect, request, session
from os import getenv
from db import db
from sqlalchemy.sql import text
import users

@app.route("/")
def index():
    #if user is logged in, display username
    username = users.user_name()
    words = ["apina", "banaani", "cembalo"]
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("index.html", message="Tervetuloa!", items=words, count=len(messages), messages=messages, username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]

    if not users.login(username, password):
        return render_template("error.html", message="Wrong username or password")
    
    #after successful login, redirect to home page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        
        #check that username is valid
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", message="Username must be between 3 and 20 characters long")
        
        password = request.form["password1"]
        check_password = request.form["password2"]

        #check that password is valid
        if len(password) < 4 or len(password) > 20:
            return render_template("error.html", message="Password must be between 4 and 20 characters long")

        #check that passwords match
        if password != check_password:
            return render_template("error.html", message="Passwords do not match")

        #check that username is not already taken
        if not users.register(username, password):
            return render_template("error.html", message="Username already exists")

    #after successful registration, redirect to login page
    return redirect("/login")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(text(sql), {"content":content})
    db.session.commit()
    return redirect("/")

@app.route("/page1")
def page1():
    return "Tämä on sivu 1"

@app.route("/page2")
def page2():
    return "Tämä on sivu 2!!!!!"

@app.route("/test")
def test():
    content = ""
    for i in range(100):
        content += str(i + 1) + " "
    return content

@app.route("/page/<int:id>")
def page(id):
    return "Tämä on sivu " + str(id)