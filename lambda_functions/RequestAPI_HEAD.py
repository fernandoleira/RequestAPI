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


def get_db_info(connection):
    cur = connection.cursor()
    info = {"database": os.environ.get("DB_NAME"), "tables": []}

    cur.execute('SELECT * FROM pg_catalog.pg_tables ORDER BY schemaname DESC;')

    rd = cur.fetchone()
    while rd is not None and rd[0] == "public":
        info["tables"].append(rd[1])
        rd = cur.fetchone()

    cur.close()
    return info


def lambda_handler(event, context):

    try:
        test_connection = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))
        test_connection.close()
    except ImportError:
        return "Could not connect to the database"

    conn = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))

    res = get_db_info(conn)

    return res

