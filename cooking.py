from db import db
from sqlalchemy import text

def add_recipe(description, price, rating, protein, carbs, fat, poster_name):
    sql = "INSERT INTO recipes (description, price, rating, protein, carbs, fat, poster_name) VALUES (:description, :price, :rating, :protein, :carbs, :fat, :poster_name) RETURNING id"
    result = db.session.execute(text(sql), {"description": description, "price": price, "rating": rating, "protein": protein, "carbs": carbs, "fat": fat, "poster_name": poster_name})
    db.session.commit()
    return result.fetchone()[0]

def get_recipe(recipe_id):
    sql = "SELECT id, description, price, rating, protein, carbs, fat, poster_name FROM recipes WHERE id=:recipe_id"
    result = db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()
    return result

def check_if_ingredient_exists(ingredient_name):
    sql = "SELECT id FROM ingredients WHERE ingredient_name=:ingredient_name"
    result = db.session.execute(text(sql), {"ingredient_name": ingredient_name}).fetchone()
    return result[0] if result else None

def add_ingredient(ingredient_name):
    sql = "INSERT INTO ingredients (ingredient_name) VALUES (:ingredient_name) RETURNING id"
    result = db.session.execute(text(sql), {"ingredient_name": ingredient_name})
    db.session.commit()
    return result.fetchone()[0]

def get_ingredients(recipe_id):
    sql = "SELECT ingredient_name FROM ingredients JOIN recipe_ingredients ON recipe_ingredients.ingredient_id = ingredients.id WHERE recipe_ingredients.recipe_id=:recipe_id"
    result = db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchall()
    ingredient_names = [row[0] for row in result]
    return ingredient_names

def add_comment(recipe_id, content, poster_name):
    sql = "INSERT INTO comments (recipe_id, content, poster_name) VALUES (:recipe_id, :content, :poster_name)"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "content": content, "poster_name": poster_name})
    db.session.commit()

def get_comments(recipe_id):
    sql = "SELECT id, content, poster_name, posted_at FROM comments WHERE recipe_id=:recipe_id ORDER BY posted_at ASC"
    result = db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchall()
    return result


def add_recipe_ingredient_relationship(recipe_id, ingredient_id):
    sql = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (:recipe_id, :ingredient_id)"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "ingredient_id": ingredient_id})
    db.session.commit()

def add_favorite(user_id, recipe_id):
    sql = "INSERT INTO favorites (user_id, recipe_id) VALUES (:user_id, :recipe_id)"
    db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()

def check_if_favorite_exists(user_id, recipe_id):
    sql = "SELECT id FROM favorites WHERE user_id=:user_id AND recipe_id=:recipe_id"
    result = db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id}).fetchone()
    return result[0] if result else None

def get_user_favorites(user_id):
    sql = "SELECT recipes.* FROM recipes JOIN favorites ON recipes.id = favorites.recipe_id WHERE favorites.user_id=:user_id"
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return result

def delete_favorite(user_id, recipe_id):
    sql = "DELETE FROM favorites WHERE user_id=:user_id AND recipe_id=:recipe_id"
    db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()
