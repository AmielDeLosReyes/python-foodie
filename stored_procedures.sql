-- Stored procedures for client
 
CREATE PROCEDURE `foodie`.`get_clients`()
BEGIN
    SELECT * FROM foodie.client;
END 

CREATE PROCEDURE `foodie`.`get_client_by_id`(client_id INT)
BEGIN
    SELECT * FROM foodie.client WHERE id = client_id;
END 

CREATE PROCEDURE `foodie`.`create_client`(
    email VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    image_url VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255)
)
BEGIN
    INSERT INTO foodie.client (email, first_name, last_name, image_url, username, password)
    VALUES (email, first_name, last_name, image_url, username, password);
END 

CREATE PROCEDURE `foodie`.`update_client`(
    client_id INT,
    email VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    image_url VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255)
)
BEGIN
    UPDATE foodie.client
    SET
        email = email,
        first_name = first_name,
        last_name = last_name,
        image_url = image_url,
        username = username,
        password = password
    WHERE id = client_id;
END 

CREATE PROCEDURE `foodie`.`delete_client`(client_id INT)
BEGIN
    DELETE FROM foodie.client WHERE id = client_id;
END 



-- Store procedures for Restaurant
 

-- Procedure to get all restaurants
CREATE PROCEDURE `foodie`.`get_restaurants`()
BEGIN
    SELECT * FROM foodie.restaurant;
END 

-- Procedure to get a restaurant by ID
CREATE PROCEDURE `foodie`.`get_restaurant_by_id`(restaurant_id INT)
BEGIN
    SELECT * FROM foodie.restaurant WHERE id = restaurant_id;
END 

-- Procedure to create a new restaurant
CREATE PROCEDURE `foodie`.`create_restaurant`(
    email VARCHAR(255),
    name VARCHAR(255),
    address VARCHAR(255),
    phone_number VARCHAR(12),
    bio TEXT,
    city VARCHAR(255),
    profile_url VARCHAR(255),
    banner_url VARCHAR(255),
    password VARCHAR(255)
)
BEGIN
    INSERT INTO foodie.restaurant (email, name, address, phone_number, bio, city, profile_url, banner_url, password)
    VALUES (email, name, address, phone_number, bio, city, profile_url, banner_url, password);
END 

-- Procedure to update an existing restaurant
CREATE PROCEDURE `foodie`.`update_restaurant`(
    restaurant_id INT,
    email VARCHAR(255),
    name VARCHAR(255),
    address VARCHAR(255),
    phone_number VARCHAR(12),
    bio TEXT,
    city VARCHAR(255),
    profile_url VARCHAR(255),
    banner_url VARCHAR(255),
    password VARCHAR(255)
)
BEGIN
    UPDATE foodie.restaurant
    SET
        email = email,
        name = name,
        address = address,
        phone_number = phone_number,
        bio = bio,
        city = city,
        profile_url = profile_url,
        banner_url = banner_url,
        password = password
    WHERE id = restaurant_id;
END 

-- Procedure to delete an existing restaurant
CREATE PROCEDURE `foodie`.`delete_restaurant`(restaurant_id INT)
BEGIN
    DELETE FROM foodie.restaurant WHERE id = restaurant_id;
END 




-- Store procedures for Menu
-- Stored procedures for menu_item
 

-- Procedure to get all menu items for a specific restaurant
CREATE PROCEDURE `foodie`.`get_menu_items`(restaurant_id INT)
BEGIN
    SELECT * FROM foodie.menu_item WHERE restaurant_id = restaurant_id;
END 

-- Procedure to get a menu item by ID
CREATE PROCEDURE `foodie`.`get_menu_item_by_id`(menu_item_id INT)
BEGIN
    SELECT * FROM foodie.menu_item WHERE id = menu_item_id;
END 

-- Procedure to create a new menu item
CREATE PROCEDURE `foodie`.`create_menu_item`(
    description TEXT,
    image_url VARCHAR(255),
    name VARCHAR(255),
    price DECIMAL(10, 2),
    restaurant_id INT
)
BEGIN
    INSERT INTO foodie.menu_item (description, image_url, name, price, restaurant_id)
    VALUES (description, image_url, name, price, restaurant_id);
END 

-- Procedure to update an existing menu item
CREATE PROCEDURE `foodie`.`update_menu_item`(
    menu_item_id INT,
    description TEXT,
    image_url VARCHAR(255),
    name VARCHAR(255),
    price DECIMAL(10, 2)
)
BEGIN
    UPDATE foodie.menu_item
    SET
        description = description,
        image_url = image_url,
        name = name,
        price = price
    WHERE id = menu_item_id;
END 

-- Procedure to delete an existing menu item
CREATE PROCEDURE `foodie`.`delete_menu_item`(menu_item_id INT)
BEGIN
    DELETE FROM foodie.menu_item WHERE id = menu_item_id;
END 




-- Store procedures for Order
 
-- Procedure to get all orders for a specific client
CREATE PROCEDURE `foodie`.`get_client_orders`(client_id INT)
BEGIN
    SELECT * FROM foodie.`order` WHERE client_id = client_id;
END 

-- Procedure to get an order by ID
CREATE PROCEDURE `foodie`.`get_order_by_id`(order_id INT)
BEGIN
    SELECT * FROM foodie.`order` WHERE id = order_id;
END 

-- Procedure to create a new order
CREATE PROCEDURE `foodie`.`create_order`(
    client_id INT,
    restaurant_id INT
)
BEGIN
    INSERT INTO foodie.`order` (client_id, restaurant_id)
    VALUES (client_id, restaurant_id);
END 

-- Procedure to update an existing order
CREATE PROCEDURE `foodie`.`update_order`(
    order_id INT,
    is_confirmed BOOLEAN,
    is_complete BOOLEAN
)
BEGIN
    UPDATE foodie.`order`
    SET
        is_confirmed = is_confirmed,
        is_complete = is_complete
    WHERE id = order_id;
END 




