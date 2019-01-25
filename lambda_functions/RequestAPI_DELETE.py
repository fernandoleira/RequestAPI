import os
import json
import psycopg2

# PostgreSQL configuration parameters
DB_CONF_PARAMS = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT")),
    "database": os.environ.get("DB_NAME"),
    "user": "",
    "password": ""
}


# Function to define and export the database connection configuration
def db_connection(username, password):
    DB_CONF_PARAMS["user"] = username
    DB_CONF_PARAMS["password"] = password

    conn = psycopg2.connect(**DB_CONF_PARAMS)
    return conn


def delete_elem_request(connection, tablename, column, elem_id):
    cur = connection.cursor()

    cur.execute('DELETE FROM {0} WHERE {1} = {2};'.format(tablename, column, elem_id))

    sm = cur.statusmessage
    cur.close()
    return sm


# API Lambda function for the GET method
def lambda_handler(event, context):
    table_name = event["params"]["path"]["table"]
    col_name = event["params"]["path"]["col"]
    id_name = event["params"]["path"]["id"]

    # Test connection with the database
    try:
        test_connection = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))
        test_connection.close()
    except ImportError:
        return "Could not connect to the database"

    conn = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))

    res = delete_elem_request(conn, table_name, col_name, id_name)

    conn.commit()
    conn.close()
    return res
