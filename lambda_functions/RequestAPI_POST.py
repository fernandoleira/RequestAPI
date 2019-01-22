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


def insert_elem_request(connection, tablename, elem):
    cur = connection.cursor()

    cur.execute('INSERT INTO {0} ({1}) VALUES ({2});'.format(
        tablename,
        ",".join(list(elem.keys())),
        ",".join(list(elem.values()))
    ))

    sm = cur.statusmessage

    cur.close()
    return sm


def lambda_handler(event, context):
    table_name = event["params"]["path"]["table"]
    new_elem = event["body-json"]
    # db_user = event["header"]["x-db-user"]
    # db_password = event["header"]["x-db-password"]

    try:
        test_connection = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))
        test_connection.close()
    except ImportError:
        return "Could not connect to the database"

    conn = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))

    # Insert the new data into the database
    res = insert_elem_request(conn, table_name, new_elem)

    conn.commit()
    conn.close()
    return res

