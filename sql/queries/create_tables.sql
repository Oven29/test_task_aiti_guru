BEGIN;

CREATE TABLE categories (
    name VARCHAR(127) NOT NULL, 
    parent_id INTEGER, 
    id SERIAL NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(parent_id) REFERENCES categories (id)
);

CREATE TABLE users (
    name VARCHAR(127) NOT NULL, 
    address VARCHAR(255), 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    id SERIAL NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TYPE orderstatus AS ENUM ('pending', 'paid', 'shipped', 'completed', 'canceled');

CREATE TABLE orders (
    amount INTEGER NOT NULL, 
    user_id INTEGER NOT NULL, 
    status orderstatus NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
    id SERIAL NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE products (
    name VARCHAR(127) NOT NULL, 
    category_id INTEGER NOT NULL, 
    count INTEGER NOT NULL, 
    price INTEGER NOT NULL, 
    id SERIAL NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(category_id) REFERENCES categories (id)
);

CREATE TABLE order_items (
    count INTEGER NOT NULL, 
    order_id INTEGER NOT NULL, 
    product_id INTEGER NOT NULL, 
    id SERIAL NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(order_id) REFERENCES orders (id), 
    FOREIGN KEY(product_id) REFERENCES products (id)
);

COMMIT;
