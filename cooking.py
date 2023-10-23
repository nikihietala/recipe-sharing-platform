from db import db
from sqlalchemy import text

def add_recipe(description, price, rating, protein, carbs, fat, poster_name):
    sql = "INSERT INTO recipes (description, price, protein, carbs, fat, poster_name) VALUES (:description, :price, :rating, :protein, :carbs, :fat, :poster_name) RETURNING id"
    result = db.session.execute(text(sql), {"description": description, "price": price, "protein": protein, "carbs": carbs, "fat": fat, "poster_name": poster_name})
    db.session.commit()
    return result.fetchone()[0]

def get_recipe(recipe_id):
    sql = "SELECT id, description, price, protein, carbs, fat, poster_name FROM recipes WHERE id=:recipe_id"
    result = db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()
    return result

def get_recipes():
    sql = "SELECT r.id, r.description, r.price, r.poster_name, COALESCE((SELECT AVG(rating) FROM recipe_ratings rr WHERE r.id = rr.recipe_id), 0) AS average_rating FROM recipes r ORDER BY average_rating DESC"
    results = db.session.execute(text(sql)).fetchall()
    return results

def delete_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id=:recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    db.session.commit()

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

def add_or_update_rating(user_id, recipe_id, rating):
    sql = "SELECT id FROM recipe_ratings WHERE user_id=:user_id AND recipe_id=:recipe_id"
    result = db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id}).fetchone()

    if result:
        sql = "UPDATE recipe_ratings SET rating=:rating WHERE user_id=:user_id AND recipe_id=:recipe_id"
    else:
        sql = "INSERT INTO recipe_ratings (user_id, recipe_id, rating) VALUES (:user_id, :recipe_id, :rating)"
    
    db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id, "rating": rating})
    db.session.commit()

def get_average_rating(recipe_id):
    sql = "SELECT AVG(rating) FROM recipe_ratings WHERE recipe_id=:recipe_id"
    result = db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()
    return round(result[0], 1) if result[0] else None

def search_recipes(ingredient=None, max_price=None, min_price=None):
    sql = "SELECT id, description, price, poster_name FROM recipes WHERE 1=1"
    # add parameters to make sure SQL injection is not possible
    params = {}

    if ingredient:
        sql += " AND EXISTS (SELECT 1 FROM recipe_ingredients ri JOIN ingredients i ON ri.ingredient_id = i.id WHERE ri.recipe_id = recipes.id AND LOWER(i.ingredient_name) = LOWER(:ingredient))"
        params["ingredient"] = ingredient.strip()
    
    if max_price:
        sql += " AND price <= :max_price"
        params["max_price"] = max_price
    
    if min_price:
        sql += " AND price >= :min_price"
        params["min_price"] = min_price

    return db.session.execute(text(sql), params).fetchall()

def get_user_recipes(user_name):
    sql = "SELECT id, description, price, poster_name FROM recipes WHERE poster_name = :poster_name"
    recipes = db.session.execute(text(sql), {"poster_name": user_name}).fetchall()
    return recipes
