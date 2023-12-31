CREATE DATABASE IF NOT EXISTS foodie;

CREATE TABLE foodie.client (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    image_url VARCHAR(255),
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE foodie.client_session (
    id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    token VARCHAR(255),
    FOREIGN KEY (client_id) REFERENCES client(id)
);

CREATE TABLE foodie.restaurant (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(12) NOT NULL,
    bio TEXT,
    city VARCHAR(255) NOT NULL,
    profile_url VARCHAR(255),
    banner_url VARCHAR(255),
    password VARCHAR(255) NOT NULL
);

CREATE TABLE foodie.restaurant_session (
    id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    token VARCHAR(255),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(id)
);

CREATE TABLE foodie.menu_item (
    id INT PRIMARY KEY AUTO_INCREMENT,
    description TEXT,
    image_url VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE foodie.`order` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    restaurant_id INT,
    is_confirmed BOOLEAN DEFAULT FALSE,
    is_complete BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (client_id) REFERENCES client(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(id)
);

CREATE TABLE foodie.order_menu_item (
    order_id INT,
    menu_item_id INT,
    PRIMARY KEY (order_id, menu_item_id),
    FOREIGN KEY (order_id) REFERENCES `order`(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_item(id)
);
