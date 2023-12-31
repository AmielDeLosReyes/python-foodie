from flask import Flask, request, jsonify, make_response
from setup import run_statement, serialize_data, execute_statement, restaurant_login
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# START OF CLIENT ENDPOINTS

# Endpoint to get all clients
from flask import jsonify, make_response

@app.route("/api/clients", methods=["GET"])
def get_clients():
    try:
        # Assuming run_statement is a function that executes a SQL statement
        result = run_statement("CALL foodie.get_clients()")

        print(f"Type of result: {type(result)}")
        print(f"Content of result: {result}")

        if result[0]:  # Check if the statement execution was successful
            result_set = result[1]  # Extract the result set from the tuple

            if isinstance(result_set, list):
                # Fetch the result set and format it
                format_data = serialize_data(["id", "email", "first_name", "last_name", "image_url", "username"], result_set)
                return make_response(jsonify(format_data), 200)
            else:
                return make_response("Failed to fetch clients", 500)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as e:
        print(f"Error: {e}")
        return make_response(f"Failed to fetch clients. Error: {e}", 500)


# Endpoint to get a client by ID
# Endpoint to get a client by ID
@app.route("/api/clients/<int:client_id>", methods=["GET"])
def get_client_by_id(client_id):
    try:
        success, result = run_statement("CALL foodie.get_client_by_id(?)", [client_id])

        if success:
            if result:
                # Format the data only if there are results
                format_data = serialize_data(["id", "email", "first_name", "last_name", "image_url", "username"], result)
                return make_response(jsonify(format_data), 200)
            else:
                return make_response("Client not found", 404)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        return make_response(str(error), 500)



# Endpoint to create a new client
@app.route("/api/clients", methods=["POST"])
def create_client():
    try:
        data = request.get_json()
        email = data["email"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        image_url = data.get("image_url", "")
        username = data["username"]
        password = data["password"]

        # Assuming run_statement is a function that executes a SQL statement
        result = run_statement("CALL foodie.create_client(?, ?, ?, ?, ?, ?)", [email, first_name, last_name, image_url, username, password])

        print(f"Type of result: {type(result)}")
        print(f"Content of result: {result}")

        # Check if the statement execution was successful
        if result[0]:
            # Check if there is a result set
            if len(result) > 1 and isinstance(result[1], list):
                # Fetch the result set and format it
                format_data = serialize_data(["id", "email", "first_name", "last_name", "image_url", "username"], result[1])

                # Print a success message
                print("Client added successfully!")

                return make_response(jsonify(format_data), 201)
            else:
                return make_response("Failed to create client. No result set returned.", 500)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        print(f"Error: {error}")
        return make_response(f"Failed to create client. Error: {error}", 500)


# Endpoint to update an existing client
@app.route("/api/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    try:
        data = request.get_json()
        email = data["email"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        image_url = data.get("image_url", "")
        username = data["username"]
        password = data["password"]

        run_statement("CALL foodie.update_client(?, ?, ?, ?, ?, ?, ?)", [client_id, email, first_name, last_name, image_url, username, password])
        return make_response("Client updated successfully", 200)
    except Exception as error:
        return make_response(str(error), 500)

# Endpoint to delete an existing client
@app.route("/api/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    try:
        run_statement("CALL foodie.delete_client(?)", [client_id])
        return make_response("Client deleted successfully", 200)
    except Exception as error:
        return make_response(str(error), 500)

# END OF CLIENTS ENDPOINTS

# START OF RESTAURANTS ENDPOINTS

# Endpoint to get all restaurants
@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():
    try:
        result = run_statement("CALL foodie.get_restaurants()")

        print(f"Type of result: {type(result)}")
        print(f"Content of result: {result}")

        if result[0]:  # Check if the statement execution was successful
            result_set = result[1]  # Extract the result set from the tuple

            if isinstance(result_set, list):
                # Fetch the result set and format it
                format_data = serialize_data(["id", "email", "name", "address", "phone_number", "bio", "city", "profile_url", "banner_url"], result_set)
                return make_response(jsonify(format_data), 200)
            else:
                return make_response("Failed to fetch restaurants", 500)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as e:
        print(f"Error: {e}")
        return make_response(f"Failed to fetch clients. Error: {e}", 500)


# Endpoint to get a restaurant by ID
@app.route("/api/restaurants/<int:restaurant_id>", methods=["GET"])
def get_restaurant_by_id(restaurant_id):
    try:
        success, result = run_statement("CALL foodie.get_restaurant_by_id(?)", [restaurant_id])

        if success:
            if result:
                # Format the data only if there are results
                format_data = serialize_data(["id", "email", "name", "address", "phone_number", "bio", "city", "profile_url", "banner_url"], result)
                return make_response(jsonify(format_data), 200)
            else:
                return make_response("Restaurant not found", 404)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        return make_response(str(error), 500)


# Endpoint to create a new restaurant
@app.route("/api/restaurants", methods=["POST"])
def create_restaurant():
    try:
        data = request.get_json()
        email = data["email"]
        name = data["name"]
        address = data["address"]
        phone_number = data["phone_number"]
        bio = data.get("bio", "")
        city = data["city"]
        profile_url = data.get("profile_url", "")
        banner_url = data.get("banner_url", "")
        password = data["password"]

        # Assuming run_statement is a function that executes a SQL statement
        result = run_statement("CALL foodie.create_restaurant(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               [email, name, address, phone_number, bio, city, profile_url, banner_url, password])

        print(f"Type of result: {type(result)}")
        print(f"Content of result: {result}")

        # Check if the statement execution was successful
        if result[0]:
            # Check if there is a result set
            if len(result) > 1 and isinstance(result[1], list):
                # Fetch the result set and format it
                format_data = serialize_data(["id", "email", "name", "address", "phone_number", "bio", "city", "profile_url", "banner_url"],
                                             result[1])

                # Print a success message
                print("Restaurant created successfully!")

                return make_response(jsonify(format_data), 201)
            else:
                return make_response("Failed to create restaurant. No result set returned.", 500)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        print(f"Error: {error}")
        return make_response(f"Failed to create restaurant. Error: {error}", 500)


# Endpoint to update an existing restaurant
@app.route("/api/restaurants/<int:restaurant_id>", methods=["PUT"])
def update_restaurant(restaurant_id):
    try:
        data = request.get_json()
        email = data["email"]
        name = data["name"]
        address = data["address"]
        phone_number = data["phone_number"]
        bio = data.get("bio", "")
        city = data["city"]
        profile_url = data.get("profile_url", "")
        banner_url = data.get("banner_url", "")
        password = data["password"]

        run_statement("CALL foodie.update_restaurant(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      [restaurant_id, email, name, address, phone_number, bio, city, profile_url, banner_url, password])
        return make_response("Restaurant updated successfully", 200)
    except Exception as error:
        return make_response(str(error), 500)


# Endpoint to delete an existing restaurant
@app.route("/api/restaurants/<int:restaurant_id>", methods=["DELETE"])
def delete_restaurant(restaurant_id):
    try:
        run_statement("CALL foodie.delete_restaurant(?)", [restaurant_id])
        return make_response("Restaurant deleted successfully", 200)
    except Exception as error:
        return make_response(str(error), 500)


# END OF RESTAURANT ENDPOINTS

# START OF MENU ENDPOINTS    
# Stored procedures for Menu

# Endpoint to get all menu items for a specific restaurant
@app.route("/api/menu_items/<int:restaurant_id>", methods=["GET"])
def get_menu_items(restaurant_id):
    try:
        success, result = run_statement("CALL foodie.get_menu_items(?)", [restaurant_id])

        if success:
            # Format the data only if there are results
            format_data = serialize_data(["id", "description", "image_url", "name", "price", "restaurant_id"], result)
            return make_response(jsonify(format_data), 200)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        return make_response(str(error), 500)


# Endpoint to get a menu item by ID
@app.route("/api/menu_items/<int:menu_item_id>", methods=["GET"])
def get_menu_item_by_id(menu_item_id):
    try:
        success, result = run_statement("CALL foodie.get_menu_item_by_id(?)", [menu_item_id])

        if success:
            if result:
                # Format the data only if there are results
                format_data = serialize_data(["id", "description", "image_url", "name", "price", "restaurant_id"], result)
                return make_response(jsonify(format_data), 200)
            else:
                return make_response("Menu item not found", 404)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        return make_response(str(error), 500)


# Endpoint to create a new menu item
@app.route("/api/menu_items", methods=["POST"])
def create_menu_item():
    try:
        data = request.get_json()
        description = data.get("description", "")
        image_url = data.get("image_url", "")
        name = data["name"]
        price = data["price"]
        restaurant_id = data["restaurant_id"]

        result = run_statement("CALL foodie.create_menu_item(?, ?, ?, ?, ?)",
                               [description, image_url, name, price, restaurant_id])

        print(f"Type of result: {type(result)}")
        print(f"Content of result: {result}")

        # Check if the statement execution was successful
        if result[0]:
            # Check if there is a result set
            if len(result) > 1 and isinstance(result[1], list):
                # Fetch the result set and format it
                format_data = serialize_data(["id", "description", "image_url", "name", "price", "restaurant_id"], result[1])

                # Print a success message
                print("Menu item created successfully!")

                return make_response(jsonify(format_data), 201)
            else:
                return make_response("Failed to create menu item. No result set returned.", 500)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        print(f"Error: {error}")
        return make_response(f"Failed to create menu item. Error: {error}", 500)


# Endpoint to update an existing menu item
@app.route("/api/menu_items/<int:menu_item_id>", methods=["PUT"])
def update_menu_item(menu_item_id):
    try:
        data = request.get_json()
        description = data.get("description", "")
        image_url = data.get("image_url", "")
        name = data["name"]
        price = data["price"]

        run_statement("CALL foodie.update_menu_item(?, ?, ?, ?)", [menu_item_id, description, image_url, name, price])
        return make_response("Menu item updated successfully", 200)
    except Exception as error:
        return make_response(str(error), 500)


# Endpoint to delete an existing menu item
@app.route("/api/menu_items/<int:menu_item_id>", methods=["DELETE"])
def delete_menu_item(menu_item_id):
    try:
        run_statement("CALL foodie.delete_menu_item(?)", [menu_item_id])
        return make_response("Menu item deleted successfully", 200)
    except Exception as error:
        return make_response(str(error), 500)
    
# END OF MENU ENDPOINTS

# START OF ORDER ENDPOINTS
    
# Endpoint to get all menu items for a specific client
@app.route("/api/client_menu_items/<int:client_id>", methods=["GET"])
def get_client_menu_items(client_id):
    try:
        result = run_statement("CALL foodie.get_client_menu_items(?)", [client_id])
        format_data = serialize_data(["id", "description", "image_url", "name", "price", "restaurant_id"], result)
        return make_response(jsonify(format_data), 200)
    except Exception as error:
        return make_response(str(error), 500)


# Endpoint to get all orders for a specific client
@app.route("/api/client_orders/<int:client_id>", methods=["GET"])
def get_client_orders(client_id):
    try:
        success, result = run_statement("CALL foodie.get_client_orders(?)", [client_id])

        if success:
            # Format the data only if there are results
            format_data = serialize_data(["id", "client_id", "restaurant_id", "is_confirmed", "is_complete"], result)
            return make_response(jsonify(format_data), 200)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        return make_response(str(error), 500)

# Endpoint to get all orders for a specific restaurant
@app.route("/api/restaurant_orders/<int:restaurant_id>", methods=["GET"])
def get_restaurant_orders(restaurant_id):
    try:
        success, result = run_statement("CALL foodie.get_restaurant_orders(?)", [restaurant_id])

        if success:
            # Format the data only if there are results
            format_data = serialize_data(["id", "client_id", "restaurant_id", "is_confirmed", "is_complete"], result)
            return make_response(jsonify(format_data), 200)
        else:
            return make_response("Failed to execute statement", 500)

    except Exception as error:
        return make_response(str(error), 500)


# Endpoint to create a new order
@app.route("/api/orders", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        client_id = data["client_id"]
        restaurant_id = data["restaurant_id"]

        run_statement("CALL foodie.create_order(?, ?)", [client_id, restaurant_id])
        return make_response("Order created successfully", 201)
    except Exception as error:
        return make_response(str(error), 500)

# Endpoint to update an existing order
@app.route("/api/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    try:
        data = request.get_json()
        is_confirmed = data.get("is_confirmed", None)
        is_complete = data.get("is_complete", None)
        session_token = data.get("session_token", None)

        # Validate the session token and get the user type (client or restaurant)
        user_type, user_id = validate_session_token(session_token)

        if user_type is None:
            return make_response("Invalid session token", 401)

        if user_type == "client":
            # Check if the client has the authority to update the order
            if not is_client_authorized(user_id, order_id):
                return make_response("Client not authorized to update the order", 403)

        elif user_type == "restaurant":
            # Check if the restaurant has the authority to update the order
            if not is_restaurant_authorized(user_id, order_id):
                return make_response("Restaurant not authorized to update the order", 403)

        # Update the order if the requester is authorized
        run_statement("CALL foodie.update_order(?, ?, ?)", [order_id, is_confirmed, is_complete])
        return make_response("Order updated successfully", 200)

    except Exception as error:
        return make_response(str(error), 500)



# Endpoint to delete an existing order
@app.route("/api/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    try:
        run_statement("CALL foodie.delete_order(?)", [order_id])
        return make_response("Order deleted successfully", 200)
    except Exception as error:
        return make_response(str(error), 500)

# END OF ORDER ENDPOINTS

def client_login(username, password):
    try:
        # Assuming run_statement is a function that executes a SQL statement
        success, result = run_statement("CALL foodie.client_login(?, ?, ?)", [username, password, None])

        if success and result:
            # Check if a valid client_id is returned
            client_id = result[0][0]
            return client_id
        else:
            return None

    except Exception as error:
        print(f"Error: {error}")
        return None


# Endpoint for client login
@app.route("/api/client_login", methods=["POST"])
def client_login_api():
    try:
        # Get username and password from the request
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Call the client_login function
        client_id = client_login(username, password)

        if client_id:
            # Check if there is a valid client_id returned
            # You can also generate a session token here if needed
            print("Client login successful!")

            return make_response(jsonify({"client_id": client_id}), 200)
        else:
            return make_response("Invalid username or password", 401)

    except Exception as error:
        return make_response(str(error), 500)



# Endpoint for restaurant login
@app.route("/api/restaurant_login", methods=["POST"])
def restaurant_login_api():
    try:
        # Get email and password from the request
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        # Call the restaurant_login function
        restaurant_id = restaurant_login(email, password)

        if restaurant_id:
            # Check if there is a valid restaurant_id returned
            # You can also generate a session token here if needed
            print("Restaurant login successful!")

            return make_response(jsonify({"restaurant_id": restaurant_id}), 200)
        else:
            return make_response("Invalid email or password", 401)

    except Exception as error:
        return make_response(str(error), 500)

    

# Root endpoint
@app.route("/")
def index():
    return "Welcome to Foodie App!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
