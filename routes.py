from flask import render_template, redirect, request, session, flash
from app import app
import users
import cooking


@app.route("/")
def index():
    return render_template("index.html", username=users.user_name())


@app.route("/recipes")
def recipes_route():
    recipes_raw = cooking.get_recipes()
    recipes = []
    for recipe in recipes_raw:
        # convert recipes into a dictionary
        recipe_dict = {
            'id': recipe.id,
            'description': recipe.description,
            'price': recipe.price,
            'poster_name': recipe.poster_name,
            'average_rating': float(recipe.average_rating)
        }
        # convert average rating to whole number to be able to display stars
        recipe_dict['whole_stars'] = int(recipe_dict['average_rating'])
        # check if the remaining decimal is greater than or equal to 0.5 to be
        # able to display a half star
        recipe_dict['half_star'] = 1 if recipe_dict['average_rating'] - \
            recipe_dict['whole_stars'] >= 0.5 else 0
        recipes.append(recipe_dict)
    return render_template(
        "recipes.html",
        recipes=recipes,
        username=users.user_name())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]

    if not users.login(username, password):
        return render_template(
            "error.html",
            message="Wrong username or password")

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

        # check that username is valid in length
        if len(username) < 3 or len(username) > 20:
            return render_template(
                "error.html",
                message="Username must be between 3 and 20 characters long")

        password = request.form["password1"]
        check_password = request.form["password2"]

        # check that password is valid in length
        if len(password) < 4 or len(password) > 20:
            return render_template(
                "error.html",
                message="Password must be between 4 and 20 characters long")

        # check that passwords match
        if password != check_password:
            return render_template(
                "error.html", message="Passwords do not match")

        # check that username is not already taken
        if not users.register(username, password):
            return render_template(
                "error.html", message="Username already exists")

    # after successful registration, redirect to home page
    flash("Registered successfully! You are now logged in", "success")
    return redirect("/")


@app.route("/newrecipe", methods=["GET", "POST"])
def newrecipe():
    form_data = {
        'description': request.form.get('description', '').strip(),
        'price': request.form.get('price', '').strip(),
        'protein': request.form.get('protein', '').strip(),
        'carbs': request.form.get('carbs', '').strip(),
        'fat': request.form.get('fat', '').strip(),
    }

    if request.method == "POST":
        users.check_csrf()

        action = request.form.get("action")

        # add ingredient to session
        if action == "Add Ingredient":
            ingredient = request.form["ingredient"]

            if not ingredient.replace(' ', '').isalpha():
                flash('Only letters are allowed for ingredients. No numbers or special characters.', 'error')
                return render_template("newrecipe.html",
                                       ingredients=session.get('ingredients', []),
                                       form_data=form_data,
                                       username=users.user_name())
            
            if not ingredient:
                return render_template("error.html")

            if 'ingredients' not in session:
                session['ingredients'] = []
            session['ingredients'].append(ingredient)
            session.modified = True
            return render_template("newrecipe.html",
                                   ingredients=session['ingredients'],
                                   form_data=form_data,
                                   username=users.user_name())

        # delete ingredient from session
        if 'ingredient_to_delete' in request.form:
            ingredient_to_delete = request.form["ingredient_to_delete"]
            if 'ingredients' in session:
                session['ingredients'] = [
                    i for i in session['ingredients'] if i != ingredient_to_delete]
                session.modified = True
            return render_template("newrecipe.html",
                                   ingredients=session['ingredients'],
                                   form_data=form_data,
                                   username=users.user_name())

        if action == "Add recipe":
            # Do not allow empty fields for description, price, or ingredients
            if not form_data['description'] or not form_data['price'] or not session.get('ingredients'):
                return render_template("error.html", message="You must fill in all fields")

            # Do not allow empty fields for nutrition
            if not form_data['protein'] or not form_data['carbs'] or not form_data['fat']:
                return render_template("error.html", message="You must fill in all fields")

            description = form_data['description']
            price = form_data['price']
            protein = form_data['protein']
            carbs = form_data['carbs']
            fat = form_data['fat']
            poster_name = users.user_name()
            ingredients = session.get('ingredients', [])

            # store recipe in DB(recipes table)
            recipe_id = cooking.add_recipe(
                description, price, protein, carbs, fat, poster_name)

            for ingredient_name in ingredients:
                # check if ingredient exists in ingredients table
                ingredient_id = cooking.check_if_ingredient_exists(ingredient_name)

                # if ingredient doesn't exist, add it to ingredients table
                if ingredient_id is None:
                    ingredient_id = cooking.add_ingredient(ingredient_name)

                cooking.add_recipe_ingredient_relationship(recipe_id, ingredient_id)

            # clear ingredients session after recipe is submitted
            session.pop('ingredients', None)
            flash("Recipe added!", "success")
            return redirect("/recipes")

    session.setdefault('ingredients', [])
    return render_template("newrecipe.html",
                           ingredients=session['ingredients'],
                           form_data=form_data,
                           username=users.user_name())



@app.route("/recipes/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = cooking.get_recipe(recipe_id)
    if not recipe:
        return render_template("error.html", message="Recipe not found")
    ingredients = cooking.get_ingredients(recipe_id)
    comments = cooking.get_comments(recipe_id)
    return render_template(
        "recipe_details.html",
        recipe=recipe,
        ingredients=ingredients,
        comments=comments,
        count=len(comments),
        current_user=users.user_name(),
        username=users.user_name())


@app.route("/recipes/<int:recipe_id>/delete", methods=["POST"])
def delete_recipe(recipe_id):
    if not users.user_id():
        return render_template(
            "error.html",
            message="You must be logged in to delete a recipe")

    recipe = cooking.get_recipe(recipe_id)
    if not recipe:
        return render_template("error.html", message="Recipe not found")

    if recipe.poster_name != users.user_name():
        return render_template(
            "error.html",
            message="You can only delete recipes you have posted")

    users.check_csrf()
    cooking.delete_recipe(recipe_id)
    flash("Recipe deleted!", "success")
    return redirect("/recipes")


@app.route("/recipes/<int:recipe_id>/comment", methods=["POST"])
def add_comment(recipe_id):
    users.check_csrf()
    content = request.form["content"]
    if len(content) > 500:
        return render_template(
            "error.html",
            message="Comment must be less than 500 characters long")
    poster_name = users.user_name()
    cooking.add_comment(recipe_id, content, poster_name)
    return redirect("/recipes/" + str(recipe_id))


@app.route("/recipes/<int:recipe_id>/favorite", methods=["POST"])
def add_favorite(recipe_id):
    user_id = users.user_id()
    if not user_id:
        return render_template(
            "error.html",
            message="You must be logged in to add a recipe to favorites")
    if cooking.check_if_favorite_exists(user_id, recipe_id):
        return render_template("error.html",
                               message="This recipe is already in favorites")
    users.check_csrf()
    cooking.add_favorite(user_id, recipe_id)
    flash("Recipe added to favorites!", "success")
    return redirect("/recipes/" + str(recipe_id))


@app.route("/favorites")
def view_favorites():
    if not users.user_id():
        return render_template(
            "error.html",
            message="You must be logged in to view favorites")
    favorite_recipes = cooking.get_user_favorites(users.user_id())
    return render_template(
        "favorites.html",
        favorite_recipes=favorite_recipes,
        username=users.user_name())


@app.route("/recipes/delete/<int:recipe_id>", methods=["POST"])
def delete_favorite(recipe_id):
    user_id = users.user_id()
    if not user_id:
        return render_template(
            "error.html",
            message="You must be logged in to delete a recipe from favorites")
    users.check_csrf()
    cooking.delete_favorite(user_id, recipe_id)
    flash("Recipe deleted from favorites!", "success")
    return redirect("/favorites")


@app.route("/rate_recipe/<int:recipe_id>", methods=["POST"])
def rate_recipe(recipe_id):
    user_id = users.user_id()
    if not user_id:
        return render_template(
            "error.html",
            message="You must be logged in to rate a recipe")
    users.check_csrf()
    rating = request.form["rating"]
    if not 1 <= int(rating) <= 5:
        return render_template("error.html",
                               message="Rating must be between 1 and 5")
    cooking.add_or_update_rating(user_id, recipe_id, rating)
    flash("Rating added!", "success")
    return redirect("/recipes/" + str(recipe_id))


@app.route("/search")
def search():
    return render_template("search.html", username=users.user_name())


@app.route("/search_results")
def search_results():
    ingredient = request.args.get('ingredient', None)
    max_price = request.args.get('max_price', None)
    min_price = request.args.get('min_price', None)

    recipes = cooking.search_recipes(ingredient, max_price, min_price)

    return render_template(
        "search.html",
        recipes=recipes,
        username=users.user_name())


@app.route('/myrecipes')
def my_recipes():
    if not users.user_id():
        return render_template(
            "error.html",
            message="You must be logged in to view your recipes")
    recipes = cooking.get_user_recipes(users.user_name())
    return render_template(
        'my_recipes.html',
        recipes=recipes,
        username=users.user_name())
