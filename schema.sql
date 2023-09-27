CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
)

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    recipe_name TEXT,
    price INTEGER,
    rating FLOAT,
    poster_id INTEGER REFERENCES users(id),
)

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    ingredient_name TEXT,
    recipe_id INTEGER REFERENCES recipes(id)
)

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(id)
)

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(id),
    comment_date DATE
)