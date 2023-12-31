STEPS TO GET STARTED:

Note: Make sure you are on the w20c folder

Also make sure you got MariaDB and MySQL downloaded on your system.
Download MariaDb server and MySQL.

C:\Program Files\MariaDB 11.4\

1. run the below script:
    python -m venv venv

2. run the below script:
    Get-ExecutionPolicy
    => If the output is "Restricted," run Step 4, if not, skip Step 4.

3. Set-ExecutionPolicy RemoteSigned -Scope Process
    => This sets the execution policy for the current session only.

4. run the below script:
    .\venv\Scripts\Activate

5. to build a flask api we need the following 3 libraries 
```
pip install flask
pip install mariadb
pip install -U flask-cors
```
--To go to MariaDB CLI:
& "C:\Program Files\MariaDB 11.4\bin\mariadb.exe" -u root -p

To run SQL Scripts to MariaDB CLI:
source C:/your_sql_file_path/foodie.sql;

--To choose a database:
USE foodie;

--To check which database we're working with:
SELECT DATABASE();

--To show tables:
SHOW TABLES;

===========================================================================
FOR TESTING:

For Testing purposes, follow these order so that you can test the API. ***Test in Postman please***

*KEY STEP*: the database should be created manually before running the "setup.py" script. Create this database named "foodie" manually on your local database, on your DBeaver.

1. Create Database Tables: /

    Before testing the API, make sure you have executed the setup script (setup.py) to create the necessary database tables. Just run the script below:
        python setup.py

    a. If this errors or says "Table 'client' already exists", run these scripts:
        & "C:\Program Files\MariaDB 11.4\bin\mariadb.exe" -u root -p

        DROP DATABASE IF EXISTS foodie;
        CREATE DATABASE foodie;
        USE foodie;

        exit;

    b. Then rerun python setup.py

2. Create Clients: /

    Use the following endpoints to create client accounts:
    POST /api/clients

    Then put to JSON body:
    Example JSON payload:
    {
        "email": "client1@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "username": "john_doe",
        "password": "password"
    }

    One more:

    POST /api/clients
    Example JSON payload:
    {
        "email": "client2@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "username": "jane_smith",
        "password": "password"
    }


3. Get Clients: /
    Use the following endpoint to retrieve a list of clients:
    GET /api/clients

4. Update Client: /
    Use the following endpoint to update the details of a client:
    PUT /api/clients/{client_id}

    Example JSON payload:
    {
        "email": "updated_email@example.com",
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "username": "updated_username",
        "password": "new_password"
    }


5. Get Client by ID: /

    Use the following endpoint to retrieve the details of a specific client by ID:
    GET /api/clients/{client_id}

    Example:
    GET /api/clients/1

6. Delete Client: /
    Use the following endpoint to delete a client:
    DELETE /api/clients/{client_id}

    Example:    
    DELETE /api/clients/1


7. Create Restaurants: /

    Use the following endpoints to create restaurant accounts:
    POST /api/restaurants
    Example JSON payload:
    {
        "email": "restaurant1@example.com",
        "name": "Restaurant One",
        "address": "123 Main St",
        "phone_number": "123-456-7890",
        "city": "Cityville",
        "password": "password"
    }

    One More:

    POST /api/restaurants
    Example JSON payload:
    {
        "email": "restaurant2@example.com",
        "name": "Restaurant Two",
        "address": "456 Oak St",
        "phone_number": "987-654-3210",
        "city": "Townsville",
        "password": "password"
    }

8. Get Restaurants: /
    Use the following endpoint to retrieve a list of restaurants:
    GET /api/restaurants

9. Update Restaurant: /
    Use the following endpoint to update the details of a restaurant:
    PUT /api/restaurants/{restaurant_id}
    
    Example JSON payload:
    {
        "email": "updated_restaurant_email@example.com",
        "name": "Updated Restaurant Name",
        "address": "789 Maple St",
        "phone_number": "111-222-3333",
        "city": "Villageville",
        "password": "new_password"
    }


10. Get Restaurant by ID: /
    Use the following endpoint to retrieve the details of a specific restaurant by ID:
    GET /api/restaurants/{restaurant_id}

    Example:
    GET /api/restaurants/1


11. Delete Restaurant: /
    Use the following endpoint to delete a restaurant:
    DELETE /api/restaurants/{restaurant_id}

    Example:
    DELETE /api/restaurants/1

12. Create Menu Items: /
    Use the following endpoints to create menu items for a restaurant:
    POST /api/menu_items

    Example JSON payload:
    {
        "description": "Delicious dish",
        "image_url": "https://example.com/dish.jpg",
        "name": "Special Dish",
        "price": 19.99,
        "restaurant_id": 1
    }

    One More.

    POST /api/menu_items
    Example JSON payload:
    {
        "description": "Tasty dessert",
        "image_url": "https://example.com/dessert.jpg",
        "name": "Sweet Treat",
        "price": 9.99,
        "restaurant_id": 2
    }


13. Get Menu Items: /
    Use the following endpoint to retrieve a list of menu items for a specific restaurant:
    GET /api/menu_items/{restaurant_id}

    Example: 
    GET /api/menu_items/1


14. Update Menu Item: /
    Use the following endpoint to update the details of a menu item:
    PUT /api/menu_items/{menu_item_id}
    
    Example JSON payload:
    {
        "description": "Updated description",
        "image_url": "https://example.com/updated_image.jpg",
        "name": "Updated Dish",
        "price": 24.99
    }

15. Get Menu Item by ID: /
    Use the following endpoint to retrieve the details of a specific menu item by ID:
    GET /api/menu_items/{menu_item_id}

    Example:
    GET /api/menu_items/1


16. Delete Menu Item: /
    Use the following endpoint to delete a menu item:
    DELETE /api/menu_items/{menu_item_id}

    Example:
    DELETE /api/menu_items/1

17. Create Orders: /
    Use the following endpoint to create orders:
    POST /api/orders

    Example JSON payload:
    {
        "client_id": 1,
        "restaurant_id": 1
    }

    One More.

    POST /api/orders
    Example JSON payload:
    {
        "client_id": 2,
        "restaurant_id": 2
    }

18. Get Client Orders: /
    Use the following endpoint to retrieve a list of orders for a specific client:
    GET /api/client_orders/{client_id}

    Example: 
    GET /api/client_orders/1


    - Get Restaurant Orders: /
    Use the following endpoint to retrieve a list of orders for a specific client:
    GET /api/restaurant_orders/{restaurant_id}

    Example:
    GET /api/restaurant_orders/1


19. Get Order by ID: /
    Use the following endpoint to retrieve the details of a specific order by ID:
    GET /api/orders/{order_id}

    Example:
    GET /api/orders/1


20. Update Order:
    Use the following endpoint to update the details of an order:
    PUT /api/orders/{order_id}

    Example JSON payload:
    {
        "is_confirmed": true,
        "is_complete": true
    }


21. Delete Order: /
    Use the following endpoint to delete an order:
    DELETE /api/orders/{order_id}

    Example:
    DELETE /api/orders/1


22. Client login and restaurant login is also provided.
### End of file ###