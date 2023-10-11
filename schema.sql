CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    description TEXT,
    price DECIMAL,
    rating INTEGER,
    poster_name TEXT REFERENCES users(name)
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    ingredient_name TEXT,
    recipe_id INTEGER REFERENCES recipes
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
    comment_date DATE
);