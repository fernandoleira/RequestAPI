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


def all_elem_request(connection, tablename):
    arr = list()
    cur = connection.cursor()

    cur.execute('SELECT * FROM {};'.format(tablename))

    rd = cur.fetchone()
    col_names = [desc[0] for desc in cur.description]
    while rd is not None:
        rd = list(rd)
        assets = dict()
        for name in col_names:
            assets[name] = ""

        cnt = 0
        for key in assets.keys():
            assets[key] = str(rd[cnt])
            cnt += 1

        arr.append(assets)
        rd = cur.fetchone()

    cur.close()
    return arr


# API Lambda function for the GET method
def lambda_handler(event, context):
    table_name = event["params"]["path"]["table"]
    # db_user = event["header"]["x-db-user"]
    # db_password = event["header"]["x-db-password"]

    try:
        test_connection = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))
        test_connection.close()
    except ImportError:
        return "Could not connect to the database"

    conn = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))

    res = all_elem_request(conn, table_name)

    conn.close()
    return res

