from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy.sql import text

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        #only insert username into database if the username is between 3 and 20 characters long
        if len(name) < 3 or len(name) > 20:
            return False
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
    return True