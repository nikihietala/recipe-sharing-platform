import os
from flask import redirect, render_template, request, session, abort
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy.sql import text

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password) VALUES (:name, :password)"
        db.session.execute(text(sql), {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(name, password)

def login(name, password):
    sql = "SELECT id, password FROM users WHERE name=:name"
    result = db.session.execute(text(sql), {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
    session["user_id"] = user.id
    session["user_name"] = name
    session["csrf_token"] = os.urandom(16).hex()
    return True

def user_name():
    return session.get("user_name")

def user_id():
    return session.get("user_id")

def logout():
    del session["user_id"]
    del session["user_name"]

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
