# setup.py
import mariadb
import dbcreds

def connect_db():
    try:
        conn = mariadb.connect(
            user=dbcreds.user, 
            password=dbcreds.password,
            host=dbcreds.host, 
            port=dbcreds.port, 
            database=dbcreds.database
        )
        cursor = conn.cursor()
        return cursor, conn
    except mariadb.Error as error:
        print("ERROR:", error)
        return None, None

def execute_statement(cursor, conn, statement, list_of_args=[]):
    try:
        if statement.lower().startswith("call"):
            # For stored procedures, execute and commit
            cursor.callproc(statement.split("(")[0][5:], list_of_args)
            if statement.split("(")[0][5:] in ["create_client", "create_restaurant", "create_menu_item", "create_order"]:
                cursor.execute("COMMIT;")
            results = None  # No result set for COMMIT
        else:
            # For regular SQL statements, execute and fetch results only if it's a SELECT statement
            if statement.upper().startswith("SELECT"):
                cursor.execute(statement, list_of_args)
                results = cursor.fetchall()
            else:
                cursor.execute(statement, list_of_args)
                conn.commit()  # Commit the changes for other operations
                results = None  # No result set for other operations

        return True, results

    except mariadb.Error as error:
        print("ERROR:", error)
        return False, str(error)

def restaurant_login(email, password):
    try:
        # Assuming run_statement is a function that executes a SQL statement
        success, result = run_statement(
            "CALL foodie.restaurant_login(?, ?, @out_restaurant_id)",
            [email, password]
        )

        if success:
            # Fetch the result of the stored procedure
            cursor, conn = connect_db()
            cursor.execute("SELECT @out_restaurant_id;")
            out_restaurant_id = cursor.fetchone()[0]
            close_connection(cursor, conn)

            # Check if there is a valid restaurant_id returned
            if out_restaurant_id:
                print("Restaurant login successful!")
                return out_restaurant_id
            else:
                return None
        else:
            return None

    except Exception as error:
        print(f"Error: {error}")
        return None


def close_connection(cursor, conn):
    try:
        cursor.close()
        conn.close()
        print("Disconnected from the database")
    except mariadb.Error as error:
        print("ERROR:", error)

def run_statement(statement, list_of_args=[]):
    cursor, conn = connect_db()

    if cursor is None:
        return False, "Connection Error"

    try:
        print("Executing statement:", statement)
        if statement.startswith("CALL"):
            if statement.split("(")[0][5:] in ["create_client", "create_restaurant", "create_menu_item", "create_order"]:
                # For insert operations, execute and commit
                cursor.callproc(statement.split("(")[0][5:], list_of_args)
                conn.commit()  # Commit the changes for INSERT operations
                results = None  # No result set for INSERT
            else:
                # For other stored procedures, fetch results if a result set is expected
                cursor.callproc(statement.split("(")[0][5:], list_of_args)
                results = cursor.fetchall() if cursor.description is not None else None
                print("Results:", results)
        else:
            # For non-stored procedure statements (e.g., SELECT, UPDATE, DELETE)
            cursor.execute(statement, list_of_args)

            # Special handling for DELETE operation
            if statement.upper().startswith("DELETE"):
                conn.commit()  # Commit the changes for DELETE operations
                results = None  # No result set for DELETE

            else:
                results = cursor.fetchall()
                print("Results:", results)

        return True, results
    except mariadb.Error as error:
        print("ERROR:", error)
        return False, str(error)
    finally:
        close_connection(cursor, conn)


def serialize_data(columns, data):
    sql_data_dict = [dict(zip(columns, row)) for row in data]
    return sql_data_dict

def client_login(username, password):
    try:
        # Check if the provided username and password match a client in the database
        success, result = run_statement("SELECT id FROM foodie.client WHERE username = ? AND password = ?", [username, password])

        if success and result:
            client_id = result[0][0]
            # Generate and return a session token
            session_token = generate_session_token("client_session", client_id)
            print(f"Client Login Success: Client ID - {client_id}, Session Token - {session_token}")
            return session_token
        else:
            print("Client Login Failed")
            return None

    except Exception as error:
        print(f"Error in client_login: {error}")
        return None

def restaurant_login(username, password):
    try:
        # Check if the provided username and password match a restaurant in the database
        success, result = run_statement("SELECT id FROM foodie.restaurant WHERE username = ? AND password = ?", [username, password])

        if success and result:
            restaurant_id = result[0][0]
            # Generate and return a session token
            session_token = generate_session_token("restaurant_session", restaurant_id)
            print(f"Restaurant Login Success: Restaurant ID - {restaurant_id}, Session Token - {session_token}")
            return session_token
        else:
            print("Restaurant Login Failed")
            return None

    except Exception as error:
        print(f"Error in restaurant_login: {error}")
        return None

def generate_session_token(session_table, user_id):
    try:
        # Generate a unique session token (you can use a library like secrets for better security)
        session_token = f"{session_table}_{user_id}_token"
        # Save the session token in the corresponding session table
        success, _ = run_statement(f"INSERT INTO foodie.{session_table} (id, token) VALUES (?, ?)", [user_id, session_token])

        if success:
            return session_token
        else:
            return None

    except Exception as error:
        print(f"Error in generate_session_token: {error}")
        return None
    

def create_database():
    try:
        conn = mariadb.connect(
            user=dbcreds.user,
            password=dbcreds.password,
            host=dbcreds.host,
            port=dbcreds.port
        )
        cursor = conn.cursor()

        # Create database
        cursor.execute("DROP DATABASE IF EXISTS foodie;")


        cursor.execute("CREATE DATABASE foodie;")
        
        # Switch to the created database
        cursor.execute("USE foodie")

        # Create table for client
        cursor.execute("""
            CREATE TABLE client (
                id INT PRIMARY KEY AUTO_INCREMENT,
                email VARCHAR(255) NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                image_url VARCHAR(255),
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """)

        # Create table for client_session
        cursor.execute("""
            CREATE TABLE client_session (
            id INT PRIMARY KEY AUTO_INCREMENT,
            client_id INT,
            token VARCHAR(255),
            FOREIGN KEY (client_id) REFERENCES client(id)
        );
        """)

        # Create table for restaurant
        cursor.execute("""
            CREATE TABLE restaurant (
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
        """)

        # Create table for restaurant_session
        cursor.execute("""
            CREATE TABLE restaurant_session (
            id INT PRIMARY KEY AUTO_INCREMENT,
            restaurant_id INT,
            token VARCHAR(255),
            FOREIGN KEY (restaurant_id) REFERENCES restaurant(id)
        );
        """)

        # Create table for menu_item
        cursor.execute("""
            CREATE TABLE menu_item (
            id INT PRIMARY KEY AUTO_INCREMENT,
            description TEXT,
            image_url VARCHAR(255),
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            restaurant_id INT
        );
        """)

        # Create table for order
        cursor.execute("""
            CREATE TABLE `order` (
            id INT PRIMARY KEY AUTO_INCREMENT,
            client_id INT,
            restaurant_id INT,
            is_confirmed BOOLEAN DEFAULT FALSE,
            is_complete BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (client_id) REFERENCES client(id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurant(id)
        );
        """)

        # Create table for order_menu_item
        cursor.execute("""
            CREATE TABLE order_menu_item (
            order_id INT,
            menu_item_id INT,
            PRIMARY KEY (order_id, menu_item_id),
            FOREIGN KEY (order_id) REFERENCES `order`(id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_item(id)
        );
        """)


        #############################################################
        # Execute for the stored procedures

        # Create stored procedures for client
        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_clients`()
            BEGIN
                SELECT * FROM foodie.client;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_client_by_id`(client_id INT)
            BEGIN
                SELECT * FROM foodie.client WHERE id = client_id;
            END 
        """)

        cursor.execute("""
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

            -- Fetch the inserted client details
            SELECT * FROM foodie.client WHERE id = LAST_INSERT_ID();
                       
            -- Explicitly commit the changes
            COMMIT;
        END;

        """)

        cursor.execute("""
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
                       
                COMMIT;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`delete_client`(client_id INT)
            BEGIN
                DELETE FROM foodie.client WHERE id = client_id;
                       
                COMMIT;
            END  
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_restaurants`()
            BEGIN
                SELECT * FROM foodie.restaurant;
            END  
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_restaurant_by_id`(restaurant_id INT)
            BEGIN
                SELECT * FROM foodie.restaurant WHERE id = restaurant_id;
            END  
        """)

        cursor.execute("""
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
                       
            
                -- Fetch the inserted client details
                SELECT * FROM foodie.restaurant WHERE id = LAST_INSERT_ID();
                       
                COMMIT;
            END
        """)

        cursor.execute("""
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
                       
                COMMIT;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`delete_restaurant`(restaurant_id INT)
            BEGIN
                DELETE FROM foodie.restaurant WHERE id = restaurant_id;
                COMMIT;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_menu_items`(restaurant_id INT)
            BEGIN
                SELECT * FROM foodie.menu_item WHERE restaurant_id = restaurant_id;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_menu_item_by_id`(menu_item_id INT)
            BEGIN
                SELECT * FROM foodie.menu_item WHERE id = menu_item_id;
            END  
        """)

        cursor.execute("""
            -- Update the stored procedure to accept restaurant_id
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

                -- Fetch the inserted menu item details
                SELECT * FROM foodie.menu_item WHERE id = LAST_INSERT_ID();

                -- Explicitly commit the changes
                COMMIT;
            END;
 
        """)

        cursor.execute("""
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
                
                COMMIT;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`delete_menu_item`(menu_item_id INT)
            BEGIN
                DELETE FROM foodie.menu_item WHERE id = menu_item_id;
                COMMIT;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_client_orders`(client_id INT)
            BEGIN
                SELECT * FROM foodie.`order` WHERE client_id = client_id;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_restaurant_orders`(restaurant_id INT)
            BEGIN
                SELECT * FROM foodie.`order` WHERE restaurant_id = restaurant_id;
            END 
        """)


        cursor.execute("""
            CREATE PROCEDURE `foodie`.`get_order_by_id`(order_id INT)
            BEGIN
                SELECT * FROM foodie.`order` WHERE id = order_id;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`create_order`(
                client_id INT,
                restaurant_id INT
            )
            BEGIN
                INSERT INTO foodie.`order` (client_id, restaurant_id)
                VALUES (client_id, restaurant_id);
                COMMIT;
            END 
        """)

        cursor.execute("""
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
                       
                COMMIT;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`delete_order`(order_id INT)
            BEGIN
                DELETE FROM foodie.`order` WHERE id = order_id;
                COMMIT;
            END 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`client_login`(
                in_username VARCHAR(255),
                in_password VARCHAR(255),
                out_client_id INT
            )
            BEGIN
                -- Check if the provided username and password match a client record
                SELECT id INTO out_client_id
                FROM foodie.client
                WHERE username = in_username AND password = in_password;

                -- If a matching client is found, set out_client_id to the client's id
                -- Otherwise, out_client_id remains null
                COMMIT;
            END;
 
        """)

        cursor.execute("""
            CREATE PROCEDURE `foodie`.`restaurant_login`(
                in_email VARCHAR(255),
                in_password VARCHAR(255),
                out_restaurant_id INT
            )
            BEGIN
                -- Check if the provided email and password match a restaurant record
                SELECT id INTO out_restaurant_id
                FROM foodie.restaurant
                WHERE email = in_email AND password = in_password;

                -- If a matching restaurant is found, set out_restaurant_id to the restaurant's id
                -- Otherwise, out_restaurant_id remains null
                COMMIT;
            END;
        """)

    except mariadb.Error as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()
