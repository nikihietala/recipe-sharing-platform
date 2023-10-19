from app import app
from flask import render_template, redirect, request, session
from os import getenv
from db import db
from sqlalchemy.sql import text
import users
import cooking

@app.route("/")
def index():
    return render_template("index.html", username = users.user_name())

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

        # Add ingredient to session
        if action == "Add Ingredient":
            ingredient = request.form["ingredient"]
            if ingredient:
                if 'ingredients' not in session:
                    session['ingredients'] = []
                session['ingredients'].append(ingredient)
                session.modified = True
            return render_template("newrecipe.html", ingredients=session['ingredients'], form_data=form_data)

        # Delete ingredient from session
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
            recipe_id = cooking.add_recipe(description, price, rating, protein, carbs, fat, poster_name)

            for ingredient_name in ingredients:
                #Check if ingredient exists in ingredients table
                ingredient_id = cooking.check_if_ingredient_exists(ingredient_name)

                # If ingredient doesn't exist, add it to ingredients table
                if ingredient_id is None:
                    ingredient_id = cooking.add_ingredient(ingredient_name)

                cooking.add_recipe_ingredient_relationship(recipe_id, ingredient_id)

            # Clear ingredients session after recipe is submitted
            session.pop('ingredients', None)

            return redirect("/recipes")

    session.setdefault('ingredients', [])
    return render_template("newrecipe.html", ingredients=session['ingredients'], form_data=form_data)

@app.route("/recipes/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = cooking.get_recipe(recipe_id)
    if not recipe:
        return render_template("error.html", message="Recipe not found")
    ingredients = cooking.get_ingredients(recipe_id)
    comments = cooking.get_comments(recipe_id)
    return render_template("recipe_details.html", recipe=recipe, ingredients=ingredients, comments=comments, count = len(comments))

@app.route("/recipes/<int:recipe_id>/comment", methods=["POST"])
def add_comment(recipe_id):
    content = request.form["content"]
    poster_name = users.user_name()
    cooking.add_comment(recipe_id, content, poster_name)
    return redirect("/recipes/" + str(recipe_id))