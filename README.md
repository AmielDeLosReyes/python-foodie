# Foodie - REST API with Python Flask

## Steps to Get Started

1. Navigate to the W20C folder.
2. Ensure MariaDB and MySQL are installed on your system. Download from [MariaDB](https://mariadb.org/download/) and [MySQL](https://dev.mysql.com/downloads/).
3. Run the following scripts in your terminal:

    ```bash
    python -m venv venv
    ```

    ```bash
    Get-ExecutionPolicy
    ```

    If the output is "Restricted," run:

    ```bash
    Set-ExecutionPolicy RemoteSigned -Scope Process
    ```

    ```bash
    .\venv\Scripts\Activate
    ```

    Install required libraries:

    ```bash
    pip install flask mariadb flask-cors
    ```

    For MariaDB CLI:

    ```bash
    & "C:\Program Files\MariaDB 11.4\bin\mariadb.exe" -u root -p
    ```

    Run SQL scripts:

    ```sql
    source C:/your_sql_file_path/foodie.sql;
    ```

4. For testing, create the "foodie" database manually using DBeaver.
5. Execute the setup script:

    ```bash
    python setup.py
    ```

6. Test the API in Postman following the order provided.

## Testing

Follow these steps to test the API using Postman:

1. **Database Setup:** Ensure the "foodie" database is created manually before running the "setup.py" script.

2. **Create Clients:**
   - Endpoint: POST /api/clients
   - Example JSON payload: `{ "email": "client1@example.com", ... }`

3. **Get Clients:**
   - Endpoint: GET /api/clients

4. **Update Client:**
   - Endpoint: PUT /api/clients/{client_id}
   - Example JSON payload: `{ "email": "updated_email@example.com", ... }`

5. **Get Client by ID:**
   - Endpoint: GET /api/clients/{client_id}

6. **Delete Client:**
   - Endpoint: DELETE /api/clients/{client_id}

7. **Create Restaurants:**
   - Endpoint: POST /api/restaurants
   - Example JSON payload: `{ "email": "restaurant1@example.com", ... }`

8. **Get Restaurants:**
   - Endpoint: GET /api/restaurants

9. **Update Restaurant:**
   - Endpoint: PUT /api/restaurants/{restaurant_id}
   - Example JSON payload: `{ "email": "updated_restaurant_email@example.com", ... }`

10. **Get Restaurant by ID:**
    - Endpoint: GET /api/restaurants/{restaurant_id}

11. **Delete Restaurant:**
    - Endpoint: DELETE /api/restaurants/{restaurant_id}

12. **Create Menu Items:**
    - Endpoint: POST /api/menu_items
    - Example JSON payload: `{ "description": "Delicious dish", ... }`

13. **Get Menu Items:**
    - Endpoint: GET /api/menu_items/{restaurant_id}

14. **Update Menu Item:**
    - Endpoint: PUT /api/menu_items/{menu_item_id}
    - Example JSON payload: `{ "description": "Updated description", ... }`

15. **Get Menu Item by ID:**
    - Endpoint: GET /api/menu_items/{menu_item_id}

16. **Delete Menu Item:**
    - Endpoint: DELETE /api/menu_items/{menu_item_id}

17. **Create Orders:**
    - Endpoint: POST /api/orders
    - Example JSON payload: `{ "client_id": 1, "restaurant_id": 1 }`

18. **Get Client Orders:**
    - Endpoint: GET /api/client_orders/{client_id}

19. **Get Restaurant Orders:**
    - Endpoint: GET /api/restaurant_orders/{restaurant_id}

20. **Get Order by ID:**
    - Endpoint: GET /api/orders/{order_id}

21. **Update Order:**
    - Endpoint: PUT /api/orders/{order_id}
    - Example JSON payload: `{ "is_confirmed": true, "is_complete": true }`

22. **Delete Order:**
    - Endpoint: DELETE /api/orders/{order_id}

23. **Client and Restaurant Login:** Provided in the API.

Feel free to explore, test, and contribute to the continuous improvement of the W20C REST API.
