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
    ingredients TEXT,
    protein DECIMAL,
    carbs DECIMAL,
    fat DECIMAL,
    poster_name TEXT REFERENCES users(name)
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    ingredient_name TEXT UNIQUE
);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER REFERENCES recipes(id),
    ingredient_id INTEGER REFERENCES ingredients(id),
    PRIMARY KEY(recipe_id, ingredient_id)
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(id),
    UNIQUE(user_id, recipe_id)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    poster_name TEXT REFERENCES users(name),
    recipe_id INTEGER REFERENCES recipes(id),
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);