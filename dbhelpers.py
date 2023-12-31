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

def execute_statement(cursor, statement, list_of_args=[]):
    try:
        if statement.lower().startswith("call"):
            # For stored procedures, execute and commit
            cursor.callproc(statement.split("(")[0][5:], list_of_args)
            cursor.execute("COMMIT;")
        else:
            # For regular SQL statements, execute and fetch results
            cursor.execute(statement, list_of_args)
            results = cursor.fetchall()
            return True, results

    except mariadb.Error as error:
        print("ERROR:", error)
        return False, str(error)


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

    success, result_or_error = execute_statement(cursor, statement, list_of_args)
    print("Run success")
    close_connection(cursor, conn)

    return success, result_or_error

def serialize_data(columns, data):
    sql_data_dict = [dict(zip(columns, row)) for row in data]
    return sql_data_dict
