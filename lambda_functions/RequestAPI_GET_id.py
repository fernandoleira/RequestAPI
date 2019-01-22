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
def connection(username, password):
    DB_CONF_PARAMS["user"] = username
    DB_CONF_PARAMS["password"] = password

    conn = psycopg2.connect(**DB_CONF_PARAMS)
    return conn


def single_elem_request(connection, tablename, elem_id):
    elm = dict()
    cur = connection.cursor()

    cur.execute('SELECT * FROM {}'.format(tablename))
    col_names = [desc[0] for desc in cur.description]

    cur.execute('SELECT * FROM {0} WHERE {1} = {2};'.format(tablename, col_names[0], str(elem_id)))
    rd = cur.fetchone()

    if rd is not None:
        rd = list(rd)
        cnt = 0
        for name in col_names:
            elm[name] = str(rd[cnt])
            cnt += 1

        cur.close()
        return elm

    else:
        cur.close()
        return "Not founded"


# API Lambda function for the GET method
def lambda_handler(event, context):
    table_name = event["params"]["path"]["table"]
    id_name = event["params"]["path"]["id"]
    # db_user = event["header"]["x-db-user"]
    # db_password = event["header"]["x-db-password"]

    # Test connection with the database
    try:
        test_connection = connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))
        test_connection.close()
    except ImportError:
        return "Could not connect to the database"

    conn = connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))

    res = single_elem_request(conn, table_name, id_name)

    conn.close()
    return res