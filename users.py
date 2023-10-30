import os
from flask import request, session, abort
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password) VALUES (:name, :password)"
        db.session.execute(text(sql), {"name": name, "password": hash_value})
        db.session.commit()
    except BaseException:
        return False
    return login(name, password)


def login(name, password):
    sql = "SELECT id, password FROM users WHERE name=:name"
    result = db.session.execute(text(sql), {"name": name})
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
    form_token = request.form.get("csrf_token")
    session_token = session.get("csrf_token")
    if not form_token or not session_token or session_token != form_token:
        abort(403)
