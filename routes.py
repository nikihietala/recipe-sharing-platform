from app import app
from flask import render_template, redirect, request, session
from os import getenv
from db import db
from sqlalchemy.sql import text
import users

@app.route("/")
def index():
    username = users.user_name()
    words = ["apina", "banaani", "cembalo"]
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("index.html", message="Tervetuloa!", items=words, count=len(messages), messages=messages, username=username)

@app.route("/recipes")
def recipes():
    result = db.session.execute(text("SELECT id, description, price, rating, poster_name FROM recipes"))
    recipes = result.fetchall()
    return render_template("recipes.html", recipes=recipes)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]

    if not users.login(username, password):
        return render_template("error.html", message="Wrong username or password")
    
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        
        #check that username is valid in length
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", message="Username must be between 3 and 20 characters long")
        
        password = request.form["password1"]
        check_password = request.form["password2"]

        #check that password is valid in length
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

@app.route("/newrecipe", methods=["GET", "POST"])
def newrecipe():
    form_data = {
        'description': request.form.get('description', ''),
        'price': request.form.get('price', ''),
        'rating': request.form.get('rating', ''),
        'protein': request.form.get('protein', ''),
        'carbs': request.form.get('carbs', ''),
        'fat': request.form.get('fat', ''),
    }

    if request.method == "POST":
        action = request.form.get("action")

        # Add ingredient
        if action == "Add Ingredient":
            ingredient = request.form["ingredient"]
            if ingredient:
                if 'ingredients' not in session:
                    session['ingredients'] = []
                session['ingredients'].append(ingredient)
                session.modified = True
            return render_template("newrecipe.html", ingredients=session['ingredients'], form_data=form_data)

        # Delete ingredient
        elif 'ingredient_to_delete' in request.form:
            ingredient_to_delete = request.form["ingredient_to_delete"]
            if 'ingredients' in session:
                session['ingredients'] = [i for i in session['ingredients'] if i != ingredient_to_delete]
                session.modified = True
            return render_template("newrecipe.html", ingredients=session['ingredients'], form_data=form_data)

        elif action == "Add recipe":
            description = request.form["description"]
            price = request.form["price"]
            rating = request.form["rating"]
            protein = request.form["protein"]
            carbs = request.form["carbs"]
            fat = request.form["fat"]
            poster_name = users.user_name()
            ingredients = session.get('ingredients', [])

            # Store recipe in DB(recipes table)
            sql = "INSERT INTO recipes (description, price, rating, protein, carbs, fat, poster_name) VALUES (:description, :price, :rating, :protein, :carbs, :fat, :poster_name) RETURNING id"
            result = db.session.execute(text(sql), {"description": description, "price": price, "rating": rating, "protein": protein, "carbs": carbs, "fat": fat, "poster_name": poster_name})
            db.session.commit()
            recipe_id = result.fetchone()[0]

            for ingredient_name in ingredients:
                # Check if ingredient exists already in ingredients table
                sql = "SELECT id FROM ingredients WHERE ingredient_name=:ingredient_name"
                result = db.session.execute(text(sql), {"ingredient_name": ingredient_name}).fetchone()
                
                # Store ingredient ID in ingredient_id
                if result:
                    ingredient_id = result[0]
                else:
                    # Insert new ingredient into DB(ingredients table)
                    sql = "INSERT INTO ingredients (ingredient_name) VALUES (:ingredient_name) RETURNING id"
                    result = db.session.execute(text(sql), {"ingredient_name": ingredient_name})
                    db.session.commit()
                    ingredient_id = result.fetchone()[0]

                # Insert relationship into recipe_ingredients table
                sql = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (:recipe_id, :ingredient_id)"
                db.session.execute(text(sql), {"recipe_id": recipe_id, "ingredient_id": ingredient_id})
                db.session.commit()

            # Clear ingredients session after recipe is submitted
            session.pop('ingredients', None)

            return redirect("/recipes")

    session.setdefault('ingredients', [])
    return render_template("newrecipe.html", ingredients=session['ingredients'], form_data=form_data)

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(text(sql), {"content":content})
    db.session.commit()
    return redirect("/")


@app.route("/test")
def test():
    content = ""
    for i in range(100):
        content += str(i + 1) + " "
    return content